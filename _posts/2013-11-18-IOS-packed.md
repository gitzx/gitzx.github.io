---
date: 2013-11-18 18:44:30+00:00
layout: post
title: IOS程序打包
thread: 01
categories: ios
tags:  ios
---

**Ios程序包分为：**

- appstore二进制文件：通过xcode工具可以生成一个.app格式的二进制文件。
- 渠道包：.ipa格式文件

**打包过程：**

	xcodebuild负责将工程源文件编译成xxx.app
	xcrun负责给xxx.app(签名并)打包成xxx.ipa

**一般的IOS打包方法**


 (1) appstore 二进制程序包

    打开你的项目，进入“Edit Project Settings”，进Configuration页面，选中Release点击下面的Duplicate，复制一个新的配置项出来，命名为Distribution。然后进入Build页面，顶上的Configuration下拉框选中Distribution，下面的Code Signing Identity里面的Any iPhone OS Device后面对应的值选中你的那个Distribution的证书。然后点击“Build”–> “Build” 就可以编译程序了。编译成功后，你就可以在相应的build目录下看到一个.app的二进制文件。
 (2) 渠道ipa包

	根据以上步骤同样配置好Distribution 证书 ，然后点击 “Build”–> “Build and Archive” 就可以编译程序了。接着打开“Window””Organizer” 左边栏中选择”ARCHIVED APPLICATIONS” 然后再右侧列表中选中刚才编译的程序包 再点击右侧右边顶部的”Share”按钮 保存到磁盘即可。就会生成一个.ipa的文件 即为渠道包。注意：以上运行设备必须选择“Deveice“
  
**IOS自动化打包**

 IOS打包命令如下：
 
	第一步清理:xcodebuild  clean
	第二步编译:xcodebuild[-project][-activetarget][-alltargets][-target]...[-parallelizeTargets][-activeconfiguration][-configuration][-sdk |][=]...[]...
	第三步打包:/usr/bin/xcrun -sdk iphoneos PackageApplication –v [{TARGET}.app] -o [{TARGET}.ipa] --sign [{Iphone Distribution:xxx}] –embed [{xxx.mobileprovision}]
	
    
   其中：-v 对应的是app文件的绝对相对路径 –o 对应ipa文件的路径跟文件名 –sign对应的是 发布证书中对应的公司名或是个人名  –embed 对应的是发布证书文件。注意如果对应的Distribution 配置中已经配置好了相关证书信息的话 –sign 和 –embed可以忽略

**IOS打包与持续集成**

 打包过程需要使用到xcode工具及其命令行，在jenkins中安装xcode插件，将上面的打包命令放在jenkins中定时执行或者通过一些命令来自动构建，将打包好的ipa文件利用rsync自动上传到svn上。



