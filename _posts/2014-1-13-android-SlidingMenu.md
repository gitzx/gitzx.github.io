---
date: 2014-1-13 11:22:30+00:00
layout: post
title: 利用Android开源库SlidingMenu实现侧滑效果
thread: 29
categories: android
tags: android
---

大量的Android应用采用了主界面左滑或右滑界面。为了更流畅，比较常用的是利用Android开源库[SlidingMenu](https://github.com/jfeinstein10/SlidingMenu)和fragment来实现，最近也想实现侧滑效果，在这小结下。

###实现步骤###

（1）SlidingMenu依赖于另一个开源库[ActionBarSherlock](http://actionbarsherlock.com/). 下载这两个项目后，将SlidingMenu目录下的library工程和ActionBarSherlock目录下的actionbarsherlock导入到exlipse中。

（2）由于library库用到了actionbarsherlock库，因此需要将actionbarsherlock库添加到library。（右键library->properties->Android->library->Add选择actionbarsherlock库）。

注：library和actionbarsherlock中的android-support-v4.jar版本不一致： 解决方法是将library中的android-support-v4.jar删除将actionbarsherlock中的android-support-v4.jar复制到actionbarsherlock中，然后clean一下这两个工程

（3）运行SlidingMenu中的example工程。

- 将SlidingMenu目录下的example导入到eclipse中，参考（2），将library和actionbarsherlock两个库添加到ExampleListActivity工程中。

- 在libary项目中SlidingFragmentActivity这个类并在声明前添加以下代码:
`import com.actionbarsherlock.app.SherlockFragmentActivity;`  

- 将`public class SlidingFragmentActivity extends FragmentActivity implements SlidingActivityBase`换成`public class SlidingFragmentActivity extends SherlockFragmentActivity implements SlidingActivityBase`

- 运行ExampleListActivity即可。

###SlidingMenu常用属性###

	menu.setMode(SlidingMenu.LEFT);//设置左滑菜单
	menu.setTouchModeAbove
	//设置滑动的屏幕范围，该设置为全屏区域都可以滑动
	(SlidingMenu.TOUCHMODE_FULLSCREEN);
	menu.setShadowDrawable(R.drawable.shadow);//设置阴影图片
	menu.setShadowWidthRes(R.dimen.shadow_width);//设置阴影图片的宽度
	menu.setBehindOffsetRes(R.dimen.slidingmenu_offset);//SlidingMenu划出时主页面显示的剩余宽度
	menu.setBehindWidth(400);//设置SlidingMenu菜单的宽度
	menu.setFadeDegree(0.35f);//SlidingMenu滑动时的渐变程度
	menu.attachToActivity(this, SlidingMenu.SLIDING_CONTENT);//使SlidingMenu附加在Activity上
	menu.setMenu(R.layout.menu_layout);//设置menu的布局文件
	menu.toggle();//动态判断自动关闭或开启SlidingMenu
	menu.showMenu();//显示SlidingMenu
	menu.showContent();//显示内容
	menu.setOnOpenListener(onOpenListener);//监听slidingmenu打开
	关于关闭menu有两个监听，简单的来说，对于menu close事件，一个是when,一个是after 
	menu.OnClosedListener(OnClosedListener);//监听slidingmenu关闭时事件
	menu.OnClosedListener(OnClosedListener);//监听slidingmenu关闭后事件
	//左右都可以划出SlidingMenu菜单只需要设置
	menu.setMode(SlidingMenu.LEFT_RIGHT);属性，然后设置右侧菜单的布局文件
	menu.setSecondaryShadowDrawable(R.drawable.shadowright);//右侧菜单的阴影图片


###设置fragment显示###

	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		// set the Above View
		if (savedInstanceState != null)
			mContent = getSupportFragmentManager().getFragment(savedInstanceState, "mContent");
		if (mContent == null)
			mContent = new ColorFragment(R.color.red);	

		// set the Above View
		setContentView(R.layout.content_frame);
		getSupportFragmentManager()
		.beginTransaction()
		.replace(R.id.content_frame, mContent)
		.commit();
		
		// set the Behind View
		setBehindContentView(R.layout.menu_frame);
		getSupportFragmentManager()
		.beginTransaction()
		.replace(R.id.menu_frame, new ColorMenuFragment())
		.commit();
		
		// customize the SlidingMenu
		getSlidingMenu().setTouchModeAbove(SlidingMenu.TOUCHMODE_FULLSCREEN);
	}

参考：[Android开源项目SlidingMenu深入剖析](http://blog.csdn.net/t12x3456/article/details/12798157)