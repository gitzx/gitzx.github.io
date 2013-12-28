---
date: 2013-12-28 18:42:30+00:00
layout: post
title: 生产者消费者问题
thread: 19
categories: java
tags: java
---

生产者消费者问题（producer-consumer problem）是一个经典的多线程同步问题。主要描述了两个共享固定大小缓冲区的线程--即“生产者”和“消费者”在处理共享缓冲区的问题：

- 生产者在缓冲区未满时向缓冲区放入数据，缓冲区满则停止放入；

- 消费者在缓冲区有数据时开始消费，缓冲区为空则停止消费；

- 生产者在缓冲区满时休眠，等下次消费者消耗数据时被唤醒；

- 消费者在缓冲区为空时休眠，等生产者向缓冲区添加数据时被唤醒。

###模拟生产者-消费者（java）###

	public class producer_consumer
	{
		public static void main(String[] argv){
			Godown godown = new Godown(30);
			Consumer c1 = new Consumer(50,godown);
			Consumer c2 = new Consumer(20,godown);
			Consumer c3 = new Consumer(30,godown);
			Producer p1 = new Producer(10,godown);
			Producer p2 = new Producer(20,godown);
			Producer p3 = new Producer(100,godown);
	
			c1.start();
			c2.start();
			c3.start();
			p1.start();
			p2.start();
			p3.start();
		}
	}
	
	class Godown
	{
		public static final int max_size = 100;
		public int curnum;
		Godown(){}
		Godown(int curnum){
			this.curnum = curnum;
		}
		public synchronized void produce(int neednum){
			while(neednum+curnum > max_size){
				System.out.println("要生产的数量"+neednum
					+"超过剩余量"+ (max_size-curnum)+",暂停生产");
				try{
					wait();
				}catch(InterruptedException e)
					{e.printStackTrace();}
			}
			curnum +=  neednum;
			System.out.println("已生产了"+neednum
				+"个产品，剩余"+curnum);
			notifyAll();
		}
		public synchronized void consume(int neednum){
			while(curnum<neednum){
				try{
					wait();
				}catch(InterruptedException e){
					e.printStackTrace();
				}
			}
			curnum -= neednum;
			System.out.println("已消费了"+neednum
				+"个产品，剩余"+curnum);
			notifyAll();
		}
	}
	class Producer extends Thread
	{
		private int neednum;
		private Godown godown;
		Producer(int neednum,Godown godown){
			this.neednum = neednum;
			this.godown = godown;
		}
		public void run(){
			godown.produce(neednum);
		}
	}
	class Consumer
	{
		private int neednum;
		private Godown godown;
		Consumer(int neednum,Godown godown){
			this.neednum = neednum;
			this.godown = godown;
		}
		public void run(){
			godown.consume(neednum);
		}
	}

JAVA多线程同步主要依赖于若干方法和关键字

1  wait方法：

该方法属于Object的方法，wait方法的作用是使得当前调用wait方法所在部分（代码块）的线程停止执行，并释放当前获得的调用wait所在的代码块的锁，并在其他线程调用notify或者notifyAll方法时恢复到竞争锁状态（一旦获得锁就恢复执行）。

调用wait方法需要注意几点：
 
- 第一点：wait被调用的时候必须在拥有锁（即synchronized修饰的）的代码块中。

- 第二点：恢复执行后，从wait的下一条语句开始执行，因而wait方法总是应当在while循环中调用，以免出现恢复执行后继续执行的条件不满足却继续执行的情况。

- 第三点：若wait方法参数中带时间，则除了notify和notifyAll被调用能激活处于wait状态（等待状态）的线程进入锁竞争外，在其他线程中interrupt它或者参数时间到了之后，该线程也将被激活到竞争状态。

- 第四点：wait方法被调用的线程必须获得之前执行到wait时释放掉的锁重新获得才能够恢复执行。

2  notify方法和notifyAll方法：

- notify方法通知调用了wait方法，但是尚未激活的一个线程进入线程调度队列（即进入锁竞争），注意不是立即执行。并且具体是哪一个线程不能保证。另外一点就是被唤醒的这个线程一定是在等待wait所释放的锁。
        
- notifyAll方法则唤醒所有调用了wait方法，尚未激活的进程进入竞争队列。


3 synchronized关键字：

- 第一点：synchronized用来标识一个普通方法时，表示一个线程要执行该方法，必须取得该方法所在的对象的锁。

- 第二点：synchronized用来标识一个静态方法时，表示一个线程要执行该方法，必须获得该方法所在的类的类锁。

- 第三点：synchronized修饰一个代码块。类似这样：synchronized(obj) { //code.... }。表示一个线程要执行该代码块，必须获得obj的锁。这样做的目的是减小锁的粒度，保证当不同块所需的锁不冲突时不用对整个对象加锁。利用零长度的byte数组对象做obj非常经济。

4 atomic action（原子操作）：
       
 在JAVA中，以下两点操作是原子操作。但是c和c++中并不如此。

- 第一点：对引用变量和除了long和double之外的原始数据类型变量进行读写。
 
- 第二点：对所有声明为volatile的变量（包括long和double）的读写。

- 另外：在java.util.concurrent和java.util.concurrent.atomic包中提供了一些不依赖于同步机制的线程安全的类和方法。

参考:[生产者消费者问题理解与Java实现](http://www.cnblogs.com/dennisit/archive/2013/02/25/2931573.html)