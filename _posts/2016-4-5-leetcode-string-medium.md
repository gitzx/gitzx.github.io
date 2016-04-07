---
date: 2016-4-5 12:29:30+00:00
layout: post
title: Leetcode中字符串类题目小结(Medium部分)
thread: 122
categories: algorithm
tags: algorithm
---

这篇小结下Leetcode中String的Medium部分的题型，目前已有的题目有：

1. Restore IP Addresses

2. Group Anagrams

3. Basic Calculator II

4. Decode Ways

5. Longest Substring Without Repeating Characters

6. Longest Palindromic Substring

7. Letter Combinations of a Phone Number

8. Simplify Path

9. Integer to Roman

10. Multiply Strings

11. Generate Parentheses

12. Reverse Words in a String


### [Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/) ###

Given a string containing only digits, restore it by returning all possible valid IP address combinations.

For example:
Given "25525511135",

return ["255.255.11.135", "255.255.111.35"]. (Order does not matter)

	{% highlight java %}
	public Lit<String> restoreIpAddresses(String s)
	{
		ArrayList<ArrayList<String>> result=new ArrayList<ArrayList<String>>();
		ArrayList<String> list=new ArrayList<String>();
		dfs(result,s,0,list);
		ArrayList<String> finalResult=new ArrayList<String>();
		for(ArrayList<String> arrayList:result)
		{
			StringBuilder sb=new StringBuilder();
			for(String str:arrayList)
			{
				sb.append(str+".");
			}
			sb.setLength(sb.length()-1);
			finalResult.add(sb.toString());
		}
	}
	public void dfs(ArrayList<ArrayList<String>> result,String s,int start,ArrayList<String> t)
	{
		if(t.size()>=4&&start!=s.length)
		{
			return;
		}
		if((t.size()+s.length()-start+1)<4)
		{
			return;
		}
		if(t.size()==4&&start==s.length())
		{
			ArrayList<String> temp = new ArrayList<String>(t);
			result.add(temp);
			return;
		}
		for(int i=1;i<4;i++)
		{
			if(start+i>s.length())
			{
				break;
			}
			String sub=s.subString(start,start+i);
			if(i>1&&s.charAt(start)=='0')
			{
				break;
			}
			if(Integer.valueOf(sub)>255)
			{
				break;
			}
			t.add(sub);
			dfs(result,s,start+i,t);
			t.remove(t.size()-1);
		}
	}
	{% endhighlight %}

### [Group Anagrams](https://leetcode.com/problems/anagrams/) ###

Given an array of strings, group anagrams together.

For example, given: ["eat", "tea", "tan", "ate", "nat", "bat"], 
Return:

[
  ["ate", "eat","tea"],
  ["nat","tan"],
  ["bat"]
]
Note:
For the return value, each inner list's elements must follow the lexicographic order.
All inputs will be in lower-case.

	{% highlight java %}
	public List<List<String>> groupAnagrams(String[] strs)
	{
		if(strs==null||strs.length==0)
		{
			return new ArrayList<List<String>>();
		}
		Map<String,List<String>> map=new HashMap<String,List<String>>();
		for(String s:strs)
		{
			char[] ca=s.toCharArray();
			Arrays.sort(ca);
			String keyStr=String.valueOf(ca);
			if(!map.containsKey(keyStr))
			{
				map.put(keyStr,new ArrayList<String>());
			}
			map.get(keyStr).add(s);
		}
		return new ArrayList<List<String>>(map.values());
	}
	{% endhighlight %}


### [Basic Calculator II](https://leetcode.com/problems/basic-calculator-ii/) ###

Implement a basic calculator to evaluate a simple expression string.

The expression string contains only non-negative integers, +, -, *, / operators and empty spaces . The integer division should truncate toward zero.

You may assume that the given expression is always valid.

Some examples:
"3+2*2" = 7
" 3/2 " = 1
" 3+5 / 2 " = 5
Note: Do not use the eval built-in library function.

	{% highlight java %}
	//逆波兰序
	public int baseCalculatorII(String s)
	{
		int len = s.length();
		if(s==null || len==0)
		{
			return 0;
		}
		Stack<Integer> stack=new Stack<Integer>();
		int num = 0;
		char sign = '+';
		for(int i=0;i<len;i++)
		{
			if(Character.isDigit(s.charAt(i)))
			{
				num=num*10+s.charAt(i)-'0';
			}
			if((!Character.isDigit(s.charAt(i))&&s.charAt(i)!='')||i==len-1)
			{
				if(sign=='+')
				{
					stack.push(num);
				}
				else if(sign=='-')
				{
					stack.push(-num);
				}
				else if(sign=='*')
				{
					stack.push(stack.pop()*num);
				}
				else if(sing=='/')
				{
					stack.push(stack.pop()/num);
				}
				sign=s.charAt(i);
				num=0;
			}
		}
		int result = 0;
		for(int i:stack)
		{
			result+=i;
		}
		return result;
	}
	{% endhighlight %}

### [Decode Ways](https://leetcode.com/problems/decode-ways/) ###

A message containing letters from A-Z is being encoded to numbers using the following mapping:

'A' -> 1
'B' -> 2
...
'Z' -> 26
Given an encoded message containing digits, determine the total number of ways to decode it.

For example,
Given encoded message "12", it could be decoded as "AB" (1 2) or "L" (12).

The number of ways decoding "12" is 2.

	{% highlight java %}
	public int decodeWays(String s)
	{
		if(s==null||s.length()==0||s.equals("0"))
		{
			return 0;
		}
		int[] result = new int[s.length()+1];
		result[0]=1;
		if(isValid(s.subString(0,1)))
		{
			result[1]=1;
		}
		else
		{
			result[1]=0;
		}
		for(int i=2;i<=s.length();i++)
		{
			if(isValid(s.subString(i-1,i)))
			{
				result[i]+=result[i-1];
			}
			if(isValid(s.subString(i-2,i)))
			{
				result[i]+=result[i-2];
			}
		}
		return result[s.length()];
	}
	public boolean isValid(String s){
	    if(s.charAt(0)=='0')
	        return false;
	    int value = Integer.parseInt(s);
	    return value>=1&&value<=26;
	}
	{% endhighlight %}


### [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) ###

Given a string, find the length of the longest substring without repeating characters. For example, the longest substring without repeating letters for "abcabcbb" is "abc", which the length is 3. For "bbbbb" the longest substring is "b", with the length of 1.

	{% highlight java %}
	//two points
	public int longestSubstringWithoutRepeatingCharacters(String s)
	{
		if(s.length()==0)
		{
			return 0;
		}
		HashMap<Character,Integer> map=new HashMap<Character,Integer>();
		int max = 0;
		for(int i=0,j=0;i<s.length();++i)
		{
			if(map.containsKey(s.charAt(i)))
			{
				j=Math.max(j,map.get(s.charAt(i))+1);
			}
			map.put(s.charAt(i),i);
			max = Math.max(max,i-j+1);
		}
		return max;
	}
	{% endhighlight %}

### [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) ###

Given a string S, find the longest palindromic substring in S. You may assume that the maximum length of S is 1000, and there exists one unique longest palindromic substring.

	{% highlight java %}
	public String longestPalindromeSubString(String s)
	{
		if(s.isEmpty())
		{
			return null;
		}
		if(s.length()==1)
		{
			return s;
		}
		String longest = s.subString(0,1);
		for(int i=0;i<s.length();i++)
		{
			String temp = helper(s,i,i);
			if(temp.length()>longest.length())
			{
				longest = temp;
			}
			temp = helper(s,i,i+1);
			if(temp.length()>longest.length())
			{
				longest = temp;
			}
		}
		return longest;
	}
	public String helper(String s, int begin, int end) {
		while (begin >= 0 && end <= s.length() - 1 && s.charAt(begin) == s.charAt(end)) {
			begin--;
			end++;
		}
		return s.substring(begin + 1, end);
	}
	{% endhighlight %}

### [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) ###

Given a digit string, return all possible letter combinations that the number could represent.

A mapping of digit to letters (just like on the telephone buttons) is given below.

Input:Digit string "23"
Output: ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].

	{% highlight java %}
	public List<String> letterCombinationsOfPhoneNumber(String digits) {
	    HashMap<Integer, String> map = new HashMap<Integer, String>();
	    map.put(2, "abc");
	    map.put(3, "def");
	    map.put(4, "ghi");
	    map.put(5, "jkl");
	    map.put(6, "mno");
	    map.put(7, "pqrs");
	    map.put(8, "tuv");
	    map.put(9, "wxyz");
	    map.put(0, "");
	    ArrayList<String> result = new ArrayList<String>();
	    if(digits == null || digits.length() == 0)
	    {
	    	return result;
	    }
	    ArrayList<Character> temp = new ArrayList<Character>();
	    getString(digits, temp, result, map);
	    return result;
	}
	public void getString(String digits, ArrayList<Character> temp, ArrayList<String> result,  HashMap<Integer, String> map){
	    if(digits.length() == 0){
	        char[] arr = new char[temp.size()];
	        for(int i=0; i<temp.size(); i++){
	            arr[i] = temp.get(i);
	        }
	        result.add(String.valueOf(arr));
	        return;
	    }
	    Integer curr = Integer.valueOf(digits.substring(0,1));
	    String letters = map.get(curr);
	    for(int i=0; i<letters.length(); i++){
	        temp.add(letters.charAt(i));
	        getString(digits.substring(1), temp, result, map);
	        temp.remove(temp.size()-1);
	    }
	}
	{% endhighlight %}


### [Simplify Path](https://leetcode.com/problems/simplify-path/) ###

Given an absolute path for a file (Unix-style), simplify it.

For example,
path = "/home/", => "/home"
path = "/a/./b/../../c/", => "/c"


### [Integer to Roman](https://leetcode.com/problems/integer-to-roman/) ###

Given an integer, convert it to a roman numeral.

Input is guaranteed to be within the range from 1 to 3999.

	{% highlight java %}
	public String intergerToRoman(int num)
	{
		int[] values={1000,900,500,400,100,90,50,40,10,9,5,4,1};
		String[] strs={"M","CM","D","CD","C","XC","L","XL","X",
			"IX","V","IV","I"};
		StringBuilder sb = new StringBuilder();
		for(int i=0;i<values.length;i++)
		{
			while(num>=values[i])
			{
				num-=values[i];
				sb.append(strs[i]);
			}
		}
		return sb.toString();
	}
	{% endhighlight %}

### [Multiply Strings](https://leetcode.com/problems/multiply-strings/) ###

Given two numbers represented as strings, return multiplication of the numbers as a string.

Note: The numbers can be arbitrarily large and are non-negative.

	{% highlight java %}
	public String multiplyStrings(String num1, String num2)
	{
		String n1 = new StringBuilder(num1).reverse().toString();
		String n2 = new StringBuilder(num2).reverse().toString();
		int[] d = new int[num1.length()+num2.length()];
		for(int i=0;i<n1.length();i++)
		{
			for(int j=0;j<n2.length();j++)
			{
				d[i+j] = (n1.charAt(i)-'0')*(n2.charAt(j)-'0');
			}
		}
		StringBuilder sb = new StringBuilder();
		for(int i=0;i<d.length;i++)
		{
			int mod = d[i]%10;
			int carry = d[i]/10;
			if(i+1<d.length)
			{
				d[i+1]+=carry;
			}
			sb.insert(0,mod);
		}
		while(sb.charAt(0)=='0'&&sb.length()>1)
		{
			sb.deleteCharAt(0);
		}
		return sb.toString();
	}
	{% endhighlight %}

### [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) ###

Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

For example, given n = 3, a solution set is:

"((()))", "(()())", "(())()", "()(())", "()()()"

	{% highlight java %}
	//Solution 1  DFS
	public List<String> generateParentheses(int n)
	{
		ArrayList<String> result = new ArrayList<String>();
		dfs(result, "", n, n);
		return result;
	}
	public void dfs(List<String> result, String s, int left, int right)
	{
		if(left>right)
		{
			return;
		}
		if(left==0&&right==0)
		{
			result.add(s);
			return;
		}
		if(left>0)
		{
			dfs(result, s+"(", left-1,right);
		}
		if(right>0)
		{
			dfs(result, s+")",left, right-1);
		}
	}
	{% endhighlight %}

### [Reverse Words in a String](https://leetcode.com/problems/reverse-words-in-a-string/) ###

Given an input string, reverse the string word by word.

For example,
Given s = "the sky is blue",
return "blue is sky the".

Update (2015-02-12):
For C programmers: Try to solve it in-place in O(1) space.

	{% highlight java %}
	public String reverseWords(String s)
	{
		if(s==null||s.length()==0)
		{
			return "";
		}
		String[] str = s.splite(" ");
		StringBuilder sb = new StringBuilder();
		for(int i=str.length-1;i>=0;i--)
		{
			if(!str[i].equals(""))
			{
				sb.append(str[i]).append(" ");
			}
		}
		return sb.length()==0?" ":sb.subString(0,sb.length()-1);
	}
	{% endhighlight %}





