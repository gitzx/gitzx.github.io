---
date: 2014-11-21 12:43:30+00:00
layout: post
title: luasocke使用小结
thread: 86
categories: cocos2d-x
tags: cocos2d-x
---

在cocos2d-x中，除了移植第三方网络库如libevent或asio等用于较复杂的网络通信，也会用到cocos2d-x自带的网络库用于简单的http请求如数据更新等。cocos2d-x3.x第三方库中自带有三个轻量级的网络库[curl](http://curl.haxx.se/)、[websocket](https://www.websocket.org/)、[luasocket](https://github.com/diegonehab/luasocket)，其中luasocket是cocos2d-x3.x新加入的。

luasocket是lua的网络模块库，可以方便的提供TCP、UDP、HTTP、FTP、SMTP、DNS、MIME等多种网络协议的访问操作，具体细节可以查看[Network support for the Lua language
](http://w3.impa.br/~diego/software/luasocket/reference.html)。在这简单小结下luasocket的基本用法。

###luasocke的安装部署###

cocos2d-x3.x的“cocos2d-x-3.3beta0\external\lua\luasocket”目录自带有luasocket，我们也可以单独安装部署luasocket来学习。

方法一：luasocket最新版3.0在[luasocket](https://github.com/diegonehab/luasocket)上，根据平台下载源码编译安装配置环境变量即可。

方法二：利用lua的应用包部署安装工具[LuaRocks](http://www.luarocks.org/)（类似python的egg或ruby的gem），利用命令`luarocks install luasocket`即可完成下载，再编译配置即可。在mac上，通过Homebrew工具命令`brew install luarocks`可以方便的安装luarocks。


###luasocket的简单用法###

luasocket分为两部分：一部分是C核心，为TCP、UDP传输层提供支持；另一部分是lua模块，主要是为SMTP、HTTP、FTP协议和上层应用接口提供支持。

	{% highlight C++ %}
	 //查询版本
	socket = require("socket")
	print(socket._VERSION)  //LuaSocket 2.0.2

	//URL简单使用
	url = require("socket.url")
	parsed_url = url.parse("http://www.example.com/cgilua/index.lua?a=2#there")
	
	//Http简单使用
	http = require("socket.http")
	print(http.request("http://www.163.com"))
	
	//echo服务器
	local socket = require("socket")
	local server = assert(socket.bind("*", 0))
	local ip, port = server:getsockname()
	print("telnet to localhost on port " .. port)
	print("10s to enter a line to be echoed")
	while 1 do
	  local client = server:accept()
	  client:settimeout(10)
	  local line, err = client:receive()
	  if not err then client:send(line .. "\n") end
	  client:close()
	end
	
	
	//smtp
	local smtp = require("socket.smtp")
	from = "<luasocket@163.com>"
	rcpt = {
	  "<hellolua@163.com>",
	  "<hellolua@126.com>",
	  "<hellolua@qq.com>"
	}
	mesgt = {
	  headers = {
	    to = "hello <cocos2dx@163.com>",
	    cc = "lua <cocos2dx@126.com>",
	    subject = "My first message"
	  },
	  body = "I hope this works."
	}
	r, e = smtp.send{
	  from = from,
	  rcpt = rcpt, 
	  source = smtp.message(mesgt)
	}
	{% endhighlight %}


参考：[Network support for the Lua language
](http://w3.impa.br/~diego/software/luasocket/reference.html)

