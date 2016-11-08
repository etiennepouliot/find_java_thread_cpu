# find_java_thread_cpu
Let's say you have a java process that is using a lot of CPU and you want to find in real time what thread is using all that CPU and the stack of that thread.  This program let's you find it out.

Options :
```
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

```

For example, launching ```java CPULoadGenerator``` (http://middlewaremagic.com/weblogic/?p=958), finding the pid and starting ``` python find_java_thread_cpu.py --pid=34538 ``` will produce :

```
---------------------------------------------------------Date : 2016-11-08 13:24:00.414002-------CPU : 99.5---------------------------------------------------------------------------------
"Thread-0" prio=10 tid=0x00007f2eb00a7800 nid=0x7a96 runnable [0x00007f2ea6365000]
   java.lang.Thread.State: RUNNABLE
        at java.lang.StrictMath.atan(Native Method)
        at java.lang.Math.atan(Math.java:204)
        at CPULoadGenerator$1.run(CPULoadGenerator.java:16)
        at java.lang.Thread.run(Thread.java:744)


---------------------------------------------------------Date : 2016-11-08 13:24:30.784752-------CPU : 99.5---------------------------------------------------------------------------------
"Thread-0" prio=10 tid=0x00007f2eb00a7800 nid=0x7a96 runnable [0x00007f2ea6365000]
   java.lang.Thread.State: RUNNABLE
        at java.lang.StrictMath.atan(Native Method)
        at java.lang.Math.atan(Math.java:204)
        at CPULoadGenerator$1.run(CPULoadGenerator.java:16)
        at java.lang.Thread.run(Thread.java:744)


---------------------------------------------------------Date : 2016-11-08 13:25:01.219618-------CPU : 99.5---------------------------------------------------------------------------------
"Thread-0" prio=10 tid=0x00007f2eb00a7800 nid=0x7a96 runnable [0x00007f2ea6365000]
   java.lang.Thread.State: RUNNABLE
        at java.lang.StrictMath.atan(Native Method)
        at java.lang.Math.atan(Math.java:204)
        at CPULoadGenerator$1.run(CPULoadGenerator.java:16)
        at java.lang.Thread.run(Thread.java:744)


```
