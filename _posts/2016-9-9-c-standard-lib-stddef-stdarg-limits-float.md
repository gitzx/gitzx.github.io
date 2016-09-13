---
date: 2016-9-9 12:24:30+00:00
layout: post
title: C标准库stddef.h/stdarg.h/limits.h/float.h小结
thread: 157
categories: c
tags: c

---

在由于种种原因而不能支持完整的c标准库的环境，c标准需要一个独立的实现来支持这个语言本身的所有特性。对于c标准库来说，这只要提供4个标准头文件定义的功能就可以了，这4个头文件是：

1. stddef.h ： 定义了一些类型和宏，许多定义也会出现在乞讨的头文件中。

2. stdarg.h : 提供了遍历可变参数表时需要的宏

3. limits.h ： 描述了整数表示的属性

4. float.h ： 描述了浮点数表示的属性


### stddef.h ###

stddef.h提供了3个类型定义和2个宏。

三个类型定义如下：

1. typedef ptrdiff_t : 两个指针相减的结果

2. typedef size_t : 是sizeof一个关键词得到的无符号整数值。

3. typedef wchar_t ： 是一个宽字符常量的大小，是整数类型。

定义了两个宏：

1. NULL ： 空指针的常量值

2. offsetof(type, member-designator) : 这个宏返回一个结构体成员相对于结构体起始地址的偏移量(字节为单位)，type是结构体的名字，member-designator是结构体成员的名字。


### stdarg.h ###


stdarg.h头文件声明了1中类型和定义了3个宏，当函数参数未知时去获取函数的参数。

声明的类型是： 

va_list ： 保存宏va_start、va_arg、va_end所需要的消息的类型。

定义的宏有：

1. void va_start(va_list ap, parmN) : 对ap进行初始化，以便后面va_arg和va_end对它的使用，参数parmN是函数定义(在......之前的那个)的可变参数表中最右边参数的标志符。要在访问所有未命名的参数之前调用宏va_start

2. type va_arg(va-list ap,type) : 宏va_arg展开为一个表达式，这个表达式的类型和值跟调用的下一个参数的相同。第一次调用va_start后，对va_arg的第一次调用返回的是parmN指定的参数后面的的参数值，后面的调用依次返回剩下的参数值。

3. void va_end(va_list ap) : 宏va_end促进函数的正常返回，该函数的可变参数表被初始化了va_list ap的va_start的扩展所引用。函数没有返回值。

简单栗子：

	{% highlight C++ %}
	＃include <stdarg.h>
	#define MAXARGS 31
	void f1(int n_ptrs, ...)
	{
		va_list ap;
		char *array[MAXARGS];
		int ptr_no = 0;
		if(n_ptrs > MAXARGS)
		{
			n_ptrs = MAXARGS;
		}
		va_start(ap,n_ptrs);
		while(ptr_no<n_ptrs)
		{
			array[ptr_no++] = va_arg(ap,char *);
		}
		va_end(ap);
		f2(n_ptrs, array);
	}
	{% endhighlight %}


### limits.h ###

limit.h中定义的宏都可以使用#if预处理指令测试。定义的宏有：

1. CHAR_BIT : 一个ASCII字符长度

2. SCHAR_MIN ： 字符型的最小值

3. SCHAR_MAX ： 字符型的最大值

4. UCHAR_MAX ： 无符号字符型的最大值

5. CHAR_MIN ： char字符的最小值

6. CHAR_MAX ： char字符的最大值

7. MB_LEN_MAX ： 一个字符所占最大字节数

8. SHRT_MIN ： 最小短整型

9. SHRT_MAX ： 最大短整型

10. USHRT_MAX ： 最大无符号短整型

11. INT_MIN： 最小整型

12. INT_MAX ： 最大整型

13. UINT_MAX ： 最大无符号整型

14. LONG_MIN ： 最小长整型

15. LONG_MAX ： 最大长整型

16. ULONG_MAX ： 无符号长整型


### float.h ###


float.h头文件定义了浮点型数值的最大最小限，浮点型数值以以下方面的方式定义：符号－value E 指数 符号是正负，value是数字的值

在所有的实例中FLT指的是float，DBL指的是double，LDBL指的是long double

float.h定义的宏：

1. FLT_ROUNDS ： 定义了浮点型数值四舍五入的方式，－1表示不确定，0是向0，1是向最近，2是向无穷大，3是负无穷大

2. FLT_RADIX 2 ： 定义指数的基本表示(如base－2是二进制，base－10是十进制，16是十六进制)

3. FLT_MANT_DIG， DBL_MANT_DIG， LDBL_MANT_DIG ： 定义数值里数字的个数

4. FIT_DIG 6， DBL_DIG 10， LDBL_DIG 10 ： 在四舍五入之后能不更改表示的最大小数位

5. FIT_MIN_EXP， DBL_MIN_EXP， LDBL_MIN_EXP ： FIT_READIX的指数的最小负整数值

6. FIT_MIN_10_EXP -37, DBL_MIN_10_EXP -37, LDBL_MIN_10_EXP -37 : 10进制表示法的指数的最小负整数值

7. FLT_MAX_EXP，DBL_MAX_EXP，LDBL_MAX_EXP ： FLT_RADIX 的指数的最大整数值

8. FLT_MAX_10_EXP +37，DBL_MAX_10_EXP +37，LDBL_MAX_10_EXP +37 ： 10进制表示法的的指数的最大整数值

9. FLT_MAX 1E+37，DBL_MAX 1E+37，LDBL_MAX 1E+37 ： 浮点型的最大限

10. FLT_EPSILON 1E-5，DBL_EPSILON 1E-9，LDBL_EPSILON 1E-9 ：能表示的最小有符号数




参考：[Standard C 语言标准函数库速查](http://ganquan.info/standard-c/)



















 




















