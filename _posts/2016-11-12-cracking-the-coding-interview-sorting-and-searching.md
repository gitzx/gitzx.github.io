---
date: 2016-11-12 18:23:30+00:00
layout: post
title: 《Cracking the coding interview》中排序搜索小结
thread: 162
categories: algorithm 
tags: algorithm 

---

这篇小结下《Cracking the coding interview》中的排序和搜索题目。

1. You are given two sorted arrays, A and B, and A has a large enough buffer at the end to hold B. Write a method to merge B into A in sorted order.

2. Write a method to sort an array of strings so that all the anagrams are next to each other.

3. Given a sorted array of n integers that has been rotated an unknown number of times, give an O(log n) algorithm that finds an element in the array. You may assume that the array was originally sorted in increasing order. EXAMPLE: Input: find 5 in array (15 16 19 20 25 1 3 4 5 7 10 14) Output: 8 (the index of 5 in the array)

4. If you have a 2 GB file with one string per line, which sorting algorithm would you use to sort the file and why?

5. Given a sorted array of strings which is interspersed with empty strings, write a method to find the location of a given string. Example: find “ball” in [“at”, “”, “”, “”, “ball”, “”, “”, “car”, “”, “”, “dad”, “”, “”] will return 4 Example: find “ballcar” in [“at”, “”, “”, “”, “”, “ball”, “car”, “”, “”, “dad”, “”, “”] will return -1

6. Given a matrix in which each row and each column is sorted, write a method to find an element in it.

7. A circus is designing a tower routine consisting of people standing atop one another’s shoulders. For practical and aesthetic reasons, each person must be both shorter and lighter than the person below him or her. Given the heights and weights of each person in the circus, write a method to compute the largest possible number of people in such a tower. EXAMPLE: Input (ht, wt): (65, 100) (70, 150) (56, 90) (75, 190) (60, 95) (68, 110) Output: The longest tower is length 6 and includes from top to bottom: (56, 90) (60,95) (65,100) (68,110) (70,150) (75,190)


### 1. 将数组B融入数组A，并使其有序 ###

You are given two sorted arrays, A and B, and A has a large enough buffer at the end to hold B. Write a method to merge B into A in sorted order.

	{% highlight java %}
	public class MergeArrays
	{
		public static void merge(int[] a, int[] b, int m, int n)
		{
			int k = m + n -1;
			int i = m - 1; 
			int j = n - 1; 
			while(i >= 0 && j >= 0)
			{
				if(a[i] > b[j])
				{
					a[k--] = a[i--];
				}
				else
				{
					a[k--] = b[j--];
				}
			}
			while(i >= 0)
			{
				a[k--] = a[i--];
			}
		}
	}
	{% endhighlight %}


### 2. 对字符串数组排序，使得所有的变位词都相邻 ###

Write a method to sort an array of strings so that all the anagrams are next to each other.

	{% highlight java %}
	public class SortArrayOfStrings
	{
		public static sortArray(String[] array)
		{
			Arrays.sort(array, new AnagramComparator());
		}
	}
	public class AnagramComparator implements Comparator<String>
	{
		public String sortChars(String s)
		{
			char[] content = s.toCharArray();
			Arrays.sort(content);
			return new String(content);
		}
		public int compare(String s1, String s2)
		{
			return sortChars(s1).copareTo(sortChars(s2));
		}
	}
	{% endhighlight %}


### 3. 一个数组有n个整数，它们排好序(假设为升序)但被旋转了未知次， 即每次把最右边的数放到最左边。给出一个O(log n)的算法找到特定的某个元素。 ###

Given a sorted array of n integers that has been rotated an unknown number of times, give an O(log n) algorithm that finds an element in the array. You may assume that the array was originally sorted in increasing order.

EXAMPLE:

Input: find 5 in array (15 16 19 20 25 1 3 4 5 7 10 14)

Output: 8 (the index of 5 in the array)

	{% highlight java %}
	public class SortRotatedString
	{
		public static int search(int a[],int l,int u, int x)
		{
			while(l<=u)
			{
				int m = (l+u)/2;
				if(x==a[m])
				{
					return m;
				}
				else if(a[l]<=a[m])
				{
					if(x>a[m])
					{
						l = m+1;
					}
					else if(x >=a[l])
					{
						u=m-1;
					}
					else
					{
						l=m+1;
					}
				}
				else if(x<a[m])
				{
					u = m-1;
				}
				else if(x<=a[u]) 
				{
					l = m+1;
				}
				else
				{
					u = m-1;
				}
			}
			return -1;
		}
		public static int search(int a[], int x)
		{
			return search(a,0, a.length-1, x);
		}
	}
	{% endhighlight %}
	

### 4. 如果你有个2GB的文件，其中每一行是一个字符串，你会使用哪种算法来排序，为什么？ ###

If you have a 2 GB file with one string per line, which sorting algorithm would you use to sort the file and why?


### 5. 给你一个排好序的并且穿插有空字符串的字符串数组，写一个函数找到给定字符串的位置。 ###

Given a sorted array of strings which is interspersed with empty strings, write a method to find the location of a given string.

Example: find “ball” in [“at”, “”, “”, “”, “ball”, “”, “”, “car”, “”,“”, “dad”, “”, “”] will return 4

Example: find “ballcar” in [“at”, “”, “”, “”, “”, “ball”, “car”, “”, “”, “dad”, “”, “”] will return -1

	{% highlight java %}
		public class SearchStringInArray
		{
			public static int search(String[] strings, String str,int first, int last)
			{
				while(first <= last)
				{
					while(first <= last && strings[last] == "")
					{
						--last;
					}
					if(last < first)
					{
						return -1;
					}
					int mid = (first + last)>>1;
					while(strings[mid] == "")
					{
						++mid;
					}
					int r = strings[mid].compareTo(str);
					if(r== 0)
					{
						return mid;
					}
					if(r < 0)
					{
						first = mid + 1;
					}
					else
					{
						last = mid -1;
					}
					return -1;
				}
			}
		}
		{% endhighlight %}

### 6. 给出一个矩阵，其中每一行和每一列都是有序的，写一个函数在矩阵中找出指定的数 ###

Given a matrix in which each row and each column is sorted, write a method to find an element in it.

	{% highlight java %}
	public class SearchElementInMatrix
	{
		public static boolean findElement(int[][] mat, int elem, int m, int n)
		{
			int row = 0;
			int col = n -1;
			while(row < m && col >= 0)
			{
				if(mat[row][col] == elem)
				{
					return true;
				}
				else if(mat[row][col] > elem)
				{
					col--;
				}
				else 
				{
					row++;
				}
			}
			return false;
		}
	}
	{% endhighlight %}


C++版实现可参考： [Cracking the coding interview--问题与解答](http://www.hawstein.com/posts/ctci-solutions-contents.html)

