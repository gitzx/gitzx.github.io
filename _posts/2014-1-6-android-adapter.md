---
date: 2014-1-6 21:44:30+00:00
layout: post
title: Android Adapter的使用
thread: 24
categories: android
tags: android
---

Adapter在设计模式中指的是适配器模式，主要用于将一个接口转换为另个一个接口，使得原来与接口不兼容的类可以一起工作。

在Android中，Adapter就是AdapterView视图与数据之间的桥梁，Adapter提供对数据项的访问，同时也负责为每一项数据产生一个View。

Android提供了一些Adapter的子类，其中最常见的是ArrayAdapter、SimpleAdapter、SimpleCursorAdapter和BaseAdapter。在这小结下。

###ArrayAdapter###

列表的显示需要三个元素：

a．ListVeiw  用来展示列表的View。

b．适配器  用来把数据映射到ListView上的中介。

c．数据    具体的将被映射的字符串，图片，或者基本组件。
 
实现如下：

	public class ArrayAdapterActivity extends ListActivity {
	     @Override
	     public void onCreate(Bundle savedInstanceState) {
	         super.onCreate(savedInstanceState);
	         //列表项的数据
	         String[] strs = {"1","2","3","4","5"};
	         ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,android.R.layout.list_item_1,strs);
	         setListAdapter(adapter);
	     }
	 }  

或

	 public class MyListView extends Activity {    
	        private ListView listView;
	        //private List<String> data = new ArrayList<String>();
	        @Override
	        public void onCreate(Bundle savedInstanceState){
	            super.onCreate(savedInstanceState);
	             
	            listView = new ListView(this);
	            listView.setAdapter(new ArrayAdapter<String>(this, android.R.layout.simple_expandable_list_item_1,getData()));
	            setContentView(listView);
	        }     
	        private List<String> getData(){
	             
	            List<String> data = new ArrayList<String>();
	            data.add("测试数据1");
	            data.add("测试数据2");
	            data.add("测试数据3");
	            data.add("测试数据4");
	            return data;
	        }
	    }

###SimpleAdapter###

simpleAdapter的扩展性最好，可以定义各种各样的布局出来，可以放上ImageView（图片），还可以放上Button（按钮），CheckBox（复选框）等等。使用simpleAdapter的数据用一般都是HashMap构成的List，list的每一节对应ListView的每一行。

实现如下：

	public class SimpleAdapterActivity extends ListActivity {
	     @Override
	     public void onCreate(Bundle savedInstanceState) {
	         super.onCreate(savedInstanceState);
	         
	         SimpleAdapter adapter = new SimpleAdapter(this, getData(), R.layout.simple, new String[] { "title",  "img" }, new int[] { R.id.title, R.id.img });
	         setListAdapter(adapter);
	     }
	     private List<Map<String, Object>> getData() {
	         //map.put(参数名字,参数值)
	         List<Map<String, Object>> list = new ArrayList<Map<String, Object>>();
	         Map<String, Object> map = new HashMap<String, Object>();
	         map.put("title", "摩托罗拉");
	         map.put("img", R.drawable.icon);
	         list.add(map);
	         
	         map = new HashMap<String, Object>();
	         map.put("title", "诺基亚");
	         map.put("img", R.drawable.icon);
	         list.add(map);
	         
	         map = new HashMap<String, Object>();
	         map.put("title", "三星");
	         map.put("img", R.drawable.icon);
	         list.add(map);
	         return list;
	         }  
	     
	 }

xml如下：
	
	<?xml version="1.0" encoding="utf-8"?>
	<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
	android:orientation="vertical"
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	>
	<ImageView
	android:id="@+id/img"
	android:layout_width="wrap_content"
	android:layout_height="wrap_content"
	android:layout_margin="5dp"
	/>
	<TextView
	android:id="@+id/title"
	android:layout_width="wrap_content" 
	android:layout_height="wrap_content" 
	android:textColor="#ffffff"
	android:textSize="20sp"
	/>
	</LinearLayout>

###SimpleCursorAdapter###

数据使用Cursor时如数据库作为数据源的时候,才能使用SimpleCursorAdapter。实现如下：

	public class SimpleCursorAdapterActivity extends ListActivity {
	     @Override
	     public void onCreate(Bundle savedInstanceState) {
	         super.onCreate(savedInstanceState);
	         //获得一个指向系统通讯录数据库的Cursor对象获得数据来源
	         Cursor cur = getContentResolver().query(People.CONTENT_URI, null, null, null, null);
	         startManagingCursor(cur);
	         //实例化列表适配器
	         
	         ListAdapter adapter = new SimpleCursorAdapter(this, android.R.layout.simple_list_item_1, cur, new String[] {People.NAME}, new int[] {android.R.id.text1});
	         setListAdapter(adapter);
	     }
	 }

在manifest中加入权限：

	<uses-permission android:name="android.permission.READ_CONTACTS"></uses-permission>

###BaseAdapter###

列表不光会用来做显示用，我们同样可以在在上面添加按钮。添加按钮首先要写一个有按钮的xml文件，然后自然会想到用上面的方法定义一个适配器，然后将数据映射到布局文件上。但是事实并非这样，因为按钮是无法映射的，即使你成功的用布局文件显示出了按钮也无法添加按钮的响应，这时就要研究一下ListView是如何现实的了，而且必须要重写一个类继承BaseAdapter。下面的示例将显示一个按钮和一个图片，两行字如果单击按钮将删除此按钮的所在行。并告诉你ListView究竟是如何工作的。

	public class MyListView4 extends ListActivity {
	       private List<Map<String, Object>> mData; 
	       @Override
	       public void onCreate(Bundle savedInstanceState) {
	           super.onCreate(savedInstanceState);
	           mData = getData();
	           MyAdapter adapter = new MyAdapter(this);
	           setListAdapter(adapter);
	       }
	    
	       private List<Map<String, Object>> getData() {
	           List<Map<String, Object>> list = new ArrayList<Map<String, Object>>();
	           Map<String, Object> map = new HashMap<String, Object>();
	           map.put("title", "G1");
	           map.put("info", "google 1");
	           map.put("img", R.drawable.i1);
	           list.add(map);
	    
	           map = new HashMap<String, Object>();
	           map.put("title", "G2");
	           map.put("info", "google 2");
	           map.put("img", R.drawable.i2);
	           list.add(map);
	    
	           map = new HashMap<String, Object>();
	           map.put("title", "G3");
	           map.put("info", "google 3");
	           map.put("img", R.drawable.i3);
	           list.add(map);
	            
	           return list;
	       }
	        
	       // ListView 中某项被选中后的逻辑
	       @Override
	       protected void onListItemClick(ListView l, View v, int position, long id) {
	            
	           Log.v("MyListView4-click", (String)mData.get(position).get("title"));
	       }
	        
	        // listview中点击按键弹出对话框
	       public void showInfo(){
	           new AlertDialog.Builder(this)
	           .setTitle("我的listview")
	           .setMessage("介绍...")
	           .setPositiveButton("确定", new DialogInterface.OnClickListener() {
	               @Override
	               public void onClick(DialogInterface dialog, int which) {
	               }
	           })
	           .show();
	            
	       }
	 
	       public final class ViewHolder{
	           public ImageView img;
	           public TextView title;
	           public TextView info;
	           public Button viewBtn;
	       }
	         
	       public class MyAdapter extends BaseAdapter{
	           private LayoutInflater mInflater;    
	           public MyAdapter(Context context){
	               this.mInflater = LayoutInflater.from(context);
	           }
	           @Override
	           public int getCount() {
	               // TODO Auto-generated method stub
	               return mData.size();
	           }
	    
	           @Override
	           public Object getItem(int arg0) {
	               // TODO Auto-generated method stub
	               return null;
	           }
	    
	           @Override
	           public long getItemId(int arg0) {
	               // TODO Auto-generated method stub
	               return 0;
	           }
	    
	           @Override
	           public View getView(int position, View convertView, ViewGroup parent) {
	                
	               ViewHolder holder = null;
	               if (convertView == null) {
	                    
	                   holder=new ViewHolder(); 
	                    
	                   convertView = mInflater.inflate(R.layout.vlist2, null);
	                   holder.img = (ImageView)convertView.findViewById(R.id.img);
	                   holder.title = (TextView)convertView.findViewById(R.id.title);
	                   holder.info = (TextView)convertView.findViewById(R.id.info);
	                   holder.viewBtn = (Button)convertView.findViewById(R.id.view_btn);
	                   convertView.setTag(holder);
	                    
	               }else {
	                    
	                   holder = (ViewHolder)convertView.getTag();
	               }
	                
	                
	               holder.img.setBackgroundResource((Integer)mData.get(position).get("img"));
	               holder.title.setText((String)mData.get(position).get("title"));
	               holder.info.setText((String)mData.get(position).get("info"));
	                
	               holder.viewBtn.setOnClickListener(new View.OnClickListener() {
	                    
	                   @Override
	                   public void onClick(View v) {
	                       showInfo();                
	                   }
	               });
	                             
	               return convertView;
	           }    
	       }     
	   }

listView在开始绘制的时候，系统首先调用getCount（）函数，根据他的返回值得到listView的长度（这也是为什么在开始的第一张图特别的标出列表长度），然后根据这个长度，调用getView（）逐一绘制每一行。如果你的getCount（）返回值是0的话，列表将不显示同样return 1，就只显示一行。

参考：[Building Layouts with an Adapter](http://developer.android.com/guide/topics/ui/declaring-layout.html#AdapterViews)