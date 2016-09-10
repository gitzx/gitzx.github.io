---
date: 2016-9-5 19:11:30+00:00
layout: post
title: C标准库stdio.h小结
thread: 155
categories: c
tags: c

---

C语言标准库stdio.h定义了用于输入和输出的函数、3种类型和宏。

三种类型有：

1. FILE ： 记录了控制流需要的所有信息

2. size_t 

3. fpos_t : 可以唯一指定文件中的每一个位置所需的所有信息

声明的宏有：

1. NULL ： 空值

2. _IOFBF : 表示完全缓冲

3. _IOLBF : 表示在线缓冲

4. _IONBF : 表示无缓冲

5. BUFFSIZ ： setbuf函数所使用的缓冲区大小

6. EOF ： EOF是负整数表示end哦分file

7. FOPEN_MAX （20）：同时打开的文件的最大数量

8. FILENAME_MAX ： 文件名的最大长度

9. L_tmpnam ： 整数，最大长度的临时文件名

10. SEEK_CUR ： 取得目前文件位置

11. SEEK_END ： 将读写位置移到文件尾时

12. SEEK_SET ： 将读写位置移到文件开头

13. TMP_MAX ： tmpnam最多次数

14. stderr ： 标准错误流，默认输出到屏幕，可输出到文件

15. stdin ： 标准输入流，默认为键盘

16. stdout ： 标准输出流，默认为屏幕

声明的函数：

对文件的操作：

1. int remove(const char *filename)

2. int rename(const char *old, const char *new)

3. FILE *tmpfile(void) : 创建一个临时的二进制文件，当这个文件关闭或者程序终止的时候会自动被移除

文件访问函数：

1. int fclose(FILE *stream) 

2. int fflush(FILE *stream) : 将所有未写入的数据传递给宿主环境，然后写入文件

3. FILE ＊fopen(const char *filename,const char *mode) : mode包括r、w、a、b组合

4. FILE ＊freopen(const char *filename,const char *mode,FILE *stream) : 打开名字为filename文件，并把它和stream指向的流关联在一起。

5. void setbuf(FILE *stream, char *buf) 和 int setvbuf(FILE *stream,char *buf,int mode,size_t size)

格式化输入输出函数：

1. int fprintf(FILE *stream,const char *format,...) : 格式化输出数据至文件

2. int fscanf(FILE *stream,const char *format,...) ： 格式化字符串输入

3. int pirntf(const char *format,...) ： 格式化输出数据

4. int scanf(const char *format,...) ： 格式输入函数

字符串输入／输出函数

1. int fgetc(FILE *stream) : 由文件中读取一个字符

2. char *fgets(char *s,int n,FILE *stream) : 文件中读取一个字符串

3. int fputc(int c, FILE *stream) : 将一指定字符写入文件流中

4. int fputs(const char *s,FILE *stream) : 将一指定的字符串写入文件内

5. int getc(FILE *stream) : 由文件中读取一个字符

6. int getchar(void) : 由标准输入设备内读进一字符

7. char *gets(char *s) : 由标准输入设备内读进一字符串

8. int putc(int c, FILE *stream) : 将一指定字符写入文件中

9. int putchar(int c) : 将制定的字符写到标准输出设备

10. int puts(const char *s) : 送一字符串到流stdout中

11. int ungetc(int c,FILE *stream) : 将指定字符写回文件流中

直接输入／输出函数

1.  size_t fread(void *ptr,size_t size,size_t nmemb,FILE *stream) : 从数据流读取数据

2.  size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream) : 将数据写入文件流

3. int fgetpos(FILE *stream, fpos_t *pos) : 移动文件流的读写位置

4. int fseek(FILE *stream, long int offset, int whence) : 移动文件流的读写位置

5. int fsetpos(FILE *stream, const fpos_t *pos) : 定位流上的文件指针

6. long int ftell(FILE *stream) : 取得文件流的读写位置

7. void rewind(FILE *stream) : 重设读取目录的位置为开头位置

错误处理函数：

1. void clearerr(FILE *stream) : 清空stream指向的流的文件结束符和错误提示符

2. int feof(FILE *stream) : 指向的流的文件结束符

3. int ferror(FILE *stream) : 指向stream指向的流的错误指示符

4. void perror(const char *s) : 打印出错误原因信息字符串




参考：[Standard C 语言标准函数库速查](http://ganquan.info/standard-c/)



















 




















