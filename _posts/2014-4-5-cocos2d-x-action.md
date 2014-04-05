---
date: 2014-4-4 19:13:30+00:00
layout: post
title: cocos2d-x的入门学习－－动作
thread: 43
categories: cocos2d-x
tags: cocos2d-x
---

动作（action）作用于游戏元素。cocos2d－x的动作由CCCAction类实现。CCAction类的派生类包括：

（1）`CCFiniteTimeAction`：绝大数我们使用的动作类都派生自CCFiniteTimeAction，如最常用的`CCActionInterval`(持续性动作)、`CCActionInstant`(瞬时动作)，这两个类又分别派生出许多我们实际用到的动作类。

（2）`CCRepeatForever` : 无限重复动作；

（3）`CCRepeatForever` : 变速动作；

（4）`CCFollow` : 跟随动作；

动作的执行：

	{% highlight java %}
	public class HelloWorld {
    	public static void main(String args[]) {
      System.out.println("Hello World!");
    	}
	}
	{% endhighlight %}

###CCFiniteTimeAction###

