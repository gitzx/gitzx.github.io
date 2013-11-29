---
date: 2013-11-29 16:45:30+00:00
layout: post
title: 检测IOS设备中已安装的App
thread: 07
categories: ios 
tags:  ios
---

最近在做个小APP，需要检测IOS设备上已安装的APP。网上查了些资料，有四种方法，在这总结下。

###URL Scheme###
由于“沙盒”的存在，ios是禁止不同的应用程序之间相互访问彼此的数据。但apple开放了URL Scheme接口。

iOS 上的应用程序可以通过向其它应用程序发送一个URL 格式的字符串来向其发送数据。这个特性通常用于在应用程序中启动另外一个应用程序来打开一种特定格式的数据。

同时，我们可以通过canopenurl来判断是否安装了某程序。这个可以用于未越狱的IOS设备。这个有机会得尝试下。

###解析MobileInstallation cache文件###

MobileInstallation cache随着SpringBoard启动而更新，包括所有已安装APP的安装信息。

	BOOL APCheckIfAppInstalled(NSString *bundleIdentifier)
	{
	    static NSString *const cacheFileName = @"com.apple.mobile.installation.plist";
	    NSString *relativeCachePath = [[@"Library" stringByAppendingPathComponent: @"Caches"] stringByAppendingPathComponent: cacheFileName];
	    NSDictionary *cacheDict = nil;
	    NSString *path = nil;
	    // Loop through all possible paths the cache could be in
	    for (short i = 0; 1; i++)
	    {
	        
	        switch (i) {
	            case 0: // Jailbroken apps will find the cache here; their home directory is /var/mobile
	                path = [NSHomeDirectory() stringByAppendingPathComponent: relativeCachePath];
	                break;
	            case 1: // App Store apps and Simulator will find the cache here; home (/var/mobile/) is 2 directories above sandbox folder
	                path = [[NSHomeDirectory() stringByAppendingPathComponent: @"../.."] stringByAppendingPathComponent: relativeCachePath];
	                break;
	            case 2: // If the app is anywhere else, default to hardcoded /var/mobile/
	                path = [@"/var/mobile" stringByAppendingPathComponent: relativeCachePath];
	                break;
	            default: // Cache not found (loop not broken)
	                return NO;
	            break; }
	        
	        BOOL isDir = NO;
			// Ensure that file exists
	        if ([[NSFileManager defaultManager] fileExistsAtPath: path isDirectory: &isDir] && !isDir) 
	            cacheDict = [NSDictionary dictionaryWithContentsOfFile: path];
	        
	        if (cacheDict) // If cache is loaded, then break the loop. If the loop is not "broken," it will return NO later (default: case)
	            break;
	    }
	    // First check all system (jailbroken) apps
	    NSDictionary *system = [cacheDict objectForKey: @"System"]; 
	    if ([system objectForKey: bundleIdentifier]) return YES;
		// Then all the user (App Store /var/mobile/Applications) apps
	    NSDictionary *user = [cacheDict objectForKey: @"User"]; 
	    if ([user objectForKey: bundleIdentifier]) return YES;
		
	    // If nothing returned YES already, we'll return NO now
	    return NO;
	}

简单验证下：

    NSArray *bundles2Check = [NSArray arrayWithObjects: @"com.apple.mobilesafari", @"Game.FileOps", @"com.blahblah.nonexistent", nil];    
    for (NSString *identifier in bundles2Check)
        if (APCheckIfAppInstalled(identifier))
        NSLog(@"App installed: %@", identifier);
        else
            NSLog(@"App not installed: %@", identifier);

检测系统的浏览器、我已安装的程序Game.FileOps、不存在的程序,在模拟器中的验证结果如下：
	
	2013-11-29 17:04:30.407 InstalledApp[27046:c07] App installed: com.apple.mobilesafari
	2013-11-29 17:04:30.409 InstalledApp[27046:c07] App installed: Game.FileOps
	2013-11-29 17:04:30.410 InstalledApp[27046:c07] App not installed: com.blahblah.nonexistent

###根据正在运行的进程信息来检测###

获得当前正在运行的进程信息，从进程信息中获得安装的app信息，这个暂时还为尝试。

###iHasAPP###

利用别人写的框架[iHasAPP](https://github.com/danielamitay/iHasApp),在模拟器上尝试了下，没有检测到结果。可能只能在真机中有效。后面再尝试下。



参考：(1)[如何获得已安装程序的资源列表？](http://www.cocoachina.com/bbs/read.php?tid=86829&page=1)；  (2)  [Is it possible to retrieve these information?](http://www.iphonedevsdk.com/forum/iphone-sdk-development/22289-possible-retrieve-these-information.html)


