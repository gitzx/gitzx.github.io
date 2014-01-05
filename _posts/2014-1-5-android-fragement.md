---
date: 2014-1-5 13:49:30+00:00
layout: post
title: Android fragments的使用
thread: 23
categories: android
tags: android
---

Android3.0提供了fragments用来解决不同屏幕分辨率的界面动态显示。类似于Activity，Fragment通常是嵌套在Activity中使用的，可用于向activity提供布局。

###Fragments的生命周期###

Fragments的生命周期和Activities的对应图如下：

![](/assets/blog_pic/activity_fragment_lifecycle.png)

和activity类似，一个fragment存在三种状态：（1）Resumed;(2)Paused;(3)Stopped.

为了使用fragment，至少实现三个方法：（1）onCreate();（2）onCreateView();（3）onPause().

###Fragments的子类###

Fragments有三个子类：

- DialogFragment

- ListFragment

- PreferenceFragment

###Fragments的使用###

####提供fragment####

	public static class ExampleFragment extends Fragment {
	    @Override
	    public View onCreateView(LayoutInflater inflater, ViewGroup container,Bundle savedInstanceState) {
	        // Inflate the layout for this fragment
	        return inflater.inflate(R.layout.example_fragment, container, false);
	    }
	}

example_fragment.xml如下：

	<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"  
	    android:layout_width="match_parent"  
	    android:layout_height="match_parent"  
	    android:background="#ffff00" >   
	    <TextView  
	        android:layout_width="wrap_content"  
	        android:layout_height="wrap_content"  
	        android:text="fragment"  
	        android:textColor="#000000"  
	        android:textSize="25sp" />  
	</LinearLayout>  

####在activity中利用xml添加fragment####
（1）在layout中声明fragment

	<?xml version="1.0" encoding="utf-8"?>
	<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
	    android:orientation="horizontal"
	    android:layout_width="match_parent"
	    android:layout_height="match_parent">
	    <fragment android:name="com.example.news.ArticleListFragment"
	            android:id="@+id/list"
	            android:layout_weight="1"
	            android:layout_width="0dp"
	            android:layout_height="match_parent" />
	    <fragment android:name="com.example.news.ArticleReaderFragment"
	            android:id="@+id/viewer"
	            android:layout_weight="2"
	            android:layout_width="0dp"
	            android:layout_height="match_parent" />
	</LinearLayout>

（2）调用fragment

	public class MainActivity extends Activity {  
	    @Override  
	    protected void onCreate(Bundle savedInstanceState) {  
	        super.onCreate(savedInstanceState);  
	        setContentView(R.layout.activity_main);  
	    }  
	}  

####在activity中动态添加fragment####

在activity中对fragment进行处理（如add、remove或replace）：

（1）指定放置fragment的ViewGroup；

（2）使用FragmentTransaction这个APIs。

	FragmentManager fragmentManager = getFragmentManager()
	FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
	ExampleFragment fragment = new ExampleFragment();
	fragmentTransaction.add(R.id.fragment_container, fragment); //增加
	fragmentTransaction.remove(R.id.fragment_container, fragment); //删除
	fragmentTransaction.replace(R.id.fragment_container, fragment2); //替换
	fragmentTransaction.commit(); //提交确认

参考：[Android Development](http://developer.android.com/guide/components/fragments.html)