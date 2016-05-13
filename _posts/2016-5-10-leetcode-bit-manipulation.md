---
date: 2016-5-10 18:26:30+00:00
layout: post
title: Leetcode中位操作类题目小结
thread: 131
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中Bit Manipulation的题目，题目不多，所有的题目就放到一篇中总结了，目前已有的题目有：

1. Power of Four

2. Reverse Bits

3. Majority Element

4. Number of 1 Bits	

5. Power of Two

6. Single Number III

7. Single Number

8. Subsets

9. Single Number II

10. Repeated DNA Sequences

11. Bitwise AND of Numbers Range

12. Maximum Product of Word Lengths

13. Missing Number

14. Counting Bits


### [Power of Four](https://leetcode.com/problems/power-of-four/) ###

Given an integer (signed 32 bits), write a function to check whether it is a power of 4.

Example:
Given num = 16, return true. Given num = 5, return false.

Follow up: Could you solve it without loops/recursion?


### [Reverse Bits](https://leetcode.com/problems/reverse-bits/) ###

Reverse bits of a given 32 bits unsigned integer.

For example, given input 43261596 (represented in binary as 00000010100101000001111010011100), return 964176192 (represented in binary as 00111001011110000010100101000000).

Follow up:
If this function is called many times, how would you optimize it?

Related problem: Reverse Integer

### [Majority Element](https://leetcode.com/problems/majority-element/) ###

Given an array of size n, find the majority element. The majority element is the element that appears more than ⌊ n/2 ⌋ times.

You may assume that the array is non-empty and the majority element always exist in the array.


### [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) ###

Write a function that takes an unsigned integer and returns the number of ’1' bits it has (also known as the Hamming weight).

For example, the 32-bit integer ’11' has binary representation 00000000000000000000000000001011, so the function should return 3.

### [Power of Two](https://leetcode.com/problems/power-of-two/) ###

Given an integer, write a function to determine if it is a power of two.

### [Single Number III ](https://leetcode.com/problems/single-number-iii/) ###

Given an array of numbers nums, in which exactly two elements appear only once and all the other elements appear exactly twice. Find the two elements that appear only once.

For example:

Given nums = [1, 2, 1, 3, 2, 5], return [3, 5].

Note:
The order of the result is not important. So in the above example, [5, 3] is also correct.
Your algorithm should run in linear runtime complexity. Could you implement it using only constant space complexity?

### [Single Number](https://leetcode.com/problems/single-number/) ###

Given an array of integers, every element appears twice except for one. Find that single one.

Note:
Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?

### [Subsets](https://leetcode.com/problems/subsets/) ###

Given a set of distinct integers, nums, return all possible subsets.

Note:
Elements in a subset must be in non-descending order.
The solution set must not contain duplicate subsets.
For example,
If nums = [1,2,3], a solution is:

	[
	  [3],
	  [1],
	  [2],
	  [1,2,3],
	  [1,3],
	  [2,3],
	  [1,2],
	  []
	]

Subscribe to see which companies asked this question


### [Single Number II](https://leetcode.com/problems/single-number-ii/) ###

Given an array of integers, every element appears three times except for one. Find that single one.

Note:
Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?

### [Repeated DNA Sequences](https://leetcode.com/problems/repeated-dna-sequences/) ###

All DNA is composed of a series of nucleotides abbreviated as A, C, G, and T, for example: "ACGAATTCCG". When studying DNA, it is sometimes useful to identify repeated sequences within the DNA.

Write a function to find all the 10-letter-long sequences (substrings) that occur more than once in a DNA molecule.

For example,

	Given s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT",
	
	Return:
	
	["AAAAACCCCC", "CCCCCAAAAA"].

Subscribe to see which companies asked this question


### [Bitwise AND of Numbers Range](https://leetcode.com/problems/bitwise-and-of-numbers-range/) ###

Given a range [m, n] where 0 <= m <= n <= 2147483647, return the bitwise AND of all numbers in this range, inclusive.

For example, given the range [5, 7], you should return 4.


### [Maximum Product of Word Lengths](https://leetcode.com/problems/maximum-product-of-word-lengths/) ###


Given a string array words, find the maximum value of length(word[i]) * length(word[j]) where the two words do not share common letters. You may assume that each word will contain only lower case letters. If no such two words exist, return 0.

Example 1:

	Given ["abcw", "baz", "foo", "bar", "xtfn", "abcdef"]
	
	Return 16
	
	The two words can be "abcw", "xtfn".

Example 2:

	Given ["a", "ab", "abc", "d", "cd", "bcd", "abcd"]
	
	Return 4
	
	The two words can be "ab", "cd".

Example 3:

	Given ["a", "aa", "aaa", "aaaa"]
	
	Return 0

No such pair of words.


### [Missing Number](https://leetcode.com/problems/missing-number/) ###

Given an array containing n distinct numbers taken from 0, 1, 2, ..., n, find the one that is missing from the array.

For example,
Given nums = [0, 1, 3] return 2.

Note:
Your algorithm should run in linear runtime complexity. Could you implement it using only constant extra space complexity?

### [Counting Bits](https://leetcode.com/problems/counting-bits/) ###

Given a non negative integer number num. For every numbers i in the range 0 ≤ i ≤ num calculate the number of 1's in their binary representation and return them as an array.

Example:
For num = 5 you should return [0,1,1,2,1,2].

Follow up:

It is very easy to come up with a solution with run time O(n*sizeof(integer)). But can you do it in linear time O(n) /possibly in a single pass?
Space complexity should be O(n).
Can you do it like a boss? Do it without using any builtin function like __builtin_popcount in c++ or in any other language.