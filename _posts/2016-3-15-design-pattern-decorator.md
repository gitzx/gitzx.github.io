---
date: 2016-3-15 8:16:30+00:00
layout: post
title: 装饰器模式
thread: 107
categories: design_pattern
tags: design_pattern
---

装饰器模式是一种动态的往一个类中添加新的行为的设计模式。相比生成子类，装饰模式可以给某个对象而不是整个类添加一些新的功能；

装饰模式和适配器模式都是“包装模式(wrapper pattern)”，都是通过封装其他对象达到设计的目的。

1. 装饰模式对被装饰对象进行功能增强的同时，要求具体构件角色、装饰角色的接口和抽象构件角色的接口完全一致。

2. 适配器模式不要求对源对象的功能进行增强，但会改变源对象的接口，以便和目标接口相符合。

###装饰模式四要素###

1. 抽象构件角色(Component)：给出一个抽象接口，以规范准备接收附加责任的对象；

2. 具体构件角色(ConcreteComponent)：定义一个将要接收附加责任的类；

3. 装饰角色(Decorator)：负责给构件对象增加附加的责任。

###基本实现###

	{% highlight java %}
	public interface Component
	{
		public void DoSomething();
	}
	public class ConcreteComponent implements Component
	{
		public void DoSomething()
		{
			System.out.println("ConcreteComponent");
		}
	}
	public class Decorator implements Component
	{
		private Component component;
		public Decorator(Component component)
		{
			this.component = component;
		}
		public void DoSomething()
		{
			component.DoSomething();
		}
	}
	public class ConcreteDecoratorA extends Decorator
	{
		public ConcreteDecoratorA(Component component)
		{
			super(component);
		}
		public void DoSomething()
		{
			super.DoSomething();
			System.out.println("ConcreteDecoratorA");
		}
	}
	public class ConcreteDecoratorB extends Decorator
	{
		public ConcreteDecoratorB(Component component)
		{
			super(component);
		}
		public void DoSomething()
		{
			super.DoSomething();
			System.out.println("ConcreteDecoratorB");
		}
	}
	{% endhighlight %}

###适用场景###

装饰器模式最常用的场景是java的IO库。例如：最里层是一个FileInputStream对象，然后把它传递给一个BufferedInputStream对象，经过BufferedInputStream处理，再把处理后的对象传递给了DataInputStream对象进行处理。

这个过程其实就是装饰器的组装过程，FileInputStream对象相当于原始的被装饰的对象，而BufferedInputStream对象和DataInputStream对象则相当于装饰器。