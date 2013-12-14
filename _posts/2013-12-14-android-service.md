---
date: 2013-12-14 13:55:30+00:00
layout: post
title: Android中两种类型的service
thread: 13
categories: android
tags:  android
---

Android中有两种类型的service：startService()和bindService()。当然，两种类型的service可以单独使用，也可以同时使用。如音乐服务。

###两类service的特点###

startService()的特点：

---

- startService()通过onStartCommand()启动，通过stopSelf()或stopService()停止。
- startService()一旦被调用启动，其是否被销毁与启动它的组件是否被销毁无关；
- startService()通常只执行单一操作，且没有返回值给调用者。例如从网上下载文件服务。
- 在内存过低时，系统会强制杀掉该类service，以便为用户交互的activity释放资源。常用做法是根据onStartCommand()的返回值来判定，当内存足够时重启该service。

---

bindService()的特点：

---
- bindService()通过bindService()启动，通过unbindService()停止。
- bindService()在有组件绑定时启动，bindService()提供C/S接口用于多个组件与服务交互，如发送请求、获取结果和跨进程通信（通过IPC）；
- 多个组件可以同时绑定一个bindService()，组件解绑，服务被销毁。
- 若该类service与此时用户交互的Activity绑定了，就算系统内存过低时，也不太可能会被杀掉。为了更保险，可以将该service声明为[run in the foreground](http://developer.android.com/guide/components/services.html#Foreground)

---

service通常是运行在主进程的main线程上。如果为了减少主进程的工作量（如CPU计算或阻塞等工作），可以在service中创建线程处理这些工作。

本地服务（Local Service）和远程服务（Remote Service）：

本地服务依附于主进程，远程服务是独立的进程，远程服务通常是一些系统服务。

startService()和bindService()的生命周期如下图：

![](/assets/blog_pic/service_lifecycle.png)


service的回调方法如下（没有onStop()的回调方法）：

	public class ExampleService extends Service {
	// indicates how to behave if the service is killed
    int mStartMode;
	// interface for clients that bind
    IBinder mBinder;  
	// indicates whether onRebind should be used
    boolean mAllowRebind; 

    @Override
    public void onCreate() {
     // The service is being created
    }
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
      // The service is starting, due to a call to startService()
        return mStartMode;
    }
    @Override
    public IBinder onBind(Intent intent) {
      // A client is binding to the service with bindService()
        return mBinder;
    }
    @Override
    public boolean onUnbind(Intent intent) {
      // All clients have unbound with unbindService()
        return mAllowRebind;
    }
    @Override
    public void onRebind(Intent intent) {
      // A client is binding to the service with bindService(),
      // after onUnbind() has already been called
    }
    @Override
    public void onDestroy() {
      // The service is no longer used and is being destroyed
    }
	}

###用于被扩展的Service类和IntentService类###

用于扩展的Service类和IntentService类:

- Service类是所有service的基类。

- IntentService类是Service的子类，通过子线程来处理请求（通常只处理单一请求），同时需要实现onHandleIntent()。

###startService###

在一个Activity中启动服务的方法如下：

	Intent intent = new Intent(this, HelloService.class);
	startService(intent);

这一过程包括：（1）系统调用onCreate()方法；（2）调用onStartCommand()方法。

由于startService不需要同时处理多个请求，因此startService常用做法是扩展IntentService类。

- 扩展IntentService类：


		public class HelloIntentService extends IntentService {
		  public HelloIntentService() {
		      super("HelloIntentService");
		  }
		
		  @Override
		  protected void onHandleIntent(Intent intent) {
		      long endTime = System.currentTimeMillis() + 5*1000;
		      while (System.currentTimeMillis() < endTime) {
		          synchronized (this) {
		              try {
		                  wait(endTime - System.currentTimeMillis());
		              } catch (Exception e) {
		              }
		          }
		      }
		  }
		}

扩展IntentService类。默认实现了onCreate(), onStartCommand(), or onDestroy()方法。也可以自己进行重写。如：

	@Override
	public int onStartCommand(Intent intent, int flags, int startId) {
	    Toast.makeText(this, "service starting", Toast.LENGTH_SHORT).show();
	    return super.onStartCommand(intent,flags,startId);
	}

对于onBind()方法，此时默认是返回null，如果需要在startService中用到bindService，需要实现onBind()方法。

- 扩展Service类：

startService通常只处理单一请求，若要同时处理多个请求，需要扩展Service类。

	public class HelloService extends Service {
	  private Looper mServiceLooper;
	  private ServiceHandler mServiceHandler;
	
	  // Handler that receives messages from the thread
	  private final class ServiceHandler extends Handler {
	      public ServiceHandler(Looper looper) {
	          super(looper);
	      }
	      @Override
	      public void handleMessage(Message msg) {
	          long endTime = System.currentTimeMillis() + 5*1000;
	          while (System.currentTimeMillis() < endTime) {
	              synchronized (this) {
	                  try {
	                      wait(endTime - System.currentTimeMillis());
	                  } catch (Exception e) {
	                  }
	              }
	          }
	          // Stop the service using the startId, so that we don't stop
	          // the service in the middle of handling another job
	          stopSelf(msg.arg1);
	      }
	  }
	
	  @Override
	  public void onCreate() {
	    // Start up the thread running the service.  Note that we create a
	    // separate thread because the service normally runs in the process's
	    // main thread, which we don't want to block.  We also make it
	    // background priority so CPU-intensive work will not disrupt our UI.
	    HandlerThread thread = new HandlerThread("ServiceStartArguments",
	            Process.THREAD_PRIORITY_BACKGROUND);
	    thread.start();
	    
	    // Get the HandlerThread's Looper and use it for our Handler 
	    mServiceLooper = thread.getLooper();
	    mServiceHandler = new ServiceHandler(mServiceLooper);
	  }
	
	  @Override
	  public int onStartCommand(Intent intent, int flags, int startId) {
	      Toast.makeText(this, "service starting", Toast.LENGTH_SHORT).show();
	
	      // For each start request, send a message to start a job and deliver the
	      // start ID so we know which request we're stopping when we finish the job
	      Message msg = mServiceHandler.obtainMessage();
	      msg.arg1 = startId;
	      mServiceHandler.sendMessage(msg);
	      // If we get killed, after returning from here, restart
	      return START_STICKY;
	  }
	
	  @Override
	  public IBinder onBind(Intent intent) {
	   // We don't provide binding, so return null
	      return null;
	  }
	  
	  @Override
	  public void onDestroy() {
	    Toast.makeText(this, "service done", Toast.LENGTH_SHORT).show(); 
	  }
	}