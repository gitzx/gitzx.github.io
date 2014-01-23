---
date: 2014-1-23 17:32:30+00:00
layout: post
title: APK的批量安装卸载等操作
thread: 31
categories: android
tags: android
---

[ADB(Android Debug Bridge )](http://developer.android.com/tools/help/adb.html)是Android重要的调试工具之一，位于`<sdk>/platform-tools/`下。

下面介绍下利用ADB来实现将多个APK文件在多台Android设备上进行安装卸载启动等。

用到的命令如下：

	#列出连接的Android设备
	adb devices 
	#安装apk到模拟器上   
	adb install <path_to_apk>
	adb -s emulator-5556 install helloWorld.apk 
	 #卸载apk 
	adb shell pm uninstall com.example.MyApp   
	#启动应用
	adb shell am start -a android.intent.action.VIEW  

卸载安装的脚本如下：
 

	#!/bin/bash
	adb devices | while read line
	do
	    if [ ! "$line" = "" ] && [ `echo $line | awk '{print $2}'` = "device" ]
	    then
	        device=`echo $line | awk '{print $1}'`
	        echo "$device $@ ..."
	        adb -s $device install *.apk
			adb -s $device uninstall com.zx.helloworld
	    fi
	done

在windows下写linux shell脚本可能会出现`^M`或其他的错误如`syntax error: unexpected end of file ”`等。需转换为linux文件，可在文本编辑器中设置，在vim中可使用如下设置：
	
	 vi  installapk.sh         
	 :set fileformat=unix 
	 :w  

除了自己写脚本，也可以利用[spoon](http://square.github.io/spoon/)来实现多设备部署测试功能。
