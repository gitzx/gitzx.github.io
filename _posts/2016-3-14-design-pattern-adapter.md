---
date: 2016-3-14 12:01:30+00:00
layout: post
title: 适配器模式
thread: 106
categories: design_pattern
tags: design_pattern
---

适配器模式是将一个类的接口转换成用户期待的另一个类的接口，使得因接口不兼容而不能一起工作的两个类能一起工作。做法是将一个类的接口包裹在另一个类中。  适配器模式有类适配器模式和对象适配器模式两种不同的形式（尽量多使用对象适配器模式，多用组合，少用继承）。

###适配器三要素###

1. 目标角色(Target)：用户期待得到的接口；

2. 源角色(Adapee)：需要适配的接口；

3. 适配器角色(Adapter)：将源接口转换为目标接口。

###类适配器模式###

	{% highlight java %}
	interface Target
	{
		void DoSomething();
	}
	class Adapee
	{
		void DoSpecialthing()
		{
			System.out.println("Adapee");
		}
	}
	class Adapter extends Adapee implements Target
	{
		public void DoSomething()
		{
			System.out.println("Adapter");
			super.DoSpecialthing();
		}
	}
	public class Client
	{
		public static void main(String[] args)
		{
			Target target = new Adapter();
			target.DoSomething();
		}
	}
	{% endhighlight %}

###对象适配器模式###

	{% highlight java %}
	interface Target
	{
		void DoSomething();
	}
	class Adapee
	{
		void DoSpecialthing()
		{
			System.out.println("Adapee");
		}
	}
	class Adapter implements Target
	{
		private Adapee adapee;
		public Adapter()
		{
			this.adapee = new Adapee();
		}
		public void DoSomething()
		{
			System.out.println("Adapter");
			adapee.DoSpecialthing();
		}
	}
	public class Client
	{
		public static void main(String[] args)
		{
			Target target = new Adapter();
			target.DoSomething();
		}
	}
	{% endhighlight %}


###适用场景###

1. 系统需要使用现有的类，而这些类的接口不符合系统的需要；

2. 建立一个可以重复使用的类，用于彼此之间没多大关联的一些类。
