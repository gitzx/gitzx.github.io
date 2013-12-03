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