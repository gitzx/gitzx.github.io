---
date: 2014-11-11 12:08:30+00:00
layout: post
title: cocos2d-x 2.x和3.x版本中lua调用C/C++
thread: 84
categories: cocos2d-x
tags: cocos2d-x
---

cocos2d-x 2.x版本是利用toLua++方式来实现lua对C/C++的调用，这个方式步骤比较繁琐，cocos2d-x 3.x版本利用bindings-generator代替了toLua++。在这一篇中比较下toLua++和bingdings-generator这两种调用方式。

###toLua++方式###

（1）基本步骤

toLua++是把C/C++和lua代码结合使用的一种工具，利用toLua++把C/C++注册到lua环境的标准步骤如下：

- 根据C/C++函数或类，将要导出的函数、对象或类定义写入.pkg文件(package文件)中，注意需要按照toLua++的规定，如移除private成员、函数或对象方法为静态函数等；

- 建立用于桥接C/C++和Lua之间的C/C++的.h头文件，运行 tolua++ 工具，将 .pkg 文件编译为目标 .cpp 文件；

- 将目标 .cpp 文件加入项目，在启用 Lua 虚拟机后调用目标文件中的 open() 函数注册导出的内容。

（2）简单示例如下：


	{% highlight C++ %}
	//MyClass.h
	class MyClass{
	public:
		MyClass(){};
		int foo(int i);
	};
	
	//MyClass.cpp
	#include "MyClass.h"
	int MyClass::foo(int i){
		return i+100;
	}
	
	//MyClass.pkg
	class MyClass
	{
		MyClass();
		int foo(int i);
	};
	
	//MyLuaModule.h
	extern "C"
	{
		#include "tolua++.h"
	}
	#include "MyClass.h"
	TOLUA_API int tolua_MyLuaModule_open(lua_State *L);
	
	//MyLuaModule.pkg
	$#include "MyLuaModule.h"
	$pfile "MyClass.pkg"
	
	//main.cpp
	extern "C"{
		#include "lua.h"
		#include "lauxlib.h"
		#include "lualib.h"
	}
	#include "MyLuaModule.h"
	int main(){
		lua_State *L=lua_newstate();
		luaL_openlibs(L);
		tolua_MyLuaModule_open(L);
		luaL_dofile(L, "main.lua");
		lua_close(L);
		return 0;
	}
	
	//main.lua
	local test = MyClass:new();
	print(test:foo(99))
	{% endhighlight %}


其中，一个package文件可以包括其他的package文件。一般的格式是：

`$pfile "include_file"`

一个package文件同样可以包括一般的C/C++头文件，使用hfile或cfile指令：

`$#include "example.h"`

最后，lua文件可以被包括在package文件里，使用$lfile:

`$lfile "example.lua"`


（3）编译运行：

	//生成MyLuaModule.cpp
	tolua++ -o MyLuaModule.cpp MyLuaModule.pkg
	
	//编译C++
	g++ MyClass.cpp MyLuaModule.cpp main.cpp -llua -ltolua++
	
	//运行显示199
	./a.out

（4）toLua++实现原理

tolua++实现基于lua调用C/C++，这里待补充，可以参考这篇博客[tolua++实现分析](http://blog.csdn.net/wtyqm/article/details/8977975)

###bindings-generator方式###


（1）基本步骤

bindings-generator方式底层使用toLua++的库函数，利用python脚本来解析C/C++，自动生成所需的C/C++代码，binding脚本位于`\cocos2d-x-3.3beta0\tools\tolua`下的`genbindings.py`。

- 定义一个ini文件，可以根据`\cocos2d-x-3.3beta0\tools\tolua`下的ini文件进行复制改写。

- 修改`genbindings.py`脚本，将定义的ini文件加进去，执行`genbindings.py`脚本,生成的C/C++文件在`\cocos2d-x-3.3beta0\cocos\scripting\lua-bindings\auto`目录下；

- 将生成的C/C++加入到工程中，修改AppDelegate.cpp，将C/C++注册到Lua环境中。

（2）简单示例

	{% highlight C++ %}
	//定义C++类
	//classes/MyClass.h
	#include "cocos2d.h"
	
	using namespace cocos2d;
	
	class MyClass : public Ref
	{
	public:
	  MyClass()   {};
	  ~MyClass()  {};
	  bool init() { return true; };
	  CREATE_FUNC(MyClass);
	
	  int foo(int i);
	};
	
	//classes/MyClass.cpp
	#include "MyClass.h"
	
	int MyClass::foo(int i)
	{
	  return i + 100;
	}
	
	//编写.ini文件
	//cocos2d-x-3.3beta0/tools/tolua/MyClass.ini
	[MyClass]
	prefix           = MyClass
	target_namespace = my
	headers          = %(cocosdir)s/../Classes/MyClass.h
	classes          = MyClass
	
	//修改genbindings.py，将MyClass.ini加进去
	cmd_args = {'cocos2dx.ini' : ('cocos2d-x', 'lua_cocos2dx_auto'), \
	            'MyClass.ini' : ('MyClass', 'lua_MyClass_auto'), \
	            ...
	
	//执行python genbindings.py
	
	//修改AppDelegate.cpp文件，加入对lua_MyClass_auto.hpp文件的引用 
	#include  "lua_MyClass_auto.hpp"     
	
	//在代码使用中加入register_all_MyClass函数的调用  
	register_all_MyClass(stack->getLuaState());  
	
	//在工程中导入如下四个文件
	//MyClass.h  MyClass.cpp 
	//lua_MyClass_auto.hpp 
	//lua_MyClass_auto.cpp
	
	//在lua中调用MyClass类
	local test = my.MyClass:create()
	print("lua bind: " .. test:foo(99))
	{% endhighlight %}


参考：

[tolua++实现分析](http://blog.csdn.net/wtyqm/article/details/8977975)

[tolua++ - Home](http://www.codenix.com/~tolua/)

[如何使用 bindings-generator 自动生成 lua绑定](http://cn.cocos2d-x.org/article/index?type=wiki&url=/doc/cocos-docs-master/manual/framework/native/wiki/how-to-use-bindings-generator/zh.md)

[Cocos2d-x下Lua调用自定义C++类和函数的最佳实践](http://segmentfault.com/blog/hongliang/1190000000631630)

[cocos2d-x 3.0 + lua 开发问题与解决吐槽](http://www.cocoachina.com/bbs/read.php?tid=200145)


