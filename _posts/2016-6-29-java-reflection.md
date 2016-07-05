---
date: 2016-6-29 18:36:30+00:00
layout: post
title: java反射和内省机制小结
thread: 148
categories: java
tags: java

---

Java的反射机制可以在运行期检测类、接口、变量和方法的信息，同时也可以在运行期实例化对象，调用方法、通过调用get/set方法获取变量的值。

Java的内省机制是java对Bean类属性、事件的一种缺省处理方法，可以在运行期检测类对象的属性和方法， Java中提供了一套API用来访问某个属性的getter/setter方法，这些API存放于包`java.beans`中。

java的内省和反射的区别类似JavaBeans和其他java类的区别，在这篇中小结下。

### java反射机制 ###

通过java反射机制，主要可以做到：

1. 在运行期检测一个类的信息(如类名、类修改、父类、实现接口、包信息、方法、域、注释等);

2. 在运行期获取构造函数和创建实例化对象；

3. 在运行期检测一个类的域和方法；

4. 在运行期调用一个类对象的方法；

5. 在运行期更改构造函数、方法、域等的访问权限。

6. 在运行期加载某个类。

反射操作的入口类是	[java.lang.class](https://docs.oracle.com/javase/8/docs/api/java/lang/Class.html)，基本使用例子：

	{% highlight java %}
	package myreflection;
	import java.lang.reflect.Method;
	class Foo
	{
	    String s;
	    public Foo()
	    {
	    }
	    public Foo(String s)
	    {
	        this.s=s;
	    }
	    public void print()
	    {
	        System.out.println("Hello World");
	    }
	}
	public class ReflectionExample
	{
	    public void main(String[] args)
	    {
	        Foo f=new Foo();
	        //Get Class name from object
			//myreflection.Foo
	        System.out.println(f.getClass().getName()); 
	        //Invoke method on unknown object
	        Method method;
	        try
	        {
	            method=f.getClass().getMethod("print",new Class<?>[0]);
	            method.invoke(f); //Hello World
	        }
	        catch(Exception e)
	        {
	            e.printStackTrace();
	        }
	        //Create Instance of "Class"
	        Class<?> c=null;
	        try
	        {
	            c=Class.forName("myreflection.Foo");
	        }
	        catch(Exception e)
	        {
	            e.printStackTrace();
	        }
	        //Create Instance of "Foo"
	        Foo f=null;
	        Foo f1=null;
	        Foo f2=null;
	        try
	        {
	            f=(Foo)c.newInstance();
	        }
	        catch(Exception e)
	        {
	            e.printStackTrace();
	        }
	        f.print(); //Hello World
	        //get all constructors
	        Constructor<?> cons[]=c.getConstructors();
	        try
	        {
	            f1=(Foo)cons[0].newInstance();
	            f2=(Foo)cons[1].newInstance("Hello reflect");
	        }
	        catch(Exception e)
	        {
	            e.printStackTrace();
	        }
	        f1.print(); //null
	        f2.print(); //Hello reflect
	        //Dynamic Class Loading
	        ClassLoader classLoader=ReflectionExample.getClassLoader();
	        try
	        {
	            Class cl=classLoader.loadClass("myreflection.Foo");
	            System.out.println(cl.getName()); //myreflection.Foo
	        }
	        catch(ClassNotFoundException e)
	        {
	            e.printStackTrace();
	        }
	    }
	}
	{% endhighlight %}


### java内省机制 ###

java内省一般是通过类[Introspector](https://docs.oracle.com/javase/7/docs/api/java/beans/Introspector.html)来获取某个对象的BeanInfo信息，然后通过BeanInfo来获取属性的描述器(PropertyDescriptor)，通过这个属性描述器可以获取某个属性的getter/setter方法，然后我们就可以通过java反射机制来调用这些方法。简单例子如下：

	{% highlight java %}
	package introspector;
	import java.beans.BeanInfo;
	import java.beans.Introspector;
	import java.beans.PropertyDescriptor;
	public class IntrospectorExample
	{
	    String name;
	    public String getName()
	    {
	        return name;
	    }
	    public void setName(String name)
	    {
	        this.name=name;
	    }
	    public static void main(String[] args)
	    {
	        IntrospectorExample introspector=new IntrospectorExample();
	        introspector.setName("Hello Introspector");
	        BeanInfo bi=Introspector.getBeanInfo(introspector.getClass(),Object.class);
	        PropertyDescriptor[] props=bi.getPropertyDescriptors();
	        for(int i=0;i<props.length;i++)
	        {
	            String strName=props[i].getName();
	            Method readMethod=props[i].getReadMethod();
	            System.out.println(strName+"="+readMethod.invoke(introspector,null));
	        }
	    }
	}
	{% endhighlight %}



参考：[Trail: The Reflection API: Table of Contents](https://docs.oracle.com/javase/tutorial/reflect/TOC.html)

[Java introspection and reflection](http://stackoverflow.com/questions/2044446/java-introspection-and-reflection)

[Java Reflection Tutorial](http://tutorials.jenkov.com/java-reflection/index.html)