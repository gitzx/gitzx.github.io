---
date: 2016-8-31 19:16:30+00:00
layout: post
title: C标准库ctype.h小结
thread: 152
categories: c
tags: c

---

C语言标准库ctype.h头文件声明了几个可以用于识别和转换字符的函数，所有的函数都是int参数、返回int型，主要有：

1. isalnum	判别字符是否为英文或数字；

2. isalpha	判别字符是否为英文字母；

3. iscntrl	判别字符是否为ASSCII控制字符

4. isdigit	判别字符是否为十进制字符

5. isgraph	判别字符是否为除空格('')之外可以打印的字符

6. isprint	判别字符是否为包括空格('')可以打印的字符

7. ispunct	判别字符是否为标点符号或特殊符号

8. isspace	判断字符是否为标准空格字符：空格、回车、换页、换行、水平制表符和垂直制表符；

9. isupper	判别字符是否为大写英文字符；

10. isxdigit  判别字符是否为十六进制数字字符；

11. tolower	  把一个大写字母转换成相应的小写字母；

12. toupper	  把一个小写字母转换成相应的大写字母。


简单例子：

	{% highlight C++ %}
	＃include<ctype.h>
	void main()
	{
		char str[] = "123 abc@#EFG\n!?";
		for(int i=0;str[i]!=0;i++)
		{
			if(isalnum(str[i]) printf("isdigit or isalpha");
			if(isalpha(str[i])) printf("isalpha");
			if(iscntrl(str[i])) printf("is ASSCII");
			if(isdigit(str[i])) printf("isdigit");
			if(isgraph(str[i])) printf("is not space");
			if(isprint(str[i])) printf("is printf");
			if(ispunct(str[i])) printf("ispunct");
			if(isspace(str[i])) printf("isspace");
			if(isupper(str[i])) printf("isupper");
			if(isxdigit(str[i])) printf("isxdigit");
			if(isupper(str[i])) printf(tolower(str[i]));
			if(!isupper(str[i])) printf(toupper(str[i]));
		}
	}
	
	{% endhighlight %}



参考：[Standard C 语言标准函数库速查](http://ganquan.info/standard-c/)



















 




















