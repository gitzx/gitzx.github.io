---
date: 2016-3-19 20:38:30+00:00
layout: post
title: 迭代器模式
thread: 115
categories: design_pattern
tags: design_pattern
---

迭代器模式提供一种方法访问一个容器对象中的各个对象，而不需要暴露该对象的内部细节。

### 迭代器模式四要素 ###

1. 迭代器角色(Iterator)：定义访问和遍历元素的接口；

2. 具体迭代器角色(ConcreteIterator)：实现迭代器接口；

3. 容器角色(Container)：提供创建具体迭代器角色的接口；

4. 具体容器角色(ConcreteContainer)：实现容器接口。

### 迭代器模式一般实现 ###

	{% highlight java %}
	//Iterator
	public interface Iterator<T>
	{
		public T next();
		public boolean hasNext();
	}
	//ConcreteIterator
	public class ConcreteIterator<T> implements Iterator<T>
	{
		private List<T> list = new ArrayList<T>();
		private int cursor = 0;
		public ConcreteIterator(List<T>  list)
		{
			this.list = list;
		}
		public boolean hasNext()
		{
			if(list.size() == cursor)
			{
				return false;
			}
			return true;
		}
		public T next()
		{
			T obj = null;
			if(this.hasNext())
			{
				obj = this.list.get(cursor++);
			}
			return obj;
		}
	}
	//Container
	public interface Container<T>
	{
		public void add(T obj);
		public void remove(T obj);
		pubic Iterator<T> iterator();
	}
	//ConcreteContainer
	public class ConcreteContainer<T> implements Container<T>
	{
		private List<T> list = new ArrayList<T>();
		public void add(T obj)
		{
			list.add(obj);
		}
		public void remove(T obj)
		{
			list.remove(obj);
		}
		public Iterator<T> iterator()
		{
			return new ConcreteContainer<T>(list);
		}
	}
	//client
	public class Client
	{
		public static void main(String[] args)
		{
			Container<String> ct = new ConcreteContainer<String>();
			ct.add("Hello");
			ct.add("Hi");
			Iterator<String> it = ct.iterator();
			while(it.hasNext())
			{
				String str = (String)it.next();
				System.out.println(str);
			}
		}
	}
	{% endhighlight %}

### 适用场景 ###

迭代器的作用就是把集合的管理和迭代相分离。java等语言已经完整实现了所有集合的迭代，使用语言自带的接口即可。