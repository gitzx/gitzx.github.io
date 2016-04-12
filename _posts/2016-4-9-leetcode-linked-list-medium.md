---
date: 2016-4-9 19:58:30+00:00
layout: post
title: Leetcode中链表类题目小结(Medium部分)
thread: 124
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中Linked List的Medium部分的题型，目前已有的题目有：

1. Add Two Numbers

2. Linked List Cycle

3. Linked List Cycle II

4. Insertion Sort List

5. Reverse Linked List II 

6. Convert Sorted List to Binary Search Tree

7. Sort List

8. Reorder List

9. Remove Duplicates from Sorted List II

10. Partition List

11. Rotate List

12. Odd Even Linked List


### [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) ###

You are given two linked lists representing two non-negative numbers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.

Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8


### [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) ###

Given a linked list, determine if it has a cycle in it.

	{% highlight java %}
	public boolean hasCycle(ListNode head)
	{
		if(head==null || head.next==null)
		{
			return false;
		}
		ListNode slow = head;
		ListNode fast = head;
		while(fast.next!=null&&fast.next.next!=null)
		{
			slow=slow.next;
			fast=fast.next.next;
			if(slow==fast)
			{
				return true;
			}
		}
		return false;
	}
	{% endhighlight %}

### [Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) ###

Given a linked list, return the node where the cycle begins. If there is no cycle, return null.

Note: Do not modify the linked list.

	{% highlight java %}
	public ListNode detectCycle(ListNode head)
	{
		if(head==null||head.next==null)
		{
			return null;
		}
		ListNode slow=head;
		ListNode fast=head;
		ListNode entry=head;
		while(fast.next!=null&&fast.next.next!=null)
		{
			slow=slow.next;
			fast=fast.next.next;
			if(fast==slow)
			{
				while(slow!=entry)
				{
					slow=slow.next;
					entry=entry.next;
				}
				return entry;
			}
		}
		return null;
	}
	{% endhighlight %}


### [Insertion Sort List](https://leetcode.com/problems/insertion-sort-list/) ###

Sort a linked list using insertion sort

	{% highlight java %}
	public ListNode insertionSortList(ListNode head)
	{
		ListNode dummy = new ListNode(0);
		ListNode pre=dummy;
		ListNode current=head;
		while(current!=null)
		{
			pre=dummy;
			while(pre.next!=null&&pre.next.val<current.val)
			{
				pre=pre.next;
			}
			ListNode next=current.next;
			current.next=pre.next;
			pre.next=current;
			current=next;
		}
		return dummy.next;
	}
	{% endhighlight %}

### [Reverse Linked List II](https://leetcode.com/problems/reverse-linked-list-ii/) ###

Reverse a linked list from position m to n. Do it in-place and in one-pass.

For example:
Given 1->2->3->4->5->NULL, m = 2 and n = 4,

return 1->4->3->2->5->NULL.

Note:
Given m, n satisfy the following condition:
1 ≤ m ≤ n ≤ length of list.

	{% highlight java %}
	public ListNode reverseBetween(ListNode head,int m,int n)
	{
		if(m==n)
		{
			return head;
		}
		n-=m;
		ListNode prehead=new ListNode(0);
		prehead.next=head;
		ListNode pre=prehead;
		while(--m)
		{
			pre=pre.next;
		}
		ListNode pstart=pre.next;
		while(n--)
		{
			ListNode p=pstart.next;
			pstart.next=p.next;
			p.next=pre.next;
			pre.next=p;
		}
		return prehead.next;
	}
	{% endhighlight %}

### [Convert Sorted List to Binary Search Tree](https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/) ###

Given a singly linked list where elements are sorted in ascending order, convert it to a height balanced BST.

	{% highlight java %}
	public ListNode node;
	public TreeNode sortedListToBST(ListNode head)
	{
		if(head==null)
		{
			return null;
		}
		int size=0;
		ListNode runner=head;
		node=head;
		while(runner!=null)
		{
			runner=runner.next;
			size++;
		}
		return inorderHelper(0,size-1);
	}
	public TreeNode inorderHelper(int start, int end)
	{
		if(start>end)
		{
			return null;
		}
		int mid=start+(end-start)/2;
		TreeNode left=inorderHelper(start,mid-1);
		TreeNode treenode=new TreeNode(node.val);
		treenode.left=left;
		node=node.next;
		TreeNode right=inorderHelper(mid+1,end);
		treenode.right=right;
		return treenode;
	}
	{% endhighlight %}

### [Sort List](https://leetcode.com/problems/sort-list/) ###

Sort a linked list in O(n log n) time using constant space complexity.

	{% highlight java %}
	public ListNode sortList(ListNode head)
	{
		if(head==null ||head.next==null)
		{
			return head;
		}
		ListNode pre=null,slow=head,fast=head;
		while(fast!=null&&fast.next!=null)
		{
			pre=slow;
			slow=slow.next;
			fast=fast.next.next;
		}
		prev.next=null;
		ListNode l1=sortList(head);
		ListNode l2=sortList(slow);
		return merge(l1,l2);
	}
	public ListNode merge(LisNode l1,ListNode l2)
	{
		ListNode l=new ListNode(0);
		ListNode p=l;
		while(l1!=null&&l2!=null)
		{
			if(l1.val<l2.val)
			{
				p.next=l1;
				l1=l1.next;
			}
			else
			{
				p.next=l2;
				l2=l2.next;
			}
			p=p.next;
		}
		if(l1!=null)
		{
			p.next=l1;
		}
		if(l2!=null)
		{
			p.next=l2;
		}
		return l.next;
	}
	{% endhighlight %}

### [Reorder List](https://leetcode.com/problems/reorder-list/) ###


Given a singly linked list L: L0→L1→…→Ln-1→Ln,
reorder it to: L0→Ln→L1→Ln-1→L2→Ln-2→…

You must do this in-place without altering the nodes' values.

For example,
Given {1,2,3,4}, reorder it to {1,4,2,3}.

	{% highlight java %}
	publicvoid reorderList(ListNode head)
	{
		if(head==null||head.next==null)
		{
			return;
		}
		ListNode slow=head;
		ListNode fast=head;
		while(fast.next!=null&&fast.next.next!=null)
		{
			slow=slow.next;
			fast=fast.next.next;
		}
		ListNode second = slow.next;
		slow.next=null;
		second = reverseOrder(second);
		ListNode p1 = head;
		ListNode p2 = second;
		while (p2 != null) 
		{
			ListNode next1 = p1.next;
			ListNode next2 = p2.next;
			p1.next = p2;
			p2.next = next1;		
			p1 = next1;
			p2 = next2;
		}
	}
	public ListNode reverseOrder(ListNode head)
	{
		if (head == null || head.next == null)
		{
			return head;
		}
		ListNode pre = head;
		ListNode curr = head.next;
		while (curr != null) 
		{
			ListNode next = curr.next;
			curr.next = pre;
			pre = curr;
			curr = next;
		}
		head.next = null;
		return pre;
	}
	{% endhighlight %}


### [Remove Duplicates from Sorted List II](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/) ###

Given a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list.

For example,
Given 1->2->3->3->4->4->5, return 1->2->5.
Given 1->1->1->2->3, return 2->3.

	{% highlight java %}
	//solution 1 recursive
	public ListNode deleteDuplicates(ListNode head)
	{
		if(head==null)
		{
			return null;
		}
		if(head.next!=null&&head.val==head.next.val)
		{
			while(head.next!=null&&head.val==head.next.val)
			{
				head=head.next;
			}
			return deleteDuplicates(head.next);
		}
		else
		{
			head.next=deleteDuplicates(head.next);
		}
	}
	//solution 2
	public LisNode deleteDuplicates(ListNode head)
	{
		if(head==null)
		{
			return null;
		}
		ListNode newHead=new ListNode(0);
		newHead.next=head;
		LisNode pre=newHead;
		ListNode cur=head;
		while(cur!=null)
		{
			while(cur.next!=null&&cur.val==cur.next.val)
			{
				cur=cur.next;
			}
			if(pre.next==cur)
			{
				pre=pre.next;
			}
			else
			{
				pre.next=cur.next;
			}
			cur=cur.next;
		}
		return newHead.next;
	}
	{% endhighlight %}

### [Partition List](https://leetcode.com/problems/partition-list/) ###

Given a linked list and a value x, partition it such that all nodes less than x come before nodes greater than or equal to x.

You should preserve the original relative order of the nodes in each of the two partitions.

For example,
Given 1->4->3->2->5->2 and x = 3,
return 1->2->2->4->3->5.

	{% highlight java %}
	public ListNode partitionList(ListNode head,int x)
	{
		ListNode newHead1=new ListNode(0);
		ListNode newHead2=new ListNode(0);
		ListNode p1=newHead1;
		ListNode p2=newHead2;
		while(head!=null)
		{
			if(head.val<x)
			{
				p1.next=head;
				p1=p1.next;
			}
			else
			{
				p2.next=head;
				p2=p2.next;
			}
			head=head.next;
		}
		p2.next=null;
		p1.next=newHead2.next;
		return newHead1.next;
	}
	{% endhighlight %}

### [Rotate List](https://leetcode.com/problems/rotate-list/) ###

Given a list, rotate the list to the right by k places, where k is non-negative.

For example:
Given 1->2->3->4->5->NULL and k = 2,
return 4->5->1->2->3->NULL.

	{% highlight java %}
	public ListNode rotateRight(ListNode head, int k)
	{
		if(k<1||head==null)
		{
			return head;
		}
		ListNode p=head;
		int len=1;
		while(p.next!=null)
		{
			p=p.next;
			len++;
		}
		p.next=head;
		k=len-k%len;
		while(k>0)
		{
			p=p.next;
			k--;
		}
		head=p.next;
		p.next=null;
		return head;
	}
	{% endhighlight %}

### [Odd Even Linked List](https://leetcode.com/problems/odd-even-linked-list/) ###

Given a singly linked list, group all odd nodes together followed by the even nodes. Please note here we are talking about the node number and not the value in the nodes.

You should try to do it in place. The program should run in O(1) space complexity and O(nodes) time complexity.

Example:
Given 1->2->3->4->5->NULL,
return 1->3->5->2->4->NULL.

Note:
The relative order inside both the even and odd groups should remain as it was in the input. 
The first node is considered odd, the second node even and so on ...

	{% highlight java %}
	public ListNode oddEventList(ListNode head)
	{
		if(head==null)
		{
			return null;
		}
		ListNode odd=head;
		ListNode even=head.next;
		ListNode evenHead=even;
		while(even!=null&&even.next!=null)
		{
			odd.next=odd.next.next;
			even.next=even.next.next;
			odd=odd.next;
			even=even.next;
		}
		odd.next=evenHead;
		return head;
	}
	{% endhighlight %}
















