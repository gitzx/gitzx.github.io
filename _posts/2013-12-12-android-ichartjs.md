---
date: 2013-12-12 12:45:30+00:00
layout: post
title: 利用ichartjs库来实现Android上绘制报表
thread: 11
categories: android
tags:  android
---

最近在做在Android上绘制报表，有两个开源库：

- 一个是仅支持Android平台的[achartengine](https://code.google.com/p/achartengine/);

- 另一个是[ichartjs](http://www.ichartjs.com/)。ichartjs 是一款基于HTML5的图形库。使用纯javascript语言, 利用HTML5的canvas标签绘制各式图形。ichartjs可以跨平台。

在这总结下利用ichartjs库来实现Android上绘制报表。

###添加ichartjs库到Android项目中###

- 下载ichartjs库放到Android项目中的assets目录下。
- 在assets目录下新建html文件，绘制报表的工作都有html文件来实现。通过webView的api来实现javascript调用。这点和[phonegap](http://phonegap.com/)类似，也是html和js文件来实现功能，Android再调用。

###简单的demo实现动态获取数据并绘制报表###

DemoActivity.java

	public class A1Activity extends Activity {	
		WebView wv;
		@Override
		protected void onCreate(Bundle savedInstanceState) {
			super.onCreate(savedInstanceState);
			this.requestWindowFeature(Window.FEATURE_NO_TITLE);
			setContentView(R.layout.demo_ichartjs);
			wv = (WebView) findViewById(R.id.wv);
			wv.getSettings().setJavaScriptEnabled(true);  
			wv.getSettings().setUseWideViewPort(true);
			wv.getSettings().setSupportZoom(true);
			wv.getSettings().setBuiltInZoomControls(true);
			wv.getSettings().setLoadWithOverviewMode(true);
			wv.requestFocus();
			wv.loadUrl("file:///android_asset/mianji_chart.html");		
		}
		public void backBtn(View view){
			this.finish();
		}
		//获取数据
		private String getRemoteData(){
			 try {  
		            JSONObject object1 = new JSONObject();  
		            object1.put("name", "姓名");  
		            object1.put("color", "#1f7e92");  
		            Random random = new Random();
		            JSONArray jadata= new JSONArray();  
		            for(int i=0;i<12;i++){
		            	jadata.put(random.nextInt(40));
		            }
		            object1.put("value", jadata);    
		            JSONArray jsonArray = new JSONArray();  
		            jsonArray.put(object1);  
		            return jsonArray.toString();  
		        } catch (JSONException e) {  
		            e.printStackTrace();  
		        }  
		        return null;  
		}
		
		public void updateBtn(View view){
			//数据传递和更新
			wv.loadUrl("javascript:setContentInfo('"+getRemoteData()+"')");  
		}
	}

DemoHtml.html

	function setContentInfo(data)  {  
		//通过eval方法处理得到json对象数组 
	    var jsonObjects = eval(data);    
	    chart.push("data",jsonObjects);
	    chart.setUp();
	    chart.draw();
	   }  

在layout的demo_ichartjs.xml中定义webview：

    <WebView
		android:id="@+id/wv"
	    android:layout_width="fill_parent"
	    android:layout_height="fill_parent"
    />

参考[Android报表解决方案 使用开源组件iChartjs](http://weixueliang89.blog.163.com/blog/static/19792177420136149560775/)