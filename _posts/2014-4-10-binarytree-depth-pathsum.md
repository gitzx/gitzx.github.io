---
date: 2014-4-10 11:45:30+00:00
layout: post
title: 二叉树的深度和路径和问题
thread: 50
categories: algorithm
tags: algorithm
---

###二叉树的深度###

(1)二叉树的最大深度（即根节点到最深叶子节点之间的节点数）

	{% highlight C++ %}
	int maxDepth(TreeNode *root){
		if(root==NULL)
			return 0;
		int nLeft=maxDepth(root->left);
		int nRight=maxDepth(root->right);
		return max(nLeft, nRight)+1;
	}
	{% endhighlight %}

(2)二叉树的最小深度（即根节点到最浅叶子节点之间的节点数）
(时间复杂度为o(n),空间复杂度为o（logn）)：

	{% highlight C++ %}
	class Solution{
	public:
		int minDepth(TreeNode *root){
			return minDepth(root, false);
		}
	private:
		static int minDepth(const TreeNode *root, bool hasbrother){
			if(root==NULL)
				return hasbrother? INT_MAX:0;
			return min(minDepth(root->left,root->right!=NULL),
				minDepth(root->right,root->left!=NULL))+1;
		}
	};
	{% endhighlight %}

###二叉树的路径和问题###

（1）给定一个二叉树和一个值，检测是否存在从根节点到叶子节点的路径，使得路径上的节点值的总和等于给定的值。

	{% highlight C++ %}
	//时间复杂度为o(n),空间复杂度为o(logn)
	int hasPathSum(TreeNode *root, int sum){
		if(root==NULL)
			return false;
		if(root->left==NULL&&root->right==NULL)
			return sum==root->data;
		return hasPathSum(root->left, sum-root->data) 
			|| hasPathSum(root->right,sum-root->data);
	}
	{% endhighlight %}

(2)给定一个二叉树和一个值，找出所有从根节点到叶子节点路径中的节点总值的路径。

	{% highlight C++ %}
	class Solution{
	public:
		vector< vector<int> > v;> v;> v; pathSum(TreeNode *root, int sum){
			vector<vector<int> > result;
			vector<int> cur;  //中间结果
			pathSum(root, sum, cur, result);
			return result;
		}
	private:
		void pathSum(TreeNode *root,int gap,vector<int>
			&cur,vector<vector<int> > &result){
			if(root==NULL)
				return;
			cur.push_back(root->data);
			if(root->left==NULL&&root->right==NULL){
				if(root->data==gap){
					result.push_back(cur);
				}		
			} //叶子节点
			pathSum(root->left,gap-root->data,cur,result);
			pathSum(root->right,gap-root->data,cur,result);
			cur.pop_back();
		}
	};
	{% endhighlight %}
 
(3)给定一个二叉树，计算最长的路径和，使得任意两节点的路径上所有节点之和最大（和最长序列和问题类似，只是变成两个方向）。

	{% highlight C++ %}
	class Solution{
	public:
		int maxDepthSum(TreeNode *root){
			max_sum=INT_MIN;
			dfs(root);
			return max_sum;
		}
	private:
		int max_sum;
		int dfs(const TreeNode *root){
			if(root==NULL)
				return 0;
			int l=dfs(root->left);
			int r=dfs(root->right);
			int sum=root->data;
			if(l>0)
				sum+=l;
			if(r>0)
				sum+=r;
			max_sum=max(max_sum, sum);
			return max(r,l)>0? max(r,l)+root->data : root->data;
		}
	};
	{% endhighlight %}


