---
date: 2016-3-23 15:25:30+00:00
layout: post
title: 策略模式
thread: 119
categories: design_pattern
tags: design_pattern
---

策略模式将每一个算法封装起来，且使它们可以相互替换。策略模式使得算法可以在不影响到客户端的情况下发生变化。

### 策略模式三要素 ###

抽象策略角色(Strategy):定义所有支持的算法的公共接口。

具体策略角色(ConcreteStrategy)：以Strategy为接口实现某具体的算法。

环境类(Context)：维护一个队Strategy的引用，定义一个接口来让Strategy访问它的方法数据。


### 策略模式一般实现 ###

	{% highlight java %}
	//Stratege
	public interface Strategy
	{
		public void algorithmRealized();
	}
	//ConcreteStrategeA
	public class ConcreteStrategyA implements Strategy
	{
		public void algorithmRealized()
		{
			//采用A算法，此处省略
		}
	}
	//ConcreteStrategeB
	public class ConcreteStrategyB implements Strategy
	{
		public void algorithmRealized()
		{
			//采用B算法，此处省略
		}
	}
	//Context
	public class Context
	{
		private Strategy strategy;
		public Context(Strategy strategy)
		{
			this.strategy = strategy;
		}
		public void contextMethod()
		{
			strategy.algorithmRealized();
		}
	}
	//Client
	public class Client
	{
		public static void main(String[] args)
		{
			//采用A算法
			Strategy strategy = new ConcreteStrategyA();
			Context context = new Context(strategy);
			context.contextMethod(); 
		}
	}
	{% endhighlight %}


### 适用场景 ###

1. 需要使用一个算法的不同变体；

2. 一个类定义了多种行为，或相关的类只是行为有异。
