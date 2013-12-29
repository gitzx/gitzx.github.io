---
date: 2013-12-29 19:28:30+00:00
layout: post
title: java多线程创建的几种方法
thread: 20
categories: java
tags: java
---

通过多线程机制，一些任务可中的每一个都将由执行线程来驱动，一个线程就是在进程中的一个单一的顺序控制流。在java中，有三种常用方法来实现多线程。

###实现Runnable接口###

如果是实现了java.lang.Runnable接口的类，在Runnable接口中编写run（）方法，则用Thread的构造方法：

- Thread(Runnable target) 

- Thread(Runnable target, String name) 

- Thread(ThreadGroup group, Runnable target) 

- Thread(ThreadGroup group, Runnable target, String name) 

- Thread(ThreadGroup group, Runnable target, String name, long stackSize)

例如：

	public class LiftOff implements Runnable{
		protected int countDown = 10;
		private static int taskCount = 0;
		private final int id = taskCount++;
		public LiftOff(){}
		public LiftOff(int countDown){
			this.countDown = countDown;
		}
		public String status(){
			return "#"+id+"("+(countDown>0?countDown:"LiftOff")+").";
		}
		public void run(){
			while(countDown-->0){
				System.out.println(status());
				Thread.yield();
			}
		}
	}
使用Thread构造器来驱动LiftOff对象：

	public class MoreBasicThreads{
		public static void main(String[] argv){
			for(int i=0;i<5;i++){
				Thread t = new Thread(new LiftOff());
				t.start();
			}
		}
	}

###直接继承Thread###

如果是扩展java.lang.Thread类的线程，则直接new即可。

例如：

	public class SimpleThread extends Thread{
		private int countDown = 5;
		private static int threadCount = 0;
		public SimpleThread(){
			super(Integer.toString(++threadCount));
			start();
		}
		public String toString(){
			return "#"+getName()+"("+countDown+").";
		}
		public void run(){
			while(true){
				System.out.print(this);
				if(--countDown==0){
					return;
				}
			}
		}
		public static void main(String[] argv){
			for(int i=0;i<5;i++){
				new SimpleThread();
			}
		}
	}

###使用Executor###

java.util.concurrent包中的执行器（Executor）将为我们管理Thread对象，Executor在客户端和任务执行之剑提供了一个间接层，这个中介对象将执行任务。帮我们管理线程的生命周期。

例如：

CachedThreadPool为每个任务都创建一个线程

	import java.util.concurrent.*;
	public class CachedThreadPool{
		public static void main(String[] argv){
			ExecutorService exec = Executors.newCachedThreadPool();
			for(int i=0;i<5;i++){
				exec.execute(new LiftOff());
			}
			exec.shutdown();
		}
	}

FixedThreadPool一次性预先执行线程分配，但线程数量预先固定了。

	import java.util.concurrent.*;
	public class FixedThreadPool{
		public static void main(String[] argv){
			ExecutorService exec = Executors.newFixedThreadPool();
			for(int i=0;i<5;i++){
				exec.execute(new LiftOff());
			}
			exec.shutdown();
		}
	}

SingleThreadExecutor就像是线程数量为1的FixedThreadPool，若向SingleThreadExecutor提交多个任务，这些任务将排队，每个任务都会在下一个任务开始前运行结束，所以的任务都使用相同的线程。

	import java.util.concurrent.*;
	public class SingleThreadExecutor{
		public static void main(String[] argv){
			ExecutorService exec = Executors.newSingleThreadExecutor();
			for(int i=0;i<5;i++){
				exec.execute(new LiftOff());
			}
			exec.shutdown();
		}
	}
