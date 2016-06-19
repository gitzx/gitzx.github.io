---
date: 2016-3-18 8:36:30+00:00
layout: post
title: 模板方法模式
thread: 113
categories: design_pattern
tags: design_pattern
---

模板方法定义了一个操作中算法的骨架，而将一些步骤延迟到子类中，模板方法模式使得子类在不改变算法的结构即可重新定义该算法的某些特定操作。模板方法模式只有类之间的继承关系，没有对象关联关系。

### 模板方法模式两要素 ###

1. 抽象类(AbstractClass)：定义抽象的原语操作(primitive operation)。抽象类中定义的方法有模板方法和基本方法。模板方法是把基本操作方法组合在一起形成一个总算法或一个总行为的方法。基本方法是实现算法各个步骤的方法，基本方法有：

	a).抽象方法(Abstract Method)：在抽象类中声明，由具体子类实现，以abstract标识；

	b).具体方法(Concrete Method)：在抽象类中声明和实现，在子类中不实现或替换；

	c).钩子方法(Hook Method)：在抽象类中声明和实现，在子类中会加以扩展，通常抽象类中给出的实现是一个空实现，作为方法的默认实现。

2. 具体子类(ConcreteClass)：实现原语操作以完成算法中与特定子类相关的步骤。


### 模板方法模式的一般实现 ###

	{% highlight java %}
	//AbstrctClass
	public abstract class AbstrctClass
	{
		//模板方法
		public void templateMethod()
		{
			//调用基本方法
			abstractMethod();
			hookMethod();
			concreteMethod();
		}
		//abstractMethod
		protected abstract void abstractMethod();
		//hookMethod 默认空实现
		protected void hookMethod(){}
		//concreteMethod 
		private final void concreteMethod()
		{
			System.out.println("template");
		}
	}
	//ConcreteClass
	public class ConcreteClass extends AbstrctClass
	{
		public void abstractMethod()
		{
			System.out.println("ConcreteClass : abstractMethod");
		}
		public void hookMethod()
		{
			System.out.println("ConcreteClass : hookMethod");
		}
	}
	//Client
	public class Client
	{
		public static void main(String[] args)
		{
			AbstrctClass ac = new ConcreteClass();
			ac.abstractMethod();
			ac.hookMethod();
		}
	}
	{% endhighlight %}


### 适用场景 ###

1. 多个子类具有公共的方法，且逻辑基本相同；

2. 重要复杂的算法可以设计为模板算法，其他算法由子类实现。


