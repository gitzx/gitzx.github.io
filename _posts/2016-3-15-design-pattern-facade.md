---
date: 2016-3-15 19:02:30+00:00
layout: post
title: 外观模式
thread: 108
categories: design_pattern
tags: design_pattern
---

外观系统是为子系统中的一组接口提供一个统一的高层接口，使得子系统更容易使用。

###外观模式两要素###

1. 外观角色(facade)：外观角色知道相关子系统的接口功能，提供共同的对外接口，客户端可以调用这个角色的方法。

2. 子系统角色：可以同时有一个或多个子系统，每个子系统都不是一个单独的类，而是一个类的集合。每个子系统都可以被客户端或外观角色调用。

###常用实现###

	{% highlight java %}
	class ClassA
	{
		public void DoSomethingA1(){}
		public void DoSomethingA2(){}
		public void DoSomethingA3(){}
	}
	class ClassB
	{
		public void DoSomethingB1(){}
		public void DoSomethingB2(){}
	}
	class ClassC
	{
		public void DoSomethingC1(){}
		public void DoSomethingC2(){}
	}
	class Facade
	{
		private ClassA ca = new ClassA();
		private ClassB cb = new ClassB();
		private ClassC cc = new ClassC();
		public void DoSomething()
		{
			ca.DoSomethingA1();
			ca.DoSomethingA3();
			cb.DoSomethingB2();
			cb.DoSomethingC1();
		}
	}
	public class Client
	{
		public static void main(String[] args)
		{
			Facade facade = new Facade();
			facade.DoSomething();
		}
	}
	{% endhighlight %}

###适用场景###

适用用只需使用某些类的某些方法，而不需要与每一个类进行交互。
