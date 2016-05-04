---
date: 2016-4-18 20:08:30+00:00
layout: post
title: Leetcode中二叉树类题目小结(Medium部分)
thread: 127
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中Tree的Medium部分的题型，目前已有的题目有：

1. Unique Binary Search Trees

2. Unique Binary Search Trees II

3. Lowest Common Ancestor of a Binary Tree

4. Validate Binary Search Tree

5. Kth Smallest Element in a BST

6. House Robber III

7. Count Complete Tree Nodes

8. Binary Tree Right Side View

9. Binary Search Tree Iterator

10. Binary Tree Preorder Traversal

11. Sum Root to Leaf Numbers

12. Populating Next Right Pointers in Each Node

13. Flatten Binary Tree to Linked List

14. Path Sum II

15. Binary Tree Zigzag Level Order Traversal

16. Construct Binary Tree from Preorder and Inorder Traversal.

17. Construct Binary Tree from Inorder and Postorder Traversal

18. Convert Sorted Array to Binary Search Tree

19. Binary Tree Inorder Traversal


### [Unique Binary Search Trees](https://leetcode.com/problems/unique-binary-search-trees/) ###


Given n, how many structurally unique BST's (binary search trees) that store values 1...n?

For example,
Given n = 3, there are a total of 5 unique BST's.

	   1         3     3      2      1
	    \       /     /      / \      \
	     3     2     1      1   3      2
	    /     /       \                 \
	   2     1         2                 3


实现如下：

	{% highlight java %}
	//dynamic
	public int numTrees(int n)
	{
		int[] count = new int[n+1];
		count[0]=1;
		count[1]=1;
		for(int i=2;i<=n;i++)
		{
			for(int j=0;j<=i-1;j++)
			{
				count[i]=count[i]+count[j]*count[i-j-1];
			}
		}
		return count[n];
	}
	{% endhighlight %}


### [Unique Binary Search Trees II](https://leetcode.com/problems/unique-binary-search-trees-ii/) ###

Given n, generate all structurally unique BST's (binary search trees) that store values 1...n.

For example,
Given n = 3, your program should return all 5 unique BST's shown below.

	   1         3     3      2      1
	    \       /     /      / \      \
	     3     2     1      1   3      2
	    /     /       \                 \
	   2     1         2                 3


实现如下：

	{% highlight java %}
	//recursive
	public List<TreeNode> generateTrees(int n)
	{
		return generateTrees(1,n);
	}
	public List<TreeNode> generateTrees(int start,int end)
	{
		List<TreeNode> list=new LinkedList<TreeNode>();
		if(start>end)
		{
			list.add(null);
			return list;
		}
		for(int i=start;i<=end;i++)
		{
			List<TreeNode> lefts=generateTrees(start,i-1);
			List<TreeNode> rights=generateTrees(i+1,end);
			for(TreeNode left:lefts)
			{
				for(TreeNode right:rights)
				{
					TreeNode node = new TreeNode(i);
					node.left=left;
					node.right=right;
					list.add(node);
				}
			}
		}
		return list;
	}
	{% endhighlight %}
	
### [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)###

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes v and w as the lowest node in T that has both v and w as descendants (where we allow a node to be a descendant of itself).”

	        _______3______
	       /              \
	    ___5__          ___1__
	   /      \        /      \
	   6      _2       0       8
	         /  \
	         7   4

For example, the lowest common ancestor (LCA) of nodes 5 and 1 is 3. Another example is LCA of nodes 5 and 4 is 5, since a node can be a descendant of itself according to the LCA definition.

	{% highlight java %}
	//solution 1 recursive
	public TreeNode lowestCommonAncestor(TreeNode root,TreeNode p,TreeNode q)
	{
		if(root==null||root==p||root==q)
		{
			return root;
		}
		TreeNode left=lowestCommonAncestor(root.left,p,q);
		TreeNode right=lowestCommonAncestor(root.right,p,q);
		if(left!=null&&right!=null)
		{
			return root;
		}
		return left==null?right:left;
	}
	{% endhighlight %}


### [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) ###

Given a binary tree, determine if it is a valid binary search tree (BST).

Assume a BST is defined as follows:

The left subtree of a node contains only nodes with keys less than the node's key.

The right subtree of a node contains only nodes with keys greater than the node's key.

Both the left and right subtrees must also be binary search trees.

	{% highlight java %}
	public boolean isValidBST(TreeNode root)
	{
		return isValidBST(root,Long.MIN_VALUE,Long.MAX_VALUE);
	}
	public boolean isValidBST(TreeNode root,long minVal,long maxVal)
	{
		if(root==null)
		{
			return true;
		}
		if(root.val>=maxVal||root.val<=minVal)
		{
			return false;
		}
		return isValidBST(root.left,minVal,root.val)&&isValidBST(root.right,root.val,maxVal);
	}
	{% endhighlight %}

### [Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) ###

Given a binary search tree, write a function kthSmallest to find the kth smallest element in it.

Note: 
You may assume k is always valid, 1 ≤ k ≤ BST's total elements.

Follow up:
What if the BST is modified (insert/delete operations) often and you need to find the kth smallest frequently? How would you optimize the kthSmallest routine?

	{% highlight java %}
	public int kthSmallest(TreeNode root,int k)
	{
		Stack<TreeNode> stack=new Stack<TreeNode>();
		TreeNode p=root;
		int result =0;
		while(!stack.isEmpty()||p!=null)
		{
			if(p!=null)
			{
				stack.push(p);
				p=p.left;
			}
			else
			{
				TreeNode t=stack.pop();
				k--;
				if(k==0)
				{
					result=t.val;
				}
				p=t.right;
			}
		}
		return result;
	}
	{% endhighlight %}

### [House Robber III](https://leetcode.com/problems/house-robber-iii/) ###

The thief has found himself a new place for his thievery again. There is only one entrance to this area, called the "root." Besides the root, each house has one and only one parent house. After a tour, the smart thief realized that "all houses in this place forms a binary tree". It will automatically contact the police if two directly-linked houses were broken into on the same night.

Determine the maximum amount of money the thief can rob tonight without alerting the police.

Example 1:

	     3
	    / \
	   2   3
	    \   \ 
	     3   1

Maximum amount of money the thief can rob = 3 + 3 + 1 = 7.
Example 2:

	     3
	    / \
	   4   5
	  / \   \ 
	 1   3   1

Maximum amount of money the thief can rob = 4 + 5 = 9.


### [Count Complete Tree Nodes](https://leetcode.com/problems/count-complete-tree-nodes/) ###

Given a complete binary tree, count the number of nodes.

Definition of a complete binary tree from Wikipedia:

In a complete binary tree every level, except possibly the last, is completely filled, and all nodes in the last level are as far left as possible. It can have between 1 and 2h nodes inclusive at the last level h.

	{% highlight java %}
	public int countNodes(TreeNode root) {
		if(root==null)
	    {
	    	return 0;
	    }
	    int left = getLeftHeight(root)+1;    
	    int right = getRightHeight(root)+1;
	    if(left==right)
	    {
	        return (2<<(left-1))-1;
	    }
	    else
	    {
	        return countNodes(root.left)+countNodes(root.right)+1;
	    }
	}
	public int getLeftHeight(TreeNode n){
	    if(n==null)
	    {
	    	return 0;
	    }
	    int height=0;
	    while(n.left!=null)
	    {
	        height++;
	        n = n.left;
	    }
	    return height;
	}
	public int getRightHeight(TreeNode n){
	    if(n==null) 
	    {
	    	return 0;
	    }
	    int height=0;
	    while(n.right!=null)
	    {
	        height++;
	        n = n.right;
	    }
	    return height;
	}
	{% endhighlight %}

### [Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) ###

Given a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.

For example:
Given the following binary tree,

	   1            <---
	 /   \
	2     3         <---
	 \     \
	  5     4       <---

You should return [1, 3, 4].

	{% highlight java %}
	public List<Integer> rightSideView(TreeNode root)
	{
		ArrayList<Integer> result=new ArrayList<Integer>();
		if(root==null)
		{
			return result;
		}
		LinkedList<TreeNode> queue=new LinkedList<TreeNode>();
		queue.add(root);
		while(queue.size()>0)
		{
			int size=queue.size();
			for(int i=0;i<size;i++)
			{
				TreeNode top=queue.remove();
				if(i==0)
				{
					result.add(top.val);
				}
				if(top.right!=null)
				{
					queue.add(top.right);
				}
				if(top.left!=null)
				{
					queue.add(top.left);
				}
			}
		}
		return result;
	}
	{% endhighlight %}


### [Binary Search Tree Iterator](https://leetcode.com/problems/binary-search-tree-iterator/) ###

Implement an iterator over a binary search tree (BST). Your iterator will be initialized with the root node of a BST.

Calling next() will return the next smallest number in the BST.

Note: next() and hasNext() should run in average O(1) time and uses O(h) memory, where h is the height of the tree.

	{% highlight java %}
	public class BSTIterator
	{
		Stack<TreeNode> stack;
		public BSTIterator(TreeNode root)
		{
			stack=new Stack<TreeNode>();
			while(root!=null)
			{
				stack.push(root);
				root=root.left;
			}
		}
		public boolean hasNext()
		{
			return !stack.isEmpty();
		}
		public int next()
		{
			TreeNode node = stack.pop();
			int result = node.val;
			if(node.right!=null)
			{
				node=node.right;
				while(node!=null)
				{
					stack.push(node);
					node=node.left;
				}
			}
			return result;
		}
	}
	{% endhighlight %}

### [Binary Tree Preorder Traversal](https://leetcode.com/problems/binary-tree-preorder-traversal/) ###

Given a binary tree, return the preorder traversal of its nodes' values.

For example:
Given binary tree {1,#,2,3},

	   1
	    \
	     2
	    /
	   3

return [1,2,3].

Note: Recursive solution is trivial, could you do it iteratively?

	{% highlight java %}
	public List<Integer> preorderTraversal(TreeNode node)
	{
		List<Integer> list=new LinkedList<Integer>();
		Stack<TreeNode> stack = new Stack<TreeNode>();
		while(node!=null)
		{
			list.add(node.val);
			if(node.right!=null)
			{
				stack.push(node.right);
			}
			node=node.left;
			if(node==null&&!stack.isEmpty())
			{
				node=stack.pop();
			}
		}
		return list;
	}
	{% endhighlight %}


### [Sum Root to Leaf Numbers](https://leetcode.com/problems/sum-root-to-leaf-numbers/) ###

Given a binary tree containing digits from 0-9 only, each root-to-leaf path could represent a number.

An example is the root-to-leaf path 1->2->3 which represents the number 123.

Find the total sum of all root-to-leaf numbers.

For example,

	    1
	   / \
	  2   3

The root-to-leaf path 1->2 represents the number 12.
The root-to-leaf path 1->3 represents the number 13.

Return the sum = 12 + 13 = 25.

	{% highlight java %}
	public int sumNumbers(TreeNode root)
	{
		if(root==null)
		{
			return 0;
		}
		return dfs(root,0,0);
	}
	public int dfs(TreeNode node,int num,int sum)
	{
		if(node==null)
		{
			return sum;
		}
		num=num*10+node.val;
		if(node.left==null&&node.righ==null)
		{
			sum+=num;
			return sum;
		}
		sum=dfs(node.left,num,sum)+dfs(node.right,num,sum);
		return sum;
	}
	{% endhighlight %}


### [Populating Next Right Pointers in Each Node](https://leetcode.com/problems/populating-next-right-pointers-in-each-node/) ###

Given a binary tree

    struct TreeLinkNode {
      TreeLinkNode *left;
      TreeLinkNode *right;
      TreeLinkNode *next;
    }

Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to NULL.

Initially, all next pointers are set to NULL.

Note:

You may only use constant extra space.
You may assume that it is a perfect binary tree (ie, all leaves are at the same level, and every parent has two children).
For example,
Given the following perfect binary tree,

         1
       /  \
      2    3
     / \  / \
    4  5  6  7

After calling your function, the tree should look like:

         1 -> NULL
       /  \
      2 -> 3 -> NULL
     / \  / \
    4->5->6->7 -> NULL



### [Flatten Binary Tree to Linked List](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/) ###

Given a binary tree, flatten it to a linked list in-place.

For example,
Given

         1
        / \
       2   5
      / \   \
     3   4   6

The flattened tree should look like:

	   1
	    \
	     2
	      \
	       3
	        \
	         4
	          \
	           5
	            \
	             6

实现如下：

	{% highlight java %}
	//solution 1 recursive
	public void flatten(TreeNode root)
	{
		if(root==null)
		{
			return;
		}
		TreeNode left=root.left;
		TreeNode right=root.right;
		root.left=null;
		flatten(left);
		flatten(right);
		root.right=left;
		TreeNode cur=root;
		while(cur.right!=null)
		{
			cur=cur.right;
		}
		cur.right=right;
	}
	{% endhighlight %}


### [Path Sum II](https://leetcode.com/problems/path-sum-ii/) ###

Given a binary tree and a sum, find all root-to-leaf paths where each path's sum equals the given sum.

For example:
Given the below binary tree and sum = 22,

              5
             / \
            4   8
           /   / \
          11  13  4
         /  \    / \
        7    2  5   1

return

	[
	   [5,4,11,2],
	   [5,8,4,5]
	]

实现如下：

	{% highlight java %}
	public List<ArrayList<Integer>> pathSum(TreeNode root, int sum)
	{
		ArrayList<ArrayList<Integer>> result=new ArrayList<ArrayList<Integer>>();
		if(root==null)
		{
			return result;
		}
		List<Integer> currentResult=new ArrayList<Integer>();
		currentResult.add(root.val);
		dfs(root,sum-root.val,result,currentResult);
		return result;
	}
	public void dfs(TreeNode t,int sum,ArrayList<ArrayList<Integer>> result,ArrayList<Integer> currentResult)
	{
		if(t.left==null&&t.right==null&&sum==0)
		{
			result.add(new ArrayList<Integer>(currentResult));
		}
		if(t.left!=null)
		{
			currentResult.add(t.left.val);
			dfs(t.left,sum-t.left.val,result,currentResult);
			currentResult.remove(currentResult.size()-1);
		}
		if(t.right!=null)
		{
			currentResult.add(t.right.val);
			dfs(t.right,sum-t.right.val,result,currentResult);
			currentResult.remove(currentResult.size()-1);
		}
	}
	{% endhighlight %}

### [Binary Tree Zigzag Level Order Traversal](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) ###

Given a binary tree, return the zigzag level order traversal of its nodes' values. (ie, from left to right, then right to left for the next level and alternate between).

For example:
Given binary tree {3,9,20,#,#,15,7},

	    3
	   / \
	  9  20
	    /  \
	   15   7

return its zigzag level order traversal as:

	[
	  [3],
	  [20,9],
	  [15,7]
	]


### [Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) ###

Given preorder and inorder traversal of a tree, construct the binary tree.

Note:
You may assume that duplicates do not exist in the tree.

	{% highlight java %}
	public TreeNode buildTree(int[] preorder,int[] inorder)
	{
		int preStart=0;
		int preEnd=preorder.length-1;
		int inStart=0;
		int inEnd=inorder.length-1;
		return construct(preorder,preStart,preEnd,inorder,inStart,inEnd);
	}
	public TreeNode construct(int[] preorder,int preStart,int preEnd,
		int[] inorder,int inStart,int inEnd)
	{
		if(preStart>preEnd||inStart>inEnd)
		{
			return null;
		}
		int val=preorder[preStart];
		TreeNode root=new TreeNode(val);
		int k=0;
		for(int i=0;i<inorder.length;i++)
		{
			if(val==inorder[i])
			{
				k=i;
				break;
			}
		}
		root.left=construct(preorder,preStart+1,preStart+(k-			inStart),inorder,inStart,k-1);
		root.right=construct(preorder,preStart+(k-inStart)+1,preEnd,inorder,k			+1,inEnd);
		return root;
	}
	{% endhighlight %}

### [Construct Binary Tree from Inorder and Postorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/) ###

Given inorder and postorder traversal of a tree, construct the binary tree.

Note:
You may assume that duplicates do not exist in the tree.

	{% highlight java %}
	public TreeNode buildTree(int[] inorder,int[] postorder)
	{
		int inStart=0;
		int inEnd=inorder.length-1;
		int postStart=0;
		int postEnd=postorder.length-1;
		return construct(inorder,inStart,inEnd,postorder,postStart,postEnd);
	}
	public TreeNode construct(int[] inorder,int inStart,int inEnd,
		int[] postorder,int postStart,int postEnd)
		{
			if(inStart>inEnd||postStart>postEnd)
			{
				return null;
			}
			int val=postorder[postEnd];
			TreeNode root=new TreeNode(val);
			int k=0;
			for(int i=0;i<inorder.length;i++)
			{
				if(inorder[i]==val)
				{
					k=i;
					break;
				}
			}
			root.left=construct(inorder,inStart,k-1,postorder,postStart,
				postStart+k-(inStart+1));
			root.right=construct(inorder,k+1,inEnd,postorder,
				postStart+k-inStart,postEnd-1);
			return root;
		}
	{% endhighlight %}

### [Convert Sorted Array to Binary Search Tree](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/) ###

Given an array where elements are sorted in ascending order, convert it to a height balanced BST.

	{% highlight java %}
	//solution 1 recursive
	public TreeNode sortedArrayToBST(int[] num)
	{
		if(num.length==0)
		{
			return null;
		}
		TreeNode head=helper(num,0,num.length-1);
		return head;
	}
	public TreeNode helper(int[] num,int low,int high)
	{
		if(low>high)
		{
			return null;
		}
		int mid = (low+high)/2;
		TreeNode node = new TreeNode(num[mid]);
		node.left=helper(num,low,mid-1);
		node.right=helper(num,mid+1,high);
		return node;
	}
	{% endhighlight %}

### [Binary Tree Inorder Traversal](https://leetcode.com/problems/binary-tree-inorder-traversal/) ###

Given a binary tree, return the inorder traversal of its nodes' values.

For example:
Given binary tree {1,#,2,3},

	   1
	    \
	     2
	    /
	   3

return [1,3,2].

Note: Recursive solution is trivial, could you do it iteratively?

	{% highlight java %}
	//solution 1 recursive
	public List<Integer> result=new ArrayList<Integer>();
	public List<Integer> inorderTraversal(TreeNode root)
	{
		if(root!=null)
		{
			inorderTraversalRecursive(root);
		}
		return result;
	}
	public void inorderTraversalRecursive(TreeNode root)
	{
		if(root==null)
		{
			return;
		}
		inorderTraversalRecursive(root.left);
		result.add(root.val);
		inorderTraversalRecursive(root.right);
	}
	{% endhighlight %}