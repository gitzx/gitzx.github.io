---
date: 2014-8-11 18:21:30+00:00
layout: post
title: 移动测试系统功能介绍
thread: 79
categories: android ios
tags: android ios
---

由于Android的开放策略，Android设备型号众多，设备技术标准不统一，Android系统的碎片化非常严重（相关数据可查看http://index.umeng.com/）。 如何较方便的测试Android应用在众多Android设备上的兼容性和性能是一个重要的问题。目前市面上提供Android应用自动化兼容性性能测试服务的主要有：

（1）Testin（http://www.testin.cn/）；

（2）腾讯安卓云测试平台（http://bita.qq.com/）；

（3）百度云测试（http://mtc.baidu.com/）；

（4）TestBird（http://www.testbird.com/）；

（5）易测云（http://www.yiceyun.com/）等等。

在这简单介绍下我参与开发的移动测试系统的基本功能。


###移动测试系统已有功能###

目前，移动测试系统的功能暂时只支持Android版应用（包括Android原生应用和手游），主要功能有：

（1）真机管理。包括曾接入到测试平台机器的信息，连接状态和使用情况，以及运行时机器的远程调度管理；

（2）简单适配测试。包括在多机上安装、启动、卸载、重装APK，同时获取对应的所用时间；

（3）遍历测试。原生Android应用基于Robotium框架，根据控件对应用做深度遍历；Android手游遍历需提供能跑场景的APK或是能让手游遍历的bash脚本；

（4）性能数据。在被测应用运行过程中自动收集应用的CPU占用、内存占用、流量和电量消耗等参数，以及logcat日志和截图的收集；

（5）Web服务。通过web上传APK，选择相应的测试如安装卸载测试、遍历测试或性能测试等，选择接入到测试平台的Android设备，即可开启测试，并展示测试结果。


###移动测试系统已有功能的实现简介###

下图是移动测试系统的结构图，系统可分为三个部分：（1）移动测试系统服务器；（2）接入到移动测试系统的PC测试机；（3）通过usb hub连接在PC测试机上的Android设备。

![](/assets/blog_pic/mtc_struct.png =602x401)

系统执行测试的主要步骤有：

（1）用户上传APK，系统解析APK获取应用信息；

（2）jenkins主节点创建job分配到从节点执行；

（3）同步apk包、执行测试的jar包、bash脚本等资源到从节点；

（4）在从节点上对APK重签名，并分发到连接在从节点上的Android设备；

（5）在各Android设备上安装启动APK；

（6）执行相应的测试，并获取相应的性能数据、截图、logcat日志等信息；

（7）各从节点回传数据到主节点，解析存储数据，生成测试报告并web展示。

####移动测试系统和测试机间的数据同步####

Jenkins有master和slave的结构，一个master可以关联多个slave用来为不同的job或相同的job的不同配置来服务。

![](/assets/blog_pic/mtc_jenkins.PNG =600x371)

当job被分配到slave上运行的时候，此时master和slave其实是建立的双向字节流的连接，主要的连接方式有：

（1）master通过ssh来启动slave。Jenkins内置有ssh客户端实现，可以用来与远程的sshd通信，从而启动slave agent；

（2）对于Windows的Slave，Jenkins可以使用Windows2000及以后内置的远程管理功能（WMI+DCOM）;

（3）通过Java web start来启动slave。jave web start使用jnlp（java network launching protocol），用户在从节点上配置jnlp文件，通过“javaws ***.jnlp”即可连接到主节点上。

移动测试系统以jenkins管理连接有Android设备的PC机，jenkins主节点与web服务器在同一台服务器上，连接有Android设备的pc机作为jenkins从节点。主节点提供web接口让用户来管理job和从节点，job分发到各个从节点进行执行，主从节点间采用Java web start来实现主从节点的连接。

下图显示的是接入到测试系统的五台PC机，能访问测试系统的用户都可创建节点，执行“javaws slave_angent.jnlp”命令接入到测试系统中，在自己的PC机上连接Android设备执行相应测试。这样，我们可以方便的将杭州MTL和广州MTL的设备接入进来，实现设备远程访问和共享等。

![](/assets/blog_pic/mtc_jenkins_node.PNG =756x251)

####真机管理和APK包处理####

由于Android设备众多，MTL通过多台PC机和usb hub管理Android设备，移动测试系统将多台PC机作为jenkins的从节点。因此，对众多真机的操作是通过jenkins插件和Android命令来实现的。

1.用于真机管理的jenkins插件的实现

由于用户通过web来管理各个jenkinns从机，进而操作连接在从机上的Android设备，测试系统通过jenkins插件的形式来管理jenkins从机及其Android设备。具体jenkins插件的制作在这就不展开了，真机管理的jenkins插件主要功能有：

（1）jenkins插件执行web发送过来的adb命令，如获取Android设备的信息、push、install等；

（2）Jenkins插件监听jenkins从机上Android设备的状态，及时更新设备状态等；

（3）Jenkins插件将jenkins从机机器设备的信息和状态保存到后台数据库中。

下图显示的是真机连接信息：

![](/assets/blog_pic/mtc_devices2.PNG =585x232)
![](/assets/blog_pic/mtc_devices.png =410x261)

2.APK包的处理

用户上传APK后，测试系统会对APK包进行处理，主要有：

（1）获取APK包的信息，如包名、图标、Activity、启动后pid和uid等；

（2）对APK包进行从签名；

（3）利用封装有获取性能数据、截图、断线重连等功能的jar包，测试APK。

####Android应用UI自动化测试####

1.Android原生应用的UI自动化测试

对于Android原生应用，测试系统在Robotium这款Android自动化测试框架的基础上，根据待测Android应用的控件对Android各个界面做遍历测试，主要分为两种：

（1）全面遍历。对各个界面按界面上控件的位置，从左到右，从上到下做类似深度遍历进行控件操作，实现各个界面的覆盖测试。

（2）部分遍历。使用Robotium框架进行测试时，需要提供一个含有UI测试用例的APK，从而对待测的Android应用进行测试。在全面遍历测试中，该功能已被测试系统提供，若需要执行有针对性的遍历，需要用户上传包含有测试用例的APk和配置文件。

Robotium是Android上常用的UI自动化测试框架，它提供了模拟各种手势操作（点击、长按、滑动等）、查找和断言机制的API，能够对各种控件进行操作。下图显示的是在测试系统中，模拟操作Android原生应用控件的截图：

![](/assets/blog_pic/mtc_robotium.PNG =460x258)

Robotium 主要通过Solo对象的实例来创建测试用例，如果有对应应用的R.java文件，可以通过类似solo.getView(R.id.**)来获取控件。Robotium的使用比较简单，限于篇幅，在这就不展开了。

2.Android手游的UI自动化测试

对于Android手游，控件大多是贴图。因此，Android手游的自动化遍历，除了调用Android手游代码中的相关入口函数实现场景遍历，也可以对控件进行识别操作等进行Android手游的自动化运行。测试系统将上传的手游APK分发到各个真机后会启动该手游，若需手游自动运行，用户需上传能自动跑场景的手游APK，或上传普通手游APK同时上传能支持跑场景的bash脚本，系统在启动游戏同时执行上传的bash脚本，如下图所示：

![](/assets/blog_pic/mtc_script.PNG =418x228)

据游戏控件进行识别操作等机型自动化运行，PC端上可使用免费skikuli来实现相应的功能，在移动端，我们可以利用相似度或特征点进行按钮等控件识别操作。

####Android应用相关数据的获取####

测试系统服务器作为jenkins主节点，将获取性能参数的jar包和待测APK包分发到各个jenkins从节点，再分发到与jenkins从节点连接的各个Android设备。对于Android原生应用，每次点击操作和在某个界面会收集性能参数、logcat日志和截图；对于Android手游，Android手游启动后，后台会定时（每隔5秒）收集性能参数、logcat日志和截图。目前，可以收集的性能参数包括：

（1）应用的CPU占用和设备总共的CPU占用率；

（2）应用的实际内存占用大小和设备总共的实际内存占用大小；

（3）应用的上下行流量消耗；

（4）应用的电量消耗；

（5）设备电压电流等。

下图显示的是自己编写的测试APP应用在三台真机上的整体信息。整体信息包括了测试的真机设备；安装、启动、卸载耗时；平均、最大内存占用；平均、最大CPU占用率；以及流量消耗等，并以图表的形式做了展示。

![](/assets/blog_pic/mtc_robotium_data.PNG =570x211)

下图显示的是Android应用(格斗类手游)在单个真机上的数据及曲线图，包括设备/应用CPU占用率曲线；设备/应用内存占用曲线；流量消耗；电量消耗等曲线信息：

![](/assets/blog_pic/mtc_game_data.PNG =566x292)

应用的CPU占用率、内存占用和流量消耗，可参考我之前的文章 [利用Android APP监测Android应用程序的资源占用消耗](http://www.gitzx.com/android-performancetest/)

4.应用截图的获取和问题截图定位

对于原生Android应用，使用Robotium的solo实例的takescreenshot()方法即可完成截图，在每次控件操作或界面跳转后调用该方法实现截图；对应Android手游，使用的是Android官方提供的Monkeyrunner程序，获取连接的Android设备后，调用devices的takeSnapShot()方法。

对于原生Android应用，根据控件操作来截图，对于Android手游，是定时截图。截图的目的是为了方便找到兼容性问题如贴图丢失、分辨率适配不正常、按钮重叠等等。

当测试的场景比较多时，每个真机获取到的截图会达到几百张，当测试真机较多时，查找问题截图的工作量会比较大。

因此，对于多台真机的所有截图，我们需要对问题截图进行筛选标识，方便定位问题截图。我们从最简单的有贴图丢失问题的截图识别做起，计算真机截图和资源场景图的结构相似度来判定标识有问题的截图。

###移动测试系统的web实现###

移动测试系统的服务器除了部署有jenkins服务作为主节点外，还部署有web服务。测试系统的web服务使用的工具有：

（1）Ruby2.0.0和ruby on rails 4.0；

（2）Mysql 5.5数据库；

（3）Passenger+Nginx作为ruby on rails的部署服务器，memcached作为缓存服务器。

测试系统前端使用的工具包和库主要有：

（1）CSS/HTML框架Bootstrap，BootStrap的矢量字体图标库Font-Awesome；

（2）Javascript框架Jquery及其插件。主要Jquery插件有:

	用于BootStrap后台管理模版sb-admin；
	用于HTML表格的DataTables；
	用于提示自动完成的TokenInput；
	用于菜单布局的metsmenu；
	用于将标准HTML Table转换为可排序表格的TableSorter等；

（3）Jquery UI框架和常见的图表库Highcharts等。

测试系统数据库包括的表如下图所示：

![](/assets/blog_pic/mtc_tables.png =224x367)

数据库主要存储了测试的APK、jenkins节点、接入过的真机及真机设备信息状态、测试后的性能数据、项目、执行测试的算法、用户等信息。


###后续计划###

由于移动设备的性能和环境，手游受到机器的影响较大，手游兼容性测试和性能测试是两项重要的测试内容。同时，手游的测试方法和工具较少。

相比Android设备，IOS设备类型较少，需求不是那么的急迫。目前测试系统完成的功能有分发IPA到多台IOS设备、安装、启动、卸载等基本功能。如何在多机上同时获取IOS设备的客户端性能数据还在实现中。

除此之外，类似PC端，移动设备的压力测试功能在单个设备上已实现，后续会移植到系统中如：（1）模拟设备CPU、内存、存储空间占用，可动态调节设备剩余的CPU、内存和存储空间占用；（2）模拟移动设备的网络环境，可动态调节网络带宽和上下行速率等等。

同时，对于在设备上获取的截图与参考图像的相似度比较，进而判断是否存在贴图丢失、黑边等常见的兼容性问题也在实现中，该功能后续也会移植到系统中。
