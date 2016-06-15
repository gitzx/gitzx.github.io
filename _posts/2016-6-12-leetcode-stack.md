---
date: 2016-6-12 18:36:30+00:00
layout: post
title: Leetcode中Stack类题目小结
thread: 138
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中Stack类部分的题目，目前已有的题目(除去之前已总结的)有：

1. Implement Queue using Stacks

2. Implement Stack using Queues

3. Min Stack

4. Verify Preorder Serialization of a Binary Tree

5. Evaluate Reverse Polish Notation

6. Flatten Nested List Iterator

7. Remove Duplicate Letters


### [Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) ###

Implement the following operations of a queue using stacks.

push(x) -- Push element x to the back of queue.

pop() -- Removes the element from in front of queue.

peek() -- Get the front element.

empty() -- Return whether the queue is empty.

Notes:

You must use only standard operations of a stack -- which means only push to top, peek/pop from top, size, and is empty operations are valid.

Depending on your language, stack may not be supported natively. You may simulate a stack by using a list or deque (double-ended queue), as long as you use only standard operations of a stack.

You may assume that all operations are valid (for example, no pop or peek operations will be called on an empty queue).

Subscribe to see which companies asked this question

	{% highlight java %}
	class MyQueue
	{
		Stack<Integer> temp=new Stack<Integer>();
		Stack<Integer> value=new Stack<Integer>();
		public void push(int x)
		{
			if(value.isEmpty())
			{
				value.push(x);
			}
			else
			{
				while(!value.isEmpty())
				{
					temp.push(value.pop());
				}
				value.push(x);
				while(!temp.isEmpty())
				{
					value.push(temp.pop());
				}
			}
		}
		public void pop()
		{
			value.pop();
		}
		public int peek()
		{
			return value.peek();
		}
		public boolean isEmpty()
		{
			return value.isEmpty();
		}
	}
	{% endhighlight %}

### [Implement Stack using Queues](https://leetcode.com/problems/implement-stack-using-queues/) ###

Implement the following operations of a stack using queues.

push(x) -- Push element x onto stack.

pop() -- Removes the element on top of the stack.

top() -- Get the top element.

empty() -- Return whether the stack is empty.


Notes:

You must use only standard operations of a queue -- which means only push to back, peek/pop from front, size, and is empty operations are valid.

Depending on your language, queue may not be supported natively. You may simulate a queue by using a list or deque (double-ended queue), as long as you use only standard operations of a queue.

You may assume that all operations are valid (for example, no pop or top operations will be called on an empty stack).

Update (2015-06-11):

The class name of the Java function had been updated to MyStack instead of Stack.

	{% highlight java %}
	class MyStack
	{
		LinkedList<Integer> queue1=new LinkedList<Integer>();
		LinkedList<Integer> queue2=new LinkedList<Integer>();
		public void push(int x)
		{
			if(empty())
			{
				queue1.offer(x);
			}
			else
			{
				if(queue1.size()>0)
				{
					queue2.offer(x);
					int size=queue1.size();
					while(size>0)
					{
						queue2.offer(quue1.poll());
						size--;
					}
				}
				else if(queue2.size()>0)
				{
					queue1.offer(x);
					int size=queue2.size();
					while(size>0)
					{
						queue1.offer(quue2.poll());
						size--;
					}
				}
			}
		}
		public void pop()
		{
			if(queue1.size()>0)
			{
				queue1.poll();
			}
			else if(queue2.size()>0)
			{
				queue2.poll();
			}
		}
		public int top()
		{
			if(queue1.size()>0)
			{
				return queue1.peek();
			}
			else if(queue2.size()>0)
			{
				return queue2.peek();
			}
			return 0;
		}
		public boolean empty()
		{
			return queue1.isEmpty()&queue2.isEmpty();
		}
	}
	{% endhighlight %}

### [Min Stack](https://leetcode.com/problems/min-stack/) ###

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

push(x) -- Push element x onto stack.

pop() -- Removes the element on top of the stack.

top() -- Get the top element.

getMin() -- Retrieve the minimum element in the stack.

Example:

	MinStack minStack = new MinStack();
	minStack.push(-2);
	minStack.push(0);
	minStack.push(-3);
	minStack.getMin();   --> Returns -3.
	minStack.pop();
	minStack.top();      --> Returns 0.
	minStack.getMin();   --> Returns -2.

Subscribe to see which companies asked this question

	{% highlight java %}
	class Elem
	{
		public int value;
		public int min;
		public Elem next;
		public Elem(int value,int min)
		{
			this.value=value;
			this.min=min;
		}
	}
	public class MinStack
	{
		public Elem top;
		public void push(int x)
		{
			if(top==null)
			{
				top=new Elem(x,x);
			}
			else
			{
				Elem e=new Elem(x,Math.min(x,top.min));
				e.next=top;
				top=e;
			}
		}
		public void pop()
		{
			if(top==null)
			{
				return;
			}
			Elem temp=top.next;
			top.next=null;
			top=temp;
		}
		public int top()
		{
			if(top==null)
			{
				return -1;
			}
			return top.value;
		}
		public int getMin()
		{
			if(top==null)
			{
				return -1;
			}
			return top.min;
		}
	}
	{% endhighlight %}

### [Verify Preorder Serialization of a Binary Tree](https://leetcode.com/problems/verify-preorder-serialization-of-a-binary-tree/) ###

One way to serialize a binary tree is to use pre-order traversal. When we encounter a non-null node, we record the node's value. If it is a null node, we record using a sentinel value such as #.

	     _9_
	    /   \
	   3     2
	  / \   / \
	 4   1  #  6
	/ \ / \   / \
	# # # #   # #

For example, the above binary tree can be serialized to the string "9,3,4,#,#,1,#,#,2,#,6,#,#", where # represents a null node.

Given a string of comma separated values, verify whether it is a correct preorder traversal serialization of a binary tree. Find an algorithm without reconstructing the tree.

Each comma separated value in the string must be either an integer or a character '#' representing null pointer.

You may assume that the input format is always valid, for example it could never contain two consecutive commas such as "1,,3".

Example 1:

	"9,3,4,#,#,1,#,#,2,#,6,#,#"
	Return true

Example 2:

	"1,#"
	Return false

Example 3:

	"9,#,#,1"
	Return false

Credits:

Special thanks to @dietpepsi for adding this problem and creating all test cases.

	{% highlight java %}
	//solution1 diff=outdegree-indegree
	//非#有2个outdegree和1个indegree
	//#y有0个outdegree和1个indegree
	public boolean isValidSerialization(String preorder)
	{
		String[] nodes=preorder.split(",");
		int diff=1;
		for(String node:nodes)
		{
			if(--diff<0)
			{
				return false;
			}
			if(!node.equals("#"))
			{
				diff+=2;
			}
		}
		return diff==0;
	} 
	//solution2 stack
	public boolean isValidSerialization(String preorder)
	{
		LinkedList<String> stack=new LinkedList<String>();
		String[] arr=preorder.split(",");
		for(int i=0;i<arr.length;i++)
		{
			stack.add(arr[i]);
			while(stack.size()>=3
				&&stack.get(stack.size()-1).equals("#")
				&&stack.get(stack.size()-2).equals("#")
				&&stack.get(stack.size()-3).equals("#"))
			{
				stack.remove(stack.size()-1);
				stack.remove(stack.size()-1);
				stack.remove(stack.size()-1);
				stack.add("#");
			}
		}
		if(stack.size()==1&&stack.get(0).equals("#"))
		{
			return true;
		}
		else
		{
			return false;
		}
	}
	{% endhighlight %}

### [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) ###

Evaluate the value of an arithmetic expression in Reverse Polish Notation.

Valid operators are +, -, *, /. Each operand may be an integer or another expression.

Some examples:

	  ["2", "1", "+", "3", "*"] -> ((2 + 1) * 3) -> 9
	  ["4", "13", "5", "/", "+"] -> (4 + (13 / 5)) -> 6

Subscribe to see which companies asked this question

	{% highlight java %}
	public int evalRPN(String[] tokens)
	{
		int returnValue=0;
		String operators="+-*/";
		Stack<String> stack=new Stack<String>();
		for(String t:tokens)
		{
			if(!operators.contains(t))
			{
				stack.push(t);
			}
			else
			{
				int a=Integer.valueOf(stack.pop());
				int b=Integer.valueOf(stack.pop());
				switch(t)
				{
					case "+":
					{
						stack.push(String.valueOf(a+b));
						break;
					}
					case "-":
					{
						stack.push(String.valueOf(b-a));
						break;
					}
					case "*":
					{
						stack.push(String.valueOf(a*b));
						break;
					}
					case "/":
					{
						stack.push(String.valueOf(b/a));
						break;
					}
				}
			}
		}
		returnValue=Integer.valueOf(stack.pop());
		return returnValue;
	}
	{% endhighlight %}

### [Flatten Nested List Iterator](https://leetcode.com/problems/flatten-nested-list-iterator/) ###

Given a nested list of integers, implement an iterator to flatten it.

Each element is either an integer, or a list -- whose elements may also be integers or other lists.

Example 1:

Given the list [[1,1],2,[1,1]],

By calling next repeatedly until hasNext returns false, the order of elements returned by next should be: [1,1,2,1,1].

Example 2:

Given the list [1,[4,[6]]],

By calling next repeatedly until hasNext returns false, the order of elements returned by next should be: [1,4,6].

	{% highlight java %}
	public class NestedIterator implements Iterator<Integer>
	{
		Stack<NestedInteger> stack=new Stack<NestedInteger>();
		public NestedIterator(List<NestedInteger> nestedList)
		{
			if(nestedList==null)
			{
				return;
			}
			for(int i=nestedList.size()-1;i>=0;i--)
			{
				stack.push(nestedList.get(i));
			}
		}
		public Integer next()
		{
			return stack.pop().getInteger();
		}
		public boolean hasNext()
		{
			while(!stack.isEmpty())
			{
				NestedInteger top=stack.peek();
				if(top.isInteger)
				{
					return true;
				}
				else
				{
					stack.pop();
					for(int i=top.getList().size()-1;i>=0;i--)
					{
						stack.push(top.getList().get(i));
					}
				}
			}
			return false;
		}
	}
	{% endhighlight %}

### [Remove Duplicate Letters](https://leetcode.com/problems/remove-duplicate-letters/) ###

Given a string which contains only lowercase letters, remove duplicate letters so that every letter appear once and only once. You must make sure your result is the smallest in lexicographical order among all possible results.

Example:

Given "bcabc"

Return "abc"

Given "cbacdcbc"

Return "acdb"

	{% highlight java %}
	//solution 1
	public String removeDuplicateLetters(String s)
	{
		int[] cnt=new int[26];
		int pos=0;
		for(int i=0;i<s.length();i++)
		{
			cnt[s.charAt(i)-'a']++;
		}
		for(int i=0;i<s.length();i++)
		{
			if(s.charAt(i)<s.charAt(pos))
			{
				pos=i;
			}
			if(--cnt[s.charAt(i)-'a']==0)
			{
				break;
			}
		}
		return s.length()==0?"":s.charAt(pos)+removeDuplicateLetters
			(s.substring(pos+1).replaceAll("",s.charAt(pos),""));
	}
	{% endhighlight %}