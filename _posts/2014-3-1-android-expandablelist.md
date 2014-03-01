---
date: 2014-3-1 18:23:30+00:00
layout: post
title: Android中expandablelistview的实现
thread: 40
categories: android
tags: android
---

有多种方式可以实现类似qq的多级列表功能，其中比较常见的是利用expandablelist来实现，最近用到了这个，在这小结下。

###布局包括三个：###

activity_main.xml：

	<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
	    xmlns:tools="http://schemas.android.com/tools"
	    android:layout_width="match_parent"
	    android:layout_height="match_parent"
	    tools:context=".MainActivity" >
	 
	    <ExpandableListView
	        android:id="@+id/laptop_list"
	        android:layout_width="match_parent"
	        android:layout_height="fill_parent" >
	    </ExpandableListView>
	</RelativeLayout>

group_item.xml：

	<?xml version="1.0" encoding="utf-8"?>
	<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
	    android:layout_width="match_parent"
	    android:layout_height="match_parent"
	    android:orientation="vertical"
	    android:padding="10dp" >
	 
	    <TextView
	        android:id="@+id/laptop"
	        android:layout_width="wrap_content"
	        android:layout_height="wrap_content"
	        android:paddingLeft="25dp"/>
	</LinearLayout>

child_item.xml：

	<?xml version="1.0" encoding="utf-8"?>
	<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
	    android:layout_width="fill_parent"
	    android:layout_height="wrap_content"
	    android:padding="10dp" >
	 
	    <TextView
	        android:id="@+id/laptop"
	        android:layout_width="wrap_content"
	        android:layout_height="wrap_content"
	        android:layout_alignParentLeft="true"
	        android:layout_centerVertical="true"
	        android:paddingLeft="25dp" />
	 
	    <ImageView
	        android:id="@+id/delete"
	        android:layout_width="wrap_content"
	        android:layout_height="wrap_content"
	        android:layout_alignParentRight="true"
	        android:src="@drawable/ic_delete"
	        android:contentDescription="@string/app_name"/>
	</RelativeLayout>

###适配器类：###

	public class ExpandableListAdapter extends BaseExpandableListAdapter {
	 
	    private Activity context;
	    private Map<String, List<String>> laptopCollections;
	    private List<String> laptops;
	 
	    public ExpandableListAdapter(Activity context, List<String> laptops,
	            Map<String, List<String>> laptopCollections) {
	        this.context = context;
	        this.laptopCollections = laptopCollections;
	        this.laptops = laptops;
	    }
	 
	    public Object getChild(int groupPosition, int childPosition) {
	        return laptopCollections.get(laptops.get(groupPosition)).get(childPosition);
	    }
	 
	    public long getChildId(int groupPosition, int childPosition) {
	        return childPosition;
	    }
	 
	    public View getChildView(final int groupPosition, final int childPosition,
	            boolean isLastChild, View convertView, ViewGroup parent) {
	        final String laptop = (String) getChild(groupPosition, childPosition);
	        LayoutInflater inflater = context.getLayoutInflater();
	 
	        if (convertView == null) {
	            convertView = inflater.inflate(R.layout.child_item, null);
	        }
	 
	        TextView item = (TextView) convertView.findViewById(R.id.laptop);
	 
	        ImageView delete = (ImageView) convertView.findViewById(R.id.delete);
	        delete.setOnClickListener(new OnClickListener() {
	 
	            public void onClick(View v) {
	                AlertDialog.Builder builder = new AlertDialog.Builder(context);
	                builder.setMessage("Do you want to remove?");
	                builder.setCancelable(false);
	                builder.setPositiveButton("Yes",
	                        new DialogInterface.OnClickListener() {
	                            public void onClick(DialogInterface dialog, int id) {
	                                List<String> child =
	                                    laptopCollections.get(laptops.get(groupPosition));
	                                child.remove(childPosition);
	                                notifyDataSetChanged();
	                            }
	                        });
	                builder.setNegativeButton("No",
	                        new DialogInterface.OnClickListener() {
	                            public void onClick(DialogInterface dialog, int id) {
	                                dialog.cancel();
	                            }
	                        });
	                AlertDialog alertDialog = builder.create();
	                alertDialog.show();
	            }
	        });
	 
	        item.setText(laptop);
	        return convertView;
	    }
	 
	    public int getChildrenCount(int groupPosition) {
	        return laptopCollections.get(laptops.get(groupPosition)).size();
	    }
	 
	    public Object getGroup(int groupPosition) {
	        return laptops.get(groupPosition);
	    }
	 
	    public int getGroupCount() {
	        return laptops.size();
	    }
	 
	    public long getGroupId(int groupPosition) {
	        return groupPosition;
	    }
	 
	    public View getGroupView(int groupPosition, boolean isExpanded,
	            View convertView, ViewGroup parent) {
	        String laptopName = (String) getGroup(groupPosition);
	        if (convertView == null) {
	            LayoutInflater infalInflater = (LayoutInflater) context
	                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
	            convertView = infalInflater.inflate(R.layout.group_item,
	                    null);
	        }
	        TextView item = (TextView) convertView.findViewById(R.id.laptop);
	        item.setTypeface(null, Typeface.BOLD);
	        item.setText(laptopName);
	        return convertView;
	    }
	 
	    public boolean hasStableIds() {
	        return true;
	    }
	 
	    public boolean isChildSelectable(int groupPosition, int childPosition) {
	        return true;
	    }
	}

###主界面类：###

	public class MainActivity extends Activity {
	 
	    List<String> groupList;
	    List<String> childList;
	    Map<String, List<String>> laptopCollection;
	    ExpandableListView expListView;
	 
	    @Override
	    protected void onCreate(Bundle savedInstanceState) {
	        super.onCreate(savedInstanceState);
	        setContentView(R.layout.activity_main);
	 
	        createGroupList();
	 
	        createCollection();
	 
	        expListView = (ExpandableListView) findViewById(R.id.laptop_list);
	        final ExpandableListAdapter expListAdapter = new ExpandableListAdapter(
	                this, groupList, laptopCollection);
	        expListView.setAdapter(expListAdapter);
	 
	        //setGroupIndicatorToRight();
	 
	        expListView.setOnChildClickListener(new OnChildClickListener() {
	 
	            public boolean onChildClick(ExpandableListView parent, View v,
	                    int groupPosition, int childPosition, long id) {
	                final String selected = (String) expListAdapter.getChild(
	                        groupPosition, childPosition);
	                Toast.makeText(getBaseContext(), selected, Toast.LENGTH_LONG)
	                        .show();
	 
	                return true;
	            }
	        });
	    }
	 
	    private void createGroupList() {
	        groupList = new ArrayList<String>();
	        groupList.add("one");
	        groupList.add("two");
	        groupList.add("three");
	        groupList.add("four");
	        groupList.add("five");
	        groupList.add("six");
	    }
	 
	    private void createCollection() {
	        // preparing laptops collection(child)
	        String[] hpModels = { "1", "1","1" };
	        String[] hclModels = { "2", "2", "2" };
	        String[] lenovoModels = { "3", "3","3", "3" };
	        String[] sonyModels = { "4", "4","4", "4" };
	        String[] dellModels = { "5", "5", "5" };
	        String[] samsungModels = { "6", "6", "6" };
	
	        laptopCollection = new LinkedHashMap<String, List<String>>();
	 
	        for (String laptop : groupList) {
	            if (laptop.equals("HP")) {
	                loadChild(hpModels);
	            } else if (laptop.equals("Dell"))
	                loadChild(dellModels);
	            else if (laptop.equals("Sony"))
	                loadChild(sonyModels);
	            else if (laptop.equals("HCL"))
	                loadChild(hclModels);
	            else if (laptop.equals("Samsung"))
	                loadChild(samsungModels);
	            else
	                loadChild(lenovoModels);
	 
	            laptopCollection.put(laptop, childList);
	        }
	    }
	 
	    private void loadChild(String[] laptopModels) {
	        childList = new ArrayList<String>();
	        for (String model : laptopModels)
	            childList.add(model);
	    }
	 
	    private void setGroupIndicatorToRight() {
	        /* Get the screen width */
	        DisplayMetrics dm = new DisplayMetrics();
	        getWindowManager().getDefaultDisplay().getMetrics(dm);
	        int width = dm.widthPixels;
	 
	        expListView.setIndicatorBounds(width - getDipsFromPixel(35), width
	                - getDipsFromPixel(5));
	    }
	 
	    // Convert pixel to dip
	    public int getDipsFromPixel(float pixels) {
	        // Get the screen's density scale
	        final float scale = getResources().getDisplayMetrics().density;
	        // Convert the dps to pixels, based on density scale
	        return (int) (pixels * scale + 0.5f);
	    }
	 
	    @Override
	    public boolean onCreateOptionsMenu(Menu menu) {
	        // Inflate the menu; this adds items to the action bar if it is present.
	        getMenuInflater().inflate(R.menu.activity_main, menu);
	        return true;
	    }
	}

参考：[ExpandableListView](http://developer.android.com/reference/android/widget/ExpandableListView.html)