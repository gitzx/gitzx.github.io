---
date: 2016-3-13 11:23:30+00:00
layout: post
title: 建造者模式
thread: 105
categories: design_pattern
tags: design_pattern
---

建造者模式是将一个复杂对象的构造和它的表示分离，使得同样的构建过程可以创建不同的表示。

###建造者四要素###

建造者设计模式有四个角色：

1. builder：为创建一个产品对象的各个部件指定抽象接口；

2. ConcreteBuilder：实现builder接口以构造和装配该产品的各个部件，定义并明确它所创建的表示，并提供一个检索产品的接口；

3. Director：构造一个使用builder接口的对象；

4. Product：表示被构造的复杂对象。


		{% highlight java %}
		public class Product
		{
			private String part1;
			private String part2;
			public String getPart1()
			{
				return part1;
			}
			public String getPart2()
			{
				return part2;
			}
			public void setPart1(String part1)
			{
				this.part1 = part1;
			}
			public void setPart2(String part2)
			{
				this.part2 = part2;
			}
		}
		
		public interface Builder
		{
			public void buildPart1();
			public void buildPart2();
			public Product retrieveResult();
		}
		
		public class ConcreteBulder implements Builder
		{
			private Product product = new Product():
			public void buildPart1()
			{
				product.setPart1("part1");
			}
			public void buildPart2()
			{
				product.setPart2("part2");
			}
			public Product retrieveResult()
			{
				return product;
			}
		}
		
		public class Director
		{
			private Builder builder;
			public Director(Builder builder)
			{
				this.builder = builder;
			}
			public void construct()
			{
				builder.buildPart1();
				builder.buildPart2();
			}
		}
		
		public class Client
		{
			public static void main(String[] args)
			{
				Builder builder = new ConcreteBulder();
				Director director = new Director(builder);
				director.construct();
				Product product = builder.retrieveResult();
				System.out.println(product.getPart1());
				System.out.println(product.getPart2());
			}
		}
		{% endhighlight %}


###使用场景###

1. 需要生成的产品对象有复杂的内部结构，每一个内部成分本身可以是对象，也可以仅仅是一个对象（即产品对象）的一个组成部分。

2. 需要生成的产品对象的属性相互依赖。建造模式可以实行一种分步骤进行的建造过程。
