---
date: 2014-10-27 10:30:30+00:00
layout: post
title: 常见的内部排序算法的C实现
thread: 80
categories: algorithm
tags:  algorithm
---

之前写了篇用伪代码描述[六个常见的比较排序算法](http://www.gitzx.com/algorithm-compare-sort/),在这用C实现下。

	{% highlight C++ %}
	#include<stdio.h>
	
	void swap(int *xp, int *yp){
		int tmp = *xp;
		*xp = *yp;
		*yp = tmp;
	}
	
	void bubbleSort(int a[], int n){
		for(int i=0; i<n; i++){
			bool isswap = false;
			for(int j=i; j<n; j++){
				if(a[j]>a[j+1]){
					swap(&a[j], &a[j+1]);
					isswap = true;
				}
			}
			if(isswap == false){
				break;
			}
		}
	}
	
	void selectionSort(int a[], int n){
		int min_idx;
		for(int i=0; i<n-1; i++){
			min_idx=i;
			for(int j=i+1; j<n; j++){
				if(a[j]<a[min_idx]){
					min_idx = j;
				}
			}
			swap(&a[i]), &a[min_idx];
		}
	}
	
	
	void insertionSort(int a[], int n){
		int key;
		for(int i=1; i<n; i++){
			key=a[i];
			for(int j=i-1; j>=0&&a[j]>key; j--){
				a[j+1] = a[j];
			}
			a[j+1] = key;
		}
	}
	
	
	void shellSort(int a[], int n){
		int key;
		for(int gap=n/2; gap>0; gap/=2){
			for(int i=gap; i<n; i++){
				key=a[i];
				for(int j=i; j>=0&&a[j-gap]>key; j-=gap){
					a[j]=a[j-gap];
				}
				a[j]=key;
			}
		}
	}
	
	
	
	int partition(int a[], int low, int high){
		int key=a[high];
		int i=low-1;
		for(int j=low-1; j<high; j++){
			if(a[j]<=key){
				i++;
				swap(&a[i], &a[j]);
			}
		}
		swap(&a[i+1], &a[high]);
		return i+1;
	}
	void quickSort(int a[], int low, int high){
		if(low<high){
			int p = partition(a, low, high);
			quickSort(a, low, p-1);
			quickSort(a, p+1, high);
		}
		
	}
	{% endhighlight %}

