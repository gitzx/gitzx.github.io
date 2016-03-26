---
date: 2016-3-20 16:22:30+00:00
layout: post
title: 观察者模式
thread: 116
categories: design_pattern
tags: design_pattern
---

观察者模式定义了一种一对多的依赖关系，让多个观察者对象同时监听某一个主题对象，这个主题对象在状态上发生变化时，会通知所有的观察者对象，使它们能自动更新自己。

### 观察者模式四要素 ###

1. 抽象主题角色(subject)：抽象主题角色提供维护一个观察者对象聚集的操作方法，如聚集的增加、删除等；

2. 具体主题角色(ConcreteSubject)：将有关状态存入具体的观察者对象，在具体主题的内部状态改变时，给所有登记过的观察者发出通知。具体主题对象负责实现抽象抽象主题中的方法；

3. 抽象观察者角色(Observer)：为具体观察者提供更新接口；

4. 具体观察者角色(ConcreteObserver)：存储与主题相关的状态，实现抽象观察者提供的更新接口。

### 观察者模式两种模型 ###

观察者模式分为推模型和拉模型两种实现：

1. 推模型：主题对象向观察者对象推送主题的详细信息(全部或部分数据)，不管观察者对象是否需要。

2. 拉模型：主题对象在通知观察者时只传递少量信息，若观察者需要具体的信息，则有观察者主动到主题对象中获取，相当于是观察者从主题对象中拉数据。一般情况是主题对象自身通过update方法传递给观察者。

### 观察者模式推模型一般实现 ###

	{% highlight java %}
	//Observer
	public interface Observer
	{
		public void update(String newState);
	}
	//ConcreteObserver
	public class ConcreteObserver implements Observer
	{
		public void update(String newState)
		{
			//业务逻辑
			System.out.println("newState: " + newState);
		}
	}
	//Subject
	public interface Subject
	{
		public void attach(Observer observer);
		public void detach(Observer observer);
		void notifyObserver();
	}
	//ConcreteSubject
	public class ConcreteSubject implements Subject
	{
		private List<Observer> list = new ArrayList<Observer>();
		//注册观察者对象
		public void attach(Observer observer)
		{
			list.add(observer);
		}
		//删除观察者对象
		public void detach(Observer observer)
		{
			list.remove(observer);
		}
		//通知观察者对象
		public void notifyObserver(String newState)
		{
			for(Observer observer:list)
			{
				observer.update(newState);
			}
		}
	}
	//Client
	public class Client
	{
		public static void main(String[] args)
		{
			Observer observer = new ConcreteObserver();
			Subject subject = new ConcreteSubject();
			subject.attach(observer);
			subject.notifyObserver("state111"); 
		}
	}
	{% endhighlight %}


### 观察者模式拉模型一般实现 ###

	{% highlight java %}
	//Observer
	public interface Observer
	{
		public void update(Subject subject);
	}
	//ConcreteObserver
	public class ConcreteObserver implements Observer
	{
		private String observerState;
		public void update(Subject subject)
		{
			observerState = ((ConcreteSubject)subject).getState();
			//业务逻辑
			System.out.println("newState: " + observerState);
		}
	}
	//Subject
	public interface Subject
	{
		public void attach(Observer observer);
		public void detach(Observer observer);
		void notifyObserver();
	}
	//ConcreteSubject
	public class ConcreteSubject implements Subject
	{
		private String state;
		private List<Observer> list = new ArrayList<Observer>();
		//注册观察者对象
		public void attach(Observer observer)
		{
			list.add(observer);
		}
		//删除观察者对象
		public void detach(Observer observer)
		{
			list.remove(observer);
		}
		//通知观察者对象
		public void notifyObserver()
		{
			for(Observer observer:list)
			{
				observer.update(this);
			}
		}
		public String getState()
		{
			return state;
		}
	}
	//Client
	public class Client
	{
		public static void main(String[] args)
		{
			Observer observer = new ConcreteObserver();
			Subject subject = new ConcreteSubject();
			subject.attach(observer);
			subject.notifyObserver(); 
		}
	}
	{% endhighlight %}


### java中Observable类和Observer接口对观察者模式支持 ###

使用`java.util.Observable`和`java.util.Observer`可以方便的实现观察者模式。一个Observable对象可以有一个或多个观察者，一个Observable实例改变后，调用Observable的notifyObservers方法的应用程序会通过调用观察者的update方法来通知观察者该实例已经改变。

主要的方法有：`notifyObservers()` , `notifyObservers(java.lang.Object)` , `Observer.update(java.util.Observable, java.lang.Object)`

