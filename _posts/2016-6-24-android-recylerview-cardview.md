---
date: 2016-6-24 21:02:30+00:00
layout: post
title: Android中RecyclerView和CardView使用小结
thread: 145
categories: android
tags: android

---

RecyclerView和CardView是Android 5.0（API级别21）提供的新组件。在这篇中小结下。


### 创建[CardView](https://developer.android.com/reference/android/support/v7/widget/CardView.html) ###

一个CardView是一个ViewGroup，因此需要附加到Activity或者Fragment中，可以通过Layout XML创建。默认情况下，CardView是不可点击的，且没有任何的触摸反馈效果。如下包括一个TexView的CardView.

	<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
	    xmlns:tools="http://schemas.android.com/tools"
	    xmlns:card_view="http://schemas.android.com/apk/res-auto"
	    ... >
	    <!-- A CardView that contains a TextView -->
	    <android.support.v7.widget.CardView
	        xmlns:card_view="http://schemas.android.com/apk/res-auto"
	        android:id="@+id/card_view"
			android:clickable="true"
	        android:layout_gravity="center"
	        android:layout_width="200dp"
	        android:layout_height="200dp"
	        card_view:cardCornerRadius="4dp">
	
	        <TextView
	            android:id="@+id/info_text"
	            android:layout_width="match_parent"
	            android:layout_height="match_parent" />
	    </android.support.v7.widget.CardView>
	</LinearLayout>


### [RecyclerView](https://developer.android.com/reference/android/support/v7/widget/RecyclerView.html) ###

相比ListView和GridView等组件，RecyclerView更高级且灵活，RecyclerView是一个用于显示庞大数据集的容器，可以通过保持有限数量的视图进行有效的滚动操作。主要包括：

1. 布局管理器。RecyclerView提供的内置布局管理器有：

	（1）LinearLayoutManager 以垂直或水平滚动列表方式显示项目。

	（2）GridLayoutManager 在网格中显示项目。

	（3）StaggeredGridLayoutManager 在分散对齐网格中显示项目。

2. 适配器

3. 数据

具体实现如下：

1. 将LayoutManager添加至布局：

		<android.support.v7.widget.RecyclerView
		    xmlns:android="http://schemas.android.com/apk/res/android"
		    android:id="@+id/crime_recycler_view"
		    android:layout_width="match_parent"
		    android:layout_height="match_parent"/>

2. 和ListView类似，RecyclerView需要使用适配器来访问数据，简单定义数据如下：

		{% highlight java %}
		public class CrimeLab {
		    private static CrimeLab sCrimeLab;
		    private ArrayList<Crime> mCrimes;
		    public static CrimeLab get(Context context) {
		        if (sCrimeLab == null) {
		            sCrimeLab = new CrimeLab(context);
		        }
		        return sCrimeLab;
		    }
		    private CrimeLab(Context context) {
		        mCrimes = new ArrayList<>();
		        for (int i = 0; i < 100; i++) {
		            Crime crime = new Crime();
		            crime.setTitle("Crime #" + i);
		            crime.setSolved(i % 2 == 0);
		            mCrimes.add(crime);
		        }
		    }
		    public List<Crime> getCrimes() {
		        return mCrimes;
		    }
		}
		{% endhighlight %}

3. 使用适配器

（1）创建一个继承RecyclerView.ViewHolder的定制类。

	{% highlight java %}
	private class CrimeHolder extends RecyclerView.ViewHolder
	        implements View.OnClickListener {
	    private CardView cv;
	    private TextView mTitleTextView;
	    private Crime mCrime;
	    public CrimeHolder(View itemView) {
	        super(itemView);
	        itemView.setOnClickListener(this);
	        cv=(CardView)itemView.findViewById(R.id.card_view);
	        mTitleTextView = (TextView) itemView.findViewById(R.id.list_item_crime_title_text_view);
	    }
	
	    public void bindCrime(Crime crime) {
	        mCrime = crime;
	        mTitleTextView.setText(mCrime.getTitle());
	    }
	
	    @Override
	    public void onClick(View v) {
	    }
	}
	{% endhighlight %}

（2）继承RecyclerView.Adapter实现一个适配器，获取数据，进而显示出来

	{% highlight java %}
    private class CrimeAdapter extends RecyclerView.Adapter<CrimeHolder> {

        private List<Crime> mCrimes;
        public CrimeAdapter(List<Crime> crimes) {
            mCrimes = crimes;
        }
        @Override
        public CrimeHolder onCreateViewHolder(ViewGroup parent, int viewType) {
            LayoutInflater layoutInflater = LayoutInflater.from(getActivity());
            View view = layoutInflater.inflate(R.layout.list_item_crime, parent, false);
            return new CrimeHolder(view);
        }
        @Override
        public void onBindViewHolder(CrimeHolder holder, int position) {
            Crime crime = mCrimes.get(position);
            holder.bindCrime(crime);
        }
        @Override
        public int getItemCount() {
            return mCrimes.size();
        }
    }
	{% endhighlight %}



4.使用适配器


	{% highlight java %}
	mAdapter = new CrimeAdapter(crimes);
	mCrimeRecyclerView.setAdapter(mAdapter);
	{% endhighlight %}


### 添加依赖项 ###

RecyclerView与CardView小组件为 v7 支持内容库的一部分。如果要在项目中使用这些小组件，需要将这些Gradle依赖项添加到应用模块：

	dependencies {
	    ...
	    compile 'com.android.support:cardview-v7:21.0.+'
	    compile 'com.android.support:recyclerview-v7:21.0.+'
	}


### 其他 ###

[CardView](https://developer.android.com/reference/android/support/v7/widget/CardView.html)和[RecyclerView](https://developer.android.com/reference/android/support/v7/widget/RecyclerView.html)还可以定制各类布局和动画。如果要定制这些动画，需要扩展RecyclerView.ItemAnimator类别并使用 RecyclerView.setItemAnimator()方法。其他实用方法需要查看源码熟悉。

参考：[创建列表与卡片](https://developer.android.com/training/material/lists-cards.html#RecyclerView)