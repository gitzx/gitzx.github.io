---
date: 2014-1-24 17:23:30+00:00
layout: post
title: Android中AsyncTask的使用
thread: 33
categories: android
tags: android
---

Android UI是线程不安全的，Android线程有一个叫UI线程，也就是Main　Thread，其他的线程称为Worker Thread，Main Thread主要负责控制UI的显示、更新和交互等。为了保证用户操作流程和避免阻塞Main Thread，需要把一些耗时的操作如网络请求、数据库操作等封装到单独的线程，如果想要在其他子线程里进行UI操作，就需要借助Android的异步消息处理机制。

Android原生的AsyncTask常用于一些耗时较短的操作(最多几秒)，如果需要进行后台较长时间操作，则需要使用`java.util.concurrent`包中提供的API如[Executor](https://developer.android.com/reference/java/util/concurrent/Executor.html)、[ThreadPoolExecutor](https://developer.android.com/reference/java/util/concurrent/ThreadPoolExecutor.html)、[FutureTask](https://developer.android.com/reference/java/util/concurrent/FutureTask.html).
 
### AsyncTask的三个泛型参数 ###

由于AsyncTask是一个抽象类，所以如果我们想使用它，就必须要创建一个子类去继承它。在继承时我们可以为AsyncTask类指定三个泛型参数，这三个参数的用途如下：

- Params。在执行AsyncTask时需要传入的参数，可用于在后台任务中使用。

- Progress。后台任务执行时，如果需要在界面上显示当前的进度，则使用这里指定的泛型作为进度单位。

- Result。当任务执行完毕后，如果需要对结果进行返回，则使用这里指定的泛型作为返回值类型。

### AsyncTask执行的步骤 ###

子类至少要重写一个方法doInbackground(Params...)。

- onPreExecute(). 在任务执行前唤醒UI线程，如精度条的显示；

- doInbackground(Params...). 在onPreExecute()执行完毕后唤醒后台线程，常用于执行耗时任务。如果AsyncTask的第三个泛型参数指定的是Void，就可以不返回任务执行结果。注意，在这个方法中是不可以进行UI操作的，如果需要更新UI元素，比如说反馈当前任务的执行进度，可以调用publishProgress(Progress...)方法来完成。

- onProgressUpdate(Progress...). 在当在后台任务中调用了publishProgress(Progress...)方法后，这个方法就很快会被调用，方法中携带的参数就是在后台任务中传递过来的。在这个方法中可以对UI进行操作，利用参数中的数值就可以对界面元素进行相应的更新。

- onPostExecute(Result)。 当后台任务执行完毕并通过return语句进行返回时，这个方法就很快会被调用。返回的数据会作为参数传递到此方法中，可以利用返回的数据来进行一些UI操作，比如说提醒任务执行的结果，以及关闭掉进度条对话框等。

### AsyncTask的简单使用 ###

	public class AsyncTaskActivity extends Activity{
		
		Button download;  
	    ProgressBar pb;  
	    TextView tv; 
		@Override
		public void onCreate(Bundle savedInstanceState){
			super.onCreate(savedInstanceState);
			setContentView(R.layout.asynctask);
			pb=(ProgressBar)findViewById(R.id.pb);  
	        tv=(TextView)findViewById(R.id.tv); 
		}	
		public void downloadfiles(View view){
			DownloadFilesTask dTask = new DownloadFilesTask();  
	        dTask.execute(100); 
		}
		class DownloadFilesTask extends AsyncTask<Integer,Integer,String> {
	
				protected void onPreExectute(){
					super.onPreExecute();
				}
	
			    @Override  
			    protected String doInBackground(Integer... params) {  
			        //第二个执行方法,onPreExecute()执行完后执行  
			        for(int i=0;i<=100;i++){  
			            pb.setProgress(i);  
			            publishProgress(i);  
			            try {  
			                Thread.sleep(params[0]);  
			            } catch (InterruptedException e) {  
			                e.printStackTrace();  
			            }  
			        }  
			        return "执行完毕";  
			    }  
	
			    @Override  
			    protected void onProgressUpdate(Integer... progress) { 
			        tv.setText(progress[0]+"%");  
			        super.onProgressUpdate(progress);  
			    }  
	
			    @Override  
			    protected void onPostExecute(String result) {  
			        setTitle(result);  
			        super.onPostExecute(result);  
			    }	
		}
	}

其中，layout中用到了一个按钮Button和一个进度条Progress。

取消任务：调用cancel(boolean)可以在任何时刻取消任务

### AsyncTask执行规则 ###

- AsyncTask类必须在UI线程中加载；

- 任务实例必须在UI线程中创建；

- execute(Params...)必须在UI线程中执行；

-  onPreExecute(), onPostExecute(Result), doInBackground(Params...), onProgressUpdate(Progress...)不能手动调用；

- 每次任务只执行一次。

### 屏幕旋转引起任务中断 ###

AsyncTask常用于最多几秒的后台操作中，但当AsyncTask执行过程中，屏幕发生旋转，屏幕前台Activity会重启，会导致依附在Activity的AsyncTask无效。主要有如下几种解决方法：

（1）在Fragment中使用AsyncTask。Fragment通过调用`setRetainInstance(true)`可以保存Fragment实例信息，即时Fragment跟着Activity消耗，我们可以通过跟踪标志位确定AsyncTask是否在运行，然后在Frament重启`onActivityCreated()`后在确定是否执行AsyncTask任务。

（2）避免使用AsyncTask，可以采用其他替代方案如`IntentService`或者其他开源库；

（3）避免屏幕旋转。


参考：[AsyncTask](http://developer.android.com/reference/android/os/AsyncTask.html)和[Android AsyncTask完全解析，带你从源码的角度彻底理解](http://blog.csdn.net/guolin_blog/article/details/11711405)
