---
date: 2016-6-25 19:24:30+00:00
layout: post
title: java中io和nio小结
thread: 146
categories: java
tags: java

---

I/O操作是编程中常用到的知识，在java中分为IO和NIO，I/O和NIO最重要的区别是数据打包和传输的方式，I/O以流的方式处理数据，是阻塞IO；NIO以块的方式处理数据，是非阻塞IO。在这篇中小结下。


### [I/O](http://docs.oracle.com/javase/tutorial/essential/io/index.html) ###

jva中的I/O操作类在java.io中，大概可以分为四组(其中在前三种中，I是从硬盘到内存；O是从内存到硬盘。)：

1. 基于字节操作的I/O接口：[InputStream](https://docs.oracle.com/javase/7/docs/api/java/io/InputStream.html)和[OutputStream](https://docs.oracle.com/javase/7/docs/api/java/io/OutputStream.html);

2. 基于字符操作的I/O接口：[Writer](https://docs.oracle.com/javase/7/docs/api/java/io/Writer.html)和[Reader](https://docs.oracle.com/javase/7/docs/api/java/io/Reader.html);

3. 基于磁盘操作的I/O接口：[File](https://docs.oracle.com/javase/7/docs/api/java/io/File.html);

4. 基于网络操作的I/O接口：[Socket](https://docs.oracle.com/javase/7/docs/api/java/net/Socket.html);


根据不同的使用场景，java中I/O子类可分为如下表：

Basic | InputStream | OutPutStream | Reader(InputStreamReader) | Writer(OutputStreamWriter)
:--|:--|:-- |:-- |:--
Arrays | ByteArrayInputStream | ByteArrayOutPutStream | CharArrayReader | CharArrayWriter
File | FileInputStream(RandomAccessFile) | FileOutPutStream(RandomAccessFile) | FileReader | FileWriter
Buffering | BufferedInputStream | BufferedOutPutStream | BufferedReader | BufferedWriter
Filtering | FilterInputStream | FilterOutPutStream | FilterReader | FilterWriter
String | StringBufferInputStream | ByteArrayOutputStream | StringReader | StringWriter
Data | DataInputStream | DataOutPutStream |   |   
Data-Formatted |   | PrintStream |   | PrintWriter
Pipes | PipedInputStream | PipedOutPutStream | PipedReader | PipedWriter
Parsing | PushbackInputStream(StreamTokenizer) |   | PushbackReader（LineNumberReader） |  
Objects | ObjectInputStream | ObjectOutPutStream |   |   
Utilities | SequenceInputStream |   |   |



### [NIO](https://docs.oracle.com/javase/7/docs/api/java/nio/package-summary.html) ###

相比原来的IO，NIO三个重要的特征是：

1. 通道(Channels)和缓存(Buffers);

2. 非阻塞IO

3. 选择器(Selectors)


#### 通道(Channels)和缓存(Buffers) ####

通道和流类似，但通道是双向的，可以同时用于读写；NIO中读写基本过程如下：

1. 读：从通道读取数据到缓冲区；

2. 写：用数据填充缓存区，让通道用这些数据执行写入操作。

java NIO中Channel实现如下：

1. FileChannel ：读文件或写文件；

2. DatagramChannel：基于UDP从网络中读取或写数据；

3. SocketChannel：基于TCP从网络中读写数据；

4. SerVerSocketChannel：服务器监听TCP连接。

java NIO中Buffers实现如下：

1. ByteBuffer

2. MappedByteBuffer

3. CharBuffer

4. DoubleBuffer

5. FloatBuffer

6. IntBuffer

7. LongBuffer

8. ShortBuffer

缓存区有三个状态变量：

1. position：类似数组，指向缓存区元素位置；

2. limit：缓存区中还有多少元素；

3. capacity：缓存区中最大数据容量。

缓存区常用方法：

1. flip() : (1)将limit设置为当前position；（2）将position设置为0。

2. clear() ：（1）将limit设置为与capacity相同；（2）将position设置为0。

3. 访问方法: get()和put()方法。

4. allocate()： 分配一个具有指定大小的缓存区

简单栗子如下：

	{% highlight java %}
	//use a FileChannel to read some data into a buffer
	RandomAccesFile file=new RandomAccesFile("example.txt","rw");
	FileChannel inChannel=file.getChannel();
	ByteBuffer buf=new ByteBuffer.allocate(48);
	int bytesRead=inChannel.read(buf);
	while(bytesRead!=-1)
	{
	    System.out.println("Read " + bytesRead);
	    buf.flip(); 
	    while(buf.hasRemaining())
	    {
	        System.out.print((char)buf.get());
	    }
		//重设缓冲区
	    buf.clear();
	    bytesRead=inChannel.read(buf);
	}
	file.close();
	{% endhighlight %}


#### 非阻塞IO ####

java IO中各种流是阻塞的。而java NIO是非阻塞模式，一个单独的线程可以管理多个输入或输出通道。

1. 一个线程从某通道发送请求读取数据，但是它仅能得到目前可用的数据，如果目前没有数据可用时，就什么都不会获取。而不是保持线程阻塞，所以直至数据变的可以读取之前，该线程可以继续做其他的事情。 

2. 一个线程请求写入一些数据到某通道，但不需要等待它完全写入，这个线程同时可以去做别的事情。 线程通常将非阻塞IO的空闲时间用于在其它通道上执行IO操作。


####　选择器(Selectors)　####

Java NIO的选择器允许一个单独的线程来监视多个输入通道，你可以注册多个通道使用一个选择器，然后使用一个单独的线程来“选择”通道：这些通道里已经有可以处理的输入，或者选择已准备写入的通道。这种选择机制，使得一个单独的线程很容易来管理多个通道。

简单栗子如下：

	{% highlight java %}
	/*1.打开一个Selector
	2.注册一个通道注册到这个Selector上
	3.监控这个Selector的四种事件（接受，连接，读，写）是否就绪
	*/
	Selector selector=Selector.open();
	channel.configureBlocking(false);
	SelectorKey key=channel.register(selector,SelectionKey.OP_READ);
	while(true)
	{
	    int readyChannels=selector.select();
	    if(readyChannels==0)
	    {
	        continue;
	    }
	    Set selectorKeys=selector.selectedKeys();
	    Iterator keyIterator=selectorKeys.iterator();
	    while(keyIterator.hasNext())
	    {
	        SelectionKey key=keyIterator.next();
	        if(key.isAcceptable())
	        {
	        //a connection was accepted by a ServerSocketChannel.
	        }
	        else if(key.isConnectable())
	        {
	        // a connection was established with a remote server.    
	        }
	        else if(key.isReadable())
	        {
	        // a channel is ready for reading   
	        }
	        else if(key.isWritable())
	        {
	        // a channel is ready for writing
	        }
	        keyIterator.remove();
	    }
	}
	{% endhighlight %}



参考：[Java IO Tutorial](http://tutorials.jenkov.com/java-io/index.html)

[Java NIO Tutorial](http://tutorials.jenkov.com/java-nio/index.html)

