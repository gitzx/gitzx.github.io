---
date: 2015-2-13 10:12:30+00:00
layout: post
title: 利用cydiasubstrate实现Android下的挂钩和代码注入
thread: 98
categories: android
tags: android
---

在前一篇文章[Android下的挂钩(hook)和代码注入(inject)](http://www.gitzx.com/android-inject-hook/)中介绍了Android下挂钩和代码注入的方法，主要是利用了看雪论坛一牛人提供的libinject库和github上提供的框架。

除此之外，Android下的hook和inject还可以使用[xposed](http://repo.xposed.info/)和[cydia Substrate](http://www.cydiasubstrate.com/).xposed主要是hook住java层，cydia substrate可以hook住java层和native层。在这简单介绍下cydia substrate的使用。

###Cydia substrate###

使用[Cydiasubstrate](http://www.cydiasubstrate.com/)可以方便以类似Android插件的形式对Android其他进程进行挂钩，修改相应的函数功能。

我们可以通过使用Cydiasubstrate的jar包和动态链接库so文件来调用相关功能。Cydiasubstrate有三个重要的api，分别如下：

我们可以通过使用Cydiasubstrate的jar包和动态链接库so文件来调用相关功能。Cydiasubstrate有三个重要的api，分别如下：

（1）MSJavaHookClassLoad.主要用于某个类被加载时调用，执行自己编写的功能。函数原型如下：

	void MSJavaHookClassLoad(JNIEnv *jni, const char *name, void (*callback)(JNIEnv *, jclass, void *), void *data);

（2）MSJavaHookMethod.主要用于某个方法被调用时调用，执行自己编写的功能，函数原型如下：

	void MSJavaHookMethod(JNIEnv *jni, jclass _class, jmethodID method, void *hook, void **old);

（3）MSJavaBlessClassLoader.执行一些不安全代码时被调用，还不清楚具体怎么使用。函数原型如下：

	void MSJavaBlessClassLoader(JNIEnv *jni, jobject loader);

在这以Android的显示系统颜色的函数getColor函数为例，分别在java层和native层对getColor函数进行挂钩，修改Android系统颜色为红色。

程序中调用getColor函数的方法如下：

	{% highlight java %}
	try {
		getColor = resources.getMethod("getColor", Integer.TYPE);
	} catch (NoSuchMethodException e) {
		getColor = null;
	}
	{% endhighlight %}

###利用cydiasubstrate实现java层的hook###

在java层我们使用MSJavaHookClassLoad来实现对getColor函数返回结果进行修改，主要代码如下：

	{% highlight java %}
	 static void initialize() {
	        MS.hookClassLoad("android.content.res.Resources", new MS.ClassLoadHook() {
	            public void classLoaded(Class<?> resources) {
	            	Method getColor; 
	            	try {
	                    getColor = resources.getMethod("getColor", Integer.TYPE);
	                } catch (NoSuchMethodException e) {
	                    getColor = null;
	                }

	                if (getColor != null) {
	                    final MS.MethodPointer old = new MS.MethodPointer();

	                    MS.hookMethod(resources, getColor, new MS.MethodHook() {
	                        public Object invoked(Object resources, Object... args)
	                            throws Throwable
	                        {
	                            int color = (Integer) old.invoke(resources, args);
	                            return color & ~0x0000ff00 | 0x00ff0000;
	                        }
	                    }, old);
	                }
	            }
	        });
	    }
	{% endhighlight %}

除此之外，我们需要在AndroidManifest中添加相关权限：

	<uses-permission android:name="cydia.permission.SUBSTRATE"/>

###利用cydiasubstrate实现native层的hook###

（1）在native层，我们用C代码实现getColor的调用修改，在java层通过jni的方式调用底层C代码实现修改，主要C代码如下：

	{% highlight C++ %}
	#include "substrate.h"
	MSConfig(MSFilterExecutable, "/system/bin/app_process")
	
	static jint (*_Resources$getColor)(JNIEnv *jni, jobject _this, ...);
	
	static jint $Resources$getColor(JNIEnv *jni, jobject _this, jint rid) {
	    jint color = _Resources$getColor(jni, _this, rid);
	    return color & ~0x0000ff00 | 0x00ff0000;
	}
	
	static void OnResources(JNIEnv *jni, jclass resources, void *data) {
	    jmethodID method = jni->GetMethodID(resources, "getColor", "(I)I");
	    if (method != NULL)
	        MSJavaHookMethod(jni, resources, method,
	            &$Resources$getColor, &_Resources$getColor);
	}
	MSInitialize {
	    MSJavaHookClassLoad(NULL, "android/content/res/Resources", &OnResources);
	}
	{% endhighlight %}

（2）利用ndk-build命令，我们将上述c文件编译成.so文件，Android.mk代码如下：

	LOCAL_PATH := $(call my-dir)
	
	include $(CLEAR_VARS)
	LOCAL_MODULE:= substrate-dvm
	LOCAL_SRC_FILES := libsubstrate-dvm.so
	include $(PREBUILT_SHARED_LIBRARY)
	
	include $(CLEAR_VARS)
	LOCAL_MODULE    := plum.cy
	LOCAL_SRC_FILES := plum.cpp
	#LOCAL_SHARED_LIBRARIES := substrate-dvm
	LOCAL_LDLIBS:= -L$(LOCAL_PATH) -lsubstrate-dvm
	include $(BUILD_SHARED_LIBRARY)

（3）除此之外，我们需要在AndroidManifest中添加相关权限：

	<uses-permission android:name="cydia.permission.SUBSTRATE"/>

###修改前后的效果###

上述两种方式，在编写Android程序时可以不指定界面，以类似Android插件的实现来实现函数修改调用。具体工程可以为[TestWidget](https://github.com/gitzx/Notes/tree/master/android_programming/TestWidget)和[TestWidget2](https://github.com/gitzx/Notes/tree/master/android_programming/TestWidget2)。以MTL的联想A300手机为例，系统颜色修改的前后截图分别如下：

![](/assets/blog_pic/cydiasubstrate_getcolor.png)

![](/assets/blog_pic/cydiasubstrate_getcolor2.png)