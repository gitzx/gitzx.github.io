---
date: 2016-6-27 18:50:30+00:00
layout: post
title: Android中Animation小结
thread: 147
categories: android
tags: android

---

在Android开发中常会使用动画(Animation)，在这篇中小结下。


### Animation分类 ###

在Android中，动画可以分为两大类：

1. Property Animation(属性动画)：  动画在一段时间类修改某控件的属性。只对Android3.0（API 11）以上版本有效。

2. View Animation(视图动画)：

 （1）Tween Animation(补间动画) ： 操作某个控件让其展现出旋转、渐变、移动、缩放的这么一种转换过程

 （2）Frame Animation(帧动画) : 一个个显示图片，类似幻灯片。


### Property Animation ###

Android Property Animation(属性动画)可以在一段时间内，有规律的改变对象的属性，从而使对象展现出动画效果。提供了以下特性：

1. Duration：动画的持续时间；

2. TimeInterpolation：动画的时间差值，线性或非线性；

3. Repeat count and behavior：动画重复次数和方式；

4. Animator sets：动画集合；

5. Frame refresh delay：刷新显示间隔。


Property Animation有三个子类，分别如下：

1. [ValueAnimator](https://developer.android.com/reference/android/animation/ValueAnimator.html): 基本的动画类，处理值动画，通过监听某些值的变化进行相应动作。

2. [ObjectAnimator](https://developer.android.com/reference/android/animation/ObjectAnimator.html)：处理对象动画；

3. [AnimatorSet](https://developer.android.com/reference/android/animation/AnimatorSet.html)：动画集。

在java层设置动画属性：

	{% highlight java %}
	//Animating with ValueAnimator
	ValueAnimator animation = ValueAnimator.ofFloat(0f, 1f);
	animation.setDuration(1000);
	animation.start();
	//Animating with objectAnimator
	ObjectAnimator anim = ObjectAnimator.ofFloat(foo, "alpha", 0f, 1f);
	anim.setDuration(1000);
	anim.start();
	//Animating with AnimatorSet
	AnimatorSet bouncer = new AnimatorSet();
	bouncer.play(bounceAnim).before(squashAnim1);
	bouncer.play(squashAnim1).with(squashAnim2);
	bouncer.play(squashAnim1).with(stretchAnim1);
	bouncer.play(squashAnim1).with(stretchAnim2);
	bouncer.play(bounceBackAnim).after(stretchAnim2);
	ValueAnimator fadeAnim = ObjectAnimator.ofFloat(newBall, "alpha", 1f, 0f);
	fadeAnim.setDuration(250);
	AnimatorSet animatorSet = new AnimatorSet();
	animatorSet.play(bouncer).before(fadeAnim);
	animatorSet.start();
	{% endhighlight %}

简单例子如下：

View Animation(视图动画)的xml文件放在res/anim/目录下，Property Animation(属性动画)的xml文件放在res/animator/目录下。

	<set android:ordering="sequentially">
	    <set>
	        <objectAnimator
	            android:propertyName="x"
	            android:duration="500"
	            android:valueTo="400"
	            android:valueType="intType"/>
	        <objectAnimator
	            android:propertyName="y"
	            android:duration="500"
	            android:valueTo="300"
	            android:valueType="intType"/>
	    </set>
	    <objectAnimator
	        android:propertyName="alpha"
	        android:duration="500"
	        android:valueTo="1f"/>
	</set>

在java层调用：

	{% highlight java %}
	AnimatorSet set = (AnimatorSet) AnimatorInflater.loadAnimator(myContext,
	    R.anim.property_animator);
	set.setTarget(myObject);
	set.start();
	{% endhighlight %}

上面栗子中，设置了View的x和y值。在Android中，有如下View属性设置的setter和getter方法：

1. alpha : 透明度，默认是1，表示不透明；

2. pivotX和pivotY ： 旋转的轴点和缩放的基准点，默认是View的中心点；

3. scaleX和scaleY ：基于pivotX和pivotY的缩放，1表示无缩放，小于1表示缩小；

4. 

#### Animation Listerners ####

[Animator.AnimatorListener](https://developer.android.com/reference/android/animation/Animator.AnimatorListener.html) :

1. onAnimationStart() : 当动画开始时调用；

2. onAnimationEnd() ；

3. onAnimationRepeat() ;

4. onAnimationCancel() .

[ValueAnimator.AnimatorUpdateListener](https://developer.android.com/reference/android/animation/ValueAnimator.AnimatorUpdateListener.html) :

1. onAnimationUpdate() : 动画每帧调用。


### View Animation ###

Animation由四种类型组成：

1. alpha ： 渐变透明动画效果；

2. scale ： 渐变尺寸伸缩动画效果；

3. translate ：画面转移位置移动动画效果；

4. rotate ： 画面转移旋转动画效果。

在java源代码中定义相对应的类，可以通过这些类来获取和操作相应的属性：

1. AlphaAnimation

2. ScaleAnimation

3. TranslateAnimation

4. RotateAnimation

### Tween Animation ###

	//res/anim/hyperspace_jump.xml
	<set xmlns:android="http://schemas.android.com/apk/res/android"
	    android:shareInterpolator="false">
	    <scale
	        android:interpolator="@android:anim/accelerate_decelerate_interpolator"
	        android:fromXScale="1.0"
	        android:toXScale="1.4"
	        android:fromYScale="1.0"
	        android:toYScale="0.6"
	        android:pivotX="50%"
	        android:pivotY="50%"
	        android:fillAfter="false"
	        android:duration="700" />
	    <set
	        android:interpolator="@android:anim/accelerate_interpolator"
	        android:startOffset="700">
	        <scale
	            android:fromXScale="1.4"
	            android:toXScale="0.0"
	            android:fromYScale="0.6"
	            android:toYScale="0.0"
	            android:pivotX="50%"
	            android:pivotY="50%"
	            android:duration="400" />
	        <rotate
	            android:fromDegrees="0"
	            android:toDegrees="-45"
	            android:toYScale="0.0"
	            android:pivotX="50%"
	            android:pivotY="50%"
	            android:duration="400" />
	    </set>
	</set>


在java层调用：

	{% highlight java %}
	ImageView spaceshipImage = (ImageView) findViewById(R.id.spaceshipImage);
	Animation hyperspaceJumpAnimation = AnimationUtils.loadAnimation(this, R.anim.hyperspace_jump);
	spaceshipImage.startAnimation(hyperspaceJumpAnimation);
	{% endhighlight %}


Interpolator是有效的改进动画相关效果，如加速、减速、重复、反弹等。Interpolator通过`android:interpolator`来实现。Android系统提供了一些常用的Interpolator，在[Interpolator](https://developer.android.com/reference/android/view/animation/Interpolator.html)子类中。除此之外，我们也可以自定义Interpolator。

Android系统提供的Interpolators有：

1. AccelerateDecelerateInterpolator

2. AccelerateInterpolator

3. AnticipateInterpolator

4. AnticipateOvershootInterpolator

5. BounceInterpolator

6. CycleInterpolator

7. DecelerateInterpolator

8. LinearInterpolator

9. OvershootInterpolator

例如`AccelerateDecelerateInterpolator`,可以通过`@android:anim/accelerate_decelerate_interpolator`来使用。

### Frame Animation ###

	//res/anim/rocket.xml
	<?xml version="1.0" encoding="utf-8"?>
	<animation-list xmlns:android="http://schemas.android.com/apk/res/android"
	    android:oneshot="false">
	    <item android:drawable="@drawable/rocket_thrust1" android:duration="200" />
	    <item android:drawable="@drawable/rocket_thrust2" android:duration="200" />
	    <item android:drawable="@drawable/rocket_thrust3" android:duration="200" />
	</animation-list>


在java层调用：

	{% highlight java %}
	ImageView rocketImage = (ImageView) findViewById(R.id.rocket_image);
	rocketImage.setBackgroundResource(R.drawable.rocket_thrust);
	rocketAnimation = (AnimationDrawable) rocketImage.getBackground();
	rocketAnimation.start();
	{% endhighlight %}



参考：[Animation Resources](https://developer.android.com/guide/topics/resources/animation-resource.html#Property)

[Animation](https://developer.android.com/reference/android/view/animation/Animation.html?hl=zh-cn)