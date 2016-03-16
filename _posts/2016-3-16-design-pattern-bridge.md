---
date: 2016-3-16 17:59:30+00:00
layout: post
title: 桥接模式
thread: 110
categories: design_pattern
tags: design_pattern
---

桥接模式是将抽象部分和实现部分分离，使它们可以独立的变化。 使用桥接模式可以使有“多维度变化”的类能沿着多个方向进行变化。

### 组合模式四要素 ###

1. Implementor：定义具体行为、特征的应用接口；

2. ConcreteImplementor：实现Implementor接口；

3. Abstraction：定义抽象的接口，该接口包括实现具体行为、特征的Implementor接口；

4. Refined Abstraction：抽象接口Abstrion的子类，也是一个抽象的。

### 桥接模式实现 ###

	{% highlight java %}
	//Implementor
	interface DrawingAPI
	{
		public void drawCircle(double x, double y);
	}
	//ConcreteImplementor
	class DrawingAPI1 implements DrawingAPI
	{
		public void drawCircle(double x, double y)
		{
			System.out.println("API1: %f : %f", x, y);
		}
	}
	class DrawingAPI2 implements DrawingAPI
	{
		public void drawCircle(double x, double y)
		{
			System.out.println("API2: %f : %f", x, y);
		}
	}
	//abstraction
	interface Shape
	{
		public void draw();
	}
	//Refined abstraction
	class CircleShape implements Shape
	{
		private double x, y;
		private DrawingAPI drawingAPI;
		public CircleShape(double x, double y, DrawingAPI drawingAPI)
		{
			this.x = x;
			this.y = y;
			this.drawingAPI = drawingAPI;
		}
		public void draw()
		{
			drawingAPI.drawCircle(x,y);
		}
	}
	//Client
	public class Client
	{
		Shape[] shapes = new Shape[2];
		shapes[0] = new CircleShape(1, 2, new DrawingAPI1());
		shapes[1] = new CircleShape(3, 4, new DrawingAPI2());
		for(Shape shape : shapes)
		{
			shape.draw();
		}
	}
	{% endhighlight %}


### 适用场景 ###

1. 如果一个系统需要在构件的抽象化角色和具体化角色之间增加更多的灵活性，避免在两个层次之间建立静态的联系。 

2. 设计要求实现化角色的任何改变不应当影响客户端，或者说实现化角色的改变对客户端是完全透明的。

3. 一个构件有多于一个的抽象化角色和实现化角色，系统需要它们之间进行动态耦合。 

4. 虽然在系统中使用继承是没有问题的，但是由于抽象化角色和具体化角色需要独立变化，设计要求需要独立管理这两者。



参考： [设计模式-----桥接模式Bridge Pattern](http://www.cnblogs.com/houleixx/archive/2008/02/23/1078877.html)