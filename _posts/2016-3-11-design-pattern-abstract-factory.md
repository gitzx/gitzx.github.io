---
date: 2016-3-11 21:53:30+00:00
layout: post
title: 抽象工厂模式
thread: 104
categories: design_pattern
tags: design_pattern
---

抽象工厂模式是工厂方法模式的升级版本，抽象工厂模式为创建一组相关或相互依赖的对象提供一个接口，且无需指定它们的具体类。 抽象工厂模式与工厂方法模式的区别在于：工厂方法模式是针对一个产品登记结构，抽象工厂模式是针对多个产品等级结构。

###抽象工厂模式的一般实现###

	{% highlight java %}
	interface IProduct1
	{
		public void show();
	}
	interface IProduct2
	{
		public void show();
	}
	class Product1 implements IProduct1
	{
		public void show()
		{
			System.out.println("Product1");
		}
	}
	class Product1 implements IProduct2
	{
		public void show()
		{
			System.out.println("Product2");
		}
	}
	interface IFactory
	{
		public IProduct1 createProduct1();
		public IProduct2 createProduct2();
	}
	class Factory implements IFactory
	{
		public IProduct1 createProduct1()
		{
			return new Product1;
		}
		public IProduct2 createProduct2()
		{
			return new Product2;
		}
	}
	public class Client
	{
		public static void main(String[] args)
		{
			IFactory factory = new Factory();
			factory.createProduct1().show();
			factory.createProduct2().show();
		}
	}
	{% endhighlight %}

