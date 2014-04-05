---
date: 2014-4-5 22:11:30+00:00
layout: post
title: cocos2d-x的入门学习－－TestCpp例子
thread: 44
categories: cocos2d-x
tags: cocos2d-x
---

cocos2d-x自带的TestCpp例子包含由多个示例，是学习cocos2d－x的极好资料，除去例子文件，其他文件包括：

(1) AppDelegate.h/cpp : 程序控制类AppDelegate；

 利用searchPaths加载资源文件；
 
 加载主场景和示例：
 
	CCScene * pScene = CCScene::create();
    CCLayer * pLayer = new TestController();
    pScene->addChild(pLayer);
    pDirector->runWithScene(pScene);

(2) controller.h/cpp : 示例场景管理类TestController，用于管理所有示例；用于主界面各示例的选择。

(3) testBasic.h/cpp : 示例场景基类TestScene，用于返回主界面场景；各示例文件均由用到该类。

(4) testResource.h : 文件资源名称定义头文件；

(5) test.h : 示例总头文件；

(6) VisibleRect.h/cpp : 自适应屏幕分辨率。以屏幕上可视区域的9个点作为参考点，相当于在该矩形内写一个米字，这9个点分别是：左上、左、左下、下、右下、右、右上、上、中心。例如：

	CCPoint VisibleRect::lef()
	{
    	lazyInit();	
    	return ccp(s_visibleRect.origi, s_visibleRect.origin.y+s_visibleRect.size.height/);
    }

