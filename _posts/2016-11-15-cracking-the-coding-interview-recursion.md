---
date: 2016-11-15 18:18:30+00:00
layout: post
title: 《Cracking the coding interview》中递归小结
thread: 163
categories: algorithm 
tags: algorithm 

---

这篇小结下《Cracking the coding interview》中的递归题目。


1. Write a method to generate the nth Fibonacci number.

2. Imagine a robot sitting on the upper left hand corner of an NxN grid. The robot can only move in two directions: right and down. How many possible paths are there for the robot? FOLLOW UP Imagine certain squares are “off limits”, such that the robot can not step on them. Design an algorithm to get all possible paths for the robot.

3. Write a method that returns all subsets of a set.

4. Write a method to compute all permutations of a string.

5. Implement an algorithm to print all valid (e.g., properly opened and closed) combinations of n-pairs of parentheses. EXAMPLE: input: 3 (e.g., 3 pairs of parentheses) output: ()()(), ()(()), (())(), ((()))

6. Implement the “paint fill” function that one might see on many image editing programs. That is, given a screen (represented by a 2 dimensional array of Colors), a point, and a new color, fill in the surrounding area until you hit a border of that color.

7. Given an infinite number of quarters (25 cents), dimes (10 cents), nickels (5 cents) and pennies (1 cent), write code to calculate the number of ways of representing n cents.

8. Write an algorithm to print all ways of arranging eight queens on a chess board so that none of them share the same row, column or diagonal.


### 1. 生成第n个斐波那契数 ###

Write a method to generate the nth Fibonacci number.

	{% highlight java %}
	public class Fibonacci
	{
		public static int fibo(int n)
		{
			if(n == 0)
			{
				return 0;
			}
			else if(n == 1)
			{
				return 1;
			}
			else if(n > 1)
			{
				return fibo(n-1) + fibo(n-2);
			}
			else
			{
				return -1;
			}
		}
		//iterative 
		public static int fibo2(int n)
		{
			if(n<0)
			{
				return -1;
			}
			if(n == 0)
			{
				return 0;
			}
			int a = 1, b=1;
			for(int i = 3; i<= n; ++i)
			{
				int c = a + b;
				a = b;
				b = c;
			}
			return b;
		}
	}
	{% endhighlight %}


### 2. 在一个N*N矩阵的左上角坐着一个机器人，它只能向右运动或向下运动。那么， 机器人运动到右下角一共有多少种可能的路径？ ###


Imagine a robot sitting on the upper left hand corner of an NxN grid. The robot can only move in two directions: right and down. How many possible paths are there for the robot?

FOLLOW UP

Imagine certain squares are “off limits”, such that the robot can not step on them. Design an algorithm to get all possible paths for the robot.

	{% highlight java %}
	public class GetPaths
	{
		ArrayList<Point> current_path = new ArrayList<Point>();
		public static boolean getPaths(int x, int y)
		{
			Point p = new Point(x, y);
			current_path.add(p);
			if(x == 0 && y == 0)
			{
				return true;
			}
			boolean success = false;
			if(x >= 1 && is_free(x-1, y))
			{
				success = getPaths(x-1, y);
			}
			if(!success && y >= 1 && is_free(x, y-1))
			{
				success = getPaths(x, y-1);
			}
			if(!success)
			{
				current_path.remove(p);
			}
			return success;
		}
	}
	{% endhighlight %}


### 3. 返回一个集合中的所有子集 ###

Write a method that returns all subsets of a set.


### 4. 返回一个字符串的所有排列 ###

Write a method to compute all permutations of a string


	{% highlight java %}
	public class GetPermutations1
	{
		public static void permutation1(String str)
		{
			permutation1("", str);
		}
		private static void permutation1(String prefix, String str)
		{
			int n = str.length();
			if(n == 0)
			{
				System.out.println(prefix);
			}
			else
			{
				for(int i = 0; i < n; i++)
				{
					permutation1(prefix + str.charAt(i), str.substring(0,i) 
						+ str.substring(i+1, n));
				}
			}
		}
	}
	
	public class GetPermutations2
	{
		public static ArrayList<String> permutation2(String s)
		{
			ArrayList<String> permutation = new ArrayList<String>();
			if(s == null)
			{
				return null;
			}
			else if(s.length() == 0)
			{
				permutation.add("");
				return permutation;
			}
			char first = s.charAt(0);
			String remainder = s.substring(1);
			ArrayList words = permutation2(remainder);
			for(String word: words)
			{
				for(int j = 0; j <= word.length(); j++)
				{
					permution.add(insertCharAt(word, first, j));
				}
			}
			return permutation;
		}
		public static String insertCharAt(String word, char c, int i)
		{
			String start = word.substring(0, i);
			String end = word.substring(i);
			return start + c + end;
		}
	}
	{% endhighlight %}


### 5. 实现一个算法打印出n对括号的有效组合 ###

Implement an algorithm to print all valid (e.g., properly opened and closed) combinations of n-pairs of parentheses.

EXAMPLE:

input: 3 (e.g., 3 pairs of parentheses)

output: ((())), (()()), (())(), ()(()), ()()()

	{% highlight java %}
	public class PrintParentheses
	{
		public static void printParentheses(int l,int r,char[] str,int count)
		{
			if(l < 0 || r < 1)
			{
				return;
			}
			if(l == 0 && r == 0)
			{
				System.out.println(str);
			}
			else
			{
				if(l > 0)
				{
					str[count] = '(';
					printParentheses(l-1, r, str, count+1);
				}
				if(r > 1)
				{
					str[count] = ')';
					printParentheses(l, r-1, str, count + 1);
				}
			}
		}
		public static void printParentheses(int count)
		{
			char[] str = new char[count*2];
			printParentheses(count,count, str, 0);
		}
	}
	{% endhighlight %}


### 6. 实现图像处理软件中的“填充”函数，给定一块区域(可以不规则)，一个种子点和一种新颜色， 填充这块区域，直到到达这块区域的边界(边界是用这种新颜色画的一条封闭曲线) ###

Implement the “paint fill” function that one might see on many image editing programs. That is, given a screen (represented by a 2-dimensional array of Colors), a point, and a new color, fill in the surrounding area until you hit a border of that color.

	{% highlight java %}
	public class PaintFillScreen
	{
		enum Color{Black, White, Red, Yellow, Green}
		public static boolean paintFill(Color[][] screen, int x, 
			int y, Color ocolor, Color ncolor)
		{
			if(x < 0 || x >= screen[0].length ||
				y < 0 || y >= screen.length)
			{
				return false;
			}
			if(screen[y][x] == ocolor)
			{
				screen[y][x] = ncolor;
				paintFill(screen, x-1, y, ocolor, ncolor);
				paintFill(screen, x+1, y, ocolor, ncolor);
				paintFill(screen, x, y-1, ocolor, ncolor);
				paintFill(screen, x, y+1, ocolor, ncolor);
			}
			return true;
		}
		public static boolean paintFill(Color[][] screen, int x, int y, Color ncolor)
		{
			return paintFill(screen, x, y, screen[y][x], ncolor);
		}
	}
	{% endhighlight %}


### 7. 有25分，10分，5分和1分的硬币无限个。写一个函数计算组成n分的方式有几种 ###

Given an infinite number of quarters (25 cents), dimes (10 cents), nickels (5 cents) and pennies (1 cent), write code to calculate the number of ways of representing n cents.

	{% highlight java %}
	public class CalculateNumsOfCents
	{
		public static int makeChange(int n, int denom)
		{
			int next_denom = 0;
			switch(denom)
			{
				case 25:
				next_denom = 10;
				break;
				case 10:
				next_denom = 5;
				break;
				case 5:
				next_denom = 1;
				break;
				case 1:
				return 1;
			}
			int ways = 0;
			for(int i = 0; i*denom <= n; i++)
			{
				ways += makeChange(n-i*denom, next_denom);
			}
			return ways;
		}
		public static void calculateNums(int n)
		{
			System.out.println(makeChange(n, 25));
		}
	}
	{% endhighlight %}


### 8. 经典的八皇后问题，即在一个8*8的棋盘上放8个皇后，使得这8个皇后无法互相攻击( 任意2个皇后不能处于同一行，同一列或是对角线上)，输出所有可能的摆放情况 ###

Write an algorithm to print all ways of arranging eight queens on a chess board so that none of them share the same row, column or diagonal.

	{% highlight java %}
	public class EightQueens
	{
		int[] columForRow = new int[8];
		public static boolean check(int row)
		{
			for(int i = 0; i < row; i++)
			{
				int diff = Math.abs(columForRow[i]-columForRow[row]);
				if(diff == 0 || diff == row-i)
				{
					return false;
				}
			}
			return true;
		}
		public static void placeQueen(int row)
		{
			if(row == 8)
			{
				printBoard();
				return;
			}
			for(int i = 0; i < 8; i++)
			{
				columForRow[row] = i;
				if(check(row))
				{
					placeQueen(row + 1);
				}
			}
		}
		public static void printEightQueen()
		{
			placeQueen(0);
		}
	}
	{% endhighlight %}



C++版实现可参考： [Cracking the coding interview--问题与解答](http://www.hawstein.com/posts/ctci-solutions-contents.html)

