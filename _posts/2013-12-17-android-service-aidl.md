---
date: 2013-12-17 12:15:30+00:00
layout: post
title: Android Service中的AIDL
thread: 16
categories: android
tags:  android
---

在使用Android bindService()，需要提供远程对象基本接口IBinder。其中有三种方法来定义IBinder：

---

- 扩展Binder类。若应用程序和Service在同一个进程，通过扩展Binder类，可返回onBind()的一个实例，定义的service能访问IBinder实现的方法。

- 使用Messenger。若需要跨进程通信（IPC），可定义一个Handler来响应不同类型的消息对象。使用Messenger时,请求在一个线程中得到处理，但一次只能处理一个。

- AIDL (Android Interface Definition Language)。若service需要同时处理多个请求时，可使用AIDL。实际上，Messenger的底层实现也是基于AIDL。

---

原则上来说，Android系统不允许一个进程访问另一个进程的内存。然而通过AIDL可以实现这样的访问。在这我对AIDL用法进行简单的小结。

###在bindService()中使用AIDL的步骤###

在bindService()中使用AIDL的步骤如下：

- 创建.aidl格式的文件。.aidl文件定义了方法的接口。.aidl文件使用和java相同的语法，.aidl文件位于项目工程中的/src/目录下。如：

		// IRemoteService.aidl
		package com.example.android;
		interface IRemoteService {
		    int getPid();
		    void basicTypes(int anInt, long aLong, boolean aBoolean, float aFloat,
		            double aDouble, String aString);
		}

- Android SDK工具根据.aidl文件生成同名的.java的文件（位于项目工程的/gen/目录下）。这个.java文件除了包括.aidl文件中定义的接口，还包括一个内部抽象类-Stub类，Stub类扩展了Binder。

- 公开接口。在自己编写的Service中重写onBind()方法，返回Stub类的实现。如：


		public class RemoteService extends Service {
		    @Override
		    public void onCreate() {
		        super.onCreate();
		    }
		
		    @Override
		    public IBinder onBind(Intent intent) {
		        // Return the interface
		        return mBinder;
		    }
		
		    private final IRemoteService.Stub mBinder = new IRemoteService.Stub() {
		        public int getPid(){
		            return Process.myPid();
		        }
		        public void basicTypes(int anInt, long aLong, boolean aBoolean,
		            float aFloat, double aDouble, String aString) {
		            // Does nothing
		        }
		    };
		}


###在应用程序中访问使用AIDL的Service###

若应用程序和Service在不同的程序中，应用程序想访问AIDL定义的接口文件，在应用程序中的项目工程中的/src/目录下需要包括.aidl文件。以便访问定义的Service.代码如：


	IRemoteService mIRemoteService;
	private ServiceConnection mConnection = new ServiceConnection() {
	    // Called when the connection with the service is established
	    public void onServiceConnected(ComponentName className, IBinder service) {
	    // Following the example above for an AIDL interface,
	   // this gets an instance of the IRemoteInterface, which we can use to call on the service
	        mIRemoteService = IRemoteService.Stub.asInterface(service);
	    }
	
	    // Called when the connection with the service disconnects unexpectedly
	    public void onServiceDisconnected(ComponentName className) {
	        Log.e(TAG, "Service has unexpectedly disconnected");
	        mIRemoteService = null;
	    }
	};


###创建支持Parcelabel的类###