---
date: 2016-6-18 9:50:30+00:00
layout: post
title: Leetcode中回溯算法类题目小结
thread: 142
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中回溯算法类部分的题目，目前已有的题目(除去之前已总结的)有：

1. Gray Code

2. Permutations

3. Permutations II

4. Add and Search Word - Data structure design

5. Palindrome Partitioning

6. Combinations

7. Word Search II

8. Word Break II

9. N-Queens

10. N-Queens II


### [Gray Code](https://leetcode.com/problems/gray-code/) ###

The gray code is a binary numeral system where two successive values differ in only one bit.

Given a non-negative integer n representing the total number of bits in the code, print the sequence of gray code. A gray code sequence must begin with 0.

For example, given n = 2, return [0,1,3,2]. Its gray code sequence is:

	00 - 0
	01 - 1
	11 - 3
	10 - 2

Note:

For a given n, a gray code sequence is not uniquely defined.

For example, [0,2,3,1] is also a valid gray code sequence according to the above definition.

For now, the judge is able to judge based on one instance of gray code sequence. Sorry about that.

	{% highlight java %}
	public List<Integer> grayCode(int n)
	{
		if(n==0)
		{
			List<Integer> result=new ArrayList<Integer>();
			result.add(0);
			return result;
		}
		List<Integer> result=grayCode(n-1);
		int numToAdd=1<<(n-1);
		for(int i=result.size()-1;i>=0;i--)
		{
			result.add(numToAdd+result.get(i));
		}
		return result;
	}
	{% endhighlight %}

### [Permutations](https://leetcode.com/problems/permutations/) ###

Given a collection of distinct numbers, return all possible permutations.

For example,

[1,2,3] have the following permutations:

	[
	  [1,2,3],
	  [1,3,2],
	  [2,1,3],
	  [2,3,1],
	  [3,1,2],
	  [3,2,1]
	]

Subscribe to see which companies asked this question

	{% highlight java %}
	//recursive
	public ArrayList<ArrayList<Integer>> permute(int[] num)
	{
		ArrayList<ArrayList<Integer>> result=new ArrayList<ArrayList<Integer>>();
		permute(num,0,result);
		return result;
	}
	public void permute(int[] num,int start,ArrayList<ArrayList<Integer>> result)
	{
		if(start>=num.length)
		{
			ArrayList<Integer> item=convertArrayToList(num);
			result.add(item);
		}
		for(int j=start;j<num.length;j++)
		{
			swap(num,start,j);
			permute(num,start+1,result);
			swap(num,start,j);
		}
	}
	public ArrayList<Integer> convertArrayToList(int[] num)
	{
		ArrayList<Integer> item=new ArrayList<Integer>();
		for(int i=0;i<num.length;i++)
		{
			item.add(num[i]);
		}
		return item;
	}
	public void swap(int[] a,int i,int j)
	{
		int temp=a[i];
		a[i]=a[j];
		a[j]=temp;
	}
	{% endhighlight %}

### [Permutations II](https://leetcode.com/problems/permutations-ii/) ###

Given a collection of numbers that might contain duplicates, return all possible unique permutations.

For example,

[1,1,2] have the following unique permutations:

	[
	  [1,1,2],
	  [1,2,1],
	  [2,1,1]
	]

Subscribe to see which companies asked this question

	{% highlight java %}
	//recursive
	public ArrayList<ArrayList<Integer>> permuteUnique(int[] num)
	{
		ArrayList<ArrayList<Integer>> result=new ArrayList<ArrayList<Integer>>();
		permuteUnique(num,0,result);
		return result;
	}
	public void permuteUnique(int[] num,int start,ArrayList<ArrayList<Integer>> result)
	{
		if(start>=num.length)
		{
			ArrayList<Integer> item=convertArrayToList(num);
			result.add(item);
		}
		for(int j=start;j<num.length;j++)
		{
			if(!containsDuplicate(num,start,j))
			{
				swap(num,start,j);
				permuteUnique(num,start+1,result);
				swap(num,start,j);
			}
		}
	}
	public ArrayList<Integer> containsDuplicate(int[] arr,int start,int end)
	{
		for(int i=start;i<end;i++)
		{
			if(arr[i]==arr[end])
			{
				return true;
			}
		}
		return false;
	}
	public ArrayList<Integer> convertArrayToList(int[] num)
	{
		ArrayList<Integer> item=new ArrayList<Integer>();
		for(int i=0;i<num.length;i++)
		{
			item.add(num[i]);
		}
		return item;
	}
	public void swap(int[] a,int i,int j)
	{
		int temp=a[i];
		a[i]=a[j];
		a[j]=temp;
	}
	{% endhighlight %}

### [Add and Search Word - Data structure design](https://leetcode.com/problems/add-and-search-word-data-structure-design/) ###

Design a data structure that supports the following two operations:

	void addWord(word)
	bool search(word)

search(word) can search a literal word or a regular expression string containing only letters a-z or .. A . means it can represent any one letter.

For example:

	addWord("bad")
	addWord("dad")
	addWord("mad")
	search("pad") -> false
	search("bad") -> true
	search(".ad") -> true
	search("b..") -> true

Note:
You may assume that all words are consist of lowercase letters a-z.

	{% highlight java %}
	class TrieNode
	{
		public HashMap<Character,TrieNode> children;
		public boolean hasWord;
		public TrieNode()
		{
			children=new HashMap<Character,TrieNode>();
			hasWord=false;
		}
	}
	public class WordDictionary
	{
		private TrieNode root;
		public WordDictionary()
		{
			root=new TrieNode();
		}
		public void addWord(String word)
		{
			TrieNode now=root;
			for(int i=0;i<word.length();i++)
			{
				Character c=word.charAt(i);
				if(!now.children.containsKey(c))
				{
					now.children.put(c,new TrieNode());
				}
				now=now.children.get(c);
			}
			now.hasWord=true;
		}
		public boolean search(String word)
		{
			return find(word,0,root);
		}
		private boolean find(Sring word,int index,TrieNode now)
		{
			if(index==word.length())
			{
				if(now.children.size()==0)
				{
					return true;
				}
				else
				{
					return false;
				}
			}
			Character c=word.charAt(index);
			if(now.children.containsKey(c))
			{
				if(index==word.length()-1&&now.children.get(c).hasWord)
				{
					return true;
				}
				return find(word,index+1,now.children.get(c));
			}
			else if(c=='.')
			{
				boolean result=false;
				for(Map.entry<Character,TrieNode> child:now.children.entrySet())
				{
					if(index==word.length()-1&&child.getValue().hasWord)
					{
						return true;
					}
					if(find(word,index+1,child.getValue()))
					{
						result=true;
					}
				}
				return result;
			}
			else
			{
				return false;
			}
		}
	}
	{% endhighlight %}

### [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) ###

Given a string s, partition s such that every substring of the partition is a palindrome.

Return all possible palindrome partitioning of s.

For example, given s = "aab",

Return

	[
	  ["aa","b"],
	  ["a","a","b"]
	]

Subscribe to see which companies asked this question

	{% highlight java %}
	public ArrayList<ArrayList<String>> partition(String s)
	{
		ArrayList<ArrayList<String>> result=new ArrayList<ArrayList<String>>();
		if(s==null)
		{
			return result;
		}
		ArrayList<String> path=new ArrayList<String>();
		helper(s,path,0,result);
		return result;
	}
	private void helper(String s,ArrayList<String> path,int pos,
		ArrayList<ArrayList<String>> result)
	{
		if(pos==s.length())
		{
			result.add(new ArrayList<String>(path));
			return;
		}
		for(int i=pos;i<s.length();i++)
		{
			String prefix=s.substring(pos,i+1);
			if(!isPalindrome(prefix))
			{
				continue;
			}
			path.add(prefix);
			helper(s,path,i+1,result);
			path.remove(path.size()-1);
		}
	
	}
	private boolean isPalindrome(String s)
	{
		int begin=0;
		int end=s.length()-1;
		while(begin<end)
		{
			if(s.charAt(begin)!=s.charAt(end))
			{
				return false;
			}
			begin++;
			end--;
		}
		return true;
	}
	{% endhighlight %}

### [Combinations](https://leetcode.com/problems/combinations/) ###

Given two integers n and k, return all possible combinations of k numbers out of 1 ... n.

For example,
If n = 4 and k = 2, a solution is:

	[
	  [2,4],
	  [3,4],
	  [2,3],
	  [1,2],
	  [1,3],
	  [1,4],
	]

Subscribe to see which companies asked this question

	{% highlight java %}
	//solution 1
	public ArrayList<ArrayList<Integer>> combine(int n,int k)
	{
		ArrayList<ArrayList<Integer>> result=new ArrayList<ArrayList<Integer>>();
		if(n<=0||n<k)
		{
			return result;
		}
		ArrayList<Integer> item=new ArrayList<Integer>();
		dfs(n,k,1,item,result);
		return result;
	}
	public void dfs(int n,int k,int start,ArrayList<Integer> item,ArrayList<ArrayList<Integer>> res)
	{
		if(item.size()==k)
		{
			res.add(new ArrayList<Integer>(item));
			return;
		}
		for(int i=start;i<=n;i++)
		{
			item.add(i);
			dfs(n,k,i+1,item,res);
			item.remove(item.size()-1);
		}
	}
	{% endhighlight %}

### [Word Search II](https://leetcode.com/problems/word-search-ii/) ###

Given a 2D board and a list of words from the dictionary, find all words in the board.

Each word must be constructed from letters of sequentially adjacent cell, where "adjacent" cells are those horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.

For example,

Given words = ["oath","pea","eat","rain"] and board =

	[
	  ['o','a','a','n'],
	  ['e','t','a','e'],
	  ['i','h','k','r'],
	  ['i','f','l','v']
	]

Return ["eat","oath"].

Note:

You may assume that all inputs are consist of lowercase letters a-z.

	{% highlight java %}
	//solution1 DFS
	public List<String> findWords(char[][] bord,String[] words)
	{
		ArrayList<String> result=new ArrayList<String>();
		int m=bord.length;
		int n=bord[0].length;
		for(String word:words)
		{
			boolean flag=false;
			for(int i=0;i<m;i++)
			{
				for(int j=0;j<n;j++)
				{
					char[][] newBoard=new char[m][n];
					for(int x=0;x<m;x++)
					{
						for(int y=0;y<n;y++)
						{
							newBoard[x][y]=bord[x][y];
						}
						if(dfs(newBoard,word,i,j,0))
						{
							flag=true;
						}
					}
				}
			}
			if(flag)
			{
				result.add(word);
			}
		}
		return result;
	}
	public boolean dfs(char[][] board,String word,int i,int j,int k)
	{
		int m=board.length;
		int n=bord[0].length;
		if(i<0||j<0||i>=m||j>=n||k>word.length()-1)
		{
			return false;
		}
		if(bord[i][j]==word.charAt(k))
		{
			char temp=bord[i][j];
			bord[i][j]='#';
			if(k==word.length()-1)
			{
				return true;
			}
			else if(dfs(board,word,i-1,j,k+1)||
				dfs(board,word,i+1,j,k+1)||
				dfs(board,word,i,j-1,k+1)||
				dfs(board,word,i,j+1,k+1))
			{
				board[i][j]=temp
				return true;
			}
		}
		else
		{
			return false;
		}
		return false;
	}
	//solution2 DFS trie
	{% endhighlight %}

### [Word Break II](https://leetcode.com/problems/word-break-ii/) ###

Given a string s and a dictionary of words dict, add spaces in s to construct a sentence where each word is a valid dictionary word.

Return all such possible sentences.

For example, given

s = "catsanddog",

dict = ["cat", "cats", "and", "sand", "dog"].

A solution is ["cats and dog", "cat sand dog"].

### [N-Queens](https://leetcode.com/problems/n-queens/) ###

The n-queens puzzle is the problem of placing n queens on an n×n chessboard such that no two queens attack each other.

Given an integer n, return all distinct solutions to the n-queens puzzle.

Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space respectively.

For example,

There exist two distinct solutions to the 4-queens puzzle:

	[
	 [".Q..",  // Solution 1
	  "...Q",
	  "Q...",
	  "..Q."],
	
	 ["..Q.",  // Solution 2
	  "Q...",
	  "...Q",
	  ".Q.."]
	]

Subscribe to see which companies asked this question

	{% highlight java %}
	public ArrayList<String[]> solveNQueens(int n)
	{
		ArrayList<String[]> result=new ArrayList<String[]>();
		if(n<=0)
		{
			return result;
		}
		search(n,new ArrayList<Integer>(),result);
		return result;
	}
	public void search(int n,ArrayList<Integer> cols,ArrayList<String[]> result)
	{
		if(cols.size()==n)
		{
			String[] chessboard =new String[cols.size()];
			for(int i=0;i<cols.size();i++)
			{
				chessboard[i]="";
				for(int j=0;j<cols.size();j++)
				{
					if(j==cols.get(i))
					{
						chessboard[i]+="Q";
					}
					else
					{
						chessboard[i]+=".";
					}
				}
			}
			result.add(chessboard);
			return;
		}
		for(int col=0;col<n;col++)
		{
			if(!isValid(cols,col))
			{
				continue;
			}
			cols.add(col);
			search(n,cols,result);
			cols.remove(cols.size()-1);
		}
	}
	public boolean isValid(ArrayList<Integer> cols,int col)
	{
		int row=cols.size();
		for(int i=0;i<row;i++)
		{
			//same column
			if(cols.get(i)==col)
			{
				return false;
			}
			//left-top to right-bottom
			if(i-cols.get(i)==row-col)
			{
				return false;
			}
			//right-top to left-bottom
			if(i+cols.get(i)==row+col)
			{
				return false;
			}
		}
		return true;
	}
	{% endhighlight %}

### [N-Queens II](https://leetcode.com/problems/n-queens-ii/) ###

Follow up for N-Queens problem.

Now, instead outputting board configurations, return the total number of distinct solutions.

