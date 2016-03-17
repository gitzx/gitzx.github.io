---
date: 2016-3-17 17:32:30+00:00
layout: post
title: 享元模式
thread: 112
categories: design_pattern
tags: design_pattern
---

享元模式是通过共享技术以便有效的支持大量细粒度对象的复用。

### 享元模式四要素 ###

1. 抽象享元角色(Flyweight)：声明具体享元类需要实现的公共接口；

2. 具体享元角色(ConcreteFlyWeight)：实现FlyWeight接口，所含的状态须是内部状态；

3. 享元工厂角色(FlyweightFactory)：负责创建和管理享元角色，确保合理共享。

### 享元模式一般实现 ###

	{% highlight java %}
	//Flyweight
	interface Shape
	{
		public void draw();
	}
	//ConcreteFlyWeight
	public class Circle implements Shape
	{
		private String color;
		private int x;
		private int y;
		public Circle(String color)
		{
			this.color = color;
		}
		public void setX(int x)
		{
			this.x = x;
		}
		public void setY(int y)
		{
			this.y = y;
		}
		public void draw()
		{
			System.out.println("color: " + color + " x : y : " + x + ":" + y);
		}
	} 
	//FlyweightFactory
	public class ShapeFactory
	{
		private static final HashMap<String, Shape> circleMap = new HashMap();
		public static Shape getCircle(String color)
		{
			Circle circle = (Circle)CircleMap.get(color);
			circle = new Circle(color);
			circleMap.put(color, circle);
			return circle;
		}
	}
	//Client
	public class Client
	{
		private static final String colors[] = { "Red", "Green", "Blue", "White", "Black" };
	    public static void main(String[] args) {
	        for (int i = 0; i < 5; ++i) {
	            Circle circle = (Circle) ShapeFactory.getCircle(getRandomColor());
	            circle.setX(getRandomX());
	            circle.setY(getRandomY());
	            circle.draw();
	        }
	    }
	    private static String getRandomColor() {
	        return colors[(int) (Math.random() * colors.length)];
	    }
	    private static int getRandomX() {
	        return (int) (Math.random() * 100);
	    }
	    private static int getRandomY() {
	        return (int) (Math.random() * 100);
	    }
	}
	{% endhighlight %}


### 适用场景 ###

1. 应用程序中使用了大量的对象，造成较大的内存开销；

2. 对象的大多数状态可以变成外部状态（如上文中的x，y）；

3. 若删除对象的外部状态，可以用较少的共享对象取代很多组对象；

4. 应用程序不依赖对象标识。


参考：  [JAVA设计模式学习14——享元模式](http://alaric.iteye.com/blog/1914498)

