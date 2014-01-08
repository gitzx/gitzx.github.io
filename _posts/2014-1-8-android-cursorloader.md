---
date: 2014-1-8 12:44:30+00:00
layout: post
title: Android中后台数据的加载
thread: 26
categories: android
tags: android
---

Android3.0加入了loaders，loaders可用于在activity或fragment中异步加载数据，loaders有多个类和接口：（1）LoaderManager；（2）LoaderManager.LoaderCallbacks；（3）Loader；（4）AsyncTaskLoader;（5）CursorLoader。

CursorLoader常用于在后台加载数据，在这小结下：

###在activity中使用CursorLoader###

通过实现LoaderManager.LoaderCallbacks接口来使用Loaders。

	public class PhotoThumbnailFragment extends FragmentActivity implements
	        LoaderManager.LoaderCallbacks<Cursor> {
	...
	}

###初始一个Loader###

每个activity或fragment只有一个LoaderManager，一个LoaderManager管理一个或多个Loader实例。在activity的onCreate()或fragment的onActivityCreated()中启动Loader。

	getLoaderManager().initLoader(0, null, this);

###启动或重连一个Loader###

通过onCreateLoader()来启动Loader，返回CursorLoader。

	public Loader<Cursor> onCreateLoader(int loaderID, Bundle bundle)
	{
	    switch (loaderID) {
	        case 0:
	            // Returns a new CursorLoader
	            return new CursorLoader(
	                        getActivity(),   // Parent activity context
	                        mDataUrl,        // Table to query
	                        mProjection,     // Projection to return
	                        null,            // No selection clause
	                        null,            // No selection arguments
	                        null             // Default sort order
	        );
	        default:
	            // An invalid id was passed in
	            return null;
	    }
	}

###重启一个Loader###

利用restartLoader()可以重启一个Loader，丢弃旧的数据。

	getLoaderManager().restartLoader(0, null, this);

###重设一个Loader###

onLoaderReset()用于重设一个Loader，使得它的数据不可用。

	SimpleCursorAdapter mAdapter;
	...
	public void onLoaderReset(Loader<Cursor> loader) {
	    mAdapter.swapCursor(null);
	}

###Loader结束###

当加载结束后，调用onLoaderFinished（）

	SimpleCursorAdapter mAdapter;
	...
	public void onLoadFinished(Loader<Cursor> loader, Cursor data) {
	    mAdapter.swapCursor(data);
	}

举个加载联系人的例子：

	public class ListViewLoader extends ListActivity implements LoaderManager.LoaderCallbacks<Cursor> {
	    SimpleCursorAdapter mAdapter;
	    static final String[] PROJECTION = new String[] {ContactsContract.Data._ID,
	            ContactsContract.Data.DISPLAY_NAME};
	
	    static final String SELECTION = "((" + 
	            ContactsContract.Data.DISPLAY_NAME + " NOTNULL) AND (" +
	            ContactsContract.Data.DISPLAY_NAME + " != '' ))";
	
	    @Override
	    protected void onCreate(Bundle savedInstanceState) {
	        super.onCreate(savedInstanceState);
	
	        ProgressBar progressBar = new ProgressBar(this);
	        progressBar.setLayoutParams(new LayoutParams(LayoutParams.WRAP_CONTENT,
	                LayoutParams.WRAP_CONTENT, Gravity.CENTER));
	        progressBar.setIndeterminate(true);
	        getListView().setEmptyView(progressBar);
	
	        ViewGroup root = (ViewGroup) findViewById(android.R.id.content);
	        root.addView(progressBar);
	
	        String[] fromColumns = {ContactsContract.Data.DISPLAY_NAME};
	        int[] toViews = {android.R.id.text1}; 
	
	        mAdapter = new SimpleCursorAdapter(this, 
	                android.R.layout.simple_list_item_1, null,
	                fromColumns, toViews, 0);
	        setListAdapter(mAdapter);
	
	        getLoaderManager().initLoader(0, null, this);
	    }
	
	    public Loader<Cursor> onCreateLoader(int id, Bundle args) {
	        return new CursorLoader(this, ContactsContract.Data.CONTENT_URI,
	                PROJECTION, SELECTION, null, null);
	    }
	
	    public void onLoadFinished(Loader<Cursor> loader, Cursor data) {
	        mAdapter.swapCursor(data);
	    }
	
	    public void onLoaderReset(Loader<Cursor> loader) {
	        mAdapter.swapCursor(null);
	    }
	
	    @Override 
	    public void onListItemClick(ListView l, View v, int position, long id) {
	        // Do something when a list item is clicked
	    }
	}

参考：[Loading Data in the Background](https://developer.android.com/training/load-data-background/index.html)

