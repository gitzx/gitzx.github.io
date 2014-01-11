---
date: 2014-1-11 11:22:30+00:00
layout: post
title: Android中的消息推送（Androidpn）
thread: 28
categories: android
tags: android
---

最近在做Android的消息推送，在这小结下。

###推送服务###

推送服务的实现方式大致可分为 Poll 和 Push 模式。推送服务本质上是服务器主动将消息，数据发送到客户端，而不是客户端主动去服务器请求数据。这种推送只需要客户端与服务器连接后，在有数据的情况下，服务器端马上将数据发送到客户端。

（1）Poll 模式，本质上是"伪推送"模式，或者叫短轮询模式。是客户端通过设定固定的时间间隔，然后在时间间隔到达后，客户端主动向服务器发送请求，去更新是否有新数据。

（2）Push 模式，一般意义上使用长连接去建立一个客户端到服务器的双向数据通道，只要在连接建立后，一旦一方有数据更新，就可以马上通过双向的数据通道向对方发送数据，平时在没有数据时，通过一些心跳等机制维持通道连接。

####移动推送服务####

- SMS（push）方式。通过拦截SMS消息并解析消息内容来了解服务器的命令，这个依赖运营商，成本较高。

- HTTP轮询（pull）方式。客户端定时向服务器发送询问消息，服务器有变化时则同步消失。轮询对带宽和电量消耗较大。

- 持久连接（push）方式。客户端和服务器建立长久连接。

在实际应用中，常使用第三种方式。

###Android推送的几种方案###

####Android C2DM####

[Android Cloud to Device Messaging (C2DM)](https://developers.google.com/android/c2dm/?csw=1)是google提供的服务，服务器依赖于google提供的C2DM服务器，在国内服务经常不可用。

####使用MQTT协议###

MQTT是IBM提供的一项异步消息传输协议，基于WebSocket。可查看[基于 WebSocket 的 MQTT 移动推送方案](http://www.ibm.com/developerworks/cn/websphere/library/techarticles/1308_xiangr_mqtt/1308_xiangr_mqtt.html).

其中，[wmqtt.jar](https://github.com/tokudu/AndroidPushNotificationsDemo) 是IBM提供的MQTT协议的Android客户端的实现。并且可以找到一个采用PHP书写的服务器端实现[PhpMQTTClient](https://github.com/tokudu/PhpMQTTClient)

####使用RSMB####

[Really Small Message Broker (RSMB)](http://www.alphaworks.ibm.com/tech/rsmb)是一个简单的MQTT代理，同样由IBM提供。缺省打开1883端口，应用程序当中，它负责接收来自服务器的消息并将其转发给指定的移动设备。[SAM](http://pecl.php.net/package/sam/download/0.2.0)是一个针对MQTT写的PHP库。

####Androidpn###

[androidpn](http://sourceforge.net/projects/androidpn/)是一个基于XMPP协议的java开源Android push notification实现。它包含了完整的客户端和服务器端。

Google官方的C2DM服务器底层也是采用XMPP协议进行的封装。XMPP(可扩展通讯和表示协议)是基于可扩展标记语言（XML）的协议，它用于即时消息（IM）以及在线探测。

####Androidpn的简单使用####

(1)下载Androidpn的Android客户端和服务端文件。

(2)在Androidpn的server的bin目录下运行run.bat，直接搭好服务，在浏览器上输入 http://127.0.0.1:7070  就进入管理界面

(3)在eclipse导入Androidpn-demoapp，修改androidpn.properties文件中的xmppHost为xmppHost=10.0.2.2，其中10.0.2.2在模拟器上在开发机上类似127.0.0.1.

遇到的错误： `java.lang.NoClassDefFoundError:`,

解决方法： 代码依赖于其他库，在project上右键属性，在java build path里的order and export里把要编译的包文件前打勾。
然后再clean该工程。

先总结到这，后面再研究下Androidpn的实现细节。

###第三方的推送服务###

第三方的推送服务如[极光推送](https://www.jpush.cn/)，除了提供Android的推送服务，还要ios版的推送服务。

