---
date: 2016-11-3 12:15:30+00:00
layout: post
title: 《Cracking the coding interview》中数组和字符串小结
thread: 159
categories: algorithm 
tags: algorithm 

---

最近又做了下《Cracking the coding interview》中的题目，在这小结下，这篇小结下数组和字符串。

1. Implement an algorithm to determine if a string has all unique characters. What if you can not use additional data structures?


2. Write code to reverse a C-Style String. (C-String means that “abcd” is represented as five characters, including the null character.)


3. Design an algorithm and write code to remove the duplicate characters in a string without using any additional buffer. NOTE: One or two additional variables are fine. An extra copy of the array is not. FOLLOW UP Write the test cases for this method.


4. Write a method to decide if two strings are anagrams or not.


5. Write a method to replace all spaces in a string with ‘%20’.


6. Given an image represented by an NxN matrix, where each pixel in the image is 4 bytes, write a method to rotate the image by 90 degrees. Can you do this in place?


7. Write an algorithm such that if an element in an MxN matrix is 0, its entire row and column is set to 0.


8. Assume you have a method isSubstring which checks if one word is a substring of another. Given two strings, s1 and s2, write code to check if s2 is a rotation of s1 using only one call to isSubstring (i.e., “waterbottle” is a rotation of “erbottlewat”).


### 1. 判断字符串中的字符是否唯一 ###

Implement an algorithm to determine if a string has all unique characters. What if you can not use additional data structures? 


	{% highlight java %}
	public class StringIsUniqueChar
	{
		public static boolean isUniqueChars(String str)
		{
			boolean[] charArray = new boolean[256];
			for(int i = 0; i < str.length(); i++) 
			{
				int val = str.charAt(i);
				if(charArray[val])
				{
					return false;
				}
				charArray[val] = true;
			}
			return true;
		}
		//ASCII表上的数字0–31分配给了控制字符，用于控制像打印机等外围设备。
		//数字32–126分配给了能在键盘上找到的字符，数字127代表DELETE命令。
		public static boolean isUniqueChars2(String str)
		{
			int[] intArray = new int[8];
			for(int i = 0; i < str.length(); i++)
			{
				int val = str.charAt(i);
				int idx = val/32;
				int shift = val%32;
				if((intArray[idx] & (1<<shift)) != 0) 
				{
					return false;
				}
				intArray[idx] = (1<<shift);
			}
			return true;
		}
		public static void main(String[] args)
		{
			String s1 = "i am helloworld.";
		    String s2 = "abcdefghijklmnopqrstuvwxyzABCD1234567890";
		    System.out.println("s1: " + isUniqueChars(s1) + " : " + 
		    	isUniqueChars2(s1));
		    System.out.println("s2: " + isUniqueChars(s2) + " : " + 
		    	isUniqueChars2(s2));
		}
	}
	{% endhighlight %}


### 2. 翻转一个C分格的字符串 ###

Write code to reverse a C-Style String. (C-String means that “abcd” is represented as five characters, including the null character.)


	{% highlight java %}
	public class ReverseString
	{
		public static String ReverseStr(String str)
		{
			char[] strArray = str.toCharArray();
			int begin = 0;
			int end = strArray.length - 1;
			char temp;
			while(begin < end)
			{
				temp = strArray[begin];
				strArray[begin] = strArray[end];
				strArray[end] = temp;
				begin++;
				end--;
			}
			return new String(strArray);
		}
		public static void main(String[] args)
		{
		    String s = "abcdefghijklmnopqrstuvwxyzABCD1234567890";
		    System.out.println("ReverseStr s: " + ReverseStr(s) );
		}
	}
	{% endhighlight %}


### 3. 移除字符串中重复的字符 ###

Design an algorithm and write code to remove the duplicate characters in a string without using any additional buffer. NOTE: One or two additional variables are fine. An extra copy of the array is not.


	{% highlight java %}
	public class RemoveDuplicate
	{
		public static String remove(char[] strArray)
		{
			if(strArray == null || strArray.length < 2)
			{
				return "";
			}
			int len = strArray.length;
			int tail = 1;
			for(int i = 1; i < len; i++)
			{
				int j;
				for(j = 0; j < tail; j++)
				{
					if(strArray[j] == strArray[i])
					{
						break;
					}
				}
				if(j == tail)
				{
					strArray[tail] = strArray[i];
					tail++; 
				}
			}
			for(int i = tail; i < len; i++)
			{
				strArray[i] = 0;
			}
			return new String(strArray);
		}
		public static void main(String[] args)
		{
			String s = "iamhelloworld";
			System.out.println("RemoveDuplicate: " + remove(s.toCharArray()));
		}
	}
	{% endhighlight %}


### 4. 判断两个字符串是否是变位词  ###

Write a method to decide if two strings are anagrams or not.


	{% highlight java %}
	import java.util.Arrays;
	public class StringIsAnagram
	{
		public static String sortString(String s)
		{
			char[] chars = s.toCharArray();
			Arrays.sort(chars);
			String sortedStr = new String(chars);
			return sortedStr;
		}
		public static boolean isAnagram1(String s1, String s2)
		{
			return (sortString(s1)).equals(sortString(s2));
		}
		public static boolean isAnagram2(String s1, String s2)
		{
			if(s1 == null || s2 == null || s1.length() != s2.length())
			{
				return false;
			}
			int[] charCountArray = new int[256];
			for(int i = 0, len = s1.length(); i < len; i++)
			{
				charCountArray[s1.charAt(i)]++;
				charCountArray[s2.charAt(i)]--;
			}
			for(int i = 0; i < 256; i++)
			{
				if(charCountArray[i] != 0)
				{
					return false;
				}
			}
			return true;
		}
		public static void main(String[] args)
		{
			String s1 = "iamhelloworld";
			String s2 = "helloworldami";
			System.out.println("isAnagram1: " + isAnagram1(s1, s2));
			System.out.println("isAnagram2: " + isAnagram2(s1, s2));
		}
	}
	{% endhighlight %}


### 5. 把字符串中所有的空格替换为%20  ###

Write a method to replace all spaces in a string with ‘%20’.


	{% highlight java %}
	public class ReplaceSpace 
	{
		public static String replace(char[] chars)
		{
			int len = chars.length;
			int spaceCount = 0;
			int newLen;
			for(int i = 0; i< len; i++)
			{
				if(chars[i] == ' ')
				{
					spaceCount++;
				}
			}
			newLen = len + spaceCount*2;
			char[] newChars = new char[newLen];
			for(int i = 0; i < newLen; i++)
			{
				newChars[i] = '\0';
			}
			for(int i = len-1; i >= 0; i--)
			{
				if(chars[i] == ' ')
				{
					newChars[newLen-1] = '0';
					newChars[newLen-2] = '2';
					newChars[newLen-3] = '%';
					newLen = newLen-3;
				}
				else
				{
					newChars[newLen-1] = chars[i];
					newLen = newLen-1;
				}
			}
			return new String(newChars);
		}
		public static void main(String[] args)
		{
			String s = "i am hello world";
			char[] chars = s.toCharArray();
			System.out.println("ReplaceSpace: " + replace(chars));
		}
	}
	{% endhighlight %}


### 6. 一张图像表示成NxN的矩阵，图像中每个像素是4个字节，写一个函数把图像旋转90度。 ###

Given an image represented by an NxN matrix, where each pixel in the image is 4 bytes, write a method to rotate the image by 90 degrees. Can you do this in place?


	{% highlight java %}
	public class RotateMatrix
	{
		public static void rotate(int[][] matrix, int n)
		{
			for(int layer = 0; layer < n/2; ++layer)
			{
				int first = layer;
				int last = n-1-layer;
				for(int i = first; i< last; ++i)
				{
					int offset = i - fist;
					int top = matrix[first][i];
					//left->top
					matrix[first][i] = matrix[last-offset][first]; 
					//bottom->left
					matrix[last-offset][first] = matrix[last][last-offset];
					//right->bottom 
					matrix[last][last-offset] = matrix[i][last]; 
					matrix[i][last] = top; //top->right
				}
			}
		}
	}
	{% endhighlight %}


### 7. 处理一个MxN的矩阵，如果矩阵中某个元素为0，那么把它所在的行和列都置为0.  ###

Write an algorithm such that if an element in an MxN matrix is 0, its entire row and column is set to 0.


	{% highlight java %}
	public class SetMatrixZeros
	{
		public static void setZeros(int[][] matrix)
		{
			int[] row = new int[matrix.length];
			int[] column = new int[matrix[0].length];
			for(int i = 0; i< matrix.length; ++i)
			{
				for(int j = 0; j< matrix[0].length; ++j)
				{
					if(matrix[i][j] == 0)
					{
						row[i] = 1;
						column[j] = 1;
					}
				}
			}
			for(int i = 0; i< matrix.length; ++i)
			{
				for(int j = 0; j< matrix[0].length; ++j)
				{
					if(row[i] == 1 || column[j] == 1)
					{
						matrix[i][j] = 0;
					}
				}
			}
		}
	}
	{% endhighlight %}


### 8. 利用isSubstring函数检测一个字符串是否是另一个字符串的子串  ###

Assume you have a method isSubstring which checks if one word is a substring of another. Given two strings, s1 and s2, write code to check if s2 is a rotation of s1 using only one call to isSubstring ( i.e., “waterbottle” is a rotation of “erbottlewat”).


	{% highlight java %}
	public class CheckStringIsRotation
	{
		public static boolean check(String s1, String s2)
		{
			if(s1 == null || s2 == null || s1.length() != s2.length())
			{
				return false;
			}
			String s1s1 = s1 + s1;
			return isSubstring(s1s1, s2);
		}
	}
	{% endhighlight %}



C++版实现可参考： [Cracking the coding interview--问题与解答](http://www.hawstein.com/posts/ctci-solutions-contents.html)

