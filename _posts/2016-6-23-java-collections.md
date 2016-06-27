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

1. 集合(collection)(接口为[java.util.Collection](https://docs.oracle.com/javase/7/docs/api/java/util/Collection.html))：存储一个元素集合。有三种主要类型的集合：规则集(Set)、线性表(List)和队列(Queue,包括Deque)；主要子接口有：

		java.util.Set
		java.util.SortedSet
		java.util.NavigableSet
		java.util.Queue
		java.util.concurrent.BlockingQueue
		java.util.concurrent.TransferQueue
		java.util.Deque
		java.util.concurrent.BlockingDeque
		java.util.List

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


### [java.util.Collections](https://docs.oracle.com/javase/7/docs/api/java/util/Collections.html) ###

类似java.util.Arrays来处理数组，Java中对集合也有java.util.Collections来处理。

1. 第一组方法主要返回集合的各种数据：

	Collections.checkedCollection / checkedList / checkedMap / checkedSet / checkedSortedMap / checkedSortedSet：检查要添加的元素的类型并返回结果。任何尝试添加非法类型的变量都会抛出一个ClassCastException异常。这个功能可以防止在运行的时候出错。//fixme
	Collections.emptyList / emptyMap / emptySet ：返回一个固定的空集合，不能添加任何元素。
	
	Collections.singleton / singletonList / singletonMap：返回一个只有一个入口的 set/list/map 集合。
	
	Collections.synchronizedCollection / synchronizedList / synchronizedMap / synchronizedSet / synchronizedSortedMap / synchronizedSortedSet：获得集合的线程安全版本（多线程操作时开销低但不高效，而且不支持类似put或update这样的复合操作）
	
	Collections.unmodifiableCollection / unmodifiableList / unmodifiableMap / unmodifiableSet / unmodifiableSortedMap / unmodifiableSortedSet：返回一个不可变的集合。当一个不可变对象中包含集合的时候，可以使用此方法。

2. 第二组方法

	Collections.addAll：添加一些元素或者一个数组的内容到集合中。
	
	Collections.binarySearch：和数组的Arrays.binarySearch功能相同。
	
	Collections.disjoint：检查两个集合是不是没有相同的元素。
	
	Collections.fill：用一个指定的值代替集合中的所有元素。
	
	Collections.frequency：集合中有多少元素是和给定元素相同的。
	
	Collections.indexOfSubList / lastIndexOfSubList：和String.indexOf(String) / lastIndexOf(String)方法类似——找出给定的List中第一个出现或者最后一个出现的子表。
	
	Collections.max / min：找出基于自然顺序或者比较器排序的集合中，最大的或者最小的元素。
	
	Collections.replaceAll：将集合中的某一元素替换成另一个元素。
	
	Collections.reverse：颠倒排列元素在集合中的顺序。如果你要在排序之后使用这个方法的话，在列表排序时，最好使用Collections.reverseOrder比较器。
	
	Collections.rotate：根据给定的距离旋转元素。
	
	Collections.shuffle：随机排放List集合中的节点，可以给定你自己的生成器——例如 
	java.util.Random / java.util.ThreadLocalRandom or java.security.SecureRandom。
	Collections.sort：将集合按照自然顺序或者给定的顺序排序。
	
	Collections.swap：交换集合中两个元素的位置（多数开发者都是自己实现这个操作的）。

常用算法实现有：

	{% highlight java %}
	import java.util.*;
	public class Collections {
	    public static void main(String[] args) {
	        List<String> list = Arrays.asList(args);
	        Collections.sort(list);  //sorting
	        Collections.shuffle(list); //shuffle
	        int pos=Collections.binarySearch(list,2); //binarySearch
	        int freq=Collections.frequency(list,"Hello"); //frequency
	        boolean isDisjoint=Collections.disjoint(list1,list2); //disjoint
	    }
	}
	{% endhighlight %}

### 单线程集合 ###

[List](http://docs.oracle.com/javase/tutorial/collections/interfaces/list.html)中常用的不支持多线程有：[ArrayList](https://docs.oracle.com/javase/7/docs/api/java/util/ArrayList.html)和[LinkedList](https://docs.oracle.com/javase/7/docs/api/java/util/LinkedList.html)

1. ArrayList的实现原理是所有元素从角标0开始一个接一个排列。访问元素开销固定，尾部添加元素开销地，在头部添加元素成本高。

2. LinkedList是Deque实现，每个节点都保存着上一个节点和下一个节点的指针。数据的存取开销低，

3. Vector：一个带有线程同步方法的ArrayList版本，现在直接用ArrayList代替了。


[Queue](http://docs.oracle.com/javase/tutorial/collections/interfaces/queue.html)中常用的不支持多线程的有：[ArrayDeque](https://docs.oracle.com/javase/7/docs/api/java/util/ArrayDeque.html)和[PriorityQueue](https://docs.oracle.com/javase/7/docs/api/java/util/PriorityQueue.html)

1. ArrayDeque是基于有首尾指针的数组(环形缓冲区)实现的，与LinkedList不同，这个类没有实现List接口。

2. PriorityQueue是一个基于优先级的队列，使用自然顺序或者制定的比较强来排序，主要属性有poll/peek/remove/element返回一个队列的最小值。另外，PriorityQueue实现了Iterable接口，队列迭代是不需要排序。

3. Stack是一种后进先出的队列，不要在生产代码中使用，使用Deque来代替。

Queue的实现接口如下：

<table border=”1″>
<tr>
<td> Type of Operation </td>
<td> Insert </td>
<td> Remove </td>
<td> Examine </td>
</tr>
<tr>
<td>Throws exception</td>
<td>add(e)</td>
<td>remove() </td>
<td>element()</td>
</tr>
<tr>
<td>Returns special value</td>
<td>offer(e)</td>
<td>poll()</td>
<td>peek()</td>
</tr>
</table>

[Maps](http://docs.oracle.com/javase/tutorial/collections/interfaces/map.html)常用的不支持多线程的有[HashMap](https://docs.oracle.com/javase/7/docs/api/java/util/HashMap.html)、[EnumMap](https://docs.oracle.com/javase/7/docs/api/java/util/EnumMap.html)、[LinkedHashMap](https://docs.oracle.com/javase/7/docs/api/java/util/LinkedHashMap.html)、[TreeMap](https://docs.oracle.com/javase/7/docs/api/java/util/TreeMap.html)、[WeakHashMap](https://docs.oracle.com/javase/7/docs/api/java/util/WeakHashMap.html)和[IdentityHashMap](https://docs.oracle.com/javase/7/docs/api/java/util/IdentityHashMap.html)

1. HashMap是最常用的Map实现，只是将一个键和值相对应，并没有其他功能，对于hashCode、method和get/put方法有固定的复杂度；

2. EnumMap是枚举类型最为键值的Map。因为键的数量相对固定，在内部使用一个数组存储对应的值。效率通常高于HashMap。

3. LinkedHashMap是HashMap和LinkedList的结合。所有的元素的插入顺序存储在LinkedList中。这个是每个元素消耗内存最大的集合；

4. TreeMap是一种基于已排序且带导向信息Map的红黑树。每次插入都会按照自然顺序或者给定的比较强排序。这个Map需要实现equals方法和Comparable/Comparator。这个类实现了一个NavigableMap接口:可以带有与键数量不同的入口，可以得到键的上一个或者下一个入口，可以得到另一Map某一范围的键.

5. WeakHashMap通常用在数据缓存中，将键存储在WeakReference中。即没有强引用指向键对象的话，这些键就可以被垃圾回收线程回送，值被保存在强引用中。

6. IdentityHashMap是一个特殊的Map版本，违背一般Map的规则，使用“==”来比较引用而不是equals来判断相等。这个特性使得此集合在遍历图表的算法中非常实用——可以方便地在IdentityHashMap中存储处理过的节点以及相关的数据。

7. HashTable是线程同步的HashMap版本，新代码中使用HashMap。

[Sets](http://docs.oracle.com/javase/tutorial/collections/interfaces/set.html)中常用不支持多线程的有[HashSet](https://docs.oracle.com/javase/7/docs/api/java/util/HashSet.html)、[EnumSet](https://docs.oracle.com/javase/7/docs/api/java/util/EnumSet.html)、BitSet、[LinkedHashSet](https://docs.oracle.com/javase/7/docs/api/java/util/LinkedHashSet.html)和[TreeSet](https://docs.oracle.com/javase/7/docs/api/java/util/TreeSet.html)

1. HashSet是一个基于HashMap的Set实现。其中，所用的值为“假值”。同一个Object对象具备和HashMap同样的性能。消耗内存较多。

2. EnumSet是值为枚举类型的Set；

3. BitSet是一个比特Set；

4. LinkedHashSet和HashSet类似，基于LinkedHashMap实现，也是唯一一个保存了插入顺序的Set；

5. TreeSet和HashSet类似，基于一个TreeMap实现，也是单线程部分唯一一个排序的Set。


### 并发集合 ###

这一部分小结[java.util.concurrent](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/package-summary.html)包中线程安全的集合，这些集合的主要熟悉是一个不可分割的必须执行的方法。

Lists中主要有[CopyOnWriteArrayList](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/CopyOnWriteArrayList.html):List的实现每一次更新都会产生一个新的隐含数组副本，这个操作成本很高。通常用在遍历操作比更新操作多的集合。如Listeners/Observers集合。

Queues/deques

1. [ArrayBlockingQueue](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/ArrayBlockingQueue.html)是基于数组实现的一个有界阻塞队列，大小不能重新定义。当你试图向一个满的队列中添加元素时，会受到阻塞，直到另一个方法从队列中取出元素。

2. [ConcurrentLinkedDeque](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/ConcurrentLinkedDeque.html)/[ConcurrentLinkedQueue](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/ConcurrentLinkedQueue.html):基于链表实现的无界队列，添加元素不会阻塞，但是这就要求这个集合的消费者工作速度至少要和生产这一样快，不然内存就会耗尽。严重依赖于CAS(compare-and-set)操作。

3. [DelayQueue](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/DelayQueue.html)是无界的报错Delayed元素的集合。

4. [LinkedBlockingDeque](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/LinkedBlockingDeque.html)/[LinkedBlockingQueue](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/LinkedBlockingQueue.html):可选择有界或者无界基于链表的实现。在队列为空或者满的情况下使用ReentrantLock-s。

5. [LinkedTransferQueue](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/LinkedTransferQueue.html):基于链表的无界队列。除了通常的队列操作，它还有一系列的transfer方法，可以让生产者直接给等待的消费者传递信息，这样就不用将元素存储到队列中了。这是一个基于CAS操作的无锁集合。

6. [PriorityBlockingQueue](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/PriorityBlockingQueue.html):PriorityQueue的无界的版本。

7. [SynchronousQueue](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/SynchronousQueue.html):一个有界队列，其中没有任何内存容量。这就意味着任何插入操作必须等到响应的取出操作才能执行，反之亦反。如果不需要Queue接口的话，通过Exchanger类也能完成响应的功能。

Sets

1. [ConcurrentSkipListSet](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/ConcurrentSkipListSet.html):使用 ConcurrentSkipListMap来存储的线程安全的Set。

2. [CopyOnWriteArraySet](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/CopyOnWriteArraySet.html)：使用CopyOnWriteArrayList来存储的线程安全的Set。

Maps

1. [ConcurrentHashMap](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/ConcurrentHashMap.html)：get操作全并发访问，put操作可配置并发操作的哈希表。并发的级别可以通过构造函数中concurrencyLevel参数设置（默认级别16）。该参数会在Map内部划分一些分区。在put操作的时候只有只有更新的分区是锁住的。这种Map不是代替HashMap的线程安全版本——任何 get-then-put的操作都需要在外部进行同步。

2. [ConcurrentSkipListMap](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/ConcurrentSkipListMap.html)：基于跳跃列表（Skip List）的ConcurrentNavigableMap实现。本质上这种集合可以当做一种TreeMap的线程安全版本来使用。


参考原文：[Java collections overview](http://java-performance.info/java-collections-overview/)
