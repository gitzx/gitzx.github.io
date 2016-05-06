---
date: 2016-5-6 8:30:30+00:00
layout: post
title: Leetcode中排序类题目小结
thread: 130
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中Sort的题目，题目不多，所有的题目就放到一篇中总结了，目前已有的题目有：

1. Valid Anagram

2. Wiggle Sort II

3. Sort Colors

4. H-Index

5. Insertion Sort List

6. Sort List

7. Largest Number

8. Merge Intervals

9. Maximum Gap

10. Insert Interval


### [Valid Anagram](https://leetcode.com/problems/valid-anagram/) ###

Given two strings s and t, write a function to determine if t is an anagram of s.

For example,
s = "anagram", t = "nagaram", return true.
s = "rat", t = "car", return false.

Note:
You may assume the string contains only lowercase alphabets.

Follow up:
What if the inputs contain unicode characters? How would you adapt your solution to such case?


### [Wiggle Sort II](https://leetcode.com/problems/wiggle-sort-ii/) ###

Given an unsorted array nums, reorder it such that nums[0] < nums[1] > nums[2] < nums[3]....

Example:
(1) Given nums = [1, 5, 1, 1, 6, 4], one possible answer is [1, 4, 1, 5, 1, 6]. 
(2) Given nums = [1, 3, 2, 2, 3, 1], one possible answer is [2, 3, 1, 3, 1, 2].

Note:
You may assume all input has valid answer.

Follow Up:
Can you do it in O(n) time and/or in-place with O(1) extra space?


### [Sort Colors](https://leetcode.com/problems/sort-colors/) ###

Given an array with n objects colored red, white or blue, sort them so that objects of the same color are adjacent, with the colors in the order red, white and blue.

Here, we will use the integers 0, 1, and 2 to represent the color red, white, and blue respectively.

Note:
You are not suppose to use the library's sort function for this problem.


### [H-Index](https://leetcode.com/problems/h-index/) ###

Given an array of citations (each citation is a non-negative integer) of a researcher, write a function to compute the researcher's h-index.

According to the definition of h-index on Wikipedia: "A scientist has index h if h of his/her N papers have at least h citations each, and the other N − h papers have no more than h citations each."

For example, given citations = [3, 0, 6, 1, 5], which means the researcher has 5 papers in total and each of them had received 3, 0, 6, 1, 5 citations respectively. Since the researcher has 3 papers with at least 3 citations each and the remaining two with no more than 3 citations each, his h-index is 3.

Note: If there are several possible values for h, the maximum one is taken as the h-index.


### [Insertion Sort List](https://leetcode.com/problems/insertion-sort-list/) ###

Sort a linked list using insertion sort.


### [Sort List](https://leetcode.com/problems/sort-list/) ###

Sort a linked list in O(n log n) time using constant space complexity.


### [Largest Number](https://leetcode.com/problems/largest-number/) ###

Given a list of non negative integers, arrange them such that they form the largest number.

For example, given [3, 30, 34, 5, 9], the largest formed number is 9534330.

Note: The result may be very large, so you need to return a string instead of an integer.


### [Merge Intervals](https://leetcode.com/problems/merge-intervals/) ###

Given a collection of intervals, merge all overlapping intervals.

For example,
Given [1,3],[2,6],[8,10],[15,18],
return [1,6],[8,10],[15,18].


### [Maximum Gap](https://leetcode.com/problems/maximum-gap/) ###

Given an unsorted array, find the maximum difference between the successive elements in its sorted form.

Try to solve it in linear time/space.

Return 0 if the array contains less than 2 elements.

You may assume all elements in the array are non-negative integers and fit in the 32-bit signed integer range.


### [Insert Interval](https://leetcode.com/problems/insert-interval/) ###

Given a set of non-overlapping intervals, insert a new interval into the intervals (merge if necessary).

You may assume that the intervals were initially sorted according to their start times.

Example 1:
Given intervals [1,3],[6,9], insert and merge [2,5] in as [1,5],[6,9].

Example 2:
Given [1,2],[3,5],[6,7],[8,10],[12,16], insert and merge [4,9] in as [1,2],[3,10],[12,16].

This is because the new interval [4,9] overlaps with [3,5],[6,7],[8,10].