---
date: 2014-4-5 19:13:30+00:00
layout: post
title: cocos2d-x的入门学习－－动作
thread: 43
categories: cocos2d-x
tags: cocos2d-x
---

动作（action）作用于游戏元素。cocos2d－x的动作由CCCAction类实现。CCAction类的派生类包括：

（1）`CCFiniteTimeAction`：绝大数我们使用的动作类都派生自CCFiniteTimeAction，如最常用的`CCIntervalAction`(持续性动作)、`CCInstantAction`(瞬时动作)，这两个类又分别派生出许多我们实际用到的动作类。

（2）`CCRepeatForever` : 无限重复动作；

（3）`CCSpeed` : 变速动作；

（4）`CCFollow` : 跟随动作；

动作或动画只能由CCNode来执行,动作的执行例如：

	CCAction *action = CCMoveTo::create(4.0f, ccp(0,0));
	sp1->runAction((CCAction *)action->copy());

###CCFiniteTimeAction###

####瞬时动作####

(1)放置 – Place  :  效果类似于 node.Position = ccp(x, y)

	CCFiniteTimeAction *action = CCPlace::create(ccp(0,0));
	sp->runAction(action);

(2)隐藏 – Hide   :   效果类似于 [node setVisible:NO]

(3)显示 – Show   :   效果类似于 [node setVisible:YES]

	CCFiniteTimeAction *action1 = CCHide::create();
	CCFiniteTimeAction *action2 = CCShow::create();
	sp->runAction(action2);

(4)可见切换 – ToggleVisibility

瞬时动作可以与其他动作形成连续动作。

####延迟动作####

函数命名规则是：XxxxTo: 意味着运动到指定的位置, XxxxBy:意味着运动到按照指定的 x、y 增量的位置。[x、y 可以是负值]）

(1)移动到 － CCMoveTo ；移动－CCMoveBy

	//duration -- 动作持续时长
	//deltaPosition -- 移动位置(To)、移动距离(By)
	CCMoveTo::create(float duration, const CCPoint& 	deltaPosition);
	CCMoveBy::create(float duration, const CCPoint& 	deltaPosition);

(2) 跳跃到 － CCJumpTo 设置终点位置和跳跃的高度和次数；跳跃 – CCJumpBy   设置终点位置和跳跃的高度和次数。

	//duration -- 动作持续时长
	//deltaPosition -- 移动位置(To)、移动距离(By)
	//height -- 跳跃高度
	//jumps -- 跳跃次数
	CCJumpTo::create(float duration, const CCPoint& position, float height, unsigned int jumps);
	CCJumpBy::create(float duration, const CCPoint& position, float height, unsigned int jumps);

(3) 贝赛尔 － CCBezierBy 支持 3 次贝塞尔曲线:P0-起点,P1-起点切线方向,P2-终点切线方向,P3-终点。

	ccBezierConfig con;
	con.controlPoint_1 = ccp(100, 100);
	con.controlPoint_2 = ccp(200, 200);
	con.endPosition = ccp(0, 0);
	CCActionInterval *action1 = CCBezierTo::create(3, con);
	sp->runAction(CCSequence::create(action1, NULL));

(4)放大到 – CCScaleTo   设置放大倍数,是浮点型。放大 – CCScaleBy

	//设置CCSprite类型节点sp的缩放值
	sp->setScale(0.25);
	//在规定时间内将节点sp以原始比例缩放2倍大小，也就是说按照	setScale(1)的比例缩放2倍，忽略节点之前的缩放
	CCFiniteTimeAction *action = CCScaleTo::create(0.5, 2);
	//在规定时间内将节点sp按照当前比例缩放2倍大小，也就是按照	setScale(0.25)的比例缩放2倍
	CCFiniteTimeAction *action = CCScaleBy::create(0.5, 2);
	sp->runAction(CCSequence::create(action, NULL));
(5)旋转到 – CCRotateTo ; 旋转 – CCRotateBy

	sp->setRotation(45);
	//在规定时间内将节点sp以原始角度进行旋转，也就是按照	setRotation(0)的角度进行旋转，忽略之前的旋转角度
	CCFiniteTimeAction *action = CCRotateTo::create(1, 0);
	//在规定时间内将节点sp以现有角度进行旋转，也就是在setRotation(45)的角度基础上进行叠加旋转
	//CCFiniteTimeAction *action = CCRotateBy::create(1,10);
(6)闪烁 – CCBlink   设定闪烁次数

	//uBlinks -- 闪烁次数
	CCBlink::create(float duration, unsigned int uBlinks)
(7) 色调变化到 – CCTintTo ; 色调变换 – CCTintBy

	//duration -- 执行时长
	//r、g、b颜色值，取值范围0~255
	CCTintTo::create(float duration, GLubyte red, GLubyte green, GLubyte blue)
	CCTintBy::create(float duration, GLubyte red, GLubyte green, GLubyte blue)
(8) 变暗到 – CCFadeTo ; 

	//duration -- 动作执行时长
	//opacity --透明度(0~255)
	CCFadeTo::create(float duration, GLubyte opacity)

(9)由无变亮 – CCFadeIn ; 由亮变无 – CCFadeOut.

	CCFadeIn::create(float d) //淡入
	CCFadeOut::create(float d) //淡出

####组合动作####

按照一定的次序将上述基本动作组合起来,形成连贯的一套组合动作。组合动作包括以下几类:

(1) 序列 － CCSquence ： 该类也从 CCIntervalAction 派生,本身就可以被 CocosNode 对象执行。该类的作用就是线序排列若干个动作,然后按先后次序逐个执行。

	//CCMoveBy动作
	CCActionInterval *action = CCMoveBy::create(1, ccp(110,110));
	CCActionInterval *action_back = action->reverse();
	//创建序列动作
	CCActionInterval *act = CCSequence::create(action, action_back, NULL);
	sp->runAction(act);
(2) 同步 – Spawn : 该类也从 IntervalAction 派生,本身就可以被CocosNode 对象执行。该类的作用就是同时并列执行若干个动作,但要求动作都必须是可以同时执行的。比如:移动式翻转、变色、变大小等。

	//CCScaleTo动作
	CCActionInterval *action1 = CCScaleTo::create(1, 0.5);
	//CCRotateTo动作
	CCActionInterval *action2 = CCRotateTo::create(2, 180);   
	//创建并列动作(使一个CCNode同时执行缩放和旋转动作)，按照CCRotateTo(2秒)执行时间计算
	CCActionInterval *act =  CCSpawn::create(action1, action2, NULL);
	sp->runAction(act);

(3) 重复有线次数 – Repeate : 重复有限次数的动作,该类也从 IntervalAction 派生,可以被 CocosNode 对象执行。

	//无限重复执行动作
	CCRepeatForever* create(CCActionInterval *pAction);
	//重复执行times次
	CCRepeat* create(CCFiniteTimeAction *pAction, unsigned int times);

(4) 反动作 – Reverse : CCFiniteTimeAction类中定义了一个reverse方法，此方法的作用是逆置动作，就是原动作的相反动作。不是所有的类都支持反动作,XxxxTo 类通常不支持反动作,XxxxBy 类通常支持。

(5) 动画 – Animation : 动画是特殊的持续性动作，且只能应用在精灵上。  动画就是让精灵自身连续执行一段影像,形成模拟运动的效果:行走时的精灵状态、打斗时的状态等。

(6)延时动作 -- CCDelayTime

	//CCMoveBy动作
	CCActionInterval *action = CCMoveBy::create(1, ccp(110,110));
	CCActionInterval *action_back = action->reverse();   
	//创建CCDelayTime
	CCDelayTime *delayTime = CCDelayTime::create(5);
	//创建序列动作,使action和action_back动作之间停顿5秒后再执行
	CCActionInterval *act = CCSequence::create(action, delayTime, action_back, NULL);
	sp->runAction(act);

###RepeatForever###

 RepeatForever也算一个组合动作。是从Action类直接派生的,因此无法参与序列和同步;自身也无法反向执行。该类的作用就是无限期执行某个动作或动作序列,直到被停止。
 
	CCActionInterval *action = CCMoveBy::create(1, ccp(110,110));
	CCActionInterval *action1 = action->reverse();
	//无限重复执行动作	sp>runAction(CCRepeatForever::create(CCSequence::create(action, action1, NULL)));

###CCSpeed###

基本动作和组合动作实现了针对精灵的各种运动、动画效果的改变,但这样的改变的速度是不变的,通过 CCEaseAction 为基类的类系和 CCSpped 类我们可以很方便的修改精灵执行劢作的速度:由快至慢还是由慢至快。

（1）EaseIn 由慢至快 ； EaseOut 由快至慢 ； EaseInOut 由慢至快再由快至慢 ； EaseSineIn 由慢至快；

（2）EaseSineOut 由快至慢 ；EaseSineInOut 由慢至快再由快至慢； EaseExponentialIn 由慢至极快 ；EaseExponentialOut 由极快至慢 ； EaseExponentialInOut 由慢至极快再由极快至慢。

（3）Speed 人工设定速度,还可通过 SetSpeed 不断调整。

	//CCMoveBy动作
	CCActionInterval *action = CCMoveBy::create(1, ccp(100,100));
	CCActionInterval *action_back = action->reverse();
	//创建CCSpeed
	CCSpeed *speed = CCSpeed::create(CCSequence::create(action, action_back, NULL), 1);   
	//执行动作
	sp->runAction(speed);   
	//设置动作速度
	speed->setSpeed(10);

###动作回调函数###

当一个CCNode执行完某个Action后，我们可能需要做一些其他的工作，这时，可以使用动作回调函数来完成这项功能。在一个动作完成之后随即调用动作回调函数，这种类型的函数有4种形式可供我们选择使用：

(1)CCCallFunc：无参回调函数;

(2)CCCallFuncN：带一个CCNode*参数回调函数，“N”表示CCNode;

(3)CCCallFuncND：带一个CCNode* 和一个void*参数的回调函数，“N”表示CCNode，"D"表示Data;

(4)CCCallFunO：带一个CCObject*参数的回调函数，"O"表示CCObject

参考：[cocos2d-x action动作整理集合](http://blog.csdn.net/cocos2der/article/details/7261774)
