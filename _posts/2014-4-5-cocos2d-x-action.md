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

	{% highlight Objective-C %}
	CCAction *action = CCMoveTo::create(4.0f, ccp(0,0));
	sp1->runAction((CCAction *)action->copy());
	{% endhighlight %}

###CCFiniteTimeAction###

####瞬时动作####

(1)放置 – Place  :  效果类似于 node.Position = ccp(x, y)

	{% highlight Objective-C %}
	CCFiniteTimeAction *action = CCPlace::create(ccp(0,0));
	sp->runAction(action);
	{% endhighlight %}

(2)隐藏 – Hide   :   效果类似于 [node setVisible:NO]

(3)显示 – Show   :   效果类似于 [node setVisible:YES]

	{% highlight Objective-C %}
	CCFiniteTimeAction *action1 = CCHide::create();
	CCFiniteTimeAction *action2 = CCShow::create();
	sp->runAction(action2);
	{% endhighlight %}

(4)可见切换 – ToggleVisibility

瞬时动作可以与其他动作形成连续动作。

####延迟动作####

函数命名规则是：XxxxTo: 意味着运动到指定的位置, XxxxBy:意味着运动到按照指定的 x、y 增量的位置。[x、y 可以是负值]）

(1)移动到 － CCMoveTo ；移动－CCMoveBy

	{% highlight Objective-C %}
	//duration -- 动作持续时长
	//deltaPosition -- 移动位置(To)、移动距离(By)
	CCMoveTo::create(float duration, const CCPoint& 	deltaPosition);
	CCMoveBy::create(float duration, const CCPoint& 	deltaPosition);
	{% endhighlight %}

(2) 跳跃到 － CCJumpTo 设置终点位置和跳跃的高度和次数；跳跃 – CCJumpBy   设置终点位置和跳跃的高度和次数。

	{% highlight Objective-C %}
	//duration -- 动作持续时长
	//deltaPosition -- 移动位置(To)、移动距离(By)
	//height -- 跳跃高度
	//jumps -- 跳跃次数
	CCJumpTo::create(float duration, const CCPoint& position, float height, unsigned int jumps);
	CCJumpBy::create(float duration, const CCPoint& position, float height, unsigned int jumps);
	{% endhighlight %}


(3) 贝赛尔 － CCBezierBy 支持 3 次贝塞尔曲线:P0-起点,P1-起点切线方向,P2-终点切线方向,P3-终点。

(4)放大到 – CCScaleTo   设置放大倍数,是浮点型。放大 – CCScaleBy

	{% highlight Objective-C %}
	//设置CCSprite类型节点sp的缩放值
	sp->setScale(0.25);
	//在规定时间内将节点sp以原始比例缩放2倍大小，也就是说按照	setScale(1)的比例缩放2倍，忽略节点之前的缩放
	CCFiniteTimeAction *action = CCScaleTo::create(0.5, 2);
	//在规定时间内将节点sp按照当前比例缩放2倍大小，也就是按照	setScale(0.25)的比例缩放2倍
	CCFiniteTimeAction *action = CCScaleBy::create(0.5, 2);
	sp->runAction(CCSequence::create(action, NULL));
	{% endhighlight %}

(5)旋转到 – CCRotateTo ; 旋转 – CCRotateBy

	{% highlight Objective-C %}
	sp->setRotation(45);
	//在规定时间内将节点sp以原始角度进行旋转，也就是按照	setRotation(0)的角度进行旋转，忽略之前的旋转角度
	CCFiniteTimeAction *action = CCRotateTo::create(1, 0);
	//在规定时间内将节点sp以现有角度进行旋转，也就是在setRotation(45)的角度基础上进行叠加旋转
	//CCFiniteTimeAction *action = CCRotateBy::create(1,10);
	{% endhighlight %}

(6)闪烁 – CCBlink   设定闪烁次数

	{% highlight Objective-C %}
	//uBlinks -- 闪烁次数
	CCBlink::create(float duration, unsigned int uBlinks)
	{% endhighlight %}

(7) 色调变化到 – CCTintTo ; 色调变换 – CCTintBy

	{% highlight Objective-C %}
	//duration -- 执行时长
	//r、g、b颜色值，取值范围0~255
	CCTintTo::create(float duration, GLubyte red, GLubyte green, GLubyte blue)
	CCTintBy::create(float duration, GLubyte red, GLubyte green, GLubyte blue)
	{% endhighlight %}

(8) 变暗到 – CCFadeTo ; 

	{% highlight Objective-C %}
	//duration -- 动作执行时长
	//opacity --透明度(0~255)
	CCFadeTo::create(float duration, GLubyte opacity)
	{% endhighlight %}

(9)由无变亮 – CCFadeIn ; 由亮变无 – CCFadeOut.

	{% highlight Objective-C %}
	CCFadeIn::create(float d) //淡入
	CCFadeOut::create(float d) //淡出
	{% endhighlight %}





####组合动作####

按照一定的次序将上述基本动作组合起来,形成连贯的一套组合动作。组合动作包括以下几类:

(1) 序列 － CCSquence ： 该类也从 CCIntervalAction 派生,本身就可以被 CocosNode 对象执行。该类的作用就是线序排列若干个动作,然后按先后次序逐个执行。

(2) 同步 – Spawn : 该类也从 IntervalAction 派生,本身就可以被CocosNode 对象执行。该类的作用就是同时并列执行若干个动作,但要求动作都必须是可以同时执行的。比如:移动式翻转、变色、变大小等。

(3) 重复有线次数 – Repeate : 重复有限次数的动作,该类也从 IntervalAction 派生,可以被 CocosNode 对象执行。

(4) 反动作 – Reverse : CCFiniteTimeAction类中定义了一个reverse方法，此方法的作用是逆置动作，就是原动作的相反动作。不是所有的类都支持反动作,XxxxTo 类通常不支持反动作,XxxxBy 类通常支持。

(5) 动画 – Animation : 动画是特殊的持续性动作，且只能应用在精灵上。  动画就是让精灵自身连续执行一段影像,形成模拟运动的效果:行走时的精灵状态、打斗时的状态等。

###RepeatForever###

 RepeatForever也算一个组合动作。是从Action类直接派生的,因此无法参与序列和同步;自身也无法反向执行。该类的作用就是无限期执行某个动作或动作序列,直到被停止。

###CCSpeed###

基本动作和组合动作实现了针对精灵的各种运动、动画效果的改变,但这样的改变的速度是不变的,通过 CCEaseAction 为基类的类系和 CCSpped 类我们可以很方便的修改精灵执行劢作的速度:由快至慢还是由慢至快。

（1）EaseIn 由慢至快 ； EaseOut 由快至慢 ； EaseInOut 由慢至快再由快至慢 ； EaseSineIn 由慢至快；

（2）EaseSineOut 由快至慢 ；EaseSineInOut 由慢至快再由快至慢； EaseExponentialIn 由慢至极快 ；EaseExponentialOut 由极快至慢 ； EaseExponentialInOut 由慢至极快再由极快至慢。

（3）Speed 人工设定速度,还可通过 SetSpeed 不断调整。


