---
date: 2014-2-16 16:17:30+00:00
layout: post
title: Android中下拉刷新
thread: 376
categories: android
tags: android
---

最近在做局域网通信，需要用到ListView的下拉刷新功能，在这小结下。

先定义一个下拉刷新的布局文件`refresh_head.xml`.

	<?xml version="1.0" encoding="utf-8"?>
	
	<!-- ListView的头部 -->
	<LinearLayout
	  xmlns:android="http://schemas.android.com/apk/res/android"
	  android:layout_width="fill_parent"
	  android:layout_height="wrap_content"
	 >
	  <!-- 内容 -->
	  <RelativeLayout
	  android:layout_width="fill_parent"
	  android:layout_height="wrap_content"
	  android:id="@+id/head_contentLayout"
	  android:paddingLeft="30dp"
	  >
	  <!-- 箭头图像、进度条 -->
	  <FrameLayout
	  android:layout_width="wrap_content"
	  android:layout_height="wrap_content"
	  android:layout_alignParentLeft="true"
	  android:layout_centerVertical="true"
	  >
	  <!-- 箭头 -->
	  <ImageView
	  android:layout_width="wrap_content"
	  android:layout_height="wrap_content"
	  android:layout_gravity="center"
	  android:src="@drawable/arrow"
	  android:id="@+id/head_arrowImageView"
	  /> 
	  <!-- 进度条 -->
	  <ProgressBar
	  android:layout_width="wrap_content"
	  android:layout_height="wrap_content"
	  style="?android:attr/progressBarStyleSmall"
	  android:layout_gravity="center"
	  android:id="@+id/head_progressBar"
	  android:visibility="gone"
	  />
	  </FrameLayout> 
	  <!-- 提示、最近更新 -->
	  <LinearLayout
	  android:layout_width="wrap_content"
	  android:layout_height="wrap_content"
	  android:layout_centerHorizontal="true"
	  android:orientation="vertical"
	  android:gravity="center_horizontal"
	  >
	  <!-- 提示 -->
	  <TextView
	  android:layout_width="wrap_content"
	  android:layout_height="wrap_content"
	  android:text="下拉刷新"
	  android:textColor="@color/black"
	  android:textSize="20sp"
	  android:id="@+id/head_tipsTextView"
	  /> 
	  <!-- 最近更新 -->
	  <TextView
	  android:layout_width="wrap_content"
	  android:layout_height="wrap_content"
	  android:id="@+id/head_lastUpdatedTextView"
	  android:text="上次更新"
	  android:textColor="@color/black"
	  android:textSize="10sp"
	  />
	  </LinearLayout>
	  </RelativeLayout>
	</LinearLayout>

下拉刷新的类如下：

	public class PullToRefreshExpandableListView extends ExpandableListView implements OnScrollListener {
	
		/** 松开刷新 */
		private final static int RELEASE_TO_REFRESH = 0;
		/** 下拉刷新 */
		private final static int PULL_TO_REFRESH = 1;
		/** 正在刷新中 */
		private final static int REFRESHING = 2;
		/** 完成 */
		private final static int DONE = 3;
	
		// 实际的padding的距离与界面上偏移距离的比例
		private final static int RATIO = 3;
		private LayoutInflater inflater;
		private LinearLayout headView;
		private TextView tipsTextview;
		private TextView lastUpdatedTextView;
		/** 箭头图像 */
		private ImageView arrowImageView;
		private ProgressBar progressBar;
		private RotateAnimation animation;
		// 反转动画
		private RotateAnimation reverseAnimation;
		private int headContentWidth;
		private int headContentHeight;
		/** 手势按下的起点位置 */
		private int startY;
		private int firstItemIndex;
		private int state;
		private boolean isBack;
		private OnRefreshListener refreshListener;
		private boolean isRefreshable;
		public PullToRefreshExpandableListView(Context context) {
			super(context);
			init(context);
		}
		public PullToRefreshExpandableListView(Context context, AttributeSet attrs) {
			super(context, attrs);
			init(context);
		}
		private void init(Context context) {
			inflater = LayoutInflater.from(context);
			headView = (LinearLayout) inflater.inflate(R.layout.refresh_head, null);//加载头布局
			arrowImageView = (ImageView) headView.findViewById(R.id.head_arrowImageView);//箭头
			arrowImageView.setMinimumWidth(70);
			arrowImageView.setMinimumHeight(50);
			progressBar = (ProgressBar) headView.findViewById(R.id.head_progressBar);
			tipsTextview = (TextView) headView.findViewById(R.id.head_tipsTextView);
			lastUpdatedTextView = (TextView) headView.findViewById(R.id.head_lastUpdatedTextView);
			// measureView(headView);
			headView.measure(0, 0);
			headContentHeight = headView.getMeasuredHeight();//头部高度
			headContentWidth = headView.getMeasuredWidth();//头部宽度
			/*
			 * 设置padding -1 * headContentHeight就可以把该headview隐藏在屏幕顶部，
			 * 前提是要得到headview的确切高度
			 */
			headView.setPadding(0, -1 * headContentHeight, 0, 0);
			/*
			 * Invalidate the whole view. If the view is visible,
			 * onDraw(android.graphics.Canvas) will be called at some point in the
			 * future. This must be called from a UI thread. To call from a non-UI
			 * thread, call postInvalidate().
			 */
			headView.invalidate();
			addHeaderView(headView, null, false);
			setOnScrollListener(this);
			animation = new RotateAnimation(0, -180, RotateAnimation.RELATIVE_TO_SELF, 0.5f, RotateAnimation.RELATIVE_TO_SELF, 0.5f);
			animation.setInterpolator(new LinearInterpolator());
			animation.setDuration(250);
			animation.setFillAfter(true);
			reverseAnimation = new RotateAnimation(-180, 0, RotateAnimation.RELATIVE_TO_SELF, 0.5f, RotateAnimation.RELATIVE_TO_SELF, 0.5f);
			reverseAnimation.setInterpolator(new LinearInterpolator());
			reverseAnimation.setDuration(200);
			reverseAnimation.setFillAfter(true);
			state = DONE;
			isRefreshable = false;
		}
	
		/**
		 * 实现OnScrollListener接口的两个方法
		 */
		public void onScroll(AbsListView arg0, int firstVisiableItem, int arg2, int arg3) {
			firstItemIndex = firstVisiableItem;
		}
		public void onScrollStateChanged(AbsListView arg0, int arg1) {
		}
		/**
		 * 设置触摸事件 总的思路就是
		 * 
		 * 1 ACTION_DOWN：记录起始位置
		 * 
		 * 2 ACTION_MOVE：计算当前位置与起始位置的距离，来设置state的状态
		 * 
		 * 3 ACTION_UP：根据state的状态来判断是否下载
		 */
		public boolean onTouchEvent(MotionEvent event) {
	
			if (isRefreshable) {
				switch (event.getAction()) {
				case MotionEvent.ACTION_DOWN:
					if (firstItemIndex == 0) {
						startY = (int) event.getY();
	//					Log.v(TAG, "在down时候记录当前位置‘");
					}
					break;
				case MotionEvent.ACTION_MOVE:
					int tempY = (int) event.getY();
					if (state == PULL_TO_REFRESH) {
						setSelection(0);// 这句代码很重要
						// 下拉到可以进入RELEASE_TO_REFRESH的状态
						if ((tempY - startY) / RATIO >= headContentHeight) {
							state = RELEASE_TO_REFRESH;
							isBack = true;
							changeHeaderViewByState();
	//						Log.v(TAG, "由done或者下拉刷新状态转变到松开刷新");
						}
						// 上推到顶了
						else if (tempY - startY <= 0) {
							state = DONE;
							changeHeaderViewByState();
	//						Log.v(TAG, "由DOne或者下拉刷新状态转变到done状态");
						}
						headView.setPadding(0, -headContentHeight + (tempY - startY) / RATIO, 0, 0);
					}
					if (state == RELEASE_TO_REFRESH) {
						setSelection(0);
						// 往上推了，推到了屏幕足够掩盖head的程度，但是还没有推到全部掩盖的地步
						if (((tempY - startY) / RATIO < headContentHeight) && (tempY - startY) > 0) {
							state = PULL_TO_REFRESH;
							changeHeaderViewByState();
	//						Log.v(TAG, "由松开刷新状态转变到下拉刷新状态");
						}
						headView.setPadding(0, -headContentHeight + (tempY - startY) / RATIO, 0, 0);
					}
					// done状态下
					if (state == DONE) {
						if (tempY - startY > 0) {
							state = PULL_TO_REFRESH;
							changeHeaderViewByState();
						}
					}
					break;
				case MotionEvent.ACTION_UP:
					if (state != REFRESHING) {
						// 不在刷新状态
						if (state == PULL_TO_REFRESH) {
							state = DONE;
							changeHeaderViewByState();
	//						Log.v(TAG, "下拉刷新状态，到done状态");
						}
						if (state == RELEASE_TO_REFRESH) {
							state = REFRESHING;
							changeHeaderViewByState();
							onRefresh();
	//						Log.v(TAG, "松开刷新状态，到done状态");
						}
					}
					isBack = false;
					break;
	
				}
			}
	
			return super.onTouchEvent(event);
		}
	
		/**
		 * 当状态改变时候，调用该方法，以更新界面
		 */
		private void changeHeaderViewByState() {
			switch (state) {
			case RELEASE_TO_REFRESH:
				arrowImageView.setVisibility(View.VISIBLE);
				progressBar.setVisibility(View.GONE);
				tipsTextview.setVisibility(View.VISIBLE);
	
				arrowImageView.clearAnimation();
				arrowImageView.startAnimation(animation);
				tipsTextview.setText("松开刷新");
	//			Log.v(TAG, "当前状态，松开刷新");
				break;
			case PULL_TO_REFRESH:
				progressBar.setVisibility(View.GONE);
				tipsTextview.setVisibility(View.VISIBLE);
	
				arrowImageView.clearAnimation();
				arrowImageView.setVisibility(View.VISIBLE);
				tipsTextview.setText("下拉刷新");
				// 是RELEASE_To_REFRESH状态转变来的
				if (isBack) {
					isBack = false;
					arrowImageView.startAnimation(reverseAnimation);
				}
	//			Log.v(TAG, "当前状态，下拉刷新");
				break;
	
			case REFRESHING:
				headView.setPadding(0, 0, 0, 0);
				progressBar.setVisibility(View.VISIBLE);
				arrowImageView.clearAnimation();
				arrowImageView.setVisibility(View.GONE);
				tipsTextview.setText("正在刷新...");
				break;
			case DONE:
				headView.setPadding(0, -headContentHeight, 0, 0);
				progressBar.setVisibility(View.GONE);
				arrowImageView.clearAnimation();
				arrowImageView.setImageResource(R.drawable.arrow);
				tipsTextview.setText("下拉刷新");
				break;
			}
		}
	
		public void setOnRefreshListener(OnRefreshListener refreshListener) {
			this.refreshListener = refreshListener;
			isRefreshable = true;
		}
	
		public interface OnRefreshListener {
			public void onRefresh();
		}
	
		public void onRefreshComplete() {
			state = DONE;
			lastUpdatedTextView.setText("最近更新:" + new Date().toLocaleString());
			changeHeaderViewByState();
		}
	
		private void onRefresh() {
			if (refreshListener != null) {
				refreshListener.onRefresh();
			}
		}
		@Override
		public void setAdapter(ListAdapter adapter) {
			lastUpdatedTextView.setText("最近更新:" + new Date().toLocaleString());
			super.setAdapter(adapter);
		}
	
	}

打开或新建activity_main.xml作为程序主界面的布局，加入如下代码：

	<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"  
	    xmlns:tools="http://schemas.android.com/tools"  
	    android:layout_width="match_parent"  
	    android:layout_height="match_parent"  
	    tools:context=".MainActivity" >  
	  
	    <com.example.pulltorefreshtest.PullToRefreshExpandableListView  
	        android:id="@+id/refreshable_view"  
	        android:layout_width="fill_parent"  
	        android:layout_height="fill_parent" >  
	  
	        <ListView  
	            android:id="@+id/list_view"  
	            android:layout_width="fill_parent"  
	            android:layout_height="fill_parent" >  
	        </ListView>  
	    </com.example.pulltorefreshtest.RefreshableView>  
	  
	</RelativeLayout>  

此时，就可以在程序中调用下拉刷新功能。

参考：[Android下拉刷新完全解析，教你如何一分钟实现下拉刷新功能](http://blog.csdn.net/guolin_blog/article/details/9255575)