---
date: 2016-3-18 15:00:30+00:00
layout: post
title: 命令模式
thread: 114
categories: design_pattern
tags: design_pattern
---

命令模式把一个请求或操作封装在一个对象中。命名模式允许系统使用不同的请求把客户端参数化，对请求排队或记录请求日志，可以提供命令的撤销功能。

### 命令模式五要素 ###

1. 接收者角色(Receiver)：负责具体实施和执行一个请求，实施和执行请求的方法叫做行动方法；

2. 抽象命令角色(Command)：声明一个给所有具体命令类的抽象接口；

3. 具体命令角色(ConcreteCommand)：实现抽象接口中的方法，负责调用接收者的相应操作；

4. 请求者角色(Invoker):负责调用命令对象执行请求；

5. 客户端角色(Client)：创建一个命令对象并确定其接收者。


### 命令模式一般实现 ###

	{% highlight java %}
	//Receiver
	public class Receiver
	{
		public void action1()
		{
			System.out.println("action111");
		}
		public void action2()
		{
			System.out.println("action222");
		}
	}
	//AbstractCommand
	public interface Command 
	{
		//执行方法
		void excute();
	}
	//ConcreteCommand1
	public class ConcreteCommand1 implements Command
	{
		private Receiver receiver = null;
		public ConcreteCommand1(Receiver receiver)
		{
			this.receiver = receiver;
		}
		public void excute()
		{
			receiver.action1();
		}
	}
	public class ConcreteCommand2 implements Command
	{
		private Receiver receiver = null;
		public ConcreteCommand2(Receiver receiver)
		{
			this.receiver = receiver;
		}
		public void excute()
		{
			receiver.action2();
		}
	}
	//Invoker
	public class Invoker
	{
		private Command command1 = null;
		private Command command2 = null;
		public void setCommand1(Command command1)
		{
			this.command1 = command1;
		}
		public void setCommand2(Command command2)
		{
			this.command2 = command2;
		}
		public void action1()
		{
			command1.excute();
		}
		public void action2()
		{
			command2.excute();
		}
	}
	//Client
	public class Client
	{
		public static void main(String[] args)
		{
			Receiver receiver = new Receiver();
			ConcreteCommand1 concreteCommand1 = new ConcreteCommand1(receiver);
			ConcreteCommand2 concreteCommand2 = new ConcreteCommand2(receiver);
			Invoker invoker = new Invoker();
			invoker.setCommand1(concreteCommand1);
			invoker.setCommand2(concreteCommand2);
			invoker.action1();
			invoker.action2():
		}
	}
	{% endhighlight %}


### 适用场景 ###

适用于大多数请求-响应的场景。


参考：[JAVA与模式之命令模式](http://www.cnblogs.com/java-my-life/archive/2012/06/01/2526972.html)