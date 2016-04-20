---
date: 2016-4-12 18:18:30+00:00
layout: post
title: Leetcode中链表类题目小结(Hard部分)
thread: 125
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中Linked List的Hard部分的题型，目前已有的题目有：

1. Reverse Nodes in k-Group

2. Merge k Sorted Lists

3. Copy List with Random Pointer

### [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) ###

Given a linked list, reverse the nodes of a linked list k at a time and return its modified list.

If the number of nodes is not a multiple of k then left-out nodes in the end should remain as it is.

You may not alter the values in the nodes, only nodes itself may be changed.

Only constant memory is allowed.

For example,
Given this linked list: 1->2->3->4->5

For k = 2, you should return: 2->1->4->3->5

For k = 3, you should return: 3->2->1->4->5

	{% highlight java %}
	//Solution 1 recursive
	public ListNode reverseKGroup(ListNode head, int k)
	{
		ListNode curr=head;
		int count=0;
		while(curr!=null&&count!=k)
		{
			curr=curr.next;
			count++;
		}
		if(count==k)
		{
			curr=reverseKGroup(curr,k);
			while(count-->0)
			{
				ListNode tmp = head.next;
				head.next=curr;
				curr=head;
				head=tmp;
			}
			head=curr;
		}
		return head;
	}
	{% endhighlight %}

### [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) ###

Merge k sorted linked lists and return it as one sorted list. Analyze and describe its complexity.

	{% highlight java %}
	//Solution 1 recursive
	public ListNode mergeKLists(ListNode[] lists)
	{
		return partion(lists,0,lists.length-1);
	}
	public ListNode partion(ListNode[] lists,int start,int end)
	{
		if(start==end)
		{
			return lists[start];
		}
		if(start<end)
		{
			int q=(start+end)/2;
			ListNode l1=partion(lists,start,q);
			ListNode l2=partion(lists,q+1,end);
			return merge(l1,l2);
		}
		else
		{
			return null;
		}
	}
	public ListNode merge(ListNode l1,ListNode l2)
	{
		if(l1==null)
		{
			return l2;
		}
		if(l2==null)
		{
			return l1;
		}
		if(l1.val<l2.val)
		{
			l1.next=merge(l1.next,l2);
			return l1;
		}
		else
		{
			l2.next=merge(l1,l2.next);
			return l2;
		}
	}
	{% endhighlight %}


### [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) ###

A linked list is given such that each node contains an additional random pointer which could point to any node in the list or null.

Return a deep copy of the list.













