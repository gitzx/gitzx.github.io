---
date: 2016-3-21 18:05:30+00:00
layout: post
title: 中介者模式
thread: 117
categories: design_pattern
tags: design_pattern
---

中介者模式是用一个中介对象来封装一系列的对象交互，中介者使各对象不需要显式的相互引用，从而使其耦合松散，且可以独立的改变它们之间的交互。

### 中介者四要素 ###

1. 抽象中介者(Mediator)：定义一个接口，用于与各同事对象之间进行通信；

2. 具体中介者(ConcreteMediator)：抽象中介者的子类，通过协调各个同事对象来实现协作行为，它维持了对各个同事对象的引用。

3. 抽象同事类(Colleague)：定义了各个同事类共有的方法，并声明一些抽象方法供子类实现，同时维持了一个对抽象中介者类的引用，其子类可以通过该引用与中介者通信；

4. 具体同事类(ConcreteColleague)：抽象同事类的子类，每个同事对象与其他同事对象通信时，先与中介者通信，通过中介者来实现与其他同事通信。


### 中介者模式的一般实现 ###

	{% highlight java %}
	//Mediator
	abstract class Mediator
	{
		//存储同事对象
		protected List<Colleague> colleagueAList =  new ArrayList<Colleague>();
		protected List<Colleague> colleagueBList = new ArrayList<Colleague>();
		public void registerColleagueAs(Colleague colleague)
		{
			colleagueAList.add(colleague);
		}
		public void registerColleagueBs(Colleague colleague)
		{
			colleagueBList.add(colleague);
		}
		public abstract void operation(Colleague colleague, String message);
	}
	//ConcreteMediator
	class ConcreteMediator extends Mediator
	{
		//通过中介者调用同事类的方法
		public void operation(Colleague colleague, String message)
		{
			if(colleague instanceof concreteColleagueA)
			{
				for(Colleague colleague: colleagueBList)
				{
					colleague.getMessage(message);
				}
			}
			else if(colleague instanceof concreteColleagueB)
			{
				for(Colleague colleague: colleagueAList)
				{
					colleague.getMessage(message);
				}
			}
		}
	}
	//Colleague
	abstract class Colleague
	{
		//维持一个抽象中介的引用
		protected Mediator mediator;
		protected String name;
		public Colleague(String name, Mediator mediator)
		{
			this.name = name;
			this.mediator = mediator;
		}
		public abstract void sendMessage(String message);
		public abstract void getMessage(String message);
	}
	//ConcreteColleagueA
	class ConcreteColleagueA extends Colleague
	{
		public ConcreteColleagueA(String name, Mediator mediator)
		{
			super(name, mediator);
		}
		public void sendMessage(String message)
		{
			mediator.operation(this, message);
		}
		public void getMessage(String message)
		{
			System.out.println("ConcreteDecoratorA " + name + " 收到ConcreteColleagueB的消息" +message);
		}
	}
	//ConcreteColleagueB
	class ConcreteColleagueB extends Colleague
	{
		public ConcreteColleagueB(String name, Mediator mediator)
		{
			super(name, mediator);
		}
		public void sendMessage(String message)
		{
			mediator.operation(this, message);
		}
		public void getMessage(String message)
		{
			System.out.println("ConcreteDecoratorB " + name + " 收到ConcreteColleagueA的消息" +message);
		}
	}
	//Client
	public class Client
	{
		public Static void main(String[] args)
		{
			Mediator mediator = new ConcreteMediator();
			Colleague colleagueA1 = new ConcreteColleagueA("colleagueA1", mediator);
			Colleague colleagueA2 = new ConcreteColleagueA("colleagueA2", mediator);
			Colleague colleagueB1 = new ConcreteColleagueB("colleagueB1", mediator);
			mediator.registerColleagueAs(colleagueA1);
			mediator.registerColleagueAs(colleagueA2);
			mediator.registerColleagueBs(colleagueB1);
			//向colleagueA1和colleagueA2发消息
			colleagueB1.sendMessage("Hello, colleagueA");
			//向colleagueB1发消息
			colleagueA1.sendMessage("Hello, colleagueB");
			colleagueA2.sendMessage("Hello, colleagueB!!!");
		}
	}
	{% endhighlight %}


### 适用场景 ###

简化对象之间的交互，用中介者和同事的一对多交互代替了原来同事之间的多对多交互。