---
date: 2014-1-14 18:32:30+00:00
layout: post
title: Android平台调用webservice
thread: 30
categories: android
tags: android
---

之前在实验室做过在Android上调用webservice来上传图片，最近想利用webservice来实现多台PC和Android设备上执行一些命令，在这总结下。

###WebService介绍###

利用webservice，应用程序可以与平台和编程语言无关的方式相互通信。Web Service 最基本的组成部分为服务的提供者（Service Provider）和服务的请求者（Service Requester）。WebService通常包括：

- SOAP（Simple Object Access Protocol），一个基于XML的可扩展消息信封格式。

- WSDL（Web Service Definition Language），一个XML格式文档，用以描述服务端口访问方式和使用协议的细节。通常用来辅助生成服务器和客户端代码及配置信息。

- UDDI（Universal Description, Discovery, and Integration），一个用来发布和搜索WEB服务的协议，应用程序可借由此协议在设计或运行时找到目标WEB服务。

Web Service 两端的应用是通过基于标准的 XML 格式的协议进行通信的，最常用的是SOAP。

服务的提供者应该首先通过 WSDL和 UDDI发布它所提供的服务到一个统注册这些服务信息的存储库中去。这样，服务的请求者就也可以通过WSDL和 UDDI发现到服务提供者提供的服务，并可以通过应用的调用方法来使用这个服务了。

###利用axis2创建WebService###

[axis2](http://axis.apache.org/axis2/java/core/) 是新一代的web service开发工具.在这之前，需先安装tomcat，将下载的axis2的war文件放到tomcat的webapp目录下，启动tomcat，访问[http://localhost:8080/axis2/](http://localhost:8080/axis2/)查看axis2是否安装正常。

####发布WebService###

已下面的代码为例来发布WebService:

	public class TestWs {
		public String showName(String name) {return name; }
		public String getName() {return "Axis2Service"; }
	}

axis2发包WebService的方法有：

- Dynamic Invocation Interface ( DII)

- Stubs方式

- Dynamic Proxy方式

DII方式只适用axis1，在axis2之前，可以利用jws的方式来发布WebService，但这在axis2中已不适用了。

（1）利用POJO类来发布WebService

---

POJO（Plain Old Java Objects）简单的Java对象，实际就是普通JavaBeans，是为了避免和EJB混淆所创造的简称。

利用pojo发布WebService比较简单，只需将TestWs编译后的TestWs.class文件放到<tomcat>\webapps\axis2\WEB-INF\pojo目录下。在[http://localhost:8080/axis2/services/listServices](http://localhost:8080/axis2/services/listServices)即可看到发布的服务。

---

（2）利用.aar发布WebService

- 手动打包

新建\Axis2Service1\deploy文件夹 ，将\Axis2Service1\bin下的class文件复制过来。
新建\Axis2Service1\deploy\META-INF\services.xml文件如下：
	
	<service name="AxisService">
	<description>AxisService</description>
	<parameter name="ServiceClass">ws.TestWs</parameter>
	<operation name="showName">
	<messageReceiver
	class="org.apache.axis2.rpc.receivers.RPCMessageReceiver" />
	</operation>
	<operation name="getName">
	<messageReceiver
	class="org.apache.axis2.rpc.receivers.RPCInOnlyMessageReceiver" />
	</operation>
	</service>

生成aar包 \Axis2Service1\deploy>jar cvf AxisService.aar . (注意带.号)

- 利用axis2-eclipse插件打包

在[Apache Axis2 Tools](http://axis.apache.org/axis2/java/core/tools/index.html)下载Service Archive Wizard - Eclipse Plug-in和Code Generator Wizard - Eclipse Plug-in两个插件。将两个插件jar文件复制到%ECLIPSE_HOME%\dropins目录下，旧版的eclipse则放入到plugins目录下。步骤如下：

---

1）IDE中选择New->other->Axis2 Service Archiver,点击Next;

2)Class File Location:选择Axis2Service1\bin目录,点击Next;

3)勾选Skip WSDL,点击Next;

4)Service Archiver 选择jar位置，如果没有jar包就直接点击Next;

5)勾选Generate the service xml automatically 自动生成XML file文件,点击Next;

6)service name,输入:AxisService,然后在class name 中填写要发布的类(全路径),点击load。勾选 Search declared methods only。点击next;

7)output File location,输入:D:\ ; output File Name,输入artiver文件的名称 AxisService。点击finish。提示 Service Archvie generated successfully! 注册表明,生成成功.

8)AxisService.aar复制到%TOMCAT-HOME%/webapps/axis2/WEB-INF/services下。（不打aar包，\Axis2Service1\deploy下面复制过去也是可以）

打开[http://localhost:8080/axis2/services/listServices](http://localhost:8080/axis2/services/listServices)即可看到发布的服务。

---

(3)利用web工程发布WebService

利用web工程发布WebService的步骤如下：

---

1）新建java web project工程；

2)文件复制

%TOMCAT-HOME%\webapps\axis2\WEB-INF\lib 复制到 \Axis2Service2\WebRoot\WEB-INF\lib 下，并加入工程引用。

%TOMCAT-HOME%\webapps\axis2\WEB-INF\conf 复制到 \Axis2Service2\WebRoot\WEB-INF\conf
%TOMCAT-HOME%\webapps\axis2\WEB-INF\modules 复制到 \Axis2Service2\WebRoot\WEB-INF\modules

3)web.xml的代码如下：

	<?xml version="1.0" encoding="UTF-8"?>
	<web-app id="wmf" version="2.4" xmlns="http://java.sun.com/xml/ns/j2ee"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://java.sun.com/xml/ns/j2ee http://java.sun.com/xml/ns/j2ee/web-app_2_4.xsd">
	<servlet>
	<servlet-name>AxisServlet</servlet-name>
	<servlet-class>org.apache.axis2.transport.http.AxisServlet</servlet-class>
	<load-on-startup>1</load-on-startup>
	</servlet>
	<servlet-mapping>
	<servlet-name>AxisServlet</servlet-name>
	<url-pattern>/services/*</url-pattern>
	</servlet-mapping>
	</web-app>

4）新建 \Axis2Service2\src\ws\TestWs.java 如上。新建\Axis2Service2\WebRoot\WEB-INF\services目录。

5）新建一个AxisService服务
AxisService\META-INF\services.xml

	<service name="AxisService">
	<description>AxisService</description>
	<parameter name="ServiceClass">ws.TestWs</parameter>
	<operation name="showName">
	<messageReceiver
	class="org.apache.axis2.rpc.receivers.RPCMessageReceiver" />
	</operation>
	<operation name="getName">
	<messageReceiver
	class="org.apache.axis2.rpc.receivers.RPCInOnlyMessageReceiver" />
	</operation>
	</service>

打开[http://localhost:8080/axis2/services2/listServices](http://localhost:8080/axis2/services2/listServices)即可看到发布的服务。

---

####调用WebService的三种方法####

WEB服务实际上是一组工具，并有多种不同的方法调用之。三种最普遍的手段是：

- 面向服务架构（SOA）

- 远程过程调用（RPC）

- 表述性状态转移（REST）。

（1）编写stub client访问web服务

####生成客户端stub文件####

1）脚本生成方式

去AXIS2的解压目录下bin(%AXIS2_HOME%\bin\)下执行下面语句
wsdl2java -uri http://localhost:8085/Axis2Service2/services/AxisService?wsdl -p ws -s -o stub
-p参数指定了生成的Java类的包名
-o参数指定了生成的一系列文件保存的根目录
在stub\src\ws自动生成AxisServiceStub.java

2）利用Code Generator Wizard - Eclipse Plug-in插件生成

---

IDE中选择New->other->Axis2 Code Generator,点击Next;

勾选Generate Java source code from a WSDL file,点击Next;

WSDL file location,输入:http://localhost:8080/Axis2Service2/services/AxisService?wsdl,点击Next;

指定输入路径,点击Next，提示：All operations completed successfully! 生成成功。在D:\src\ws 自动生成了stub一系列文件,其中ws是包名。

---

####stub客户端调研WebService####

1）新建 java工程 Axis2Client
新建\Axis2Client\lib文件夹
将%AXIS2_HOME%\lib\ 下的jar包复制到\Axis2Client\lib，并加入工程引用中

2）将通过脚本生成的单一AxisServiceStub.java文件或通过stb生成的一系列文件加入到src\ws下；

3)新建TestWs.java如下：

	package ws;
	import ws.AxisServiceStub;
	import ws.ShowName;
	public class TestWs {
		public static void main(String[] args) throws Exception {
			//初始化Sub类
			AxisServiceStub stub = new AxisServiceStub();
			//传递AxisServiceStub.ShowName对象，相关参数在这边赋值。
			ShowName command = new ShowName();
			command.setName("Hello!");
			//取得返回值
			String name = stub.showName(command).get_return();
			System.out.println(name);
		}
	}

####Android客户端利用rpc调用WebService服务####

 在Android平台调用Web Service需要依赖于第三方类库[ksoap2](https://code.google.com/p/ksoap2-android/)，它是一个SOAP Web service客户端开发包.

简单使用步骤如下：

1）向Android工程中添加ksoap2的jar包。

2）调用[http://webservice.webxml.com.cn/WebServices/MobileCodeWS.asmx?wsdl](http://webservice.webxml.com.cn/WebServices/MobileCodeWS.asmx?wsdl)来查询手机归属地。

3）实现代码如下：

	package com.zx.exerciseapp;
	
	import android.app.Activity;
	import android.os.Bundle;
	import android.os.StrictMode;
	import android.view.View;
	import android.widget.EditText;
	import android.widget.TextView;
	import org.ksoap2.SoapEnvelope;  
	import org.ksoap2.serialization.SoapObject;  
	import org.ksoap2.serialization.SoapSerializationEnvelope;  
	import org.ksoap2.transport.HttpTransportSE;  
	
	public class WebServiceActivity extends Activity{
		private EditText phoneedittext;
		private TextView phonetextview;
		@Override
		public void onCreate(Bundle savedInstancestate){
			super.onCreate(savedInstancestate);
			setContentView(R.layout.webservice);
		    phoneedittext = (EditText)findViewById(R.id.phonenum);
		    phonetextview = (TextView)findViewById(R.id.tv);
		    StrictMode.setThreadPolicy(new StrictMode.ThreadPolicy.Builder().detectDiskReads() 
		    		.detectDiskWrites().detectNetwork().penaltyLog().build()); 
		    		StrictMode.setVmPolicy(new StrictMode.VmPolicy.Builder().detectLeakedSqlLiteObjects() 
		    		.detectLeakedClosableObjects().penaltyLog().penaltyDeath().build());
		}
		
		public void invokingws(View view){
			String phone = phoneedittext.getText().toString().trim();
			//String phone = "13545108785";
			if("".equals(phone)){
				phonetextview.setError("-1");
				phonetextview.requestFocus();
				phonetextview.setText("");
				return;			
			}
			getRemoteInfo(phone);
		}
		
		public void getRemoteInfo(String phone){
			//phonetextview.setText("hello world");
			
			// 命名空间  
	        String nameSpace = "http://WebXml.com.cn/";  
	        // 调用的方法名称  
	        String methodName = "getMobileCodeInfo";  
	        // EndPoint  
	        String endPoint = "http://webservice.webxml.com.cn/WebServices/MobileCodeWS.asmx";  
	        // SOAP Action  
	        String soapAction = "http://WebXml.com.cn/getMobileCodeInfo";  
	        // 指定WebService的命名空间和调用的方法名  
	        SoapObject rpc = new SoapObject(nameSpace, methodName);  
	  
	        // 设置需调用WebService接口需要传入的两个参数mobileCode、userId  
	        rpc.addProperty("mobileCode", phone);  
	        rpc.addProperty("userId", "");  
	  
	        // 生成调用WebService方法的SOAP请求信息,并指定SOAP的版本  
	        SoapSerializationEnvelope envelope = new SoapSerializationEnvelope(SoapEnvelope.VER12);  
	  
	        envelope.bodyOut = rpc;  
	        // 设置是否调用的是dotNet开发的WebService  
	        envelope.dotNet = true;  
	        // 等价于envelope.bodyOut = rpc;  
	        envelope.setOutputSoapObject(rpc);  
	  
	        HttpTransportSE transport = new HttpTransportSE(endPoint);  
	        try {  
	            // 调用WebService  
	            transport.call(soapAction, envelope);  
	        } catch (Exception e) {  
	            e.printStackTrace();  
	        }  
	  
	        // 获取返回的数据  
	        SoapObject object = (SoapObject) envelope.bodyIn;  
	        
	        if(object == null){
	        	System.out.println("object == null");
	        	phonetextview.setText("hello hello"); 
	        }
	        // 获取返回的结果  
	        String result = object.getProperty(0).toString();  
	  
	        // 将WebService返回的结果显示在TextView中  
	        phonetextview.setText(result);  
	        
		}
	
	}

其中用到了StrictMode来防止NRP的出现。

	 public void onCreate() {
	     if (DEVELOPER_MODE) {
	         StrictMode.setThreadPolicy(new StrictMode.ThreadPolicy.Builder()
	                 .detectDiskReads()
	                 .detectDiskWrites()
	                 .detectNetwork()   // or .detectAll() for all detectable problems
	                 .penaltyLog()
	                 .build());
	         StrictMode.setVmPolicy(new StrictMode.VmPolicy.Builder()
	                 .detectLeakedSqlLiteObjects()
	                 .detectLeakedClosableObjects()
	                 .penaltyLog()
	                 .penaltyDeath()
	                 .build());
	     }
	     super.onCreate();
	 }

参考：[ Android平台调用WebService详解](http://blog.csdn.net/lyq8479/article/details/6428288#quote)








