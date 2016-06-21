---
date: 2016-6-20 18:49:30+00:00
layout: post
title: Leetcode中动态规划算法类题目小结
thread: 143
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中动态规划算法类部分的题目，目前已有的题目(除去之前已总结的)有：

1. Russian Doll Envelopes

2. Coin Change

3. Best Time to Buy and Sell Stock with Cooldown

4. Range Sum Query 2D - Immutable

5. Range Sum Query - Immutable

6. Longest Increasing Subsequence

7. Maximal Square

8. House Robber

9. House Robber II

10. Best Time to Buy and Sell Stock IV

11. Dungeon Game

12. Palindrome Partitioning II

13. Climbing Stairs


### [Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) ###

You have a number of envelopes with widths and heights given as a pair of integers (w, h). One envelope can fit into another if and only if both the width and height of one envelope is greater than the width and height of the other envelope.

What is the maximum number of envelopes can you Russian doll? (put one inside other)

Example:

Given envelopes = [[5,4],[6,4],[6,7],[2,3]], the maximum number of envelopes you can Russian doll is 3 ([2,3] => [5,4] => [6,7]).


### [Coin Change](https://leetcode.com/problems/coin-change/) ###

You are given coins of different denominations and a total amount of money amount. Write a function to compute the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

Example 1:

coins = [1, 2, 5], amount = 11

return 3 (11 = 5 + 5 + 1)

Example 2:

coins = [2], amount = 3

return -1.

Note:

You may assume that you have an infinite number of each kind of coin.

Credits:

### [Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) ###

Say you have an array for which the ith element is the price of a given stock on day i.

Design an algorithm to find the maximum profit. You may complete as many transactions as you like (ie, buy one and sell one share of the stock multiple times) with the following restrictions:

You may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).

After you sell your stock, you cannot buy stock on next day. (ie, cooldown 1 day)

Example:

	prices = [1, 2, 3, 0, 2]
	maxProfit = 3
	transactions = [buy, sell, cooldown, buy, sell]

Credits:

### [Range Sum Query 2D - Immutable](https://leetcode.com/problems/range-sum-query-2d-immutable/) ###

Given a 2D matrix matrix, find the sum of the elements inside the rectangle defined by its upper left corner (row1, col1) and lower right corner (row2, col2).

Range Sum Query 2D

The above rectangle (with the red border) is defined by (row1, col1) = (2, 1) and (row2, col2) = (4, 3), which contains sum = 8.

Example:

	Given matrix = [
	  [3, 0, 1, 4, 2],
	  [5, 6, 3, 2, 1],
	  [1, 2, 0, 1, 5],
	  [4, 1, 0, 1, 7],
	  [1, 0, 3, 0, 5]
	]
	
	sumRegion(2, 1, 4, 3) -> 8
	sumRegion(1, 1, 2, 2) -> 11
	sumRegion(1, 2, 2, 4) -> 12

Note:

You may assume that the matrix does not change.

There are many calls to sumRegion function.

You may assume that row1 ≤ row2 and col1 ≤ col2.

Subscribe to see which companies asked this question

### [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) ###

Given an integer array nums, find the sum of the elements between indices i and j (i ≤ j), inclusive.

Example:

Given nums = [-2, 0, 3, -5, 2, -1]

	sumRange(0, 2) -> 1
	sumRange(2, 5) -> -1
	sumRange(0, 5) -> -3

Note:

You may assume that the array does not change.

There are many calls to sumRange function.

### [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) ###

Given an unsorted array of integers, find the length of longest increasing subsequence.

For example,

Given [10, 9, 2, 5, 3, 7, 101, 18],

The longest increasing subsequence is [2, 3, 7, 101], therefore the length is 4. Note that there may be more than one LIS combination, it is only necessary for you to return the length.

Your algorithm should run in O(n2) complexity.

Follow up: Could you improve it to O(n log n) time complexity?

### [Maximal Square](https://leetcode.com/problems/maximal-square/) ###

Given a 2D binary matrix filled with 0's and 1's, find the largest square containing all 1's and return its area.

For example, given the following matrix:

	1 0 1 0 0
	1 0 1 1 1
	1 1 1 1 1
	1 0 0 1 0

Return 4.

### [House Robber](https://leetcode.com/problems/house-robber/) ###

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security system connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount of money you can rob tonight without alerting the police.

Credits:

Special thanks to @ifanchu for adding this problem and creating all test cases. Also thanks to @ts for adding additional test cases.

### [House Robber II](https://leetcode.com/problems/house-robber-ii/) ###

Note: This is an extension of House Robber.

After robbing those houses on that street, the thief has found himself a new place for his thievery so that he will not get too much attention. This time, all houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Meanwhile, the security system for these houses remain the same as for those in the previous street.

Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount of money you can rob tonight without alerting the police.

### [Best Time to Buy and Sell Stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/) ###

Say you have an array for which the ith element is the price of a given stock on day i.

Design an algorithm to find the maximum profit. You may complete at most k transactions.

Note:

You may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).

### [Dungeon Game](https://leetcode.com/problems/dungeon-game/) ###

The demons had captured the princess (P) and imprisoned her in the bottom-right corner of a dungeon. The dungeon consists of M x N rooms laid out in a 2D grid. Our valiant knight (K) was initially positioned in the top-left room and must fight his way through the dungeon to rescue the princess.

The knight has an initial health point represented by a positive integer. If at any point his health point drops to 0 or below, he dies immediately.

Some of the rooms are guarded by demons, so the knight loses health (negative integers) upon entering these rooms; other rooms are either empty (0's) or contain magic orbs that increase the knight's health (positive integers).

In order to reach the princess as quickly as possible, the knight decides to move only rightward or downward in each step.


Write a function to determine the knight's minimum initial health so that he is able to rescue the princess.

For example, given the dungeon below, the initial health of the knight must be at least 7 if he follows the optimal path RIGHT-> RIGHT -> DOWN -> DOWN.

	-2 (K)	-3	3
	-5	-10	1
	10	30	-5 (P)

Notes:

The knight's health has no upper bound..
Any room can contain threats or power-ups, even the first room the knight enters and the bottom-right room where the princess is imprisoned.

### [Palindrome Partitioning II](https://leetcode.com/problems/palindrome-partitioning-ii/) ###

Given a string s, partition s such that every substring of the partition is a palindrome.

Return the minimum cuts needed for a palindrome partitioning of s.

For example, given s = "aab",
Return 1 since the palindrome partitioning ["aa","b"] could be produced using 1 cut.

### [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) ###

You are climbing a stair case. It takes n steps to reach to the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

