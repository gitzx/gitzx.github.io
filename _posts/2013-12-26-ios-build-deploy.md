---
date: 2013-12-26 12:12:30+00:00
layout: post
title: ios应用自动打包和发布
thread: 18
categories: ios
tags: ios
---

之前介绍过ios应用打包的方法,可见[ios程序打包](http://gitzx.github.io/IOS-packed/)。下面介绍ios自动打包的脚本，再利用itms-services协议在网站上发布ios应用，这样就可以直接在ios设备上访问网址下载安装ios应用。

###ios自动打包脚本###

（1）将二进制.app文件生成ipa文件

因为ipa文件实际上就是一个zip文件，我们使用系统的zip命令来生成ipa文件即可。需要注意的是，ipa文件并不是简单地将编辑好的app文件打成zip文件，它需要将app文件放在一个名为Payload的文件夹下，然后将整个Payload目录打包成为.ipa文件，命令如下：

	cd $BUILD_PATH
	mkdir -p ipa/Payload
	cp -r ./DailyBuild-iphoneos/$PRODUCT_NAME ./ipa/Payload/
	cd ipa
	zip -r $FILE_NAME *


（2）ios自动打包脚本


	#!/bin/bash
	#参数判断
	if [ $# != 2 ] && [ $# != 1 ];then
		echo "Number of params error! Need one or two params!"
		echo "1.path of project(necessary) 2.name of ipa file(optional)"
		exit	
	elif [ ! -d $1 ];then
		echo "Params Error!! The first param must be a dictionary."
		exit	
	fi
	
	#工程绝对路径
	cd $1
	project_path=$(pwd)
	#build文件夹路径
	build_path=${project_path}/build
	
	#工程配置文件路径
	project_name=$(ls | grep xcodeproj | awk -F.xcodeproj '{print $1}')
	project_infoplist_path=${project_path}/${project_name}/${project_name}-Info.plist
	#取版本号
	bundleShortVersion=$(/usr/libexec/PlistBuddy -c "print CFBundleShortVersionString" ${project_infoplist_path})
	#取build值
	bundleVersion=$(/usr/libexec/PlistBuddy -c "print CFBundleVersion" ${project_infoplist_path})
	#取bundle Identifier前缀
	#bundlePrefix=$(/usr/libexec/PlistBuddy -c "print CFBundleIdentifier" `find . -name "*-Info.plist"` | awk -F$ '{print $1}')
	
	
	#IPA名称
	if [ $# = 2 ];then
	ipa_name=$2
	fi
	
	
	#编译工程
	cd $project_path
	xcodebuild || exit
	
	#打包
	cd $build_path
	target_name=$(basename ./Release-iphoneos/*.app | awk -F. '{print $1}')
	if [ $# = 1 ];then
	ipa_name="${target_name}_${bundleShortVersion}_build${bundleVersion}_$(date +"%Y%m%d")"
	fi
	
	if [ -d ./ipa-build ];then
		rm -rf ipa-build
	fi
	mkdir -p ipa-build/Payload
	cp -r ./Release-iphoneos/*.app ./ipa-build/Payload/
	cd ipa-build
	zip -r ${ipa_name}.ipa *
	rm -rf Payload


将shell脚本保存，命名为“ipa-build”，然后为其添加可执行权限，命令如下：

 	chmod +x ipa-build

使用非常简单，ipa-build执行需要两个参数，第一个参数是IOS工程所在的根目录(必须)，第二个参数就是生成ipa文件的文件名（不需要带后缀名ipa），第二个参数是可选的，如果不输入，则ipa文件生成默认格式：(targetname)_(version)_build(buildversion)_yyyyMMdd.ipa 括号里分别代表所对应的值，yyyyMMdd是当前日期格式。如果未将ipa-build加入环境变量中，使用时需要使用绝对路径。例如：需要打包的工程根路径为：~/iphone/HuaRongDao，而ipa-build放在了 ~/shell 路径下，要生成名为“HuaRongDao.ipa”的文件，则使用如下命令：

	~/shell/ipa-build ~/iphone/HuaRongDao HuaRongDao

命令执行完成后，会在工程目录下生成一个名为“build”的文件夹，打包好的ipa就放在build文件夹下的“ipa-build”文件夹中。

###利用itms-services协议部署ipa###

通过itms-services协议，可以通过浏览器直接在IOS设备上安装应用程序。利用这种方式，只要在内网布置一个服务器，这样就可以通过浏览器访问安装了。

itms-services协议需要一个plist配置文件。可见[分发用于 iOS 设备的企业级应用程序](http://help.apple.com/iosdeployment-apps/mac/1.1/#appc28ee0f4)。

（1）带 itms-services 协议的链接的html文件示例如下：

	<!DOCTYPE HTML>
	<html>
	  <head>
	    <title>Install your application</title>
	  </head>
	  <body>
	    <ul>
	      <li><a href="itms-services://?action=download-manifest&url=http%3A%2F%2Fwww.example.com%2Fdownload%2Fmyapp.plist">Install Application</a></li>
	    </ul>
	    </div>
	  </body>
	</html>

（2）生成plist文件的示例如下：

	<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
	<dict>
	   <key>items</key>
	   <array>
	       <dict>
	           <key>assets</key>
	           <array>
	               <dict>
	                   <key>kind</key>
	                   <string>software-package</string>
	                   <key>url</key>
	                   <string>http://www.yourdomain.com/$FILE_NAME</string>
	               </dict>
	               <dict>
	                   <key>kind</key>
	                   <string>display-image</string>
	                   <key>needs-shine</key>
	                   <true/>
	                   <key>url</key>
	                   <string>http://www.yourdomain.com/icon.png</string>
	               </dict>
	           <dict>
	                   <key>kind</key>
	                   <string>full-size-image</string>
	                   <key>needs-shine</key>
	                   <true/>
	                   <key>url</key>
	                   <string>http://www.yourdomain.com/icon.png</string>
	               </dict>
	           </array><key>metadata</key>
	           <dict>
	               <key>bundle-identifier</key>
	               <string>com.yourdomain.productname</string>
	               <key>bundle-version</key>
	               <string>1.0.0</string>
	               <key>kind</key>
	               <string>software</string>
	               <key>subtitle</key>
	               <string>ProductName</string>
	               <key>title</key>
	               <string>ProductName</string>
	           </dict>
	       </dict>
	   </array>
	</dict>
	</plist>

（3）在mac上利用apache搭建ios应用下载服务

- 在mac上开启/关闭/重启apache的命令如下：

		sudo apachectl start
		sudo apachectl stop
		sudo apachectl restart

输入 “http://localhost”，可以看到内容为“It works!”的页面。其位于“/Library（资源库）/WebServer/Documents/”下，这就是Apache的默认根目录。

- Apache的安装目录在：/etc/apache2/，etc默认是隐藏的。有两种方式查看：（a）dock下右键Finder，选择"前往文件夹"，输入"/etc"；（b）在terminal 输入 "open /etc"

- 设置虚拟主机

使用sudo vim httpd.conf命令，在文件末尾添加如下代码：

		Listen 9999
		<VirtualHost *:9999>
			ServerName 127.0.0.1
			#指定文件路径
			Alias /sharefolder  /users/ipafolder/downloads
			#指定文件权限
			<Directory "/users/ipafolder/downloads">
				Order Deny,Allow
				Allow from all
			</Directory>
		</ViretualHost>

重启apache，就可以在127.0.0.1/sharefolder/xxx.ipa中直接下载ipa文件。

- 部署


用127.0.0.1/sharefolder/xxx.ipa替换plist文件中的http://www.yourdomain.com/$FILE_NAME，将plist放到共享文件夹/users/ipafolder/downloads中，带 itms-services 协议的链接的html文件中替换成生成的plist路径127.0.0.1/sharefolder/xxx.plist。  这样就可以在ios设备上输入网址下载安装ios应用了。

参考：[给iOS工程增加Daily Build](http://blog.devtang.com/blog/2012/02/16/apply-daily-build-in-ios-project/)