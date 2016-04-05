---
date: 2016-3-27 18:06:30+00:00
layout: post
title: Leetcode中字符串类题目小结(Easy部分)
thread: 121
categories: algorithm
tags: algorithm
---

这篇小结下Leetcode中String的Easy部分的题型，目前已有的题目有：

1. Longest Common Prefix

2. Add Binary

3. Valid Palindrome

4. Compare Version Numbers

5. Count and Say

6. Length of Last Word

7. Valid Parentheses

8. ZigZag Conversion

9. String to Integer (atoi)

10. Implement strStr()

11. Roman to Integer


### [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) ###

Write a function to find the longest common prefix string amongst an array of strings.

	{% highlight java %}
	public String longestCommonPrefix(String[] strs)
	{
		if(strs == null || strs.length == 0)
		{
			return n;
		}
		String minStr = strs[0];
		for(int i=0;i<strs.length;i++)
		{
			if(strs[i].length()<minStr.length())
			{
				minStr = strs[i];
			}
		}
		int minLength = minStr.length();
		for(int i = 0;i<strs.length;i++)
		{
			int j;
			for(j=0;j<minLength;j++)
			{
				if(minStr.charAt(j) != strs[i].charAt(j))
				{
					break;
				}
			}
			if(j<minLength)
			{
				minLength = j;
			}
		}
		return minStr.subString(0, minLength);
	}
	{% endhighlight %}

### [Add Binary](https://leetcode.com/problems/add-binary/) ###

Given two binary strings, return their sum (also a binary string).

For example,
a = "11"
b = "1"
Return "100".

	{% highlight java %}
	//add Binary
	public String addBinary(String a, String b)
	{
		if(a==null ||a.length()==0)
		{
			return b;
		}
		if(b==null ||b.length()==0)
		{
			return a;
		}
		int pa = a.length()-1;
		int pb = b.length()-1;
		int flag = 0;
		StringBuilder sb = new StringBuilder();
		while(pa>=0 || pb>=0)
		{
			int va = 0;
			int vb = 0;
			if(pa>=0)
			{
				va=a.charAt(pa)=='0'?0:1;
				pa--;
			}
			if(pb>=0)
			{
				vb = b.charAt(pb)=='0'?0:1;
				pb--;
			}
			int sum = va+vb+flag;
			if(sum>=2)
			{
				sb.append(String.valueOf(sum-2));
				flag =1;
			}
			else
			{
				sb.append(string.valueOf(sum));
				flag=0;
			}
		}
		if(flag ==1)
		{
			sb.append("1");
		}
		String reversed = sb.reverse().toString();
		return reversed;
	}
	{% endhighlight %}

### [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) ###

Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.

For example,
"A man, a plan, a canal: Panama" is a palindrome.
"race a car" is not a palindrome.

Note:
Have you consider that the string might be empty? This is a good question to ask during an interview.

For the purpose of this problem, we define empty string as valid palindrome.

	{% highlight java %}
	public bool validPalindrome(String str)
	{
		int start = 0;
		int end = str.length()-1;
		while(start < end)
		{
			if(!isAlnum(str[start]))
			{
				start++;
			}
			else if(!isAlnum(str[end]))
			{
				end--;
			}
			else if(toLower(str[start++]) != toLower(str[end--]))
			{
				return false;
			}
		}
		return true;
	}
	{% endhighlight %}

### [Compare Version Numbers](https://leetcode.com/problems/compare-version-numbers/) ###

Compare two version numbers version1 and version2.
If version1 > version2 return 1, if version1 < version2 return -1, otherwise return 0.

You may assume that the version strings are non-empty and contain only digits and the . character.
The . character does not represent a decimal point and is used to separate number sequences.
For instance, 2.5 is not "two and a half" or "half way to version three", it is the fifth second-level revision of the second first-level revision.

Here is an example of version numbers ordering:

0.1 < 1.1 < 1.2 < 13.37

	{% highlight java %}
	public int compareVersionNumbers(String version1, String version2)
	{
		String[] s1 = version1.splite("\\.");
		String[] s2 = version2.splite("\\.");
		int length = max(s1.length, s2.length);
		for(int i=0;i<length;i++)
		{
			Integer v1 = i<s1.length?Integer.parseInt(s1[i]):0;
			Integer v2 = i<s2.length?Integer.parseInt(s2[i]):0;
			int compare = v1.copareTo(v2);
			if(compare != 0)
			{
				return compare;
			}
		}
		return 0;
	}
	{% endhighlight %}

### [Count and Say](https://leetcode.com/problems/count-and-say/) ###

The count-and-say sequence is the sequence of integers beginning as follows:
1, 11, 21, 1211, 111221, ...

1 is read off as "one 1" or 11.
11 is read off as "two 1s" or 21.
21 is read off as "one 2, then one 1" or 1211.
Given an integer n, generate the nth sequence.

Note: The sequence of integers will be represented as a string.

	{% highlight java %}
	public String countAndSay(int n)
	{
		if(n<0)
		{
			return null;
		}
		String result = "1";
		int i = 1;
		while(i<n)
		{
			StringBuilder sb = new StringBuilder();
			int count = 1;
			for(int j=1;j<result.length();j++)
			{
				if(result.charAt(j) == result.charAt(j-1))
				{
					count++;
				}
				else 
				{
					sb.append(count);
					sb.append(result.charAt(j-1));
					count=1;
				}
			}
			sb.append(count);
			sb.append(result.charAt(result.length()-1));
			result=sb.toString();
			i++;
		}
		return result;
	}
	{% endhighlight %}

### [Length of Last Word](https://leetcode.com/problems/length-of-last-word/) ###

Given a string s consists of upper/lower-case alphabets and empty space characters ' ', return the length of last word in the string.

If the last word does not exist, return 0.

Note: A word is defined as a character sequence consists of non-space characters only.

For example, 
Given s = "Hello World",
return 5.

	{% highlight java %}
	//Solution 1
	public int lengthOfLastWord(String s)
	{
		return s.trim().length()-s.trim().lastIndexOf(" ")-1;
	}
	//Solution 2
	public int lengthOfLastWord(String s)
	{
		int len = 0;
		int tail = s.length()-1;
		while(tail>=0 && s[tail] == ' ')
		{
			tail--;
		}
		while(tail>=0 && s[tail] != ' ')
		{
			len++;
			tail--;
		}
		return len;
	}
	//Solution 3
	public int lengthOfLastWord(String s)
	{
		if(s==null || s.length()==0)
		{
			return 0;
		}
		int len = 0;
		bool flag = false;
		for(int i=s.length()-1;i>=0;i--)
		{
			char c = s.charAt(i);
			if((c>='a'&&c<='z')||(c>='A'&&c<='Z'))
			{
				len++;
				flag= true;
			}
			else 
			{
				if(flag)
				{
					return len;
				}
			}
		}
		return len;
	}
	{% endhighlight %}


### [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) ###

Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

The brackets must close in the correct order, "()" and "()[]{}" are all valid but "(]" and "([)]" are not.

	{% highlight java %}
	//Solution 1
	public bool validParentheses(String s)
	{
		int len = 0;
		do
		{
			len = s.length();
			s = s.replace("()", "").replace("[]", "").replace("{}", "");
		}
		while(len != s.length());
		return s.length()==0;
	}
	//Solution 2
	public bool validParentheses(String s)
	{
		Stack<Character> stack = new Stack<Character>();
		for(int i=0;i<s.length();i++)
		{
			if(s.charAt(i)=='(' || s.charAt(i)=='['||s.charAt(i)=='{')
			{
				stack.push(s.charAt(i));
			}
			else if(s.charAt(i)==')'&&!stack.empty()&&stack.peek()=='(')
			{
				stack.pop();
			}
			else if(s.charAt(i)==']'&&!stack.empty()&&stack.peek()=='[')
			{
				stack.pop();
			}
			else if(s.charAt(i)=='}'&&!stack.empty()&&stack.peek()=='{')
			{
				stack.pop();
			}
			else
			{
				return false;
			}
		}
		return stack.empty();
	}
	{% endhighlight %}


### [ZigZag Conversion](https://leetcode.com/problems/zigzag-conversion/) ###

The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)

P   A   H   N
A P L S I I G
Y   I   R
And then read line by line: "PAHNAPLSIIGYIR"
Write the code that will take a string and make this conversion given a number of rows:

string convert(string text, int nRows);
convert("PAYPALISHIRING", 3) should return "PAHNAPLSIIGYIR".


### [String to Integer (atoi)](https://leetcode.com/problems/string-to-integer-atoi/) ###

Implement atoi to convert a string to an integer.

Hint: Carefully consider all possible input cases. If you want a challenge, please do not see below and ask yourself what are the possible input cases.

Notes: It is intended for this problem to be specified vaguely (ie, no given input specs). You are responsible to gather all the input requirements up front.

Update (2015-02-10):
The signature of the C++ function had been updated. If you still see your function signature accepts a const char * argument, please click the reload button  to reset your code definition.

	{% highlight java %}
	publit int atoi(String s)
	{
		int index = 0, sign = 1, total = 0;
		if(s.length()==0)
		{
			return 0;
		}
		while(s.charAt(index)==' '&&index<s.length())
		{
			index++;
		}
		if(s.charAt(index)=='+' ||s.charAt(index)=='-')
		{
			sign=s.charAt(index)=='+'?1:-1;
			index++;
		}
		while(index<s.length())
		{
			int digit= s.charAt(index)-'0';
			if(digit<0 || digit>9)
			{
				break;
			}
			if(Integer.MAX_VALUE/10<total ||Integer.MAX_VALUE/10==total
				&&Integer.MAX_VALUE%10<digit)
			{
				return sign==1?Integer.MAX_VALUE:Integer.MIN_VALUE;
			}
			total = 10*total+digit;
			index++;
		}
		return total*sign;
	}
	{% endhighlight %}

### [Implement strStr()](https://leetcode.com/problems/implement-strstr/) ###

Implement strStr().

Returns the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack.

	{% highlight java %}
	//Solution 1
	public int strStr(String str1, String str2)
	{
		int m= str1.length();
		int n = str2.length();
		int len = m-n;
		if(len<0)
		{
			return -1;
		}
		else if(n==0)
		{
			return 0;
		}
		for(int i=0;i<=len;i++)
		{
			if(str1.subString(i,i+n).equals(str2))
			{
				return i;
			}
		}
		return -1;
	}
	//Solution 2
	public int strStr(String str1, String str2)
	{
		int m=str1.length();
		int n= str2.length();
		int len = m-n;
		if(len<0)
		{
			return -1;
		}
		else if(n==0)
		{
			return 0;
		}
		for(int i=0;i<=len;i++)
		{
			int j=0;
			for(;j<n;j++)
			{
				if(str1[i+j]!=str2[j])
				{
					break;
				}
			}
			if(j==n)
			{
				return i;
			}
		}
		return -1;
	}
	{% endhighlight %}

### [Roman to Integer](https://leetcode.com/problems/roman-to-integer/) ###

Given a roman numeral, convert it to an integer.

Input is guaranteed to be within the range from 1 to 3999.

	{% highlight java %}
	//Solution 1
	public int romanToInt(String s)
	{
		if(s==null||s.length()==0)
		{
			return 0;
		}
		int len = s.length();
		HashMap<Character,Integer> map=new HashMap<Character,Integer>();
		map.put('I',1);
		map.put('V',5);
		map.put('X',10);
		map.put('L',50);
		map.put('C',100);
		map.put('D',500);
		map.put('M',1000);
		int result = map.get(s.charAt(len-1));
		int pivot = result;
		for(int i=len-2;i>=0;i--)
		{
			int curr=map.get(s.charAt(i));
			if(curr>=pivot)
			{
				result+=curr;
			}
			else
			{
				result-=curr;
			}
			pivot = curr;
		}
		return result;
	}
	//Solution 2
	public int romanToInt(String s)
	{
		int sum = 0;
		if(s.indexOf("IV")!=-1){sum-=2}
		if(s.indexOf("IX")!=-1){sum-=2}
		if(s.indexOf("XL")!=-1){sum-=20}	
		if(s.indexOf("XC")!=-1){sum-=20}
		if(s.indexOf("CD")!=-1){sum-=200}
		if(s.indexOf("CM")!=-1){sum-=200}
		char c[] = s.toCharArray();
		int count = 0;
		for(;count<=s.length()-1;count++)
		{
			if(c[count]=='M'){sum+=1000}
			if(c[count]=='D'){sum+=500}
			if(c[count]=='C'){sum+=100}
			if(c[count]=='L'){sum+=50}
			if(c[count]=='X'){sum+=10}
			if(c[count]=='V'){sum+=5}
			if(c[count]=='I'){sum+=1}
		}
		return sum;
	}
	{% endhighlight %}
