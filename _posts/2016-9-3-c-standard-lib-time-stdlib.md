---
date: 2016-9-3 14:25:30+00:00
layout: post
title: C标准库time.h和stdlib.h小结
thread: 154
categories: c
tags: c

---

### time.h小结 ###

C语言标准库time.h定义了两个宏，声明了四种类型和几个操作时间的函数。定义的宏有：

1. NULL

2. CLOCKS_PER_SEC ：函数clock的返回值的每秒的时间单位数。

声明的类型有：

1. size_t

2. clock_t ： 表示时间的算术类型

3. time_t ： 表示时间的算术类型

4. struct tm ： 保存了一个日历时间的各组成部分

时间操作函数有：

1. clock_t clock(void) : 确定处理器使用的时间

2. double difftime(time_t t1,time_t t0) : 计算两个日历时间之差

3. time_t mktime(struct tm *timeptr) ：把timeptr指向的结构中的表示为本地时间的细分时间转换为一个日历时间值

4. time_t time(time_t *timer) : 确定当前的日历时间

5. char *asctime(const struct tm *timeptr) : 把timeptr指向的结构中的表示为本地时间的细分时间转换为一个字符串时间值

6. char ＊ctime(const time_t *timer) : 把日历时间转换为串形式的本地时间

7. struct tm *gmtime(const time_t *timer) : 把日历时间转换为UTC表示的细分时间

8. struct tm *localtime(const time_t *timer) : 把日历时间转换为本地时间的细分时间



### stdlib.h ###

c标准库定义和声明了那些没有明显的归属的宏和函数，可以分为6组：

整型算术函数：

1. abs ： 计算绝对值

2. div ： 除法运算

3. labs ： 函数labs和abs类似，只是参数和返回值都是long int类型。

4. ldiv ： 函数ldiv和div类似，只是参数和返回值都是long int类型。


算法函数：

1. void *bsearch(const void *key,const void *base, size_t nmemb, size_t size, int ( *compar)(congst void *, const void *)) ：函数bsearch搜索一个nmemb个对象的数组，来查找与key指向的对象匹配的元素，base指向这个数组的第一个元素，数组的每个元素大小由size决定。

2. void qsort(void *base, siez_t numb, size_t size, int( *compar)(const void *,const void *)) ：函数qsort对一个包含numb个对象的数组进行排序，其中第一个元素由base指向，数组的每个元素的大小由size指定。

3. int rand(void) : 计算一个伪随机整数序列 

4. void srand(unsigned int seed) : 使用参数作为一个新的伪随机序列的种子，如果使用相同的种子调用srand，那么伪随机序列就会重复。 

文本转换函数：

1. atof ：把nprt指向的字符串初始部分转换为double类型表示

2. atoi ：把nprt指向的字符串初始部分转换为int类型表示

3. atol ：把nprt指向的字符串初始部分转换为long类型表示

4. strtod ：把nprt指向的字符串初始部分转换为double类型表示

5. strtol ： 把nprt指向的字符串初始部分转换为long int类型表示

6. strtoul ：把nprt指向的字符串初始部分转换为unsigned long int类型表示

多字节转换函数：

1. void mblen(const char *s,size_t n) ：确定s指向的多字节中包含的字节数

2. int mbstowcs(wchar_t *pwc, const char *s,size_t n) ：确定s指向的多字节中包含的字节数,然后确定和这个多字节符对应的wchar_t类型的值的编码。

存储分配函数：

1. void ＊calloc(size_t nmemb, size_t size) ：函数calloc为numb个对象的数组分配空间，每个元素的大小为size，分配空间的所有位都被初始化为零，函数calloc返回一个空指针或指向一个分配的空间的指针。

2. void free(void *ptr) ：释放ptr指向的空间，释放的空间还可以再被分配，如果ptr是一个空指针，则不发生任何行为，如果参数与calloc、malloc或realloc之前返回的指针不匹配，或者指向的空间已经被free和realloc释放了，那么行为是未定义的。函数free没有返回值。

3. void *malloc(size_t size) ：函数malloc为一个对象分配空间，其中该对象的大小由size指定且对象的值是不确定的。函数malloc返回一个空指针或指向分配空间的指针。

4. void *realloc(void *ptr, size_t size) ：函数realloc将ptr指向的对象的大小改为友size指定的大小，如果新空间比较大，那对象新分配部分的值是不确定的。其余的和calloc类似。

环境接口：

1. void abort(void) ：函数使程序异常终止。

2. int atexit(void (*func)(void)) ：函数atexit注册func指向的函数，该函数在程序正常终止的时候被调用。如果注册成功，函数atexit返回零，否则返回非零。

3. void exit(int status) ：函数exit使程序的执行正常终止。

4. char *getenv(const char *name) ：函数getenv搜索宿主环境提供的环境表。

5. int system(const char *string) ：函数system把string指向的串传递给宿主环境。



参考：[Standard C 语言标准函数库速查](http://ganquan.info/standard-c/)



















 




















