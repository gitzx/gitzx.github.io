---
date: 2013-11-26 12:54:30+00:00
layout: post
title: 使用SocketServer库进行分叉和线程处理多连接
thread: 04
categories: python 
tags:  python socket
---

###SocketServer：###
SocketServer模块简化了编写网络服务程序的任务。同时SocketServer模块也是Python标准库中很多服务器框架的基础。

SocketServer提供了4个基本的服务类：

- TCPServer针对TCP套接字流
- UDPServer针对UDP数据报套接字
- UnixStreamServer和UnixDatagramServer，针对UNIX域套接字

一个基于SocketServer的服务器示例：

		from SocketServer import TCPServer, StreamRequestHandler
		class Handler(StreamRequestHandler):
			def handle(self):
				addr = self.request.getpeername()
				print 'got connection from',addr
				self.wfile.write('connection')
		
		server = TCPServer(('',9000),Handler)
		server.serve_forever()


- 创建一个request handler class（请求处理类），继承自BaseRequestHandler class并重写它的handle()方法，该方法将处理到的请求。
- 实例化一个server class对象，并将服务的地址和之前创建的request handler class传递给它。
- 调用server class对象的handle_request() 或 serve_forever()方法来开始处理请求。

  BaseRequestHandler 子类方法可以接触到下面三个变量：

- request: 一个 socket 对象代表着客户端的请求。在 MirrorServer 例子里 socket.accept 也返回这样一个对象。

- rfile: 这个文件对应着从 socket 进来的数据。等同于调用 request.makefile(‘rb’) 。

- wfile: 这个文件对应着从 socket 发送的数据。等同于调用 request.makefile(‘wb’)。

###处理多连接：###

有3种主要的方法能处理多个连接：分叉（foking）、线程（threading）和异步I/O(asynthronous I/O).

SocketServer的四个基本的服务类默认是同步模型的。要想支持异步可以利用多继承从ForkingMixIn 或ThreadingMixInmix-in classes和一个基本的服务类继承来定义一个支持异步的服务类。

一个使用分叉技术的服务器示例：

	from SocketServer import TCPServer,ForkingMixIn,StreamRequestHandler
	class Server(ForkingMixIn,TCPServer):pass
	class Handler(StreamRequestHandler):
		def handler(self):
			addr = self.request.getpeername()
			print 'got connection from',addr
			self.wfile.write('connection')
	
	server = Server(('',9000),Handler)
	server.serve_forever()

关于fork，可参考酷壳上的[一个fork的面试题](http://coolshell.cn/articles/7965.html)

一个使用线程处理的服务器示例：

	from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler
	class Server(ThreadingMixIn,TCPServer):pass
	class Handler(StreamRequestHandler):
		def handler(self):
			addr = self.request.getpeername()
			print 'got connection from',addr
			self.wfile.write('connection')
		
	server = Server(('',5000),Handler)
	server.serve_forever()




