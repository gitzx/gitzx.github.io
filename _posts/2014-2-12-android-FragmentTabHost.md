---
date: 2014-2-12 18:17:30+00:00
layout: post
title: Android中FragmentTabHost底部显示
thread: 36
categories: android
tags: android
---

Android在3.0的版本引入了Fragment，在TabHost中可以嵌入Fragment。在这小结下FragmentTabHost的用法。

MainActivity.java如下：

	public class MainActivity extends FragmentActivity {
	
		@Override
		protected void onCreate(Bundle savedInstanceState) {
			super.onCreate(savedInstanceState);
			
			setContentView(R.layout.main);
		
			FragmentTabHost tabHost = (FragmentTabHost)findViewById(android.R.id.tabhost);
			tabHost.setup(this, getSupportFragmentManager(), R.id.realtabcontent);
			//1
			tabHost.addTab(tabHost.newTabSpec("Apple")
				   				  .setIndicator("Apple"), 
	   					  AppleFragment.class, 
	   					  null);
		    //2
			tabHost.addTab(tabHost.newTabSpec("Google")
					   			  .setIndicator("Google"), 
						  GoogleFragment.class, 
						  null);
		    //3
			tabHost.addTab(tabHost.newTabSpec("Facebook")
					   			  .setIndicator("Facebook"), 
						  FacebookFragment.class, 
					      null);
		    //4
			tabHost.addTab(tabHost.newTabSpec("Twitter")
				   				  .setIndicator("Twitter"), 
						  TwitterFragment.class, 
						  null);
		}
	｝

在布局文件main.xml如下（Tab底部显示）：

	<?xml version="1.0" encoding="utf-8"?>
	<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
	    android:layout_width="match_parent"
	    android:layout_height="match_parent"
	    android:orientation="vertical" >
	    
	      
	     <FrameLayout android:id="@+id/realtabcontent"
	         android:layout_width="match_parent"
	         android:layout_height="0dp"
	         android:layout_weight="1"
	          />
	 <android.support.v4.app.FragmentTabHost
	        android:id="@android:id/tabhost"
	        android:layout_width="match_parent"
	        android:layout_height="wrap_content" >
	
	    
	       <TabWidget 
	         android:id="@android:id/tabs"
	         android:layout_width="match_parent"
	         android:layout_height="wrap_content"
	         android:layout_alignParentBottom="true" 
	         />
	    
	       <FrameLayout 
	         android:id="@android:id/tabcontent"
	         android:layout_width="match_parent"
	         android:layout_height="wrap_content"
	         />
	    </android.support.v4.app.FragmentTabHost>
	</LinearLayout>

在每个Tab页面中加入Fragment如AppleFragment等。

参考：[FragmentTabHost](http://developer.android.com/reference/android/support/v4/app/FragmentTabHost.html)