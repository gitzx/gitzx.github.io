---
date: 2013-11-27 18:45:30+00:00
layout: post
title: IOS沙盒（sandbox）和文件操作
thread: 06
categories: ios 
tags:  ios
---

###IOS沙盒###

 iOS的沙盒机制，应用只能访问自己应用目录下的文件。iOS不像android，没有SD卡概念，不能直接访问图像、视频等内容。iOS应用产生的内容，如图像、文件、缓存内容等都必须存储在自己的沙盒内。

IOS应用程序只能在为该改程序创建的文件系统中读取文件，不可以去其它地方访问，此区域被成为沙盒，所以所有的非代码文件都要保存在此，例如图像，图标，声音，映像，属性列表，文本文件等。

- 每个应用程序都有自己的存储空间
- 应用程序不能翻过自己的围墙去访问别的存储空间的内容
- 应用程序请求的数据都要通过权限检测，假如不符合条件的话，不会被放行。

###打开模拟器沙盒目录###


沙盒文件都在个人用户名文件夹下的一个隐藏文件夹里，中文叫资源库，目录其实是Library。默认情况下，每个沙盒含有3个文件夹：Documents, Library 和 tmp。设置查看隐藏文件的方法如下：打开终端，输入命名：

- 显示Mac隐藏文件的命令：`defaults write com.apple.finder AppleShowAllFiles -bool true`
- 隐藏Mac隐藏文件的命令：`defaults write com.apple.finder AppleShowAllFiles -bool false`

重新启动Finder就可以了重启Finder：鼠标单击窗口左上角的苹果标志-->强制退出-->Finder-->前往->前往文件夹，输入/Users/username/Library/Application Support/iPhone Simulator/ 前往。

###IOS沙盒和文件操作：###

	//获取程序的Home目录
    NSString *homeDirectory = NSHomeDirectory();
    NSLog(@"path:%@",homeDirectory);
    //获取document目录
    NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentationDirectory, NSUserDomainMask, YES);
    NSString *docDir = [paths objectAtIndex:0];
	NSLog(@"document path:%@",docDir);
    if(!docDir){
        NSLog(@"Documents not foud");
    }
	//写入文件
    NSArray *array = [[NSArray alloc]initWithObjects:@"neirong",@"content", nil];
    NSString *filePath = [docDir stringByAppendingPathComponent:@"testFile.txt"];
    [array writeToFile:filePath atomically:YES];
    NSLog(@"%@",array);
    //读取文件
    NSArray *array_output = [[NSArray alloc]initWithContentsOfFile:filePath];
    NSLog(@"%@",array_output);
    //利用NSFileManager在documents里创建目录
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSString *testDirectory = [docDir stringByAppendingPathComponent:@"test"];
    [fileManager createDirectoryAtPath:testDirectory withIntermediateDirectories:YES attributes:nil error:nil];
    //在test目录下创建文件并获取文件名
    NSString *testPath = [testDirectory stringByAppendingPathComponent:@"test00.txt"];
    NSString *testPath2 = [testDirectory stringByAppendingPathComponent:@"test22.txt"];
    NSString *testPath3 = [testDirectory stringByAppendingPathComponent:@"test33.txt"];
    NSString *string = @"write String";
    [fileManager createFileAtPath:testPath contents:[string dataUsingEncoding:NSUTF8StringEncoding] attributes:nil];
    [fileManager createFileAtPath:testPath2 contents:[string dataUsingEncoding:NSUTF8StringEncoding] attributes:nil];
    [fileManager createFileAtPath:testPath3 contents:[string dataUsingEncoding:NSUTF8StringEncoding] attributes:nil];
    NSArray *files = [fileManager subpathsAtPath:testDirectory];
    NSLog(@"%@",files);
    //fileManager使用操作当前目录
    [fileManager changeCurrentDirectoryPath:[docDir stringByExpandingTildeInPath]];
    NSString *fileName = [docDir stringByAppendingPathComponent:@"testFileNSFileManager.txt"];
    NSString *string1 = @"helloworld";
    [fileManager createFileAtPath:fileName contents:[string1 dataUsingEncoding:NSUTF8StringEncoding] attributes:nil];
    //删除文件
    //[fileManager removeItemAtPath:fileName error: nil];
	//用NSMutableData创建混合数据并写入
    NSString *temp = @"hello";
    NSMutableData *writer = [[NSMutableData alloc]init];
    [writer appendData:[temp dataUsingEncoding:NSUTF8StringEncoding]];
    [writer writeToFile:fileName atomically:YES];
    //读取写入的混合数据
    NSData *reader = [NSData dataWithContentsOfFile:fileName];
    NSString *stringData = [[NSString alloc]initWithData:[reader subdataWithRange:NSMakeRange(0, [temp length])] encoding:NSUTF8StringEncoding];
    NSLog(@"stringData:%@",stringData);
  
参考：[IOS学习之IOS沙盒(sandbox)机制和文件操作](http://www.uml.org.cn/mobiledev/201209211.asp)  