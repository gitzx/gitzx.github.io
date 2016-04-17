---
date: 2016-4-15 19:12:30+00:00
layout: post
title: Leetcode中二叉树类题目小结(Easy部分)
thread: 126
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中Tree的Easy部分的题型，目前已有的题目有：

1. Lowest Common Ancestor of a Binary Search Tree

2. Maximum Depth of Binary Tree

3. Binary Tree Level Order Traversal

4. Binary Tree Level Order Traversal II

5. Balanced Binary Tree

6. Minimum Depth of Binary Tree

7. Invert Binary Tree

8. Path Sum

9. Symmetric Tree

10. Same Tree

11. Binary Tree Paths


### [Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) ###

Given a binary search tree (BST), find the lowest common ancestor (LCA) of two given nodes in the BST.

According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes v and w as the lowest node in T that has both v and w as descendants (where we allow a node to be a descendant of itself).”

        _______6______
       /              \
    ___2__          ___8__
   /      \        /      \
   0      _4       7       9
         /  \
         3   5
         
For example, the lowest common ancestor (LCA) of nodes 2 and 8 is 6. Another example is LCA of nodes 2 and 4 is 2, since a node can be a descendant of itself according to the LCA definition.

	{% highlight java %}
	public TreeNode lowestCommonAncestor(TreeNode root,TreeNode p,TreeNode q)
	{
		if(root==null||p==null||q==null)
		{
			return root;
		}
		TreeNode left=lowestCommonAncestor(root.left,p,q);
		TreeNode right=lowestCommonAncestor(root.right,p,q);
		return left==null?right:right==null?left:root;
	}
	{% endhighlight %}


### [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) ###

Given a binary tree, find its maximum depth.

The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

	{% highlight java %}
	public int maxDepth(TreeNode root)
	{
		if(root==null)
		{
			return 0;
		}
		int left = maxDepth(root.left);
		int right = maxDepth(root.right);
		return Math.max(left, right)+1;
	}
	{% endhighlight %}


### [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) ###

Given a binary tree, return the level order traversal of its nodes' values. (ie, from left to right, level by level).

For example:

Given binary tree {3,9,20,#,#,15,7},

	    3
	   / \
	  9  20
	    /  \
	   15   7
   
return its level order traversal as:

	[
	  [3],
	  [9,20],
	  [15,7]
	]


### [Binary Tree Level Order Traversal II](https://leetcode.com/problems/binary-tree-level-order-traversal-ii/) ###

Given a binary tree, return the bottom-up level order traversal of its nodes' values. (ie, from left to right, level by level from leaf to root).

For example:
Given binary tree {3,9,20,#,#,15,7},

	    3
	   / \
	  9  20
	    /  \
	   15   7
   
return its bottom-up level order traversal as:

	[
	  [15,7],
	  [9,20],
	  [3]
	]
	

### [Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) ###

Given a binary tree, determine if it is height-balanced.

For this problem, a height-balanced binary tree is defined as a binary tree in which the depth of the two subtrees of every node never differ by more than 1.

	{% highlight java %}
	public boolean isBalanced(TreeNode root)
	{
		if(root==null)
		{
			return true;
		}
		return isBalancedRecursive(root)>-1;
	}
	public int isBalancedRecursive(TreeNode root)
	{
		if(root==null)
		{
			return 0;
		}
		int left=isBalancedRecursive(root.left);
		int right = isBalancedRecursive(root.right);
		if(left==-1||right==-1)
		{
			return -1;
		}
		if(Math.abs(left-right)>1)
		{
			return -1;
		}
		return Math.max(left,right)+1;
	}
	{% endhighlight %}

### [Minimum Depth of Binary Tree](https://leetcode.com/problems/minimum-depth-of-binary-tree/) ###

Given a binary tree, find its minimum depth.

The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

	{% highlight java %}
	public int minDepth(TreeNode root)
	{
		if(root==null)
		{
			return 0;
		}
		int left = minDepth(root.left);
		int right = minDepth(root.right);
		return Math.min(left,right)+1;
	}
	{% endhighlight %}


### [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) ###

Invert a binary tree.

	     4
	   /   \
	  2     7
	 / \   / \
	1   3 6   9

to

	     4
	   /   \
	  7     2
	 / \   / \
	9   6 3   1
	
	
	{% highlight java %}
	public TreeNode invertTree(TreeNode root)
	{
		if(root==null)
		{
			return null;
		}
		TreeNode left=root.left;
		TreeNode right=root.right;
		root.left=invertTree(right);
		root.right=invertTree(left);
		return root;
	}
	{% endhighlight %}


### [Path Sum](https://leetcode.com/problems/path-sum/) ###

Given a binary tree and a sum, determine if the tree has a root-to-leaf path such that adding up all the values along the path equals the given sum.

For example:
Given the below binary tree and sum = 22,

              5
             / \
            4   8
           /   / \
          11  13  4
         /  \      \
        7    2      1
        
return true, as there exist a root-to-leaf path 5->4->11->2 which sum is 22.

	{% highlight java %}
	public boolean hasPathSum(TreeNode root,int sum)
	{
		if(root==null)
		{
			return false;
		}
		if(root.left==null&&root.right==null)
		{
			return sum==root.val;
		}
		return hasPathSum(root.left,sum-root.val)||hasPathSum(root.right,sum-root.val);
	}
	{% endhighlight %}


### [Symmetric Tree](https://leetcode.com/problems/symmetric-tree/) ###

Given a binary tree, check whether it is a mirror of itself (ie, symmetric around its center).

For example, this binary tree is symmetric:

	    1
	   / \
	  2   2
	 / \ / \
	3  4 4  3

But the following is not:

	    1
	   / \
	  2   2
	   \   \
	   3    3
   
Note:
Bonus points if you could solve it both recursively and iteratively.

	{% highlight java %}
	public boolean isSymmetric(TreeNode root)
	{
		if(root==null)
		{
			return true;
		}
		return isSymmetricRecursive(root.left,root.right);
	}
	public boolean isSymmetricRecursive(TreeNode t1, TreeNode t2)
	{
		if(t1==null||t2==null)
		{
			return true;
		}
		if(t1==null&&t2!=null || t1!=null&&t2==null ||t1.val!=t2.val)
		{
			return false;
		}
		return isSymmetricRecursive(t1.left,t2.left)&&isSymmetricRecursive(t1.right,t2.right);
	}
	{% endhighlight %}

### [Same Tree](https://leetcode.com/problems/same-tree/) ###

Given two binary trees, write a function to check if they are equal or not.

Two binary trees are considered equal if they are structurally identical and the nodes have the same value.

	{% highlight java %}
	public boolean isSameTree(TreeNode p, TreeNode q)
	{
		if(p==null&&q==null)
		{
			return true;
		}
		if((p==null&&q!=null)||(p!=null&&q==null))
		{
			return false;
		}
		if(p.val!=q.val)
		{
			return false;
		}
		return isSameTree(p.left,q.left)&&isSameTree(p.right,q.right);
	}
	{% endhighlight %}


### [Binary Tree Paths](https://leetcode.com/problems/binary-tree-paths/) ###

Given a binary tree, return all root-to-leaf paths.

For example, given the following binary tree:

	   1
	 /   \
	2     3
	 \
	  5
  
All root-to-leaf paths are:

["1->2->5", "1->3"]

	{% highlight java %}
	public List<String> binaryTreePaths(TreeNode root)
	{
		List<String> answer=new ArrayList<String>();
		if(root!=null)
		{
			searchBT(root,"",answer);
		}
		return answer;
	}
	public void searchBT(TreeNode root,String path,List<String> answer)
	{
		if(root.left==null&&root.right==null)
		{
			answer.add(path+root.val);
		}
		if(root.left!=null)
		{
			searchBT(root.left,path+root.val+"->", answer);
		}
		if(root.right!=null)
		{
			searchBT(root,right,path+root.val+"->",answer);
		}
	}
	{% endhighlight %}









