---
date: 2014-4-18 21:19:30+00:00
layout: post
title: 线程库pthread的使用小结
thread: 56
categories: c++
tags: c++
---

C++11提供了std::thread用于多线程开发，除此之外，在linux上，最常见的线程库就是pthread了。 

Pthreads定义了一套C语言的类型、函数和常量，它以pthread.h头文件和一个线程库实现。

Pthreads API中大致共有100个函数调用，全部以“pthread_”开头，可以分为四类：

- 线程管理。如创建线程、等待线程、查询线程状态等；

- Mutex。如创建、摧毁、锁定、解锁、设置属性等操作；

- Condition Variable.如创建、摧毁、等待、通知、设置和查询属性等操作；

- 使用了读写锁的线程间的同步管理。

###线程基本操作###

(1)线程创建

int pthread_create(pthread_t *thread, const pthread_attr_t *attr,void *( * start_routine) (void *), void *arg);

第一个参数是线程的唯一标识；第二个参数设置线程的属性，如果为NULL则使用默认的属性；第三个参数是一个函数指针，指向线程要执行的回调函数；第四个参数是传递给回调函数的参数。

(2)终止当前线程；

void pthread_exit(void *retval);

pthread_exit()函数结束当前的线程并把传递给它的值保存在pthread_join()函数第二个参数中；pthread_exit()不同于exit()，前者只会结束当前线程，而后者则会结束整个进程。

	{% highlight C++ %}
	#include<pthread.h>
	#include<stdio.h>
	#define NUM_THREADS 5
	void *printHello(void *threadid){
		long tid;
		tid=(long)threadid;
		printf("Thread #%ld\n", tid);
		pthread_exit(NULL);
	}
	int main(){
		pthread_t threads[NUM_THREADS];
		int rc;
		long t;
		for(t=0;t<NUM_THREADS;t++){
			rc=pthread_create(&threads[t],NULL,printHello,(void*)t);
			if(rc){
				printf("error\n");
			}
		}
		pthread_exit(NULL);
	}
	{% endhighlight %}

###互斥和同步###

(1)阻塞当前的线程，直到另一个线程运行结束；

int pthread_join(pthread_t thread, void **retval);

第一个参数是由pthread_create()创建线程时分配的thread id，第二个参数是一个二级指针，如果retval为空则忽略回调函数的返回值，否则回调函数的返回值保存在*retval中。

(2)互斥(mutual exclusion，缩写mutex)是指一段区域在同一时间内只能有一个线程对其进行操作，否则会造成不一致的情况，这段区域叫做临界区。互斥只要求同一时间内只能有一个线程进行访问，但是线程之间的访问顺序可以是任意的；同步要求线程之间的访问有一定的顺序，并且一般都要求线程之间互斥访问(如果不修改临界区的值的话可以允许多个只读线程同时访问)。

	{% highlight C++ %}
	#include <stdio.h>
	#include <stdlib.h>
	#include <pthread.h>
	void *functionC();
	pthread_mutex_t mutex1 = PTHREAD_MUTEX_INITIALIZER;
	int  counter = 0;	
	int main()
	{
   		int rc1, rc2;
   		pthread_t thread1, thread2;
   		if( (rc1=pthread_create( &thread1, NULL, &functionC, NULL)) )
   		{
      		printf("Thread creation failed: %d\n", rc1);
   		}
   		if( (rc2=pthread_create( &thread2, NULL, &functionC, NULL)) )
   		{
      		printf("Thread creation failed: %d\n", rc2);
   		}

   		pthread_join( thread1, NULL);
   		pthread_join( thread2, NULL); 
   		exit(EXIT_SUCCESS);
	}

	void *functionC()
	{
   		pthread_mutex_lock( &mutex1 );
   		counter++;
   		printf("Counter value: %d\n",counter);
   		pthread_mutex_unlock( &mutex1 );
	}
	{% endhighlight %}
	
###条件变量###

与互斥锁不同，条件变量是用来等待而不是用来上锁的。条件变量用来自动阻塞一个线程，直到某特殊情况发生为止。通常条件变量和互斥锁同时使用.

条件变量使我们可以睡眠等待某种条件出现。条件变量是利用线程间共享的全局变量进行同步的一种机制，主要包括两个动作：

(1)一个线程等待"条件变量的条件成立"而挂起；

(2)另一个线程使"条件成立"（给出条件成立信号,条件的检测是在互斥锁的保护下进行的。如果一个条件为假，一个线程自动阻塞，并释放等待状态改变的互斥锁。如果另一个线程改变了条件，它发信号给关联的条件 变量，唤醒一个或多个等待它的线程，重新获得互斥锁，重新评价条件。如果两进程共享可读写的内存，条件变量可以被用来实现这两进程间的线程同步。

使用条件变量之前要先进行初始化。可以在单个语句中生成和初始化一个条件变量如：
pthread_cond_t my_condition=PTHREAD_COND_INITIALIZER;（用于进程间线程的通信）。
也可以利用函数pthread_cond_init动态初始化。

	{% highlight C++ %}
	#include <stdio.h>
	#include <stdlib.h>
	#include <pthread.h>
	pthread_mutex_t count_mutex     = PTHREAD_MUTEX_INITIALIZER;
	pthread_cond_t  condition_var   = PTHREAD_COND_INITIALIZER;
	void *functionCount1();
	void *functionCount2();
	int  count = 0;
	#define COUNT_DONE  10
	#define COUNT_HALT1  3
	#define COUNT_HALT2  6
	int main()
	{
   		pthread_t thread1, thread2;
   		pthread_create( &thread1, NULL, &functionCount1, NULL);
   		pthread_create( &thread2, NULL, &functionCount2, NULL);
   		pthread_join( thread1, NULL);
   		pthread_join( thread2, NULL);
   		printf("Final count: %d\n",count);
   		exit(EXIT_SUCCESS);
	}
	void *functionCount1()
	{
   		for(;;)
   		{
      		pthread_mutex_lock( &count_mutex );
      		pthread_cond_wait( &condition_var, &count_mutex );
      		count++;
      		printf("Counter value functionCount1: %d\n",count);
      		pthread_mutex_unlock( &count_mutex );
      		if(count >= COUNT_DONE) return(NULL);
    		}
	}

	void *functionCount2()
	{
    	for(;;)
    	{
       		pthread_mutex_lock( &count_mutex );

       		if( count < COUNT_HALT1 || count > COUNT_HALT2 )
       		{
          		pthread_cond_signal( &condition_var );
       		}
       		else
       		{
          		count++;
          		printf("Counter value functionCount2: %d\n",count);
       		}
       		pthread_mutex_unlock( &count_mutex );
       		if(count >= COUNT_DONE) return(NULL);
    	}
	}
	{% endhighlight %}