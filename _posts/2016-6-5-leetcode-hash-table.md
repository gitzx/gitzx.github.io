---
date: 2016-6-5 19:06:30+00:00
layout: post
title: Leetcode中Hash table题目小结
thread: 136
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中Hash table类部分的题目，目前已有的题目(除去之前已总结的)有：

1. Isomorphic Strings

2. Valid Sudoku

3. Intersection of Two Arrays

4. Intersection of Two Arrays II

5. Bulls and Cows

6. Word Pattern

7. Design Twitter

8. Top K Frequent Elements

9. Sudoku Solver


### [Isomorphic Strings](https://leetcode.com/problems/isomorphic-strings/) ###

Given two strings s and t, determine if they are isomorphic.

Two strings are isomorphic if the characters in s can be replaced to get t.

All occurrences of a character must be replaced with another character while preserving the order of characters. No two characters may map to the same character but a character may map to itself.

For example,

Given "egg", "add", return true.

Given "foo", "bar", return false.

Given "paper", "title", return true.

Note:

You may assume both s and t have the same length.

	{% highlight java %}
	public boolean isIsomorphic(String s,String t)
	{
		if(s==null || t==null)
		{
			return false;
		}
		if(s.length()!=t.length())
		{
			return false;
		}
		HashMap<Character,Character> map=new HashMap<Character,Character>();
		for(int i=0;i<s.length();i++)
		{
			char c1=s.charAt(i);
			char c2=t.charAt(i);
			if(map.containsKey(c1))
			{
				if(map.get(c1)!=c2)
				{
					return false;
				}
			}
			else
			{
				if(map.containsValue(c2))
				{
					return false;
				}
				map.put(c1,c2);
			}
		}
		return true;
	}
	{% endhighlight %}

### [Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) ###

Determine if a Sudoku is valid, according to: Sudoku Puzzles - The Rules.

The Sudoku board could be partially filled, where empty cells are filled with the character '.'.


A partially filled sudoku which is valid.

Note:

A valid Sudoku board (partially filled) is not necessarily solvable. Only the filled cells need to be validated.

### [Intersection of Two Arrays](https://leetcode.com/problems/intersection-of-two-arrays/) ###

Given two arrays, write a function to compute their intersection.

Example:

Given nums1 = [1, 2, 2, 1], nums2 = [2, 2], return [2].

Note:

Each element in the result must be unique.
The result can be in any order.

	{% highlight java %}
	//solution1 HashSet
	public int[] intersection(int[] nums1,int[] nums2)
	{
		HashSet<Integer> set1=new HashSet<Integer>();
		for(int i:nums1)
		{
			set1.add(i);
		}
		HashSet<Integer> set2=new HashSet<Integer>();
		for(int i:nums2)
		{
			set2.add(i);
		}
		Iterator<Integer> iter=set1.iterator();
		while(iter.hasNext())
		{
			int i=iter.next();
			if(!set2.contains(i))
			{
				iter.remove();
			}
		}
		int[] result=new int[set1.size()];
		int i=0;
		for(int x:set1)
		{
			result[i++]=x;
		}
		return result;
	}
	//solution2 Binary search
	public int[] intersection(int[] nums1, int[] nums2)
	{
		Arrays.sort(nums1);
		Arrays.sort(nums2);
		ArrayList<Integer> list=new ArrayList<Integer>();
		for(int i=0;i<nums.length;i++)
		{
			if(i=0||i>0&&nums1[i]!=nums1[i-1])
			{
				if(Arrays.binarySearch(nums2,nums1[i])>-1)
				{
					list.add(nums1[i]);
				}
			}
		}
		int[] result=new int[list.size()];
		int k=0;
		for(int i:list)
		{
			result[k++]=i;
		}
		return result;
	}
	{% endhighlight %}

### [Intersection of Two Arrays II](https://leetcode.com/problems/intersection-of-two-arrays-ii/) ###

Given two arrays, write a function to compute their intersection.

Example:
Given nums1 = [1, 2, 2, 1], nums2 = [2, 2], return [2, 2].

Note:

Each element in the result should appear as many times as it shows in both arrays.

The result can be in any order.

Follow up:

What if the given array is already sorted? How would you optimize your algorithm?

What if nums1's size is small compared to nums2's size? Which algorithm is better?

What if elements of nums2 are stored on disk, and the memory is limited such that you cannot load all elements into the memory at once?

	{% highlight java %}
	//solution1 hashmap
	public int[] intersect(int[] nums1,int[] nums2)
	{
		HashMap<Integer,Integer> map=new HashMap<Integer,Integer>();
		for(int i:nums1)
		{
			if(map.containsKey(i))
			{
				map.put(i,map.get(i)+1);
			}
			else 
			{
				map.put(i,1);
			}
		}
		ArrayList<Integer> list=new ArrayList<Integer>();
		for(int i:nums2)
		{
			if(map.containsKey(i))
			{
				if(map.get(i)>1)
				{
					map.put(i,map.get(i)-1);
				}
				else 
				{
					map.remove(i);
				}
				list.add(i);
			}
		}
		int[] result=new int[list.size()];
		int i=0;
		while(i<list.size())
		{
			result[i]=list.get(i);
			i++;
		}
		return result;
	}
	
	//solution2 two points
	public int[] intersect(int[] nums1,int[] nums2)
	{
		Arrays.sort(nums1);
		Arrays.sort(nums2);
		ArrayList<Integer> list=new ArrayList<Integer>();
		int p1=0,p2=0;
		while(p1<nums1.length&&p2<nums2.length)
		{
			if(nums1[p1]<nums2[p2])
			{
				p1++;
			}
			else if(nums1[p1]>nums2[p2])
			{
				p2++;
			}
			else 
			{
				list.add(nums1[p1]);
				p1++;
				p2++;
			}
		}
		int[] result=new int[list.size()];
		int i=0;
		while(i<list.size())
		{
			result[i]=list.get(i);
			i++;
		}
		return result;
	}
	{% endhighlight %}

### [Bulls and Cows](https://leetcode.com/problems/bulls-and-cows/) ###

You are playing the following Bulls and Cows game with your friend: You write down a number and ask your friend to guess what the number is. Each time your friend makes a guess, you provide a hint that indicates how many digits in said guess match your secret number exactly in both digit and position (called "bulls") and how many digits match the secret number but locate in the wrong position (called "cows"). Your friend will use successive guesses and hints to eventually derive the secret number.

For example:

	Secret number:  "1807"
	Friend's guess: "7810"

Hint: 1 bull and 3 cows. (The bull is 8, the cows are 0, 1 and 7.)

Write a function to return a hint according to the secret number and friend's guess, use A to indicate the bulls and B to indicate the cows. In the above example, your function should return "1A3B".

Please note that both secret number and friend's guess may contain duplicate digits, for example:

	Secret number:  "1123"
	Friend's guess: "0111"

In this case, the 1st 1 in friend's guess is a bull, the 2nd or 3rd 1 is a cow, and your function should return "1A1B".

You may assume that the secret number and your friend's guess only contain digits, and their lengths are always equal.

	{% highlight java %}
	//solution1 Array
	public String getHint(String secret,String guess)
	{
		int countBull=0;
		int countCow=0;
		int[] arr1=new int[10];
		int[] arr2=new int[10];
		for(int i=0;i<secret.length();i++)
		{
			char c1=secret.charAt(i);
			char c2=guess.charAt(i);
			if(c1==c2)
			{
				countBull++;
			}
			else
			{
				arr1[c1-'0']++;
				arr2[c2-'0']++;
			}
		}
		for(int i=0;i<10;i++)
		{
			countCow+=Math.min(arr1[i],arr2[i]);
		}
		return countBull+"A"+countCow+"B";
	}
	
	//solution2 HashMap
	public String getHint(String secret,String guess)
	{
		int countBull=0;
		int countCow=0;
		HashMap<Integer,Integer> map=new HashMap<Integer,Integer>();
		for(int i=0;i<secret.length();i++)
		{
			char c1=secret.charAt(i);
			char c2=guess.charAt(i);
			if(c1==c2)
			{
				countBull++;
			}
			else
			{
				if(map.countsKey(c1))
				{
					map.put(c1,map.get(c1)+1);
				}
				else
				{
					map.put(c1,1);
				}
			}
		}
		for(int i=0;i<secret.length();i++)
		{
			char c1=secret.charAt(i);
			char c2=guess.charAt(i);
			if(c1!=c2)
			{
				if(map.containsKey(c2))
				{
					countCow++;
					if(map.get(c2)==1)
					{
						map.remove(c2);
					}
					else
					{
						map.put(c2,map.get(c2)-1);
					}
				}
			}
		}
		return countBull+"A"+countBull+"B";
	}
	{% endhighlight %}

### [Word Pattern](https://leetcode.com/problems/word-pattern/) ###

Given a pattern and a string str, find if str follows the same pattern.

Here follow means a full match, such that there is a bijection between a letter in pattern and a non-empty word in str.

Examples:

1. pattern = "abba", str = "dog cat cat dog" should return true.

2. pattern = "abba", str = "dog cat cat fish" should return false.

3. pattern = "aaaa", str = "dog cat cat dog" should return false.

4. pattern = "abba", str = "dog dog dog dog" should return false.

Notes:

You may assume pattern contains only lowercase letters, and str contains lowercase letters separated by a single space.

	{% highlight java %}
	public boolean wordPattern(String pattern,String str)
	{
		String[] arr=str.split(" ");
		if(pattern.length()!=arr.length)
		{
			return false;
		}
		HashMap<Character,String> map=new HashMap<Character,String>();
		for(int i=0;i<arr.length;i++)
		{
			char c=pattern.charAt(i);
			String s=arr[i];
			if(map.containsKey(c))
			{
				if(!map.get(c).equals(s))
				{
					return false;
				}
			}
			else 
			{
				if(map.containsValue(s))
				{
					return false;
				}
				map.put(c,s);
			}
		}
		return true;
	}
	{% endhighlight %}

### [Design Twitter](https://leetcode.com/problems/design-twitter/) ###

Design a simplified version of Twitter where users can post tweets, follow/unfollow another user and is able to see the 10 most recent tweets in the user's news feed. Your design should support the following methods:

1. postTweet(userId, tweetId): Compose a new tweet.

2. getNewsFeed(userId): Retrieve the 10 most recent tweet ids in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user herself. Tweets must be ordered from most recent to least recent.

3. follow(followerId, followeeId): Follower follows a followee.

4. unfollow(followerId, followeeId): Follower unfollows a followee.

Example:

	Twitter twitter = new Twitter();
	
	// User 1 posts a new tweet (id = 5).
	twitter.postTweet(1, 5);
	
	// User 1's news feed should return a list with 1 tweet id -> [5].
	twitter.getNewsFeed(1);
	
	// User 1 follows user 2.
	twitter.follow(1, 2);
	
	// User 2 posts a new tweet (id = 6).
	twitter.postTweet(2, 6);
	
	// User 1's news feed should return a list with 2 tweet ids -> [6, 5].
	// Tweet id 6 should precede tweet id 5 because it is posted after tweet id 5.
	twitter.getNewsFeed(1);
	
	// User 1 unfollows user 2.
	twitter.unfollow(1, 2);
	
	// User 1's news feed should return a list with 1 tweet id -> [5],
	// since user 1 is no longer following user 2.
	twitter.getNewsFeed(1);

Subscribe to see which companies asked this question

	{% highlight java %}
	public class Twitter
	{
		class Tweet
		{
			int time;
			int id;
			Tweet(int time,int id)
			{
				this.time=time;
				this.id=id;
			}
		}
		Map<Integer,Set<Integer>> fans=new HasMap<>();
		Map<Integer,LinkedList<Integer>> tweets=new HasMap<>();
		int cnt=0;
		public void postTweet(int userId,int tweetId)
		{
			if(!fans.containsKey(userId))
			{
				fans.put(userId,new HashSet<>());
			}
			fans.get(userId).add(userId);
			if(!tweets.containsKey(userId))
			{
				tweets.put(userId,new LinkedList<>());
			}
			tweets.get(userId).addFirst(new Tweet(cnt++,tweetId));
		}
		public List<Integer> getNewsFeed(int userId)
		{
			if(!fans.containsKey(userId))
			{
				return new LinkedList<>();
			}
			PriorityQueue<Tweet> feed=new PriorityQueue<>((t1,t2)->t2.time-t1.time);
			fans.get(userId).forEach(f->tweets.get(f).forEach(feed::add));
			List<Integer> res=new LinkedList<>();
			while(feed.size()>0&&res.size()<10)
			{
				res.add(feed.poll.id);
			}
			return res;
		}
		public void follow(int followerId,int followeeId)
		{
			if(!fans.containsKey(followerId))
			{
				fans.put(followerId,new HashSet<>());
			}
			fans.get(followerId).add(followeeId);;
		}
		public void unfollow(int followerId,int followeeId)
		{
			if(fans.containsKey(followerId)&&followeeId!=followerId)
			{
				fans.get(followerId).remove(followeeId);
			}
		}
	}
	{% endhighlight %}

### [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) ###

Given a non-empty array of integers, return the k most frequent elements.

For example,

Given [1,1,1,2,2,3] and k = 2, return [1,2].

Note: 

You may assume k is always valid, 1 ≤ k ≤ number of unique elements.

Your algorithm's time complexity must be better than O(n log n), where n is the array's size.

	{% highlight java %}
	class Pair
	{
		int num;
		int count;
		public Pair(int num,int count)
		{
			this.num=num;
			this.count=count;
		}
	}
	public class Solution
	{
		public List<Integer> topKFrequent(int[] nums,int k)
		{
			HashMap<Integer,Integer> map=new HashMap<Integer,Integer>();
			for(int num:nums)
			{
				if(map.containsKey(num))
				{
					map.put(num,map.get(num)_1);
				}
				else
				{
					map.put(num,1);
				}
			}
			PriorityQueue<Pair> queue=new PriorityQueue<Pair>(
				new Comparator<Pair>(){
					public int compare(Pair a,Pair b)
					{
						return a.count-b.count;
					}
			});
			for(map.Entry<Integer,Integer> entry:map.entrySet())
			{
				Pair p=new Pair(entry.getKey(),entry.getValue());
				queue.offer(p);
				if(queue.size()>k)
				{
					queue.poll();
				}
			}
			List<Integer> result=new ArrayList<Integer>();
			while(queue.size()>0)
			{
				result.add(queue.poll().num);
			}
			Conllections.reverse(result);
			return result;
		}
	}
	{% endhighlight %}

### [Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) ###


Write a program to solve a Sudoku puzzle by filling the empty cells.

Empty cells are indicated by the character '.'.

You may assume that there will be only one unique solution.


A sudoku puzzle...


...and its solution numbers marked in red.

Subscribe to see which companies asked this question
