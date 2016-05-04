---
date: 2016-5-3 18:01:30+00:00
layout: post
title: XCode 7 iOS 9提交AppStore失败小记
thread: 128
categories: ios
tags: ios

---

使用XCode 7且需要兼容iOS 9，提交AppStore报了两个错误，错误如下：

1. "Invalid Bundle. iPad Multitasking support requires these orientations: 'UIInterfaceOrientationPortrait,UIInterfaceOrientationPortraitUpsideDown,UIInterfaceOrientationLandscapeLeft,UIInterfaceOrientationLandscapeRight'. Found 'UIInterfaceOrientationLandscapeRight' in bundle 'com.xxx.xxx'."

2. "This bundle is invalid. The Info.plist contains an invalid key 'CFBundleResourceSpecification' in bundle xxx.

### iPad Multitasking ###

#### 解决的方法1： ####

In Xcode, check the "Requires Full Screen" checkbox under General > Targets。

脚本打包的话，可以在类似info.plist在脚本配置中增加如下设置：

	<key>UIRequiresFullScreen</key>
	<true/>

#### 解决方法2： ####

Check the following device orientations

Portrait

Upside Down

Landscape Left

Landscape Right

In this case, we need to support launch storyboard.


### invalid key 'CFBundleResourceSpecification' ###

#### 解决方法1： ####

Project settings under Build Settings > Code Signing > Code Signing Resource Rules Path - Delete the value for Code Signing Resource Rules Path.

#### 解决方法2： ####

这个方法适合Jenkins和脚本打包。

(1) 去掉脚本打包中的`CODE_SIGN_RESOURCE_RULES_PATH=$(SDKROOT)/ResourceRules.plist`;

(2) 在脚本`/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/usr/bin/PackageApplication`中将

	my @codesign_args = ("/usr/bin/codesign", "--force", "--preserve-metadata=identifier,entitlements,resource-rules",
	                  "--sign", $opt{sign},
	                  "--resource-rules=$destApp/ResourceRules.plist");

改为：

	my @codesign_args = ("/usr/bin/codesign", "--force", "--preserve-metadata=identifier,entitlements",
	                  "--sign", $opt{sign});

或者 打包脚本中使用`xcodebuild -exportArchive -exportPlistOptions`，具体可以见
[iOS builds / ipa creation no longer works from the command line](https://stackoverflow.com/questions/32763288/ios-builds-ipa-creation-no-longer-works-from-the-command-line/32845990#32845990)

参考：

1. [iPad Multitasking support requires these orientations](http://stackoverflow.com/questions/32559724/ipad-multitasking-support-requires-these-orientations)

2. [Error Itms-90339: This bundle is invalid . The info.plist contains an invalid key 'CFBundleResourceSpecification’ in app bundle](http://stackoverflow.com/questions/32504355/error-itms-90339-this-bundle-is-invalid-the-info-plist-contains-an-invalid-ke)