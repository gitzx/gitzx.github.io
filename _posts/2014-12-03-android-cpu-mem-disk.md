---
date: 2014-12-03 18:12:30+00:00
layout: post
title: Android设备资源占用模拟
thread: 94
categories: android
tags: android
---

类似windows上对CPU、内存、硬盘存储空间占用模拟和网络上下行速率的模拟，我们可以对Android设备上的CPU、内存、存储空间大小和网络上下行速率进行模拟，并作为移动测试系统中的一项测试服务。这个很早之前做的，但一直卡在网络上下行速率限速的功能上。在这小结下之前的工作。

###CPU占用模拟###

对CPU占用模拟，主要是在现有CPU占用率至100%之间进行动态调节。

需要先计算CPU占用率，与CPU时间相关。CPU时间可以通过读取/proc/stat系统文件获取或通过top等命令获取，如下：

![](/assets/blog_pic/proc_stat.PNG)

CPU时间包括：

- 系统时间sy(System time)

- 用户时间us(User time)

- 空闲时间id(Idle time)

- 等待时间wa(Waiting time)

- Nice时间ni(Nice time)

- 硬中断处理时间hi(Hard Irq time)

- 软中断时间si(Soft Irq time)

- 丢失时间st(Steal time)

CPU占用率主要关心系统态占用率(sys)、
用户态占用率(user)和空闲态占用率(idle)，CPU占用率的计算公式如下：

（1）CPU时间=sy+us+id+wa+ni+hi+si+st

（2）%us=(user+system)/cpu时间*100%

（3）%sy=(system+hardIrq+softIrq)/CPU时间*100%

（4）%id=(Idle)/CPU时间*100%

提高CPU占用率，最简单有效的方法就是通过死循环+sleep来实现：

	{% highlight C++ %}
	while(true){ 
	  if(CPU占用率 > 设定的值）{ 
	        sleep（一段时间） 
	    } 
	} 
	{% endhighlight %}

为了保证CPU占用率稳定在用户自定义的占用率附近，需要准确确定“一段时间”值。

###内存占用率模拟###

内存分类(可读取/proc/meminfo获取)：

- VSS（Virtual Set Size）虚拟内存占用；

- RSS（Resident Set Size）实际占用的物理内存包含共享库占用

- PSS（Proportional Set Size）实际占用包含比例分配共享库占用
- USS（Unique Set Size）进程独自占用但不包含共享库占用

其中，VSS>=RSS>=PSS>=USS。

(1)直接在应用层使用new/delete的问题：

- Android内存分为：虚拟机堆和native堆。Android虚拟机堆有最大内存限制如32MB。

- 不能控制进程什么时候把内存还给操作系统

(2)利用mmap让应用程序直接访问设备内存

- 不直接单独使用malloc/free，无法控制进程将内存还给系统的时间

- 使用mmap()映射匿名文件到共享区域申请内存

- 使用munmap()取消映射来释放内存

![](/assets/blog_pic/mmap.PNG)

在这我们使用Android NDK来实现对内存占用的模拟，底层C代码简化如下：

	{% highlight C++ %}
	JNIEXPORT void JNICALL Java_com_netease_AllocateMemory_allocateMem
	(JNIEnv * ev, jclass c, jint size) {
		int allocateSize = (memSize + size) - (memSize + size)%(1024*8);
		if(memSize + size >= 0) {
			if(p) {
				munmap(p,memSize);
			}
			p = (char *)mmap(0,allocateSize,PROT_READ|PROT_WRITE,MAP_ANON|MAP_PRIVATE,-1,0);
		} else {
			return;
		}
		if(p) {
			memSize = allocateSize;
		}
	}
	{% endhighlight %}

生成动态链接库文件.so文件后，上层即可实现调用：

	{% highlight java %}
	public class AllocateMemory {
		public static native void allocateMem(int size);
	    static {
	        System.loadLibrary("memManage");
	    }	
	}
	{% endhighlight %}

###存储空间大小模拟###

磁盘存储空间大小获取和占用模拟：

（1）获取Android设备内部存储控件大小或SD卡大小。

（2）向存储空间内读写文件实现存储空间占用模拟





