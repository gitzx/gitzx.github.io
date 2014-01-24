---
date: 2014-1-24 10:42:30+00:00
layout: post
title: 利用Actionbarsherlock库实现滑动翻页Tabs
thread: 32
categories: android
tags: android
---

在Android3.0之前，adnroid的tabs常使用TabHost来实现。在Android3.0以后，可以使用ActionBar来实现Tabs.

但ActionBar是在3.0以上才有的，google并没有给我提供在3.0以下支持ActionBar的包，我们可以利用[Actionbarsherlock](http://actionbarsherlock.com/)来实现对Android3.0以下版本ActionBar的支持。在这小结下利用Actionbarsherlock库和viewpager来实现Tabs。

####实现步骤####

（1）下载Actionbarsherlock库并导入到Android项目中。

（2）在activity_main.xml中使用ViewPager。
	
	<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
	    xmlns:tools="http://schemas.android.com/tools"
	    android:layout_width="match_parent"
	    android:layout_height="match_parent" >
	
	    <android.support.v4.view.ViewPager
	        android:id="@+id/pager"
	        android:layout_width="wrap_content"
	        android:layout_height="wrap_content"
	     />
	
	</RelativeLayout>

（3）MainActivity.java如下：
	
	package io.github.gitzx;
	
	import android.os.Bundle;
	import android.support.v4.app.FragmentManager;
	import android.support.v4.app.FragmentTransaction;
	import android.support.v4.view.ViewPager;
	import android.view.Window;
	import com.actionbarsherlock.app.ActionBar;
	import com.actionbarsherlock.app.ActionBar.Tab;
	import com.actionbarsherlock.app.SherlockFragmentActivity;
	import com.actionbarsherlock.view.Menu;
	
	public class MainActivity extends SherlockFragmentActivity {
		ActionBar mActionBar;
		ViewPager mPager;
		
	    @Override
	    public void onCreate(Bundle savedInstanceState) {
	        super.onCreate(savedInstanceState);
	        setContentView(R.layout.activity_main);
	        
	        mActionBar = getSupportActionBar();  
	        /** 设置tab导航类型*/
	        mActionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_TABS);
	        mPager = (ViewPager) findViewById(R.id.pager);
	        FragmentManager fm = getSupportFragmentManager();            
	        ViewPager.SimpleOnPageChangeListener pageChangeListener = new ViewPager.SimpleOnPageChangeListener(){
	        	@Override
	        	public void onPageSelected(int position) {        		
	        		super.onPageSelected(position);
	        		mActionBar.setSelectedNavigationItem(position);        		
	        	}
	        	
	        };
	        mPager.setOnPageChangeListener(pageChangeListener);
	        MyFragmentPagerAdapter fragmentPagerAdapter = new MyFragmentPagerAdapter(fm);
	        mPager.setAdapter(fragmentPagerAdapter);
	        mActionBar.setDisplayShowTitleEnabled(true);   
	        /** 定义Tab监听*/
	        ActionBar.TabListener tabListener = new ActionBar.TabListener() {
				
				@Override
				public void onTabUnselected(Tab tab, FragmentTransaction ft) {				
				}
				
				@Override
				public void onTabSelected(Tab tab, FragmentTransaction ft) {
					mPager.setCurrentItem(tab.getPosition());
					
				}
				
				@Override
				public void onTabReselected(Tab tab, FragmentTransaction ft) {
				}
			};
	
			/** 创建Tabs*/
	        Tab tab = mActionBar.newTab()
	                           .setText("Android")
	                           .setIcon(R.drawable.android)
	                           .setTabListener(tabListener);
	        
	        mActionBar.addTab(tab);
	
	        tab = mActionBar.newTab()
	                       .setText("Apple")
	                       .setIcon(R.drawable.apple)
	                       .setTabListener(tabListener);                               
	
	        mActionBar.addTab(tab);        
	        
	    }
	
	    @Override
	    public boolean onCreateOptionsMenu(Menu menu) {
	        getSupportMenuInflater().inflate(R.menu.activity_main, menu);
	        return true;
	    }
	}

（4）程序中扩展了FragmentPagerAdapter，如下：

	package io.github.gitzx;
	
	import android.os.Bundle;
	import android.support.v4.app.Fragment;
	import android.support.v4.app.FragmentManager;
	import android.support.v4.app.FragmentPagerAdapter;
	
	public class MyFragmentPagerAdapter extends FragmentPagerAdapter{  
	    final int PAGE_COUNT = 2;
	    public MyFragmentPagerAdapter(FragmentManager fm) {
	        super(fm);
	        
	    }
	    @Override
	    public Fragment getItem(int arg0) {
	        Bundle data = new Bundle();
	        switch(arg0){
	            case 0:
	                AndroidFragment androidFragment = new AndroidFragment();                
	                data.putInt("current_page", arg0+1);
	                androidFragment.setArguments(data);
	                return androidFragment;
	            case 1:
	                AppleFragment appleFragment = new AppleFragment();
	                data.putInt("current_page", arg0+1);
	                appleFragment.setArguments(data);
	                return appleFragment;   
	        }
	        
	        return null;
	    }
	    /** 返回pages页数 */
	    @Override
	    public int getCount() {     
	        return PAGE_COUNT;
	    }
	}

（4）程序中需在定义实现多个个Fragment用于Tabs之间的切换，如上使用的AndroidFragment和AppleFragment来实现两个Tabs之间的切换。AndroidFrament如下（用于显示Android的版本代号列表）：

	package io.github.gitzx;
	
	import android.os.Bundle;
	import android.view.LayoutInflater;
	import android.view.View;
	import android.view.ViewGroup;
	import android.widget.ArrayAdapter;
	import android.widget.ListView;
	import com.actionbarsherlock.app.SherlockListFragment;
	public class AndroidFragment extends SherlockListFragment{
	    String android_versions[] = new String[]{
	            "Jelly Bean",
	            "IceCream Sandwich",
	            "HoneyComb",
	            "Ginger Bread",
	            "Froyo"
	    };
	    
	    @Override
	    public View onCreateView(LayoutInflater inflater, ViewGroup container,
	            Bundle savedInstanceState) {
	        ArrayAdapter<String> adapter = new ArrayAdapter<String>(getActivity().getBaseContext(), android.R.layout.simple_list_item_multiple_choice, android_versions);
	        setListAdapter(adapter);
	        return super.onCreateView(inflater, container, savedInstanceState);
	
	    }
	    @Override
	    public void onStart() {
	        super.onStart();
	        getListView().setChoiceMode(ListView.CHOICE_MODE_MULTIPLE);
	
	    }
	}


