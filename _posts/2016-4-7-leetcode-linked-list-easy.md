---
date: 2016-4-7 18:15:30+00:00
layout: post
title: Leetcode中链表类题目小结(Easy部分)
thread: 123
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中Linked List的Easy部分的题型，目前已有的题目有：

1. Swap Nodes in Pairs

2. Reverse Linked List

3. Intersection of Two Linked Lists

4. Remove Nth Node From End of List

5. Delete Node in a Linked List

6. Merge Two Sorted Lists

7. Remove Duplicates from Sorted List

8. Remove Linked List Elements

9. Palindrome Linked List


### [swap Nodes in Pairs](https://leetcode.com/problems/swap-nodes-in-pairs/) ###

Given a linked list, swap every two adjacent nodes and return its head.

For example,
Given 1->2->3->4, you should return the list as 2->1->4->3.

Your algorithm should use only constant space. You may not modify the values in the list, only nodes itself can be changed.

	{% highlight java %}
	//Solution 1
	public ListNode swapNodesInPairs(ListNode head)
	{
		if(head==null||head.next==null)
		{
			return head;
		}
		ListNode n=head.next;
		head.next=swapNodesInPairs(head.next.next);
		n.next=head;
		return n;
	}
	//Solution 2
	public ListNode swapNodesInPairs(ListNode head)
	{
		ListNode dummy=new ListNode(0);
		dummy.next=head;
		ListNode current=dummy;
		while(current.next!=null&&current.next.next!=null)
		{
			ListNode first=current.next;
			ListNode second=current.next.next;
			first.next=second.next;
			current.next=second;
			current.next.next=first;
			current=current.next.next;
		}
		return dummy.next;
	}
	{% endhighlight %}

### [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) ###

Reverse a singly linked list.

	{% highlight java %}
	//Solution 1  Iterative
	public ListNode reverseLinkedList(ListNode head)
	{
		ListNode newHead = null;
		while(head!=null)
		{
			ListNode next = head.next;
			head.next = newHead;
			newHead = head;
			head = next;
		}
		return newHead;
	}
	//Solution 2  Recursive
	public ListNode reverseLinkedList(ListNode head)
	{
		return reverseListRecursive(head,null);
	}
	public ListNode reverseListRecursive(ListNode head, ListNode newHead)
	{
		if(head==null)
		{
			return newHead;
		}
		ListNode next = head.next;
		head.next = newHead;
		return reverseListRecursive(next,head);
	}
	{% endhighlight %}

### [Intersection of Two Linked Lists](https://leetcode.com/problems/intersection-of-two-linked-lists/) ###

Write a program to find the node at which the intersection of two singly linked lists begins.

For example, the following two linked lists:

A:          a1 → a2
                   ↘
                     c1 → c2 → c3
                   ↗            
B:     b1 → b2 → b3
begin to intersect at node c1.

Notes:

If the two linked lists have no intersection at all, return null.
The linked lists must retain their original structure after the function returns.
You may assume there are no cycles anywhere in the entire linked structure.
Your code should preferably run in O(n) time and use only O(1) memory.

	{% highlight java %}
	//Solution 1
	public ListNode getIntersectionNode(ListNode headA, ListNode headB)
	{
		int lenA=length(headA);
		int lenB=length(headB);
		while(lenA>lenB)
		{
			headA=headA.next;
			lenA--;
		}
		while(lenA<lenB)
		{
			headB=headB.next;
			lenB--;
		}
		while(headA!=headB)
		{
			headA=headA.next;
			headB=headB.next;
		}
		return headA;
	}
	public int length(ListNode head)
	{
		int length=0;
		while(head!=null)
		{
			head=head.next;
			length++;
		}
		return length;
	}
	//Solution 2
	public ListNode getIntersectionNode(ListNode headA, ListNode headB)
	{
	    if(headA==null || headB==null)
	    {
	        return null;
	    }
	    while(headA!=headB)
	    {
	        headA=(headA==null)?headB:headA.next;
	        headB=(headB==null)?headA:headB.next;
	    }
	    return headA;
	}
	{% endhighlight %}

### [Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) ###

Given a linked list, remove the nth node from the end of list and return its head.

For example,

   Given linked list: 1->2->3->4->5, and n = 2.

   After removing the second node from the end, the linked list becomes 1->2->3->5.
Note:
Given n will always be valid.
Try to do this in one pass.

	{% highlight java %}
	public ListNode removeNthNodeFromEndOfList(ListNode head, int n)
	{
		ListNode start= new ListNode(0);
		ListNode slow=start, fast=start;
		slow.next=head;
		fast.next=head;
		for(int i=0;i<n;i++)
		{
			fast=fast.next;
		}
		while(fast!=null)
		{
			slow=slow.next;
			fast=fast.next;
		}
		slow.next=slow.next.next;
		return start.next;
	}
	{% endhighlight %}

### [Delete Node in a Linked List](https://leetcode.com/problems/delete-node-in-a-linked-list/) ###

Write a function to delete a node (except the tail) in a singly linked list, given only access to that node.

Supposed the linked list is 1 -> 2 -> 3 -> 4 and you are given the third node with value 3, the linked list should become 1 -> 2 -> 4 after calling your function.

	{% highlight java %}
	public void deleteNode(ListNode node)
	{
		if(node==null)
		{
			return;
		}
		node.val=node.next.val;
		node.next=node.next.next;
	}
	{% endhighlight %}

### [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) ###

Merge two sorted linked lists and return it as a new list. The new list should be made by splicing together the nodes of the first two lists.
	
	//solution1   recursive
	public ListNode MergeTwoLists(ListNode l1,ListNode l2)
	{
		if(l1==null)
		{
			return l2;
		}
		if(l2==null)
		{
			return l1;
		}
		ListNode mergeHead;
		if(l1.val<l2.val)
		{
			mergeHead=l1;
			mergeHead.next=MergeTwoLists(l1.next,l2);
		}
		else
		{
			mergeHead=l2;
			mergeHead.next=MergeTwoLists(l1,l2.next);
		}
		return mergeHead;
	}
	//solution 2
	public ListNode MergeTwoLists(ListNode l1,ListNode l2)
	{
		ListNode mergeHead = new ListNode(0);
		while(l1!=null&&l2!=null)
		{
			if(l1.val<l2.val)
			{
				mergeHead.next=l1;
				l1=l1.next;
			}
			else 
			{
				mergeHead.next=l2;
				l2=l2.next;
			}
			mergeHead=mergeHead.next;
		}
		mergeHead.next=l1?l1:l2;
		return mergeHead;
	}
	{% endhighlight %}

### [Remove Duplicates from Sorted List](https://leetcode.com/problems/remove-duplicates-from-sorted-list/) ###

Given a sorted linked list, delete all duplicates such that each element appear only once.

For example,
Given 1->1->2, return 1->2.
Given 1->1->2->3->3, return 1->2->3.

	{% highlight java %}
	//solution 1 recursive
	public ListNode deleteDuplicates(ListNode head)
	{
		if(head==null||head.next==null)
		{
			head.next=deleteDuplicates(head.next);
		}
		return head.val==head.next.val?head.next:head;
	}
	//solution 2
	public ListNode deleteDuplicates(ListNode head)
	{
		ListNode tempHead = head;
		while(tempHead!=null)
		{
			if(tempHead.next==null)
			{
				break;
			}
			if(tempHead.val==tempHead.next.val)
			{
				tempHead.next=tempHead.next.next;
			}
			else
			{
				tempHead=tempHead.next;
			}
		}
		return head;
	}
	{% endhighlight %}

### [Remove Linked List Elements](https://leetcode.com/problems/remove-linked-list-elements/) ###

Remove all elements from a linked list of integers that have value val.

Example
Given: 1 --> 2 --> 6 --> 3 --> 4 --> 5 --> 6, val = 6
Return: 1 --> 2 --> 3 --> 4 --> 5

	{% highlight java %}
	//solution 1 recursive
	public ListNode removeElements(ListNode head, int val)
	{
		if(head==null)
		{
			return null;
		}
		head.next=removeElements(head.next,val);
		return head.val==val?head.next:head;
	}
	//solution 2
	public ListNode removeElements(ListNode head,int val)
	{
		ListNode tempHead=head;
		while(tempHead!=null&&tempHead.next!=null)
		{
			if(tempHead.val==tempHead.val)
			{
				tempHead.next=tempHead.next.next;
			}
			else
			{
				tempHead=tempHead.next;
			}
		}
		return head;
	}
	{% endhighlight %}

### [Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) ###

Given a singly linked list, determine if it is a palindrome.

Follow up:
Could you do it in O(n) time and O(1) space?

	{% highlight java %}
	public bool isPalindromLinkedList(ListNode head)
	{
		if(head==null||head.next=null)
		{
			return true;
		}
		ListNode slow = head;
		ListNode fast = head;
		while(fast.next!=null&&fast.next.next!=null)
		{
			slow=slow.next;
			fast=fast.next.next;
		}
		slow.next=reverseList(slow.next);
		slow=slow.next;
		while(slow!=null)
		{
			if(head.val!=slow.val)
			{
				return false;
			}
			head=head.next;
			slow=slow.next;
		}
		return true;
	}
	public listNode reverseList(ListNode head)
	{
		ListNode pre;
		ListNode next;
		while(head!=null)
		{
			next=head.next;
			head.next=pre;
			pre=head;
			head=next;
		}
		return pre;
	}
	{% endhighlight %}
