#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import subprocess
import time
import datetime
import os
import pwd
from optparse import OptionParser,OptionValueError

def main():
    parser = OptionParser()
    parser.add_option("--pidfile",type="string", dest="pidfile",help=u"name of file contaning the pid of the java process")
    parser.add_option("--pid",type="string", dest="pid",help=u"pid of the java procress")
    parser.add_option("--duration",type="int", dest="duration",help=u"Duration in minutes (default to 60)",default=60)
    parser.add_option("--every",type="int", dest="every",help=u"Check every X seconds (default to 30)",default=30)
    parser.add_option("--log",type="string", dest="log",help=u"Log to file (default to none)")
    parser.add_option("--jstack",type="string", dest="jstack",help=u"Full path to jstack (default to $JDK_HOME/bin/jstack")
    parser.add_option("--username",type="string", dest="username",help=u"Username of the owner of the process (default try to find it)")
    parser.add_option("--appenddate",action="store_true", dest="appenddate",help=u"If using a log file, append date to the file")
    parser.add_option("--mincpu",type="int", dest="mincpu",help=u"Don't get a stack if the CPU usager is less than %x (default to 0)",default=0)
    (options, args) = parser.parse_args()

    pid = None
    if options.pid is None and options.pidfile is None :
        raise SystemExit('You must specify --pid or --pidfile')
    elif options.pid is not None and options.pidfile is None:
        pid = options.pid
    elif options.pid is None and options.pidfile is not None:
        with open(options.pidfile, 'r') as f: 
          pid = f.readline().replace('\n','')
    else : 
        raise SystemExit("You can't specify both --pid and --pidfile")

    jstack = None
    if options.jstack is not None :
        jstack =  options.jstack 
    else : #we try to find jstack
        for var in ['JDK_HOME','JAVA_HOME','JRE_HOME'] :
            if os.getenv(var)  != None :
                if os.path.isfile(os.getenv(var) + '/bin/jstack') :
                    jstack = os.getenv(var) + '/bin/jstack'
                    break
        if jstack is None :
            raise SystemExit("Could not find jstack , try to specify with --jstack")
    username = 'root'
    if options.username is not None :
        username = options.username
    else :
        proc_stat_file = os.stat("/proc/{0}".format(pid)) #get the process owner from /proc
        username = proc_stat_file.st_uid
        if unicode(username).isnumeric(): #we got the uid, go get the username
            username = pwd.getpwuid(int(username)).pw_name

    filename = None
    if options.log is not None :
        filename = options.log
        if options.appenddate :
            filename = options.log + datetime.datetime.now().strftime("%d_%m_%Y-%H")

    limit = datetime.datetime.now() + datetime.timedelta(minutes=options.duration)

    while datetime.datetime.now() < limit :
        #command = 'ps --no-headers -To pcpu,tid -p {0} | sort -r -k1 | head  -1 | sed -e "s/^ //"'.format(pid)
        command = '/usr/bin/top -n 1 -H -p {0} -o %CPU -b -w 1000 | grep -m1 java'.format(pid)
        #print command
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = process.communicate()
        while '  '  in out :
            out = out.replace('  ',' ')
        if err != '' :
            print(err)
        out = out.split(' ')
        cpu = out[-4]
        nid = out[0]
        if nid == '' :
            nid=out[1]
        if nid == '' :
            nid=out[2]
        if nid != pid and int(cpu.split('.')[0]) > options.mincpu : #not worth taking a stack if the main process is using most CPU
            nid_hex=hex(int(nid))
            if (os.getenv('USER') == 'root' and username != 'root'): #we run the command as the user running the java process
                command = 'su {username} -c "{jstack} -l {pid}"'.format(username=username,jstack=jstack,pid=pid)
            else : #we are running as the same user as the java process
                command = '{jstack} -l {pid}'.format(jstack=jstack,pid=pid)
            process = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)
            out,err = process.communicate()
            begin = None
            end = None
            out = out.split('\n')
            for index, line in enumerate(out):
                if len(line) > 0:
                    if begin is not None and line[0] not in [' ','\t'] :
                        end = index -1
                        break
                    if nid_hex in line :
                        begin = index
            lines =  '\n'.join(out[begin:end])
            towrite = '---------------------------------------------------------Date : {0}-------CPU : {1}---------------------------------------------------------------------------------\n'.format(datetime.datetime.now(),cpu) + lines
            if err != '' :
                print(err)
            print(towrite)
            if filename is not None :
                try : 
                    with open(filename,'ab') as f :
                        f.write(towrite)
                except :
                    print('Could not write to ' + filename)
            time.sleep(options.every)
        else :
            time.sleep(1)

if __name__ == '__main__' :
    main()
