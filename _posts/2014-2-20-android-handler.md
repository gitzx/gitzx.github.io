---
date: 2014-2-20 18:23:30+00:00
layout: post
title: Android中的消息处理
thread: 39
categories: android
tags: android
---

类似windows，Android应用程序也是消息驱动的，在这小结下Android中的消息处理机制。

Android中用于消息处理的类包括：

- Message：消息表示

- MessageQueue：消息队列

- Handler：消息处理。发送和处理Message或者Runnable对象，并且会关联到主线程的MessageQueue中

- Looper：用于某个线程的消息循环。

- HandlerThread：开启一个包含looper的线程，其中该looper能用于创建handler类。

- Messenger：引用一个Handler，其他handler可以发送消息给它。通过在一个进程中创建指向一个Handler的Messenger，在另一个进程中管理这个Messenger,用于基于消息的跨进程间通信。

###Message###

Message是一个final类，不能被继承。通常使用Message.obtain() 或Handler.obtainMessage()获取Message对象。Message.obtain()会从消息池中获取一个Message对象，如果消息池中是空的，才会使用构造方法实例化一个新Message，这样有利于消息资源的利用。并不需要担心消息池中的消息过多，它是有上限的，上限为10个。Handler.obtainMessage()具有多个重载方法，如果查看源码，会发现其实Handler.obtainMessage()在内部也是调用的Message.obtain()。　　

Message提供了getData()和setData()方法来获取与设置数据，其中操作的数据是一个Bundle对象，这个Bundle对象提供一系列的getXxx()和setXxx()方法用于传递基本数据类型的键值对。可用于基本类型和复杂的数据类型。对于复杂的数据类型，可以使用putParcelable(String key,Parcelable value)或pubSerializable(String key,Serializable value)方法：

- putParcelable(String key,Parcelable value)：需要传递的对象类实现Parcelable接口。

- pubSerializable(String key,Serializable value)：需要传递的对象类实现Serializable接口。

###Handler###

为了不阻塞用户界面，出现ANR的响应提示窗口，需要使用多线程来处理一些耗时操作。但Android的UI操作是线程非安全的，因此需要使用一些同步机制来使其刷新。

常使用的方法就是使用Handler来处理这些。

Handler会关联一个单独的线程和消息队列。Handler默认关联主线程，虽然要提供Runnable参数 ，但默认是直接调用Runnable中的run()方法。也就是默认下会在主线程执行，如果在这里面的操作会有阻塞，界面也会卡住。如果要在其他线程执行，可以使用HandlerThread。

####1. Handler有两个主要作用：####

- to schedule messages and runnables to be executed as some point in the future; 

- to enqueue an action to be performed on a different thread than your own.

####2. Handler将Runnable对象或Message对象到队列的方法：####

- post的方法：  （1）post(Runnable), （2）postAtTime(Runnable, long), （3）postDelayed(Runnable, long)

- sendMessage的方法： （1）sendEmptyMessage(int), （2）sendMessage(Message), （3）sendMessageAtTime(Message, long), （4）sendMessageDelayed(Message, long) 

####3. post方法举例####

	new Handler().postDelayed(new Runnable(){
	  @Override
	  public void run() {
	    // TODO Auto-generated method stub
	    Intent intent = new Intent(StartActivity.this, RegisterLoginActivity.class);
	    startActivity(intent);
	    StartActivity.this.finish();
	  }
	},3000);
或

	private static Handler handler=new Handler();
	public void buttonclicked(View view){
	  new Thread(new Runnable(){
	    public void run(){
	      handler.post(new Runnable(){
	        public void run(){
	          textview1.setText("hello Handler");
	        }
	      });
	    }
	  }).start();
	}

####4. sendMessage方法举例####

	public class HandlerMessageActivity1 extends Activity {
	    private Button btnDown;
	    private ImageView ivImage;
	    private static String image_path = "http://ww4.sinaimg.cn/bmiddle/786013a5jw1e7akotp4bcj20c80i3aao.jpg";
	    private ProgressDialog dialog;
	    private static int IS_FINISH = 1;
	
	    @Override
	    protected void onCreate(Bundle savedInstanceState) {
	        super.onCreate(savedInstanceState);
	        setContentView(R.layout.asynctask_activity);
	
	        btnDown = (Button) findViewById(R.id.btnDown);
	        ivImage = (ImageView) findViewById(R.id.ivSinaImage);
	
	        dialog = new ProgressDialog(this);
	        dialog.setTitle("提示信息");
	        dialog.setMessage("正在下载，请稍后...");
	        dialog.setCancelable(false);
	
	        btnDown.setOnClickListener(new View.OnClickListener() {
	            @Override
	            public void onClick(View v) {
	                    new Thread(new MyThread()).start();
	                    dialog.show();
	            }
	        });
	    }
	
	    private  Handler handler = new Handler() {
	        // 在Handler中获取消息，重写handleMessage()方法
	        @Override
	        public void handleMessage(Message msg) {            
	            // 判断消息码是否为1
	            if(msg.what==IS_FINISH){
	                byte[] data=(byte[])msg.obj;
	                Bitmap bmp=BitmapFactory.decodeByteArray(data, 0, data.length);
	                ivImage.setImageBitmap(bmp);
	                dialog.dismiss();
	            }
	        }
	    };
	
	    public class MyThread implements Runnable {
	
	        @Override
	        public void run() {
	            HttpClient httpClient = new DefaultHttpClient();
	            HttpGet httpGet = new HttpGet(image_path);
	            HttpResponse httpResponse = null;
	            try {
	                httpResponse = httpClient.execute(httpGet);
	                if (httpResponse.getStatusLine().getStatusCode() == 200) {
	                    byte[] data = EntityUtils.toByteArray(httpResponse
	                            .getEntity());
	                    // 获取一个Message对象，设置what为1
	                    Message msg = Message.obtain();
	                    msg.obj = data;
	                    msg.what = IS_FINISH;
	                    // 发送这个消息到消息队列中
	                    handler.sendMessage(msg);
	                }
	            } catch (Exception e) {
	                e.printStackTrace();
	            }
	        }
	    }
	}

###Looper###

Android中每一个Thread都跟着一个Looper，Looper可以帮助Thread维护一个消息队列，创建一个Looper对象时，会同时创建一个MessageQueue对象。

是Looper和Handler没有什么关系，我们从开源的代码可以看到Android还提供了一个Thread继承类HanderThread可以帮助我们处理，在HandlerThread对象中可以通过getLooper方法获取一个Looper对象控制句柄，我们可以将其这个Looper对象映射到一个Handler中去来实现一个线程同步机制，Looper对象的执行需要初始化Looper.prepare方法就是昨天我们看到的问题，同时推出时还要释放资源，使用Looper.release方法。

除了主线程有默认的Looper，其他线程默认是没有MessageQueue对象的，所以，不能接受Message。如需要接受，自己定义一个Looper对象(通过prepare函数),这样该线程就有了自己的Looper对象和MessageQueue数据结构了。 

Looper是MessageQueue的管理者。每一个MessageQueue都不能脱离Looper而存在，Looper对象的创建是通过prepare函数来实现的。同时每一个Looper对象和一个线程关联。通过调用Looper.myLooper()可以获得当前线程的Looper对象。调研loop（）方法用于创建一个初始化的Handler去与Looper通信。

Looper从MessageQueue中取出Message然后，交由Handler的handleMessage进行处理。处理完成后，调用Message.recycle()将其放入Message Pool中。

	class LooperThread extends Thread{
	  public Handler mHandler;
	  public void run(){
	    Looper.prepare();
	    mHandler=new Handler(){
	      public void handleMessage(Message msg){
	
	      }
	    }
	    Looper.loop();
	  }
	}

###MessageQueue###

MessageQueue是一种数据结构，就是一个消息队列，存放消息的地方。

每一个线程最多只可以拥有一个MessageQueue数据结构。 
创建一个线程的时候，并不会自动创建其MessageQueue。通常使用一个Looper对象对该线程的MessageQueue进行管理。主线程创建时，会创建一个默认的Looper对象，而Looper对象的创建，将自动创建一个Message Queue。其他非主线程，不会自动创建Looper，要需要的时候，通过调用prepare函数来实现。

###HandlerThread###

相比Handler，HandlerThread类用于启动一个新的线程，且该线程带有一个looper.

Handler和HandlerThread用法对比：

	//Handler常用用法：
	Handler handler = new Handler() {
	...
	}
	//改为HandlerThread：
	HandlerThread thread = new HandlerThread("athread");
	thread.start(); //要把线程启动
	Handler handler = new Handler(thread.getLooper()) {
	...
	} 

###Messenger###

之前我们使用Handler+Message的方式进行通信，都是在同一个进程中，从线程持有一个主线程的Handler对象，并向主线程发送消息。

Android既然可以使用bindler机制进行跨进行通信，所以我们当然可以将Handler与bindler结合起来进行跨进程发送消息。

一般使用方法如下：

- 远程通过`mMessenger = new Messenger(mHandler)`创建一个信使对象

- 客户端使用bindlerService请求连接远程

- 远程onBind方法返回一个bindler,`return mMessenger.getBinder();`

- 客户端使用远程返回的bindler得到一个信使（即得到远程信使）

	public void onServiceConnected(ComponentName name, IBinder service) {    
	    rMessenger = new Messenger(service);  　　　　
	    ...... 
	 }    

- 客户端可以使用这个远程信使对象向远程发送消息:`rMessenger.send(msg);`

###Android的其他界面刷新方法###

（1）postInvalidate()方法

（2）Task以及AsyncTask

参考：[Android Reference](http://developer.android.com/reference/android/os/Handler.html)和[android Messenger 跨进程通信](http://blog.csdn.net/cs_lht/article/details/6698468)


