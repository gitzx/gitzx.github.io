---
date: 2014-4-18 21:19:30+00:00
layout: post
title: 线程库pthread的使用小结
thread: 56
categories: c++
tags: c++
---

C++11提供了std::thread用于多线程开发，除此之外，在linux上，最常见的线程库就是pthread了。 

Pthreads定义了一套C语言的类型、函数和常量，它以pthread.h头文件和一个线程库实现。

Pthreads API中大致共有100个函数调用，全部以“pthread_”开头，可以分为四类：

- 线程管理。如创建线程、等待线程、查询线程状态等；

- Mutex。如创建、摧毁、锁定、解锁、设置属性等操作；

- Condition Variable.如创建、摧毁、等待、通知、设置和查询属性等操作；

- 使用了读写锁的线程间的同步管理。

###常用函数###

(1)线程创建

int pthread_create();