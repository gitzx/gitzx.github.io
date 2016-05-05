---
date: 2016-5-4 19:23:30+00:00
layout: post
title: Leetcode中二叉树类题目小结(Hard部分)
thread: 129
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中Tree的Medium部分的题型，目前已有的题目有：

1. Binary Tree Maximum Path Sum

2. Serialize and Deserialize Binary Tree

3. Recover Binary Search Tree

4. Binary Tree Postorder Traversal

5. Populating Next Right Pointers in Each Node II


### [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) ###

Given a binary tree, find the maximum path sum.

For this problem, a path is defined as any sequence of nodes from some starting node to any node in the tree along the parent-child connections. The path does not need to go through the root.

For example:
Given the below binary tree,

       1
      / \
     2   3

Return 6.

	{% highlight java %}
	public int maxPathSum(TreeNode root)
	{
		int max[] = new int[1];
		max[0]=Integer.MIN_VALUE;
		calculateSum(root,max);
		return max[0];
	}
	public int calculateSum(TreeNode root, int[] max)
	{
		if(root==null)
		{
			return 0;
		}
		int left=calculateSum(root.left,max);
		int right=calculateSum(root.right,max);
		int current=Math.max(root.val,Math.max(root.val+left, root.val+right));
		max[0] = Math.max(max[0],Math.max(current, left+root.val+right));
		return current;
	}
	{% endhighlight %}

### [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) ###

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

For example, you may serialize the following tree

	    1
	   / \
	  2   3
	     / \
	    4   5

as "[1,2,3,null,null,4,5]", just the same as how LeetCode OJ serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.

Note: Do not use class member/global/static variables to store states. Your serialize and deserialize algorithms should be stateless.


### [Recover Binary Search Tree](https://leetcode.com/problems/recover-binary-search-tree/) ###

Two elements of a binary search tree (BST) are swapped by mistake.

Recover the tree without changing its structure.

Note:
A solution using O(n) space is pretty straight forward. Could you devise a constant space solution?

	{% highlight java %}
	public class Solution
	{
		TreeNode first;
		TreeNode second;
		TreeNode pre;
		public void inorder(TreeNode root)
		{
			if(root==null)
			{
				return;
			}
			inorder(root.left);
			if(pre==null)
			{
				pre=root;
			}
			else
			{
				if(root.val<pre.val)
				{
					if(first==null)
					{
						first=pre;
					}
					second=root;
				}
				pre=root;
			}
			inorder(root.right);
		}
		public void recoverTree(TreeNode root)
		{
			if(root==null)
			{
				return;
			}
			inorder(root);
			if(second!=null&&first!=null)
			{
				int val=second.val;
				second.val=first.val;
				first.val=val;
			}
		}
	}
	{% endhighlight %}

### [Binary Tree Postorder Traversal](https://leetcode.com/problems/binary-tree-postorder-traversal/) ###

Given a binary tree, return the postorder traversal of its nodes' values.

For example:
Given binary tree {1,#,2,3},

	   1
	    \
	     2
	    /
	   3

return [3,2,1].

Note: Recursive solution is trivial, could you do it iteratively?

	{% highlight java %}
	public List<Integer> postorderTraversal(TreeNode root)
	{
		List<Integer> list=new ArrayList<Integer>();
		if(root==null)
		{
			return list;
		}
		Stack<TreeNode> stack=new Stack<TreeNode>();
		stack.push(root);
		while(!stack.isEmpty())
		{
			TreeNode temp=stack.peek();
			if(temp.left==null&&temp.right==null)
			{
				TreeNode pop=stack.pop();
				list.add(pop.val);
			}
			else
			{
				if(temp.right!=null)
				{
					stack.push(temp.right);
					temp.right=null;
				}
				if(temp.left!=null) 
				{
					stack.push(temp.left);
					temp.left=null;
				}
			}
		}
		return list;
	}
	{% endhighlight %}

### [Populating Next Right Pointers in Each Node II](https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/) ###

Follow up for problem "Populating Next Right Pointers in Each Node".

What if the given tree could be any binary tree? Would your previous solution still work?

Note:

You may only use constant extra space.
For example,
Given the following binary tree,

         1
       /  \
      2    3
     / \    \
    4   5    7

After calling your function, the tree should look like:

         1 -> NULL
       /  \
      2 -> 3 -> NULL
     / \    \
    4-> 5 -> 7 -> NULL

Subscribe to see which companies asked this question



