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
  --mincpu=MINCPU      Don't get a stack if the CPU usager is less than %x
                       (default to 0)

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

# Q & A
**Why I am getting something like this :**
```
   java.lang.Thread.State: WAITING (parking)
        at sun.misc.Unsafe.park(Native Method)
        - parking to wait for  <0x000000061d8fe5f8> (a java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject)
        at java.util.concurrent.locks.LockSupport.park(Unknown Source)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject.await(Unknown Source)
        at java.util.concurrent.LinkedBlockingQueue.take(Unknown Source)
        at java.util.concurrent.ThreadPoolExecutor.getTask(Unknown Source)
        at java.util.concurrent.ThreadPoolExecutor.runWorker(Unknown Source)
        at java.util.concurrent.ThreadPoolExecutor$Worker.run(Unknown Source)
        at java.lang.Thread.run(Unknown Source)
```

The script is not perfect, it means that beetween the time the top command was run to find the thread and the time the stack was run, the thread got to a park state, meaning it's waiting, you can ignore those.

**Why using top to find most used thread :**

At first I tryed with ps, but surprisingly the result wasn't reliable for threads.   If you have a better way to do it I would to like to hear it. 
