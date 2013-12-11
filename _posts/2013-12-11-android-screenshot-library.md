---
date: 2013-12-11 18:45:30+00:00
layout: post
title: 利用android-screenshot-library(ASL)来实现截屏
thread: 10
categories: android
tags:  android
---

Android上截屏的方法比较多，但大多都需要root权限或修改APP签名。利用
[android-screenshot-library(ASL)](https://code.google.com/p/android-screenshot-library/)可以不受这两个限制。

###启动android-screenshot-library(ASL)服务###

android-screenshot-library(ASL)利用后台本地服务来实现截屏，应用程序中可以调用这个服务来实现截屏功能。

- 利用adb工具安装asl-native到Android设备中。

		adb.exe push ./asl-native /data/local			
		adb shell /system/bin/chmod 0777 /data/local/asl-native

- 启动asl-native服务

		adb.exe shell kill -9 "/data/local/asl-native"
		start /B %ANDROID%\platform-tools\adb.exe shell "/data/local/asl-native /data/local/asl-native.log"

可以通过asl-native.log可以查看服务建立信息：


![](/assets/blog_pic/asl-native-log.PNG)


###在Android程序中加入ASL服务###

- 在应用程序中加入ScreenshotService.java（which contains Android service class communicating with the native service）和IScreenshotProvider.aidl（包含isAvailable()和takeScreenshot()的声明）

- 绑定服务

		// (using class name)
		Intent intent = new Intent();
		intent.setClass (this, pl.polidea.asl.ScreenshotService.class);
		bindService (intent, aslServiceConnection, Context.BIND_AUTO_CREATE);
		或// (using BIND action)
		bindService (new Intent(pl.polidea.asl.ScreenshotService.BIND), aslServiceConnection, Context.BIND_AUTO_CREATE);

- 在manifest.xml中设置权限和服务

由于需要与底层进行socket通信，需要加入网络权限。

<uses-permission 
android:name="android.permission.INTERNET"/>

声明asl服务

	<service android:name="pl.polidea.asl.ScreenshotService">
	        <intent-filter>
	                <action android:name="pl.polidea.asl.ScreenshotService.BIND" />
	                <category android:name="android.intent.category.DEFAULT"/>
	        </intent-filter>
	</service>

- 调用该服务

		private IScreenshotProvider screenshotProvider = null;
		private ServiceConnection aslServiceConnection = new ServiceConnection() {
		    @Override
		    public void onServiceConnected(ComponentName name, IBinder binder) {
		        screenshotProvider = IScreenshotProvider.Stub.asInterface(binder);
		    }
		    @Override
		    public void onServiceDisconnected(ComponentName name) { }
		};

这个截屏的方法有个不足就是每次重启手机后，需要利用adb工具在手机上启动asl服务。