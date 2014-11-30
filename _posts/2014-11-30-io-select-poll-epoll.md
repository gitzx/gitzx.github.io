---
date: 2014-11-30 10:10:30+00:00
layout: post
title: I/O多路复用中select/poll/epoll小结
thread: 91
categories: network-programming
tags: network-programming
---

linux下I/O多路复用常用于处理多个文件或网络套接字描述符、。linux下I/O多路复用有select、poll、epoll三种机制，通过监视多个描述符，一旦某个描述符准备就绪(读就绪或写就绪)，就通知应用程序进行相应的读写操作。在这小结下linux下I/O多路复用中select/poll/epoll的基本知识。

###select返回套接字描述符就绪的条件###

对于描述符就绪条件包括读就绪、写就绪和是否异常。描述符就绪条件如下：

![](/assets/blog_pic/readytoselect.PNG)

有数据可读指的是套接字接收缓冲区中的数据字节数大于等于套接字接收缓冲区低水位标记的当前大小。对这样的套接字执行读操作不会阻塞并返会一个大于0的值。

有数据可写指的是套接字发送缓冲区的可用空间字节数大于等于套接字发送缓冲区低水位标记的当前大小。

###select用法###

	{% highlight C++ %}
	#include <sys/select.h>
	#include <sys/time.h>
	//若有就绪描述符则返回其数目，超时返回0，出错返回-1
	int select(int maxfdpl, fd_set *readset, fd_set *writeset,
		fd_set *excepset, const struct timeval *timeout);
	{% endhighlight %}

select简单使用如下：

	{% highlight C++ %}
	fd_set fd_in, fd_out;
	struct timeval tv;
	// Reset the sets
	FD_ZERO( &fd_in );
	FD_ZERO( &fd_out );
	// Monitor sock1 for input events
	FD_SET( sock1, &fd_in ); 
	// Monitor sock2 for output events
	FD_SET( sock1, &fd_out ); 
	// Find out which socket has the largest numeric value as select requires it
	int largest_sock = sock1 > sock2 ? sock1 : sock2;
	// Wait up to 10 seconds
	tv.tv_sec = 10;
	tv.tv_usec = 0;
	// Call the select
	int ret = select( largest_sock, &fd_in, &fd_out, NULL, &tv );
	// Check if select actually succeed
	if ( ret == -1 )
		// report error and abort
	else if ( ret == 0 )
		// timeout; no event detected
	else
	{
	    if ( FD_ISSET( sock1, &fd_in ) )
	        // input event on sock1
	    if ( FD_ISSET( sock2, &fd_out ) )
	        // output event on sock2
	}
	{% endhighlight %}

select的主要缺点如下：

（1）linux下select支持的文件描述符数量最大为1024；

（2）在等待文件描述符返回时，不能通过另一个线程对其修改；

（3）若select修改了一个fd_sets，其他所有的fd_sets都必须重新创建；

（4）查找某个文件描述符是否抛出异常需便利FD_ISSET下所有的文件描述符；

（5）在select返回之前，不能使用该下的套接字描述符；

select的主要优势在于：

(1)可移植性；

(2)超时设定可以精确到纳秒，而poll和epoll只能精确到毫秒；

###poll用法###

	{% highlight C++ %}
	#include <poll.h>
	//若有就绪描述符则返回其数目，超时返回0，出错返回-1
	int poll(struct pollfd *fdarray, unsigned long nfds,int timeout);
	{% endhighlight %}

第一个参数指向一个结构数组第一个元素的指针，每个数组元素都是一个pollfd结构，用于指定测试某个给定的fd的条件。

	{% highlight C++ %}
	struct pollfd{
		int fd;
		//events of interest on fd
		short events;
		//events that occurred on fd
		short revents;
	};
	{% endhighlight %}

poll的简单使用如下：
	
	{% highlight C++ %}
	// The structure for two events
	struct pollfd fds[2];
	// Monitor sock1 for input
	fds[0].fd = sock1;
	fds[0].events = POLLIN;
	// Monitor sock2 for output
	fds[1].fd = sock2;
	fds[1].events = POLLOUT;
	// Wait 10 seconds
	int ret = poll( &fds, 2, 10000 );
	// Check if poll actually succeed
	if ( ret == -1 )
		// report error and abort
	else if ( ret == 0 )
		// timeout; no event detected
	else
	{
	    // If we detect the event, zero it out so we can reuse the structure
	    if ( pfd[0].revents & POLLIN )
	        pfd[0].revents = 0;
	        // input event on sock1
	    if ( pfd[1].revents & POLLOUT )
	        pfd[1].revents = 0;
	        // output event on sock2
	}
	{% endhighlight %}

poll修正了select的一些缺点，poll的优势有：

（1）poll支持的文件描述符最大数量没有限制；

（2）不能修改pollfd结构中的数据；

（3）相比select，poll对events控制更好，例如poll在不监控写事件的情况下，能检测到远端shutdown事件。

poll的缺点有：

（1）poll的超时设定只能精确到毫秒。

（2）和select类似，查找某个文件描述符需要遍历所有的pollfd；

（3）和select类似，在poll返回之前，不能使用该下的套接字描述符。

###epoll用法###

epoll只能在linux上使用(封装的除外，如libevent等)，select和poll不限于linux。

epoll的简单使用如下：
	
	{% highlight C++ %}
	// Create the epoll descriptor. Only one is needed per app, and is used to monitor all sockets.
	// The function argument is ignored (it was not before, but now it is), so put your favorite number here
	int pollingfd = epoll_create( 0xCAFE ); 
	if ( pollingfd < 0 )
	 // report error
	// Initialize the epoll structure in case more members are added in future
	struct epoll_event ev = { 0 };
	// Associate the connection class instance with the event. You can associate anything
	// you want, epoll does not use this information. We store a connection class pointer, pConnection1
	ev.data.ptr = pConnection1;
	// Monitor for input, and do not automatically rearm the descriptor after the event
	ev.events = EPOLLIN | EPOLLONESHOT;
	// Add the descriptor into the monitoring list. We can do it even if another thread is 
	// waiting in epoll_wait - the descriptor will be properly added
	if ( epoll_ctl( epollfd, EPOLL_CTL_ADD, pConnection1->getSocket(), &ev ) != 0 )
	    // report error
	// Wait for up to 20 events (assuming we have added maybe 200 sockets before that it may happen)
	struct epoll_event pevents[ 20 ];
	// Wait for 10 seconds
	int ready = epoll_wait( pollingfd, pevents, 20, 10000 );
	// Check if epoll actually succeed
	if ( ret == -1 )
	    // report error and abort
	else if ( ret == 0 )
	    // timeout; no event detected
	else
	{
	    // Check if any events detected
	    for ( int i = 0; i < ret; i++ )
	    {
	        if ( pevents[i].events & EPOLLIN )
	        {
	            // Get back our connection pointer
	            Connection * c = (Connection*) pevents[i].data.ptr;
	            c->handleReadEvent();
	         }
	    }
	}
	{% endhighlight %}

相比select/poll，epoll主要的优点有：

（1）poll支持的文件描述符最大数量没有限制；

（2）使用nmap加速内核与用户空间的消息传递

（3）当events被触发时，epoll只返回文件描述符列表，不用去遍历所有的文件描述符查找哪个event被触发。

（4）epoll可以向触发事件添加内容，而不是通过套接字描述符；

（5）epoll能增加或删除监控的套接字描述符，计算在epoll_wait期间；

（6）epoll允许有多个线程同时等待同一个epoll queue with epoll_wait().

相比poll，epoll主要的缺点有：

（1）改变事件的标识(如读写)需要执行epoll_ctl系统调用；

（2）每个accept()ed socket需要被添加到set中，epoll也是如此，并需要执行两次epoll_ctl系统调用；

###select、poll、epoll比较###

select和poll采用的是内核轮询方式，epoll采用的是事件触发机制。

从触发方式来看，select和poll只有条件触发(或叫水平触发)，epoll则有Level Trigger(LT) 条件触发和Edge Trigger(ET)事件触发(或叫边缘触发)

边缘触发和条件触发的区别如下：

- 边缘触发是指每当状态改变时发生一个io事件；

- 条件触发是只要满足条件就发生一个io事件。

相比select，应优先使用poll。

相比epoll，在一下场景下应优先使用poll：

（1）在不利于libevent等封装epoll的情况下，不止应用与linux系统；

（2）应用程序一次需要监控的套接字数少于1000个，应优先使用poll；

（3）应用程序一次需要监控的套接字数大于1000个，但都是短连接，应优先使用poll。（epoll添加描述符开销较大）

（4）在其他线程等待返回结果时不希望event被改变时，应使用poll。

参考：

[select、poll、epoll之间的区别总结](http://www.cnblogs.com/Anker/p/3265058.html)

[select / poll / epoll: practical difference for system architects](http://www.ulduzsoft.com/2014/01/select-poll-epoll-practical-difference-for-system-architects/)