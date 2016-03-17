---
date: 2016-3-17 8:35:30+00:00
layout: post
title: 代理模式
thread: 111
categories: design_pattern
tags: design_pattern
---

代理模式是为其他对象提供一种代理以控制整个对象的访问。代理模式在客户端和目标对象之前起到中介作用，降低系统耦合度。常见的代理有引用计数。

### 代理模式三要素 ###

1. 抽象主题角色(Subject)：声明真实对象和代理对象的共同接口；

2. 代理主题角色(Proxy)：代理对象角色内部含有对真实对象的引用，在执行真实对象的操作时，可以附加其他操作，相当于对真实对象进行封装；

3. 真实主题角色(RealSubject)：我们需要引用的角色对象。

### 代理模式一般实现 ###

	{% highlight java %}
	//Subject
	interface Subject
	{
		void DoSomethingA();
		void DoSomethingB();
	}
	//RealSubject
	public class RealSubject implements Subject
	{
		void DoSomethingA()
		{
			System.out.println("DoSomethingA");
		}
		void DoSomethingB()
		{
			System.out.println("DoSomethingB");
		}
	}
	//proxy
	public class Proxy implements Subject
	{
		void DoSomethingA()
		{
			RealSubject rsa = new RealSubject();
			rsa.DoSomethingA();
			System.out.println("Proxy: DoSomethingA");
		}
		void DoSomethingB()
		{
			RealSubject rsb = new RealSubject();
			rsb.DoSomethingB();
			System.out.println("Proxy: DoSomethingB"); 
		}
	} 
	//Client
	public class Client
	{
		public Static void main(String[] args)
		{
			Subject proxy = new Proxy();
			proxy.DoSomethingA();
			proxy.DoSomethingB();
		}
	}
	{% endhighlight %}


### 适用场景 ###

1. 智能引用计数；

2. 远程代理：为位于不同地址空间的对象提供一个本地的代理对象；

3. 虚拟代理：如果需要创建一个资源消耗较大的对象，先创建一个消耗相对较小的对象来表示，真实对象只在需要时才会被真正创建。

4. 保护代理：控制对一个对象的访问，可以给不同的用户提供不同级别的使用权限。

5. 缓冲代理： 为某一个目标操作的结果提供临时的存储空间，以便多个客户端可以共享这些结果。

参考：

[6. 代理模式](http://design-patterns.readthedocs.org/zh_CN/latest/structural_patterns/proxy.html)