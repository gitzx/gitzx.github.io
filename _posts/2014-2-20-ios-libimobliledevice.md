---
date: 2014-2-20 10:17:30+00:00
layout: post
title: 利用libimobiledevice实现多台ios设备的访问和管理
thread: 38
categories: ios
tags: ios
---

通过PC端连接ios设备，通常使用的是苹果官方提供的iTunes，或者类似PP助手、itools等工具，但这些工具大多只支持windows系统和mac系统，对Linux桌面系统并不支持。通过开源的[libmobiledevice](https://github.com/libimobiledevice/libimobiledevice)库可以实现在windows、mac、linux三大平台实现对ios设备的访问和管理。

###编译libimobiledevice库###

1. 下载源码[libmobiledevice](https://github.com/libimobiledevice/libimobiledevice)；
2. 编译和安装 (`cd libimobiledevice目录`---`./configure`---`make`---`sudo make install`)
3. 验证编译是否成功，在终端输入`idevice_id -l`,返回连接的ios设备的UDID，则说明安装成功。

###libmobiledevice下的usbmuxd###

iTunes使用一种叫[usbmux](https://github.com/libimobiledevice/usbmuxd)的东西与iphone通信, 这个东西提供了TCP Tunneling这个USB--TCP的转换服务.

这个服务在Mac端是由/System/Library/PrivateFrameworks/MobileDevice.framework/Resources/usbmuxd 提供的, 当然, 开机自动启动.
 
它创建了一个Unix Domain Socket 在 /var/run/usbmuxd. usbmuxd服务程序监控iPhone在USB口上的连接, 当它监控到iPhone以用户模式连接到USB, (相对的是recovery模式), usbmuxd服务程序就会连接到这个/var/run/usbmuxd的TCP端口, 并开始成为一个USB--TCP请求转发器.

在libmobiledevice下也包含有usbmuxd。

####利用usbmuxd访问ios设备####

之前利用过usbmuxd来实现通过usb来访问ios设备，在这再小结下：

1. 在ios设备上安装openssh
2. 运行usbmuxd目录下的python-client下的tcprelay.py，`python tcprelay.py -t 22:2222`. 其中22为默认的ssh端口，2222为本地端提供的另一个端口。
3. 在windows上就可以通过putty或secureCRT等ssh工具连接，在mac下通过`$ ssh root@localhost -p 2222`即可连接。

###libimobiledevice的常用命令###

编译安装libimobiledevice后，就可以使用libimobiledevice命令来实现对ios设备进行管理。常用命令如下：

####idevice_id####

返回连接设备的UDID，常用选项如下：

-l或--list 。list UDID of all attached devices

####ideicebackup####

为连接的设备创建或还原备份，`idevicebackup [OPTIONS] CMD [CMDOPTIONS] DIRECTORY`

1. 常用选项如下：

-u或--udid UDID 。 list UDID of all attached devices

2. CMD包括：

 `backup` ：saves a device backup into DIRECTORY.

 `restore` : restores a device backup from DIRECTORY.

	(1)--system  : restore system files, too.
	(2)--reboot  : reboot the system when done.
	(3)--copy    : create a copy of backup folder before restoring.
	(4)--settings: restore device settings from the backup.

 `info` :show details about last completed backup of device

 `list` :list files of last completed backup in CSV format.

 `unback` :unpack a completed backup in DIRECTORY/_unback_/.

####idevicedate####

显示或设置设备的当前时间：  `idevicedate [OPTIONS]`

常用选项如下：

 -u 或 --udid UDID :target specific device by its 40-digit device UDID.

 -s 或 --set TIMESTAMP ：set UTC time described by TIMESTAMP

 -c 或 --sync ：  set time of device to current system time

####ideviceenterrecovery####

使设备进入恢复模式  ：  `ideviceenterrecovery [OPTIONS] UDID`

####ideviceimagemounter####

在设备上增加磁盘映像。 ： `ideviceimagemounter [OPTIONS] IMAGE_FILE IMAGE_SIGNATURE_FILE`

####ideviceinfo####

显示连接设备的信息。  ： `ideviceinfo [OPTIONS]`

####idevicepair####

管理设备和电脑之间配对（ Manage pairings with devices and this host）。 ： `idevicepair [OPTIONS] COMMAND`

####idevicesyslog####

显示连接设备的系统log信息  ：  `idevicesyslog [OPTIONS]`

####idevicescreenshot####

获取设备的截图  ：  `idevicescreenshot [OPTIONS]`

常用的选项如下：

-d 或 --udid UDID  ：  target specific device by its 40-digit device UDID. 

####注：####

每个命令均包括选项：

-d， --debug   ：  enable communication debugging.

-h，  --help   ：   prints usage information

在实际尝试中，指定设备时，用-u无效，用--udid UDID可以成功。。。

###Filesystem Access###

利用libimobiledevice，可以对设备的文件系统进行访问，但需要安装[iFuse](http://fuse.sourceforge.net/).这个后面再做尝试。

参考：[Ituns与iphone的通信协议usbmuxd解析](http://blog.csdn.net/doorxp/article/details/10910151)，[被低估的 Libimobiledevice](http://www.mcuapps.com/blog/2012/05/29/the-undervalued-libimobiledevice/)



 





