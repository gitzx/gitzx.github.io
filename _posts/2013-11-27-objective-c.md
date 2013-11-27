---
date: 2013-11-27 12:45:30+00:00
layout: post
title: objective-c基本知识小结
thread: 05
categories: ios 
tags:  ios objective-c
---

最近在学习ios开发，学习了些 Objective-C。在这简单的小结下。

Objective-C 作为 C 程序设计语言的超集，支持与 C 相同的基本语法。
简要的小结以下内容：（1）类和对象；（2）静态和动态类型化；（3）方法调用（称为发消息）；（4）属性和存取方法；（5）内存管理。


###类和对象：###
（1）interface（在 ObjC 中被称为 @protocol ）

	@interface MyClass:NSObject
	{
		int count;
		id data;
		NSString* name; 
	}
	- (id)initWithString:(NSString *) aName;
	+ (MyClass*)createMyClassWithString:(NSString *) aName;
	@end

（2）implementation

	#import "MyClass.h"
	@implementation MyClass
	- (id)initWithString:(NSString *) aName
	{
		//code goes here
	}
	+ (MyClass *)myClassWithString:(NSString *) aName
	{
		//code goes here
	}
	@end


###静态和动态类型化：###

对于包含对象的变量，Objective-C 支持动态类型化和静态类型化。

- 静态类型化的变量，要在变量类型声明中包括类名称。
- 动态类型化的变量，则要给对象使用类型 id。

您会发现在某些情况下，会需要使用动态类型化的变量。例如，集 (collection) 对象，如数组，在它包含对象的类型未知的情况下，可能会使用动态类型化的变量。

下面的例子，展示了静态类型化和动态类型化的变量声明：

	MyClass *myObject1;  // Static typing
	id       myObject2;  // Dynamic typing
	NSString *userName;  // static typing

###方法调用（称为发消息）:###

Objective-C 中有两种类型的方法：实例方法和类方法。

- 实例方法，由类的实例来执行。换言之，在调用实例方法之前，必须先创建该类的实例。实例方法是最常见的方法类型。声明前面是减号 (-)；
- 类方法，由它所在的类直接执行。它不需要对象的实例作为消息的接收者。对于类方法，对应指示器是加号 (+)。


###属性和存取方法:###

- 属性通常是指某些由对象封装或储存的数据。
- 一个对象的类定义一个接口，该接口使其对象的用户能获取并设定所封装属性的值。执行这些操作的方法，称为存取方法.存取方法有两种类型：（1）getter方法；（2）setter方法。

除了上面的方法，Objective-C 提供已声明的属性作为一种方便的写法，用于存取方法的声明和实现。

- 属性的基本声明使用 @property 编译器指令

		#import <Cocoa/Cocoa.h>
		@interface Photo : NSObject {
		    NSString* caption;
		    NSString* photographer;
		}
		@property (retain) NSString* caption;
		@property (retain) NSString* photographer;
		@end
- 在类实现中使用 @synthesize 编译器指令，让编译器产生存取方法，以及进行特殊命名的实例变量。

		#import "Photo.h"      
		@implementation Photo
		@synthesize caption;
		@synthesize photographer;
		- (void) dealloc
		{
		    [caption release];
		    [photographer release];
		    [super dealloc];
		}
		@end

###内存管理：###
objective-c使用自动引用计数（called reference counting）来管理内存。

	- (void) setTotalAmount: (NSNumber*)input
	{
	    [totalAmount autorelease];
	    totalAmount = [input retain];
	}
	
	- (void) dealloc
	{
	    [totalAmount release];
	    [super dealloc];
	}
 
###其他：###
Objective-C 中其他两个重要的保留术语，是 self 和 super。

- self 是可在消息实现内使用的局部变量，用于引用当前对象；它等同于 C++ 中的 this。
- super 如果在那里找不到方法，则在其超类中查找（依此类推）。如果您将消息发送到 super，运行时先在超类中查找方法实现。

参考：(1)[马上着手开发 iOS 应用程序](https://developer.apple.com/library/ios/referencelibrary/GettingStarted/RoadMapiOSCh/chapters/WriteObjective-CCode/WriteObjective-CCode/WriteObjective-CCode.html)  (2)[云风博客:Objective-C 的对象模型](http://blog.codingnow.com/2013/03/objective_c.html)
(3)[learn Objective-C](http://cocoadevcentral.com/d/learn_objectivec/)