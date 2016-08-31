---
date: 2016-8-28 11:18:30+00:00
layout: post
title: 使用Flex和Bison实现计算器程序
thread: 150
categories: compile
tags: compile

---

这两个月一直忙于一unity3d项目开发，没有坚持做笔记，惭愧。这两个月空余时间重新学习了下编译原理和c标准库的知识，在这实践下，利用Flex和Bison实现一个简易计算器程序。

在Unix环境中，常使用Lex和Yacc工具创建编译器，Lex 代表`Lexical Analyzar`。Yacc 代表 `Yet Another Compiler Compiler`。在GNU/Linux中，这两个工具对应于[Flex和Bison](http://dinosaur.compilertools.net/)。

### 编译器构建流程 ###

编译器可以大概分为3个步骤：

1. 词法分析器：将字符串转化成内部的表示结构，即token标记流；

2. 语法分析器：将词法分析得到的标记流Token生成一个语法树；

3. 生成目标代码：将语法树转化为目标代码。

其中，Flex用于词法分析，Bison用于语法分析。

### Flex小结 ###

[FLex](http://dinosaur.compilertools.net/flex/index.html)是一种生成扫描器的工具，扫描器事一种识别文本中词汇模式的程序。

Lex常用变量：

1. yyin : FILE*类型，指向lexer正在解析的当前文件；

2. yyout : FILE＊类型，指向记录lexer的输出位置，缺省情况下，yyin和yyout都指向标准输入和输出；

3. yytext : 匹配模式的文本存储在这个变量中(char*);

4. yyleng : 给出匹配模式的长度；

5. yylineno : 提供当前的行数信心。

Lex常用函数：

1. yylex(） : 这个函数开始分析，它由Lex自动生成；

2. yywrap() : 这个函数在文件或输入的末尾调用，可以返回1来表示解析的结束。


Flex编程可以分为三步：

1. 以lex可以理解的格式指定模式相关的动作；

2. 在这文件上运行lex，生成扫描器的C代码；

3. 编译和链接c代码，生成可执行的扫描器。

Lex程序生成的文件被称为分词器，它时一个函数，输入为字符流，只要发现一段字符能够匹配一个关键字，就会采取对应的动作。例如：

	{% highlight C++ %}
	%{
		#include <math.h>
	%}
	
	DIGIT    [0-9]
	ID       [a-z][a-z0-9]*
	
	%%
	
	{DIGIT}+    {
	            printf( "An integer: %s (%d)\n", yytext,
	                    atoi( yytext ) );
	            }
	
	{DIGIT}+"."{DIGIT}*        {
	            printf( "A float: %s (%g)\n", yytext,
	                    atof( yytext ) );
	            }
	
	if|then|begin|end|procedure|function        {
	            printf( "A keyword: %s\n", yytext );
	            }
	
	{ID}        printf( "An identifier: %s\n", yytext );
	
	"+"|"-"|"*"|"/"   printf( "An operator: %s\n", yytext );
	
	"{"[^}\n]*"}"     /* eat up one-line comments */
	
	[ \t\n]+          /* eat up whitespace */
	
	.           printf( "Unrecognized character: %s\n", yytext );
	
	%%
	
	main( argc, argv )
	int argc;
	char **argv;
	{
	    ++argv, --argc;  /* skip over program name */
	    if ( argc > 0 )
	            yyin = fopen( argv[0], "r" );
	    else
	            yyin = stdin;
	
	    yylex(); /* start the analysis*/
	 }
	{% endhighlight %}	

其中，flex中引用了正则，模式匹配规则和正则表达式类似。位于`%{`和`%}`之间的原封不动的导出到输出程序，段之间以`%%`分割。如果扫描器是用作Yacc开发的解析器的一部分，则只需要进行第一步和第二步。


### Bison小结 ###

Yacc的GNU版叫做Bison，将任何一种编程语言的所有语法翻译成针对此种语言的Yacc语法解析器，它用BNF(巴克斯范式)来书写，以.y为后缀。

使用Yacc或Bison创建一个编译起包括四个步骤：

1. 通过在语法文件上运行Yacc生成的一个解析器；

2. 说明语法：

 （1） 编写一个.y的语法文件；
  
  (2)  编写一个词法分析器来处理输入并将标记传递给解析器，使用lex完成；
  
  (3)  编写一个函数，通过调用yyparse()来进行解析；
  
  (4)  编写错误处理函数如yyerror();

  
3. 编译Yacc生成的代码及其他相关的源文件；

4. 将目标文件链接到适当可以执行解析器库。


BNF(巴克斯范式)是描述计算机语法的符号集，常用于定义编程语言的语法规则。BNF的内容如下：

1. 在双括号中字表示这些字符本身；

2. 在双括号外的字代表语法部分；

3. 尖括号内包含的为必选项；

4. 方括号内包含的为可选项；

5. 大括号内包含的为可以重复0至无数次的项；

6. 竖线表示在其左右两边任选一项，相当于or；

7. `::=`表示“被定义为”的意思。

例如： 利用BNF来定义java语言的for语句的实例：

	FOR_STATEMENT ::= 
	      "for" "(" ( variable_declaration | 
	  ( expression ";" ) | ";" ) 
	      [ expression ] ";" 
	      [ expression ] ";" 
	      ")" statement
	      

在yacc或Bison语法中，`::=`省略为`:`,如下为波兰逆序表示法计算器的语法规则：

	input:    /* empty */
	        | input line;
	
	line:     '\n'
	        | exp '\n'  { printf ("\t%.10g\n", $1); };
	
	exp:      NUM             { $$ = $1;         }
	        | exp exp '+'     { $$ = $1 + $2;    }
	        | exp exp '-'     { $$ = $1 - $2;    }
	        | exp exp '*'     { $$ = $1 * $2;    }
	        | exp exp '/'     { $$ = $1 / $2;    }
	        | exp exp '^'     { $$ = pow ($1, $2); }
	        | exp 'n'         { $$ = -$1;        };
	%%
	


### 使用flex和bison实现简易计算器 ###
 
 简易计算器功能有：加减乘除和负数、幂。优先级排序为幂－－》乘除－－》加减、负数，

词法分析文件lex.l如下：

	{% highlight C++ %}
	%{
	#include <stdio.h>
	#include <stdlib.h>
	#include <string.h>
	#include "grammar.tab.h"
	 
	#define TABSIZE 1000
	#define true 1
	#define false 0
	 
	char* var_names[TABSIZE];   
	int var_def[TABSIZE];      
	int n_of_names = 0;        
	 
	void reset()
	{
	    int j;
	    for(j = 0; j < TABSIZE; j++)
	        var_def[j] = false;
	}
	 
	int install(char *txt)
	{
	    int j; char *s;
	    if(n_of_names == 0) {
	        s = strdup(txt);
	        var_names[0] = s;
	        ++n_of_names;
	        return 0;
	    }
	    for(j = 0; j < n_of_names; ++j) {
	        if(strcmp(txt, var_names[j]) == 0) {
	            return j;
	        }
	    }
	     
	    s = strdup(txt);
	    var_names[j] = s;
	    ++n_of_names;
	    return j;
	}
	 
	%}
	 
	ALPHA   [a-z]|[a-z][a-z]
	NUM     [0-9]|[0-9][0-9]
	 
	%%
	 
	[ \n\t]                 { }
	 
	[0-9][0-9]*(\.[0-9]+)?  {
	    yylval.num = atof(yytext);
	    return NUMBER;
	}
	 
	{ALPHA}|{ALPHA}{NUM}    {
	    yylval.index = install(yytext);
	    return VARIABLE;
	}
	 
	.                       {
	    return yytext[0];
	}
	 
	%%
	 
	int yywrap(void)
	{
	    return 1;
	}
	{% endhighlight %}
	
	
语法分析文件grammary.y如下：

	{% highlight C++ %}
	%{
	#include <stdio.h>
	#include <stdlib.h>
	#include <string.h>
	#include <math.h>
	#include "grammar.tab.h"
	 
	#define TABSIZE 1000
	#define true 1
	#define false 0
	 
	/* the following were defined in lexana.l */
	extern char* var_names[TABSIZE];
	extern int var_def[TABSIZE];
	extern int n_of_names;
	extern int install(char *txt);
	extern void reset();
	 
	/* variables for the grammar file */
	int invalid = false;         
	double var_values[TABSIZE];     
	 
	int yyerror(const char *p) 
	{
	    fprintf(stderr, "%s\n", p); 
	    invalid = true;
	}
	 
	%}
	 
	%union {
	    double num;     
	    int index;  
	};
	 
	%start manycmds
	%token <index> VARIABLE
	%token <num> NUMBER
	%type <num> onecmd
	%type <num> expression
	%type <num> assignment
	%type <num> term
	%type <num> factor
	%type <num> primary
	 
	%%
	 
	manycmds : onecmd                           { }
	|   manycmds onecmd                         { }
	;
	 
	onecmd : expression ';'                     { if(!invalid) fprintf(stderr, "%lf\n", $1); invalid = 0; }
	|   assignment ';'                          { if(!invalid) fprintf(stderr, "%lf\n", $1); invalid = 0; }
	 
	expression : term                           { $$ = $1; }
	|   '-' term                                { $$ = -$2; }
	|   expression '+' term                     { $$ = $1 + $3; }
	|   expression '-' term                     { $$ = $1 - $3; }
	;
	 
	term : factor                               { $$ = $1; }
	|   term '*' factor                         { $$ = $1 * $3; }
	|   term '/' factor                         { if($3 == 0) yyerror("undefined"); else $$ = $1 / $3;  }
	;
	 
	factor : primary                            { $$ = $1; }
	|   primary '^' factor                      { $$ = pow($1, $3); }
	;
	 
	primary : NUMBER                            { $$ = $1; }
	|   VARIABLE                                { if(!var_def[$1]) yyerror("undefined"); else $$ = var_values[$1]; }
	|   '(' expression ')'                      { $$ = $2; }
	;
	 
	assignment : '@' VARIABLE '=' expression    { $$ = var_values[$2] = $4; var_def[$2] = 1; }
	;
	 
	%%
	 
	int main(void)
	{
	    reset();
	    yyparse();
	    return 0;
	}
	{% endhighlight %}
	
	
执行命令如下：

	bison -d grammar.y
	flex lex.l
	gcc grammar.tab.c lex.yy.c -lm -o calculator

执行结果如下：

	Mac-mini:Demo zx$ ./calculator 
	@a = 11;
	11.000000
	@b = 22;
	22.000000
	a+b;
	33.000000
	@c = (a+b)*2;    
	66.000000
	


参考： [The Lex & Yacc Page](http://dinosaur.compilertools.net/)

[Yacc 与 Lex 快速入门](https://www.ibm.com/developerworks/cn/linux/sdk/lex/)




 




















