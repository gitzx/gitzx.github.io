---
date: 2014-11-22 15:22:30+00:00
layout: post
title: lua中metatable和metamethod小结
thread: 87
categories: cocos2d-x
tags: cocos2d-x
---

元表(metatable)和元方法(metamethod)是lua中的基本概念，是扩展lua操作、lua库以及其他高级特性如面向对象、弱引用、垃圾回收等基础，在这小结下元表和元方法的基本使用。

###基本知识###

和其他语言一样，lua中每个值都有一些预定义的操作。通过元表(metatable)修改一个值的行为，可以在面对一个非预定义的操作时执行一个指定的操作。

例如执行两个table相加时，由于table中没有预定义，执行时会先检查两者之一是否有元表(metatable)，然后检查该元表是否有一个叫`__add`的字段，若有该字段，则调用该字段对应的值，调用该字段执行加法操作就是元方法(metamethod)，"add"操作就是event.

lua中每个值都有一个元表，除了table和userdata可以有各自独立的元表，其他类型的值共享其类型所属的单一元表。

在lua代码中，只能设置table的元表，其他类型值的元表，需要通过C代码来完成。

设置和查看元表的方法分别是`setmetatable`和`getmetatable`:

	--创建新table不会创建元表
	t={}
	print(getmetatable(t))  --nil 
	
	--可通过setmetatable来设置修改table元表
	t1={}
	setmetatable(t,t1)
	assert(getmetatable(t)==t1)

table可以作为任何值的元表，如多个table共享一个元表、作为自己的元表等等。

###元方法分类###

介绍完元表，再小结下元方法，常用的元方法有19个，这些元方法的主要可分为：

- 算术类元方法.  `__unm`，`__add`， `__sub`， `__mul`， `__div`， `__mod`， `__pow`， `__concat`

- 关系类元方法.  `__eq`, `__lt`, `__le`

- 库定义的元方法.  `__tostring`,  `__metatable`

- table访问的元方法. `__index`, `__newindex`

- 其他元方法. `__len`, `__call`, `__mode`, `__gc`

###算术类元方法###




