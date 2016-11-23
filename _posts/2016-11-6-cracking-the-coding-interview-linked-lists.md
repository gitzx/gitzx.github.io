---
date: 2016-11-6 18:01:30+00:00
layout: post
title: 《Cracking the coding interview》中链表小结
thread: 160
categories: algorithm 
tags: algorithm 

---

这篇小结下《Cracking the coding interview》中的链表题目。

1. Write code to remove duplicates from an unsorted linked list. FOLLOW UP How would you solve this problem if a temporary buffer is not allowed?

2. Implement an algorithm to find the nth to last element of a singly linked list.

3. Implement an algorithm to delete a node in the middle of a single linked list, given only access to that node. EXAMPLE Input: the node ‘c’ from the linked list a->b->c->d->e Result: nothing is returned, but the new linked list looks like a->b->d->e

4. You have two numbers represented by a linked list, where each node contains a single digit. The digits are stored in reverse order, such that the 1’s digit is at the head of the list. Write a function that adds the two numbers and returns the sum as a linked list. EXAMPLE Input: (3 -> 1 -> 5) + (5 -> 9 -> 2) Output: 8 -> 0 -> 8

5. Given a circular linked list, implement an algorithm which returns node at the beginning of the loop. DEFINITION Circular linked list: A (corrupt) linked list in which a node’s next pointer points to an earlier node, so as to make a loop in the linked list. EXAMPLE input: A -> B -> C -> D -> E -> C (the same C as earlier) output: C


### 1. 从一个未排序的链表中移除重复的项  ###

Write code to remove duplicates from an unsorted linked list.


	{% highlight java %}
	public class DeleteDumplicates
	{
		//use a buffer
		public static void DeleteDups(LinkedListNode n)
		{
			HashMap map = new HashMap();
			LinkedListNode previous = null;
			while(n != null)
			{
				if(map.containsKey(n.data))
				{
					previous.next = n.next;
				}
				else
				{
					map.put(n.data, true);
					previous = n;
				}
			}
			n = n.next;
		}
		//without a buffer
		public static void DeleteDups2(LinkedListNode head)
		{
			if(head == null)
			{
				return;
			}
			LinkedListNode previous = head;
			LinkedListNode current = previous.next;
			while(current != null)
			{
				LinkedListNode runner = head;
				while(runner != current)
				{
					if(runner.data == current.data)
					{
						LinkedListNode tmp = current.next;
						previous.next = tmp;
						current = tmp;
						break;
					}
					runner = runner.next;
				}
			}
			if(runner == current)
			{
				previous = current;
				current = current.next;
			}
		}
	}
	{% endhighlight %}


### 2. 从一个单链表中返回倒数第n个元素 ###

Implement an algorithm to find the nth to last element of a singly linked list.


	{% highlight java %}
	public class NthToLast
	{
		public static LinkedListNode nthToLast(LinkedListNode head, int n)
		{
			if(head == null || n < 1)
			{
				return null;
			}
			LinkedListNode p1 = head;
			LinkedListNode p2 = head;
			for(int j = 0; j < n-1; ++j)
			{
				if(p2 == null)
				{
					return null;
				}
				p2 = p2.next;
			}
			while(p2.next != null)
			{
				p1 = p1.next;
				p2 = p2.next;
			}
			return p1;
		}
	}
	{% endhighlight %}


### 3. 删除单链表中间的一个结点，只给出指向那个结点的指针 ###

Implement an algorithm to delete a node in the middle of a single linked list, given only access to that node.


	{% highlight java %}
	public class DeleteNode
	{
		public static boolean deleteNode(LinkedListNode n)
		{
			if(n == null || n.next == null)
			{
				return;
			}
			LinkedListNode next = n.next;
			n.data = next.data;
			n.next = next.next;
			return true;
		}
	}
	{% endhighlight %}


### 4. 两个链表每个结点代表其中的一位数字。数字的存储是逆序的，写一函数使这两个数相加并返回结果，结果也由链表表示  ###

You have two numbers represented by a linked list, where each node contains a single digit. The digits are stored in reverse order, such that the 1’s digit is at the head of the list. Write a function that adds the two numbers and returns the sum as a linked list.

EXAMPLE

Input: (3 -> 1 -> 5), (5 -> 9 -> 2)

Output: 8 -> 0 -> 8

	{% highlight java %}
	public class AddLists
	{
		public static LinkedListNode addLists(LinkedListNode l1, LinkedListNode l2, int carry)
		{
			if(l1 == null && l2 == null)
			{
				return null;
			}
			LinkedListNode result = new LinkedListNode(carry, null, null);
			int value = carry;
			if(l1 != null)
			{
				value += l1.data;
			}
			if(l2 != null)
			{
				value += l2.data;
			}
			result.data = value % 10 ;
			LinkedListNode more = addLists(l1 == null ? null:l1.next, 
				l2 == null ? null : l2.next, value >= 10? 1: 0);
			result.setNext(more);
			return result;
		}
	}
	{% endhighlight %}


### 5. 给定一个循环链表，实现一个算法返回这个环的开始结点。 ###

Given a circular linked list, implement an algorithm which returns node at the beginning of the loop.

DEFINITION

Circular linked list: A (corrupt) linked list in which a node’s next pointer points to an earlier node, so as to make a loop in the linked list.

EXAMPLE

Input: A -> B -> C -> D -> E -> C [the same C as earlier]

Output: C


	{% highlight java %}
	public class FindBeginningOfLoop
	{
		public static LinkedListNode findBeginning(LinkedListNode head)
		{
			LinkedListNode n1 = head;
			LinkedListNode n2 = head;
			while(n2.next != null)
			{
				n1 = n1.next;
				n2 = n2.next.next;
				if(n1 == n2)
				{
					break;
				}
			}
			if(n2.next == null)
			{
				return null;
			}
			n1 = head;
			while(n1 != n2)
			{
				n1 = n1.next;
				n2 = n2.next;
			}
			return n2;
		}
	}
	{% endhighlight %}


C++版实现可参考： [Cracking the coding interview--问题与解答](http://www.hawstein.com/posts/ctci-solutions-contents.html)

