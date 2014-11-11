---
date: 2014-11-11 12:08:30+00:00
layout: post
title: lua和C/C++的相互调用
thread: 83
categories: cocos2d-x
tags: cocos2d-x
---

cocos2d-x 2.x版本是利用toLua++方式来实现lua和C/C++的相互调用，这个方式步骤比较繁琐，cocos2d-x 3.x版本利用bindings-generator代替了toLua++。在这一篇中总结下lua中C API，lua和C/C++的相互调用，在下一篇中比较下toLua++和bingdings-generator这两种调用方式。

###lua中的C API###

（1）为了使用lua中的C API，需安装lua和liblua，在debian或ubuntu系统中，使用`sudo apt-get install lua5.1`和`sudo apt-get install liblua5.1-0-dev`即可完成安装配置。

（2）Lua和C的两大差异：

- Lua使用垃圾回收，C语言需要显示释放内存；

- Lua使用动态类型，C语言使用静态类型


（3）lua和C/C++之间有两种交换形式：

- C/C++拥有控制权，Lua作为一个库，这种形式的C/C++代码称为“应用程序代码”；

- Lua拥有控制权，C/C++作为一个库，此时C/C++称为“库代码”。

其中，“应用程序代码”和“库代码”都使用同样的C API来与Lua通信。

（4）简单示例：

	#include <stdio.h>
	#include <string.h>
	#include "lua.h" //若为C++则#include"lua.hpp"
	#include "lauxlib.h"
	#include "lualib.h"
	int main()
	{
		char buff[256] = "print(\"hello lua\")"; 
		int errror;
	   //打开lua，所有的C API都需要
	   //该指针作为第一个参数
		lua_State *L = luaL_newstate(); 
		luaL_openlibs(L); //打开标准库
		while(fgets(buff, sizeof(buff),stdin) != NULL){
			error = luaL_loadbuffer(L,buff,strlen(buff),"line") ||lua_pcall(L,0,0,0);
			if(error){
				fprint(stderr,"%s",lua_tostring(L,-1)); 
				//从栈中弹出错误信息
				lua_pop(L,1); 
			}
		}
		//释放状态指针所引用的资源
		lua_close(L);
		return 0;
	}

(5)栈的使用。根据lua和c的两大差异，lua和C通过一个虚拟栈来实现数据交换。。在C/C++程序中，如果要获取Lua的值，只需调用Lua的C API函数，Lua就会将指定的值压入栈中。要将一个值传给Lua时，需要先将该值压入栈，然后调用Lua的C API，Lua就会获取该值并将其从栈中弹出。为了可以将不同类型的值压入栈，以及从栈中取出不同类型的值，Lua为每种类型均设定了一个特定函数。

	//压入元素，lua调用C时，栈中至少会有20个空闲的槽
	void lua_pushnil(lua_State *L);
	void lua_pushboolean(lua_State *L,int bool);
	void lua_pushnumber(lua_State *L,lua_Number n);
	void lua_pushinteger(lua_State *L,lua_Integer n);
	void lua_pushlstring(lua_State *L, const char *s, size_t len);
	void lua_pushstring(lua_State *L, const char *s);
	//检查栈中是否有足够的空间
	int lua_checkstack(lua_State *L, int sz);
	
	//栈底元素索引为1，栈底上面一个为2，-1表示栈顶元素
	//查询元素，*可为任意Lua类型,成功返回1，是吧返回0
	int lua_is*(lua_State *L,int index);
	
	//获取元素类型，常用swith中
	int lua_type (lua_State *L, int index);
	
	//lua_to*函数用于从栈中获取一个值 
	//如果调用失败，lua_toboolean、lua_tonumber、lua_tointeger
	//和lua_objlen均返回0，而其他函数则返回NULL
	int lua_toboolean(lua_State *L,int index);
	lua_Number lua_tonumber(lua_State *L, int index);
	lua_Integer lua_tointeger(lua_State *L, int index);
	const char *lua_tolstring(lua_State *L,int index,size_t *len);
	size_t lua_objlen(lua_State *L, int index);
	
	//其他栈操作
	//返回栈中元素的个数。
	int lua_gettop(lua_State* L); 
	//将栈顶设置为它的当前值。
	void lua_settop(lua_State* L, int index);
	//将指定索引的元素副本压入栈。
	void lua_pushvalue(lua_State* L, int index); 
	//删除指定索引上的元素，其上面的元素自动下移。
	void lua_remove(lua_State* L, int index); 
	//将栈顶元素插入到该索引值指向的位置。
	void lua_insert(lua_State* L, int index); 
	//弹出栈顶元素，并将该值设置到指定索引上。
	void lua_replace(lua_State* L, int index); 

（6）C API的错误处理

C没有提供异常处理机制，lua使用了C语言中的setjmp机制（类似异常处理机制）。

对于“应用程序代码”中的错误，通常是让代码在“保护模式”下运行，通过调用`lua_pcall`来运行lua代码；

对于库代码中的错误，通过调用`lua_error`，`lua_error`函数会清理lua中所用需要清理的东西，然后跳转会发起执行的那个`lua_pcall`，并附上一条错误消息。

###C/C++调用Lua###

C/C++调用lua函数的基本协议是c向lua传递参数，从lua中获取结果。

（1）基本调用

	//ccalllua.cpp
	#include <stdio.h>
	#include <string.h>
	//若为C程序，则删除extern "C"
	extern "C"{
		#include <lua.h>
		#include <lauxlib.h>
		#include <lualib.h>
	}

	void load(lua_State *L,const char *fname,int *w,int *h)
	{
		if(luaL_loadfile(L,fname)||lua_pcall(L,0,0,0))
			error(L,"cannot run file:%s",lua_tostring(L,-1));
		lua_getglobal(L,"width");
		lua_getglobal(L,"height");
		if(!lua_isnumber(L,-1)||!lua_isnumber(L,-2))
			errror("height or width should be number\n");
		*w = lua_tointeger(L, -2);
		*h = lua_tointeger(L, -1);
	}
	
	int main(){
		lua_State *L=luaL_newstate();
		int w, h;
		load(L,"size.lua", &w, &h);
		printf("width=%d, height=%d\n", w,h);
		lua_close(L);
		return 0;
	}
	
	//size.lua
	if getenv("DISPLAY")==":0.0" then
		width=300; height=300
	else
		width=200; height =200
	end

（2）编译运行

安装lua和liblua后，需配置环境变量，通过如下命令即可运行：

	g++ -o ccalllua ccalllua.cpp -llua -llualib
	./ccalllua

###Lua调用C/C++###

当Lua调用C函数时，使用了一个与C语言调用Lua时相同的栈。C函数从栈中获取函数参数，并将结果压入栈中，为了在栈中将函数结果与其他值区分开，C函数还应返回其压入栈中的结果数量。

所有注册到Lua中的函数都有相同的原型，即是定义在lua.h中的lua_CFunction:

`typedef int (*lua_CFunction)(lua_State *L);`

(1)以C函数形式作为程序一部分

	//luacallc.c
	#include <stdio.h>
	#include "lua.h"
	#include "lualib.h"
	#include "lauxlib.h"
	
	static int average(lua_State *L){
		//获取栈中数量
		int n = lua_gettop(L);
		double sum = 0;
		for(int i=1;i<=n;i++){
			sum += lua_tonumber(L, i);
		}
		lua_pushnumber(L, sum/n);
		lua_pushnumber(L, sum);
		//
		return 2;
	}
	
	int main(){
		lua_State *L = lua_newstate();
		luaL_openlibs(L);
		//注册函数
		lua_register(L, "average", average);
		luaL_dofile(L, "avg.lua");
		lua_close(L);
		getchar();
		return 0;
	}
	
	//avg.lua
	//call a C++ function
	avg, sum = average(10, 20, 30, 40, 50)
	print("The average is ", avg)
	print("The sum is ", sum)


以C函数形式作为程序一部分,这种调用和C调用lua的区别在于参数和结果的传递和获取方式，同样，通过如下命令即可运行：

	g++ -o luacallc luacallc.c -llua -llualib
	./luacallc

（2）将C注册为lua的模块

Lua模块式一个程序块，定义了一些lua函数，这些函数通常存储为table条目。编写使用C模块的主要步骤有：

- 定义一些C函数和一个公共函数（相当于Lua模块的主程序块），C模块中只有一个公共（外部）函数，其他所有函数都是私有的，在C语言中声明为static；

- 声明一个数组，包含模块中所有的函数和名称，这些数组元素的类型为luaL_Reg结构，该结构有两个字段，一个字符串和一个函数指针，数组的最后一个元素总是`{NULL,NULL}`，以此来标识结尾；

- 编写C模块后，必须将其链接到解释器，如果Lua解释器支持动态链接，可使用动态链接机制生成动态链接库，然后使用require从Lua中加载该模块.

Lua通过使用函数地址来直接调用它们，即只依赖注册时传入的函数地址
 
	//luacallcmodule.c
	#include <stdio.h>
	#include "lua.h"
	#include "lualib.h"
	#include "lauxlib.h"
	
	static int add(lua_State* L) 
	{
	    double op1 = luaL_checknumber(L,1);
	    double op2 = luaL_checknumber(L,2);
	    lua_pushnumber(L,op1 + op2);
	    return 1;
	}
	
	static int sub(lua_State* L)
	{
	    double op1 = luaL_checknumber(L,1);
	    double op2 = luaL_checknumber(L,2);
	    lua_pushnumber(L,op1 - op2);
	    return 1;
	}
	
	static const struct luaL_Reg mylibs[] = { 
	    {"add", add},
	    {"sub", sub},
	    {NULL, NULL} 
	}; 
	
	int luaopen_mytestlib(lua_State* L) 
	{
	    const char* libName = "mytestlib";
	    luaL_register(L,libName,mylibs);
	    return 1;
	}
	
	
	//luacallcmodule.lua
	//生成动态链接库.so或.dll，指定包名
	require "mytestlib"  
	//在调用时，必须是package.function
	print(mytestlib.add(1.0,2.0))
	print(mytestlib.sub(20.1,19))

如果解释器不支持动态链接，必须用心的模块来重新编译Lua，此外，还需要以某种方式告诉解释器，应该在打开一个新状态的同时打开这个模块，最简单的做法是，将上面的`luaopen_mytestlib`加到luaL_openlibs会打开的标准库列表中，这个列表在文件linit.c中。


参考：

[Calling C++ Functions From Lua](http://gamedevgeek.com/tutorials/calling-c-functions-from-lua/)

[Step By Step(Lua调用C函数)](http://www.cnblogs.com/stephen-liu74/archive/2012/07/23/2469902.html)

[Sample Code](http://lua-users.org/wiki/SampleCode)

