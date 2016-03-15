---
date: 2016-3-11 9:10:30+00:00
layout: post
title: 原型模式
thread: 102
categories: design_pattern
tags: design_pattern
---

原型模式是用原型实例指定创建对象的种类，并通过拷贝这些原型创建新的对象。由于Object类的clone()方法是一个本地方法，直接操作内存中的二进制流，因此利用原型模型创建对象比直接new一个对象在性能上好的多。

原型模式设计三个角色：

 1. 客户角色(client)：客户端提出创建对象的请求；

 2. 抽象原型(prototype)：给出具体原型类的接口，通常是接口类或抽象类；

 3. 具体原型(concrete prototype)：实现抽象原型，是被复制的对象。


###抽象原型###

抽象原型(prototype)需满足以下两个条件：

1. 实现Cloneable接口。 在java虚拟机中，只有实现了Cloneable接口的类才可以被拷贝；

2. 重写Object类的clone方法。 Object类中有一个clone方法，作用是返回对象的一个拷贝，但其作用域是protected类型的，一般类无法调用，需要重写将clone方法的作用域修改为public类型。

		{% highlight java %}
		public class Prototype implements Cloneable
		{
			public Prototype clone()
			{
				Prototype prototype = null;
				prototype = (Prototype)super.clone();
				return prototype;
			}
		}
		{% endhighlight %}


###具体原型###

	{% highlight java %}
	public class ConcretePrototype extends Prototype
	{
		public void show(int i)
		{
			System.out.println(i);
		}
	}
	{% endhighlight %}

###客户角色(client)###

	{% highlight java %}
	public class Client
	{
		public static void main(String[] args)
		{
			ConcretePrototype cp = new ConcretePrototype();
			for(int i=0;i<5;i++)
			{
				ConcretePrototype clonecp = (ConcretePrototype)cp.clone();
				clonecp.show(i);
			}
		}
	}
	{% endhighlight %}

###其他注意点###

1. 使用原型模式不会调用类的构造方法。因为对象的复制是通过Object类的clone()来实现的，直接在内存中复制数据，因此不会调用类的构造方法；

2. 深拷贝和浅拷贝。 Object类中的clone()方法只会拷贝对象中的基本数据类型(深拷贝)(String除外，String是浅拷贝)，字符串、数组、容器对象和引用对象等都不会拷贝(浅拷贝)。若需要实现深拷贝，需将原型模式中的数组、容器对象、引用对象等另行拷贝。例如(以ArrayList为例):

		{% highlight java %}
		public class Prototype implements Cloneable
		{
			private ArrayList list = new ArrayList();
			public Prototype clone()
			{
				Prototype prototype = null;
				prototype = (Prototype)super.clone();
				prototype.list = (ArrayList)this.list.clone();
				return prototype;
			}
		}
		{% endhighlight %}


参考：[23种设计模式（5）：原型模式](http://blog.csdn.net/zhengzhb/article/details/7393528)

[JAVA设计模式学习9——原型模式](http://alaric.iteye.com/blog/1909960)

 