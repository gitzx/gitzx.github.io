---
date: 2016-11-9 19:10:30+00:00
layout: post
title: 《Cracking the coding interview》中树和图小结
thread: 161
categories: algorithm 
tags: algorithm 

---

这篇小结下《Cracking the coding interview》中的树和图题目。

1 Implement a function to check if a tree is balanced. For the purposes of this question, a balanced tree is defined to be a tree such that no two leaf nodes differ in distance from the root by more than one.

2. Given a directed graph, design an algorithm to find out whether there is a route between two nodes.

3. Given a sorted (increasing order) array, write an algorithm to create a binary tree with minimal height.

4. Given a binary search tree, design an algorithm which creates a linked list of all the nodes at each depth (i.e., if you have a tree with depth D, you’ll have D linked lists).

5. Write an algorithm to find the ‘next’ node (i.e., in-order successor) of a given node in a binary search tree where each node has a link to its parent.

6. Design an algorithm and write code to find the first common ancestor of two nodes in a binary tree. Avoid storing additional nodes in a data structure. NOTE: This is not necessarily a binary search tree.

7. You have two very large binary trees: T1, with millions of nodes, and T2, with hun- dreds of nodes. Create an algorithm to decide if T2 is a subtree of T1.

8. You are given a binary tree in which each node contains a value. Design an algorithm to print all paths which sum up to that value. Note that it can be any path in the tree - it does not have to start at the root.


### 1. 检查一棵树是否平衡  ###

Implement a function to check if a tree is balanced. For the purposes of this question, a balanced tree is defined to be a tree such that no two leaf nodes differ in distance from the root by more than one.


	{% highlight java %}
	public class TreeIsBalanced
	{
		public static int maxDepth(TreeNode root)
		{
			if(root == null)
			{
				return 0;
			}
			return 1 + Math.max(maxDepth(root.right), maxDepth(root.left));
		}
		public static int minDepth(TreeNode root)
		{
			if(root == null)
			{
				return 0;
			}
			return 1 + Math.min(minDepth(root.right), minDepth(root.left));
		}
		public static boolean isBalanced(TreeNode root)
		{
			return ((maxDepth(root) - maxDepth(root)) <= 1);
		}
	}
	{% endhighlight %}



### 2. 给定一个有向图，设计算法判断两结点间是否存在路径 ###

Given a directed graph, design an algorithm to find out whether there is a route between two nodes.


### 3. 给定一个有序数组(递增)，写程序构建一棵具有最小高度的二叉树 ###

Given a sorted (increasing order) array, write an algorithm to create a binary tree with minimal height.

	{% highlight java %}
	public class ArrayToTree
	{
		public static TreenNode ArrayToTree(int[] array, int start, int end)
		{
			if(start < end)
			{
				return null;
			}
			int mid = (start + end)/2;
			TreenNode node = new TreenNode(mid);
			node.left = ArrayToTree(array, start, mid-1);
			node.right = ArrayToTree(array, mid+1, end);
			return node;
		}
	}
	{% endhighlight %}


### 4. 给定一棵二叉查找树，设计算法，将每一层的所有结点构建为一个链表 ###

Given a binary search tree, design an algorithm which creates a linked list of all the nodes at each depth (i.e., if you have a tree with depth D, you’ll have D linked lists).

	{% highlight java %}
	public class FindLevelLinkedlist
	{
		int level = 0;
		ArrayList<LinkedList<TreeNode>> result = 
			new ArrayList<LinkedList<TreeNode>>();
		LinkedList<TreeNode> list = new LinkedList<TreeNode>();
		list.add(root);
		result.add(level, list);
		while(true)
		{
			list = new LinkedList<TreeNode>();
			for(int i = 0; i < result.get(level).size(); ++i)
			{
				TreeNode n = (TreeNode)result.get(level).get(i);
				if(n != null)
				{
					if(n.left != null)
					{
						list.add(n.left);
					}
					if(n.right != null)
					{
						list.add(n.right);
					}
				}
			}
			if(list.size() > 0)
			{
				result.add(level+1, list);
			}
			else
			{
				break;
			}
			level++;
		}
		return result;
	}
	{% endhighlight %}


### 5. 查找二叉树的一个节点的“下一个”结点(即中序遍历后它的后继结点)， 其中每个结点都有指向其父亲的链接 ###

Write an algorithm to find the ‘next’ node (i.e., in-order successor) of a given node in a binary search tree where each node has a link to its parent.

	{% highlight java %}
	public class InorderSuccessor
	{
		public static TreeNode inorderSucc(TreeNode e)
		{
			if(e == null)
			{
				return null;
			}
			TreeNode p;
			if(e.parent == null || e.right != null)
			{
				p = leftMostChild(e.right);
			}
			else
			{
				while((p = e.parent) != null)
				{
					if(e.left == e)
					{
						break;
					}
					e = e.parent;
				}
			}
			return p;
		}
		public static TreeNode leftMostChild(TreeNode e)
		{
			if(e == null)
			{
				return null;
			}
			while(e.left != null)
			{
				e = e.left;
			}
			return e;
		}
	}
	{% endhighlight %}


### 6. 在一棵二叉树中找到两个结点的第一个共同祖先。不允许存储额外的结点 ###

Design an algorithm and write code to find the first common ancestor of two nodes in a binary tree. Avoid storing additional nodes in a data structure. NOTE: This is not necessarily a binary search tree.


	{% highlight java %}
	public class CommonAncestor
	{
		public static TreeNode commonAncestor(TreeNode root, TreeNode p, TreeNode q)
		{
			if(covers(root.left, p) && covers(root.left, q))
			{
				return commonAncestor(root.left, p, q);
			}
			if(covers(root.right, p) && covers(root.right, q))
			{
				return commonAncestor(root.right, p, q);
			}
			return root;
		}
		public static boolean covers(TreeNode root, TreeNode p)
		{
			if(root == null)
			{
				return false;
			}
			if(root == p)
			{
				return true;
			}
			return covers(root.left, p) || covers(root.right, p);
		}
	}
	{% endhighlight %}


### 7. 判断二叉树T2是否为二叉树T1的子树 ###

You have two very large binary trees: T1, with millions of nodes, and T2, with hundreds of nodes. Create an algorithm to decide if T2 is a subtree of T1


	{% highlight java %}
	public class IsSubTree
	{
		public static boolean subTree(TreeNode t1, TreeNode t2)
		{
			if(t2 == null)
			{
				return true;
			}
			if(t1 == null)
			{
				return false;
			}
			if(t1.data == t2.data)
			{
				if(matchTree(t1, t2))
				{
					return true;
				}
			}
			return (subTree(t1.left, t2) || (subTree(t1.right, t2)))
		}
		public boolean matchTree(TreeNode t1, TreeNode t2)
		{
			if(t1 == null && t2 == null)
			{
				return true;
			}
			if(t1 == null || t2 == null)
			{
				retur false;
			}
			if(t1.data != t2.data)
			{
				return false;
			}
			return (matchTree(t1.left, t2.left) 
				&& matchTree(t1.right, t2.right));
		}
	}
	{% endhighlight %}


### 8. 打印出所有满足以下条件的路径： 二叉树路径上结点的值加起来等于给定的一个值。 ###

You are given a binary tree in which each node contains a value. Design an algorithm to print all paths which sum up to that value. Note that it can be any path in the tree - it does not have to start at the root.


	{% highlight java %}
	public class FindSum
	{
		public static void findSum(TreeNode head, int sum, ArrayList<Integer> buffer, int level)
		{
			if(head == null)
			{
				return;
			}
			int tmp = sum;
			buffer.add(head.data);
			for(int i = level; i >= 1; i--)
			{
				tmp -= buffer.get(i);
				if(tmp == 0)
				{
					for(int j = i; i <= level; j++)
					{
						System.out.print(buffer.get(j) + " ");
					}
				}
			}
			ArrayList<Integer> c1 = (ArrayList<Integer>)buffer.clone();
			ArrayList<Integer> c2 = (ArrayList<Integer>)buffer.clone();
			findSum(head.left, sum, c1, level+1);
			findSum(head.right, sum, c2, level+1);
		}
	}
	{% endhighlight %}


C++版实现可参考： [Cracking the coding interview--问题与解答](http://www.hawstein.com/posts/ctci-solutions-contents.html)

