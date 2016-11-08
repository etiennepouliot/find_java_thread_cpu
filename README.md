# find_java_thread_cpu
Let you find out what specify thread is using most CPU in a java process and print the stack

Let's say you have a java process that is using a lot of CPU and you want to find in real time what thread is using all that CPU.  This program let's you find it out.

Options :
<code>
Usage: find_java_thread_cpu.py [options]

Options:
  -h, --help           show this help message and exit
  --pidfile=PIDFILE    name of file contaning the pid of the java process
  --pid=PID            pid of the java procress
  --duration=DURATION  Duration in minutes (default to 60)
  --every=EVERY        Check every X seconds (default to 30)
  --log=LOG            Log to file (default to none)
  --jstack=JSTACK      Full path to jstack (default to $JDK_HOME/bin/jstack
  --username=USERNAME  Username of the owner of the process (default try to
                       find it)
  --appenddate         If using a log file, append date to the file
</code>

