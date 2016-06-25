---
date: 2016-6-23 19:06:30+00:00
layout: post
title: java集合小结
thread: 144
categories: java
tags: java

---

java中常用数组和java集合框架来存储数据，这篇小结下。

[java集合框架](https://docs.oracle.com/javase/7/docs/technotes/guides/collections/index.html)分为两种：

1. 集合(collection)(接口为[java.util.Collection](https://docs.oracle.com/javase/7/docs/api/java/util/Collection.html))：存储一个元素集合。有三种主要类型的集合：规则集(Set)、线性表(List)和队列(Queue)；主要子接口有：

		java.util.Set
		java.util.SortedSet
		java.util.NavigableSet
		java.util.Queue
		java.util.concurrent.BlockingQueue
		java.util.concurrent.TransferQueue
		java.util.Deque
		java.util.concurrent.BlockingDeque

2. 图(map)(接口为[java.util.Map](https://docs.oracle.com/javase/7/docs/api/java/util/Map.html))：存储键/值对。 主要子接口有：

		java.util.SortedMap
		java.util.NavigableMap
		java.util.concurrent.ConcurrentMap
		java.util.concurrent.ConcurrentNavigableMap

### Collection Implementations ###

集合实现总结如下：

<table border=”1″>
<tr>
<td> Interface </td>
<td> Hash Table </td>
<td> Resizable Array </td>
<td> Balanced Tree </td>
<td> Linked List </td>
<td> Hash Table + Linked List </td>
</tr>
<tr>
<td>Set</td>
<td>HashSet</td>
<td> </td>
<td>TreeSet</td>
<td> </td>
<td>LinkedHashSet</td>
</tr>
<tr>
<td>List</td>
<td></td>
<td>ArrayList</td>
<td></td>
<td>LinkedList</td>
<td></td>
</tr>
<tr>
<td>Deque</td>
<td></td>
<td>ArrayDeque</td>
<td></td>
<td>LinkedList</td>
<td></td>
</tr>
<tr>
<td>Map</td>
<td>HashMap</td>
<td></td>
<td>TreeMap</td>
<td></td>
<td>LinkedHashMap</td>
</tr>
</table>

### [Arrays](https://docs.oracle.com/javase/7/docs/api/java/util/Arrays.html) ###

java.util.Arrays包括了一系列处理数组的方法，该类也是java集合框架的一员，常用的方法如下：
	
	Arrays.asList：可以从 Array 转换成 List。可以作为其他集合类型构造器的参数。
	Arrays.binarySearch：在一个已排序的或者其中一段中快速查找。
	Arrays.copyOf：如果你想扩大数组容量又不想改变它的内容的时候可以使用这个方法。
	Arrays.copyOfRange：可以复制整个数组或其中的一部分。
	Arrays.deepEquals、Arrays.deepHashCode：Arrays.equals/hashCode的高级版本，支持子数组的操作。
	Arrays.equals：如果你想要比较两个数组是否相等，应该调用这个方法而不是数组对象中的 equals方法
	（数组对象中没有重写equals()方法，所以这个方法之比较引用而不比较内容）。
	这个方法集合了Java 5的自动装箱和无参变量的特性，来实现将一个变量
	快速地传给 equals() 方法——所以这个方法在比较了对象的类型之后是直接传值进去比较的。
	Arrays.fill：用一个给定的值填充整个数组或其中的一部分。
	Arrays.hashCode：用来根据数组的内容计算其哈希值（数组对象的hashCode()不可用）。
	这个方法集合了Java 5的自动装箱和无参变量的特性，来实现将一个变量快速地传给 Arrays.hashcode方法——只是传值进去，不是对象。
	Arrays.sort：对整个数组或者数组的一部分进行排序。也可以使用此方法用给定的比较器对对象数组进行排序。
	Arrays.toString：打印数组的内容。


所有的集合都可以用T[] Collection.toArray( T[] a ) 这个方法复制到数组中。通常会用这样的方式调用：`return coll.toArray( new T[ coll.size() ] );`这个方法会分配足够大的数组来储存所有的集合，这样 toArray 在返回值时就不必再分配空间了。

