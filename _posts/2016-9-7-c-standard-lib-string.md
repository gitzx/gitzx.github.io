---
date: 2016-9-7 16:50:30+00:00
layout: post
title: C标准库sring.h小结
thread: 156
categories: c
tags: c

---

C语言标准库string.h声明了一种类型和一些函数，并定义了一个宏。声明的类型是size_t且定义的宏是NULL，声明的函数可以对以下三种形式的串进行操作：

1. 名字以mem开头的函数对任意的字符序列进行操作，其中一个参数s指向字符串的起始位置，另一个参数n对元素的个数进行计数；

2. 名字以strn开头的函数对非空字符序列进行操作，其中一个参数s指向字符串的起始位置，另一个参数n对元素的个数进行计数；

3. 以str开头的函数对空字符串结尾的字符序列进行操作，这些函数只使用参数s来确定串的开头。

string.h声明的字符串可以分为：

复制函数：

1. void ＊memcpy(void *s1, void *s2, size_t n) : 从s2指向的对象中复制n个字符到s1指向的对象中。返回s1的值

2. void *memmove(void *s1,const void *s2, size_t n) : 从s2指向的对象中复制n个字符到s1指向的对象中。函数返回s1的值

3. char *strcpy(char *s2, congst char *s2) ：把s2指向的字符串(包括终止的空字符)复制到s1指向的数组中。函数返回s1的值

4. char *strncpy(char *s1, const char *s2,size_t n) : 从s2指向的数组中复制最多n个字符(不包括空字符后面的字符)到s1指向的数组中，如果s2指向的数组是一个比n短的字符串，则在s1指向的数组后添加空字符，直到写入n个字符，函数返回s1的值

连接函数：

1. char *strcat(char *s1,const char *s2) : 把s2指向的串(包括终止的空字符)的副本添加到s1指向的串的末尾，s2的第一个字符覆盖s1的末尾的空字符。函数返回s1的值。

2. char *strncat(char *s1,const char *s2,size_t n) : 从s2指向的数组中奖最多n个字符(不包括空字符及后面的字符)添加到s1指向的串的末尾，s2的第一个字符覆盖s1末尾的空字符。函数返回s1的值。

比较函数：

1. int memcmp(const void *s1,const void *s2,size_t n) : 将s1指向的对象的前n个字符和s2指向的对象的前n个字符进行比较。大于等于或者小于则返回大于等于或小于零的整数。

2. int strcmp(const char *s1, const char *s2) : 函数strcmp对s1指向的串和s2指向的串进行比较

3. int strncmp(const char *s1,const char *s2,size_t n) : 对s1和s2指向的数组中的最多n个字符(空字符后面的字符不参加比较)进行比较

4. int strcoll(const char *s1, cosnt char *s2) ：对s1指向的串和s2指向的串进行比较，只是比较时串都被解释为适合当前区域设置的类别LC_COLLATE的形式。

查找函数：

1. void *memchr(const void *s,int c,size_t n) : 确定c(转换为unsigned char类型)在s指向的对象的前n个字符中第一次出现的位置。

2. char *strchr(const char *s, int c) ： 确定c(转换为char类型)在s指向的串中第一次出现的位置，终止符被认为是串的一部分。

3. size_t strcspn(const char *s1,const char *s2) : 计算s1指向的字符串完全由不是s2指向的串中的字符组成的最大初始段的长度。函数返回段的长度。

4. char *strpbrk(const char *s1, const char *s2) : 确定s2指向的串中的任意字符在s1指向的串中第一次出现的位置。

5. char *strrchr(const char *s, int c) : 函数strrchr确定c(转换为char类型)在s指向的串中最后一次出现的位置。

6. size_t strspn(const char *s1,const char *s2) : 计算s1指向的字符串中完全由s2指向的串中的字符组成的最大初始段的长度。

7. char *strstr(const char *s1,const char *s2) : 确定s2指向串的字符序列(不包括终止的空字符)在s1指向的串中第一次出现的位置。

8. char *strtok(char *s1,const char *s2) : 把s1指向的串分解为一系列记号，每个记号都是由s2指向的串中的字符界定。

其他的函数：

1. void *memset(void *s,int c,size_t n) : 把c(转换为unsigned char类型)的值复制到s指向的对象的前n个字符的每个字符中。函数返回s的值。

2. char *strerror(int errnum) : 将errnum中的错误编号对应到一个错误信息中。

3. size_t strlen(const char *s) : 计算s指向的串的长度。





参考：[Standard C 语言标准函数库速查](http://ganquan.info/standard-c/)



















 




















