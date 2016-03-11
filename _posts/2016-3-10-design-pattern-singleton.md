---
date: 2016-3-10 8:18:30+00:00
layout: post
title: 单例模式
thread: 101
categories: design_pattern
tags: design_pattern
---

单例模式是设计模式中运用最广泛的设计模式了，主要是确保一个类只有一个实例，且自行实例化向整个系统提供服务。 单例模式常用实现有：懒汉式、饿汉式、双重检验锁、静态内部类、枚举。在这小结下。

###懒汉式实现###

 1. 线程不安全（当多个线程并行调用getInstance()时，会创建多个实例）
	
		{% highlight java %}
		public class Singleton	//Singleton.getInstance()获取实例
		{
			//private表明这个类不可能从外部形成实例
			private static Singleton instance; 
			private Singleton(){}
			public static Singleton getInstance()  
			{
				if(instance == null)
				{
					instance = new Singleton();
				}
				return instance;
			} 
		}
		{% endhighlight %}

 2. 线程安全

		{% highlight java %}
		public class Singleton	
		{
			private static Singleton instance; 
			private Singleton(){}
			public static synchronized Singleton getInstance()  
			{
				if(instance == null)
				{
					instance = new Singleton();
				}
				return instance;
			} 
		}
		{% endhighlight %}

上面解决了多个实例的问题，但不高效，因为在任何时候都只能有一个线程调用getInstan()方法，但同步操作只需要在第一次调用时才被需要。此时需要双重检验锁。

###双重检验锁###

双重检验锁模式是一种使用同步块加锁的方法。可实现在只有第一次调用时才进行同步操作。

	{% highlight java %}
	public class Singleton	
	{
		private static Singleton instance; 
		private Singleton(){}
		public static Singleton getInstance()  
		{
			//两次检测install==null
			if(instance == null) //一次在同步块外
			{
				synchronized(Singleton.class)
				{
					if(instance == null) //一次在同步块内
					{
						instance = new Singleton();
					}
				}
			}
			return instance;
		} 
	}
	{% endhighlight %}

`instance = new Singleton();`并非一个原子操作，在jvm中做了下面3步：

 1. 给instance分配内存；
 
 2. 调用Sington构造函数来初始化成员变量；

 3. 给instance对象分配内存空间，此时instance变非null了。

在jvm中的即时编译器中存在指令重排序的优化，即2和3步的顺序不确定，在多线程中可能会报错。解决方法时将instance变量声明为`volatile`(特性1：直接从内存读取；特性2：禁止指令重排序优化)即可。

	{% highlight java %}
	public class Singleton	
	{
		private volatile static Singleton instance; 
		private Singleton(){}
		public static Singleton getInstance()  
		{
			//两次检测install==null
			if(instance == null) //一次在同步块外
			{
				synchronized(Singleton.class)
				{
					if(instance == null) //一次在同步块内
					{
						instance = new Singleton();
					}
				}
			}
			return instance;
		} 
	}
	{% endhighlight %}


###饿汉式实现###

	{% highlight java %}
	public class Singleton	
	{
		private static final Singleton instance = new Singleton(); 
		private Singleton(){}
		public static Singleton getInstance()  
		{
			return instance;
		} 
	}
	{% endhighlight %}

单例的实例被声明为static和final变量，在第一次加载类到内存中就会初始化(缺点)，创建实例本身是线程安全的。


###静态内部类###

	{% highlight java %}
	public class Singleton
	{
		private static class SingletonHolder
		{
			private static final instance = new Singleton();
		}
		private Singleton(){}
		public static final Singleton getInstance()
		{
			return SingletonHolder.instance;
		}
	}
	{% endhighlight %}

利用静态内部类来实现，读取实例是不会进行同步，没有性能缺陷，除了getInstance()外没有其他方法访问，也是懒汉式的。

###枚举###

	{% highlight java %}
	public enum Singleton //利用Singleton.instance来访问
	{
		instance;
	}
	{% endhighlight %}

默认枚举的创建是线程安全的。


参考：[深入浅出单实例Singleton设计模式](http://blog.csdn.net/haoel/article/details/4028232)


 