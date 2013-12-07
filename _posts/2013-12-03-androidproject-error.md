---
date: 2013-12-03 12:45:30+00:00
layout: post
title: Android开发中遇到的常用错误
thread: 08
categories: android
tags:  android
---

最近在做Android的资源占用信息监控，在导入别人的Android工程时遇到了一些环境配置的错误，以前在实验室做的时候也遇到过，但有些忘记了，在这总结下。

###导入Android项目时的错误###

- the import java.* cannot be resolved

解决方法：（1）检测电脑上是否安装了jdk；（2）检查项目的build path：右键点击项目-》Build Path-》Configure Build Path-》Java Build Path-》libraries-》Add Library-》添加JRE system Library即可。

- the import android cannot be resolved

解决方法：检查项目的build path：右键点击项目-》Build Path-》Configure Build Path-》Android-》选中Target Name下的Android版本即可。

###在Android中调用ddmlib.jar时的错误###
Android的DDMS工具可以方便的截屏，但需要Android设备和PC端建立连接。在Android的APP中实现截屏功能时，首先想到的是利用DDMS的方法，通过调用ddmlib.jar这个包（位于Android SDK目录下的tools\lib下，加入到eclipse的build path下调用）。

但获取屏幕截图时，需要import java.awt.Image，此时就出现了java.awt.Image cannot be resolved.错误。后面在[stackoverflow](http://stackoverflow.com/questions/16140431/android-the-type-java-awt-image-cannot-be-resolved-it-is-indirectly-referenced)上发现这个答案：`You can't use projects that are dependent on java.awt.Image or other awt packages (except java.awt.font) in Android as the dalvik runtime doesn't have these classes in it.` 原来是Android中没有这个类。因此不能在Android的app中来使用这种方法截屏，但可以用来自己实现在pc端对Android设备进行截屏。可以参考[android－pc截屏](http://www.cnblogs.com/pandans/archive/2011/07/12/2104255.html)

