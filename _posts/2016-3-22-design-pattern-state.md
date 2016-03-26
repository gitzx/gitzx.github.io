---
date: 2016-3-22 17:31:30+00:00
layout: post
title: 状态模式
thread: 118
categories: design_pattern
tags: design_pattern
---

状态模式允许一个对象在内部状态改变时改变其行为，这个对象看上去就像是改变了它的类一样。

### 状态模式三要素 ###

1. 抽象状态角色(State)：定义一个接口，用于封装环境(Context)对象的一个特定状态所对应的行为。

2. 具体状态角色(ConcreteState)：每个具体状态类都是些了环境的一个状态所对应的行为。

3. 环境角色(Context)：定义客户端所需接口，并保留一个具体状态类的实例。

### 状态模式一般实现 ###

	{% highlight java %}
	//state
	public interface State 
	{
		public void change(Context context);
	}
	//ConcreteStateA
	public class ConcreteStateA implements State
	{
		public void change(Context context)
		{
			//具体状态所对应的行为
			System.out.println("convert to ConcreteStateB");
			context.setState(new CocncreteStateB());
		}
	}
	//ConcreteStateB
	public class ConcreteStateB implements State
	{
		public void change(Context context)
		{
			//具体状态所对应的行为
			System.out.println("convert to ConcreteStateA");
			context.setState(new CocncreteStateA());
		}
	}
	//Context
	public class Context
	{
		private State state;
		public Context(State state)
		{
			super();
			this.state = state;
		}
		public void change()
		{
			state.change(this);
		}
		public void setState(State state)
		{
			this.state = state;
		}
	
	}
	//Client
	public void Client
	{
		public static void main(String[] args)
		{
			State state = new ConcreteStateA();
			Context context = new Context(state);
			context.change();//ConcreteStateA装换后变成ConcreteStateB
			context.change();//ConcreteStateB装换后变成ConcreteStateA
		}
	}
	{% endhighlight %}


### 适用场景 ###

状态模式是封装对象的内部状态，强调对象内部状态变化改变对象的行为。

