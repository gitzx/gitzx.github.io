---
date: 2014-4-3 20:29:30+00:00
layout: post
title: cocos2d-x的入门学习（1）
thread: 41
categories: cocos2d-x
tags: cocos2d-x
---

之前为了练习object－c，跟着[raywenderlich](http://www.raywenderlich.com/tutorials)教程捣鼓了一阵cocos2d－iphone，学了一点皮毛。由于接触cocos2d－x的更多，决定好好学下这个，同时要坚持写博客！！！

###创建cocos2d－x新项目###
我用的cocos2d-x的版本是cocos2d－x2.2.3, python是python2.7.5版本。利用命令来创建新的项目：

- 切换到/cocos2d-x-2.2.3/tools/project-creator目录下；

- 执行python命令：`python create_project.py -project DemoExercise -package io.gitzx.demo -language cpp`（注：b包名默认是xx.xx.xx格式，其他格式会报错，用其他格式需修改create_project.py）

###cocos2d-x常用类###

####节点类(CCNode)####

cocos2d－x创建的游戏的任何可见的元素都派生自cocos2d－x的节点（CCNode），常见的节点有：场景（CCScene）、层（CCLayer）、精灵（CCSprite）、菜单（CCMenu）。通常情况下，游戏按照场景、层、精灵的层次顺序组织。

节点类继承自CCObject，继承关系：CCCopying <-- CCObject <--CCNode.CCNode类包括的主要功能如下：

- 每个节点都可以包含子节点；

- 节点包含有周期性回调方法（如Schedule、Unschedule等）；

- 节点包含有动作CCAction

####导演类(CCDirector)####

导演类用于创建并控制主屏幕的显示，控制场景的显示时间和显示方式。游戏中一般只有一个导演，控制游戏的开始、结束、暂停。

此类为单例模式，调用标准方式：CCDirector::shareDirector()。继承关系如下：CCObject <-- CCDirector <-- CCDisplayLinkDirector （其中，CCDisplayLinkDirector继承CCDirector，一个可以自动刷新的导演类，只支持1/60、1/30、1/15三种动画间隔。）

导演类的主要功能如下：

- 初始化OpenGL会话，设置OpenGl的一些参数和方式；

- 访问和改变场景以及访问cocos2d-x的配置细节、访问视图、设置投影和朝向等。


###cocos2d-x例子（HelloCpp）###

####程序入口main####

cocos2d－x项目的入口是main文件，不同平台下用不同语言实现及文件后缀。在windows下是main.cpp，在mac下是main.mm。以mac平台为例，main.mm的内容如下：

	#import <UIKit/UIKit.h>
		int main(int argc, char *argv[]) { 
    	NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
    	int retVal = UIApplicationMain(argc, argv, nil, @"AppController");
    	[pool release];
    	return retVal;
	}

和cocos2d－iphone类似，通过AppController来管理应用程序的生命周期。

####程序控制类####

AppDelegate是程序的控制类，里面有三个函数:

- applicationDidFinishLaunching
- applicationDidEnterBackground
- applicationWillEnterForeground

关键代码：
`CCDirector*pDirector=CCDirector::sharedDirector();`
CCDirector是游戏管理类，他的实例全局一份，通过CCDirector::sharedDirector()这个静态函数取得，通过它可以取得一些游戏设置信息，也可以通过它控制当前运行哪个场景。

	// turn on display FPS
    pDirector->setDisplayStats(true);
    // set FPS. the default value is 1.0/60 if you don't call this
    pDirector->setAnimationInterval(1.0 / 60);
    // create a scene. it's an autorelease object
    CCScene *pScene = HelloWorld::scene();
    // run
    pDirector->runWithScene(pScene);

显示FPS信息，设置帧率、创建并启动新场景。

####场景类####

在例子中，场景文件最基本的两个函数是创建场景和场景初始化：

（1）创建场景：


	CCScene* HelloWorld::scene()
	{	
    	// 'scene' is an autorelease object
    	CCScene *scene = CCScene::create();  
    	// 'layer' is an autorelease object
    	HelloWorld *layer = HelloWorld::create();
    	// add layer as a child to scene
    	scene->addChild(layer);
    	return scene;
	}
	
（2）场景初始化

	bool HelloWorld::init()
	{
    	if ( !CCLayer::init() )
    	{
        	return false;
    	}
    
    	CCSize visibleSize = CCDirector::sharedDirector()->getVisibleSize();
    	CCPoint origin = CCDirector::sharedDirector()->getVisibleOrigin();
    	//添加节点信息如层、菜单、精灵等 。。
    	return true;
	}






