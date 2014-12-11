---
date: 2014-12-11 15:32:30+00:00
layout: post
title: Linux下进程控制的一些函数小结
thread: 95
categories: network-programming
tags: network-programming
---

在小结进程间通信前，先小结下linux下进程控制（创建新进程、执行进程和终止进程）的一些函数，主要包括进程终止、一个进程启动另一个进程、复制进程、等待进程等函数。

###进程标识符###

每个进程都有一个非负整数的唯一进程ID。进程ID为0、1、2分别为调度进程(或交换进程)、init进程、页精灵进程。

- 调度进程：作为内核的一部分，不执行磁盘上的任何程序；

- init进程：在自举过程结束时由内核调用，此进程负责在内核自举后启动一个unix系统，它不是系统进程，但以超级用户特权运行；

- 页精灵进程：负责支持虚存系统的请页操作，和交换进程一样，页精灵进程也是内核进程。

获取进程标识符的函数如下：

	{% highlight C++ %}

	#include <sys/types.h>
	#include <unistd.h>
	pid_t getpid(void); //返回调用进程的进程ID
	pid_t getppid(void); //返回调用进程的父进程ID
	uid_t getuid(void);  //返回调用进程的实际用户ID
	uid_t geteuid(void); //返回调用进程的有效用户ID
	gid_t getgit(void); //返回调用进程的实际组ID
	gid_t getegit(void); //返回调用进程的有效组ID
	{% endhighlight %}

###进程终止###

进程终止的五种方式：

正常终止：

（1）从main返回；

（2）调用exit函数，如exit(main(argc, argv));

（3）调用_exit函数

异常终止：

（4）调用abort；

（5）由一个信号终止。

exit和_exit函数的区别：_exit立即进入内核，exit函数则先执行一些清除处理如调用执行各终止处理程序和关闭所有标准I/O流等，然后进入内核。

另外，exit是由ANSIC说明的，而_exit是有POSIX.1说明的。

###fork函数和vfork函数###

一个现存的进程调用fork函数时unix内核创建一个新进程唯一的方法（不能创建交换进程、init进程和页精灵进程）。

	{% highlight C++ %}
	#include <sys/types.h>
	#include <unistd.h>
	pid_t fork(void);
	{% endhighlight %}

由fork创建的新进程为子进程，fork函数调用一次，返回两次，两次返回的区别是子进程的返回值是0，而父进程中的返回值是新子进程的进程ID。若返回的值小于0，则表示创建进程出错（如系统内存不足或进程数达到系统上限）。

	{% highlight C++ %}
	#include <unistd.h>
	#include <stdio.h>
	int main()
	{
		pid_t pid;
		int cout=0;
		pid=fork();
		if(pid<0)
			printf("error");
		else if(pid==0)
		{
			printf("执行的是子进程,PID:%d\n",getpid())；
			cout++;
		}else{
			printf("执行的是父进程,PID:%d\n",getpid());
			cout++
		}
		printf("cout:%d\n", cout);
		return 0;
	}
	

	/*执行的是子进程,PID:5875
	   cout:1
	   执行的是父进程,PID:5876
	   cout:1 */
	{% endhighlight %}

子进程是父进程的复制品，例如子进程获得父进程数据空间、堆和栈的复制品（子进程拥有的拷贝）。

执行fork()函数生成子进程的过程，类似于二叉树的不断生成。例如下面的例子打印3个parent和3个child。

	{% highlight C++ %}
	#include <unistd.h>  
	#include <stdio.h>  
	int main(void)  
	{  
	   int i=0;  
	   for(i=0;i<2;i++){  
	       pid_t fpid=fork();  
	       if(fpid==0)  
	           printf("child/n");  
	       else  
	           printf("parent/n");  
	   }  
	   return 0;  
	}  
	{% endhighlight %}

Unix下的设备有“块设备”和“字符设备”的概念，所谓块设备，就是以一块一块的数据存取的设备，字符设备是一次存取一个字符的设备。磁盘、内存都是块设备，字符设备如键盘和串口。块设备一般都有缓存，而字符设备一般都没有缓存。

如果标准输出到终端设备，则它是行缓存的，否则就是带缓存的。

write函数是不带缓存的，但标准I/O库是带缓存的。若不使用"\n"或fflush(stdout)时，调用fork函数，该行的数据仍在缓存中，然后在父进程数据空间复制到子进程中，该缓存数据也被复制到子进程中了。因此，下面的例子会打印4个parent和4个child。

	{% highlight C++ %}
	#include <unistd.h>  
	#include <stdio.h>  
	int main(void)  
	{  
	   int i=0;  
	   for(i=0;i<2;i++){  
	       pid_t fpid=fork();  
	       if(fpid==0)  
	           printf("child ");  
	       else  
	           printf("parent ");  
	   }  
	   return 0;  
	}  
	{% endhighlight %}


vfork函数和fork函数的区别如下：

（1）vfork函数用于创建一个新进程，新进程的目的是执行一个新程序，且子进程不会讲父进程的地址空间完全复制到子进程中，因为子进程会立即调用exec(或exit);

（2）vfork保证子进程先运行，在它调用exec或exit之后父进程才可能被调度运行。

###wait和waitpid函数###



参考：

[一个fork的面试题](http://coolshell.cn/articles/7965.html)