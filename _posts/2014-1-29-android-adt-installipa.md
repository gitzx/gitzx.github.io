---
date: 2014-1-29 13:47:30+00:00
layout: post
title: 利用ADT对ipa进行部署
thread: 35
categories: ios
tags: ios
---

利用[AIR Developer Tool（ADT）](http://help.adobe.com/zh_CN/air/build/WS901d38e593cd1bac1e63e3d128cdca935b-8000.html)可以实现APK和ipa的远程安装、启动和卸载。在这小结下ipa文件的部署。

###安装命令###

`adt -installApp -platform platformName -platformsdk path-to-sdk -device deviceID ‑package fileName`

-platform 设备的平台的名称。指定 ios 或 android。

-platformsdk 指向目标设备的平台 SDK 的路径（可选）：

Android - AIR 2.6 以上版本的 SDK 包含 Android SDK 中实现相关 ADT 命令所需的工具。只有在使用其他版本的 Android SDK 时才需要设置此值。此外，如果已设置了 AIR_ANDROID_SDK_HOME 环境变量，则不需要在命令行上提供平台 SDK 路径。（如果在两处都进行了设置，则会使用在命令行上提供的路径。）

iOS - AIR SDK 附带绑定的 iOS SDK。通过 -platformsdk 选项，您可以使用外部 SDK 打包应用程序，因此不必局限于使用绑定的 iOS SDK。例如，如果您使用最新的 iOS SDK 构建了一个扩展名，则可以在打包应用程序时指定此 SDK。此外，与 iOS Simulator 一起使用 ADT 时，您必须始终将 -platformsdk 选项包括在内，指定 iOS Simulator SDK 的路径。

-package 要安装的包的文件名。在 iOS 上，它必须是 IPA 文件。在 Android 上，此项必须是 APK 包。如果已安装指定的包，ADT 会返回错误代码 14：设备错误。

###卸载命令###

`adt -uninstallApp -platform platformName -platformsdk path_to_sdk -device deviceID -appid applicationID`

-appid 已安装应用程序的 AIR 应用程序 ID。如果在设备上未安装具有指定 ID 的应用程序，ADT 会返回退出代码 14：设备错误。

###运行命令###

`adt -launchApp -platform platformName -platformsdk path_to_sdk -device deviceID -appid applicationID`

###列出设备列表###

`idb -devices`可列出连接的ios设备列表

###批量部署脚本如下###

	#!/bin/bash
	idb -devices | while read line
	do
		if [ ! "$line" = "" ] && [ `echo $line | awk '{if ($2 == "iPhone" || $2 == "iPad") print "OK"; else print "FAIL"; }'` = "OK" ]
		then
			device=`echo $line | awk '{print $1}'`
			devicename=`echo $line | awk '{print $4}'`
			echo "$devicename $@ ..."
			adt -installApp -platform ios -device $device -package /Users/script/*.ipa
		fi
	done

参考：[AIR3.4实现对IPA文件的直接部署](http://jamesli.cn/blog/?p=1484)