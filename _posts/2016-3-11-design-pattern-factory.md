---
date: 2016-3-11 20:13:30+00:00
layout: post
title: 工厂模式
thread: 103
categories: design_pattern
tags: design_pattern
---

工厂模式可以分为工厂模式和抽象工厂模式，将简单工厂模式看作为工厂模式的一个特例。工厂模式定义了一个用于创建对象的接口，让子类决定实例化哪一个类，工厂方法模式使的一个类的实例化延迟到其子类。在这小结下工厂方法模式。

###工厂模式四要素###

工厂模式有四个要素：

1. 工厂接口：工厂接口是工厂方法模式的核心，与调用者直接交互来提供产品；

2. 工厂实现：工厂实现决定如何实例化产品；

3. 产品接口：产品接口定义产品的规范；

4. 产品实现：实现产品接口的具体类，决定了产品在客户端中的具体行为。


		{% highlight java %}
		interface IProduct
		{
			public void productMethod();
		}
		
		class Product implements IProduct
		{
			public void productMethod()
			{
				System.out.println("product");
			}
		}
		
		interface IFactory
		{
			public IProduct createProduct();
		}
		
		class Factory implements IFactory
		{
			public IProduct createProduct()
			{
				return new Product();
			}
		}
		
		public class Client
		{
			public static void main(String[] args)
			{
				IFactory factory = new Factory();
				IProduct product = factory.createProduct();
				product.productMethod();
			}
		}
		{% endhighlight %}


###适用场景###

1. 需要封装对象的创建过程，例如复杂对象的创建，简单对象如只需new即可创建的对象，无需使用工厂方法模式；

2. 客户端程序使用的对象存在变动的可能，或者事先不知道使用哪一个具体对象。

例如汽车组装：

	{% highlight java %}
	interface ICar
	{
		public void show();
	}
	class Car implements ICar
	{
		public void show()
		{
			System.out.println("Car");
		}
	}
	interface IFactory {  
	    public ICar createCar();  
	}  
	class Factory implements IFactory {  
	    public ICar createCar() {  
	        Engine engine = new Engine();  
	        Underpan underpan = new Underpan();  
	        Wheel wheel = new Wheel();  
	        ICar car = new Car(underpan, wheel, engine);  
	        return car;  
	    }  
	}  
	public class Client {  
	    public static void main(String[] args) {  
	        IFactory factory = new Factory();  
	        ICar car = factory.createCar();  
	        car.show();  
	    }  
	} 
	{% endhighlight %} 


参考：[23种设计模式：工厂方法模式](http://blog.csdn.net/zhengzhb/article/details/7348707)