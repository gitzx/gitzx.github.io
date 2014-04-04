---
date: 2014-4-4 23:13:30+00:00
layout: post
title: 在mac或ios上模拟恶劣网络环境
thread: 42
categories: ios
tags: ios
---

移动应用大多需要联网，在Android上有人已经做出APP来限制网速。在mac或ios上，有两种方法可以模拟恶劣的网络环境：

- 利用xcode提供的Network Link Connector这个程序来限制上下行传输速率、模拟丢包率和延迟等。

- 利用TC命令工具来实现模拟

###Network Link Connector###

（1）下载Network Link Connector： Xcode －> Open Developer Tool －> More Developer Tools －>get "Hardware IO Tools for Xcode" -> install "Network Link Connector"

(2)打开网速限制之后，会显示一个Menubar Adddon. 这个程序默认包含了多种预置的网络设置，包括3G，WiFi，Edge(电话线)，DSL(GSM)等。

（3）自己创建网络Profile，对网速限制进行自定义。可定义的包括：

- 下行速率、丢包率和延迟；
- 上行速率、丢包率和延迟；
- DNS延迟。

###TC命令工具###

Tc用于Linux内核的流量控制。流量控制包括以下几种方式：

(1)SHAPING(限制带宽)：

当流量被限制，它的传输速率就被控制在某个值以下。限制值可以大大小于有效带宽。shaping（限制）只适用于向外的流量。
	
(2)DROPPING(丢弃):

如果流量超过某个设定的带宽，就丢弃数据包，不管是向内还是向外。 
	
(3)SCHEDULING(调度):

通过调度数据包的传输，可以在带宽范围内，按照优先级分配带宽。SCHEDULING(调度)也只适于向外的流量。
	
(4)POLICING(策略):

SHAPING用于处理向外的流量，而POLICIING(策略)用于处理接收到的数据。 
	
流量的处理由三种对象控制，它们是：qdisc(排队规则)、class(类别)和filter(过滤器)。

####使用tc限制单个IP进行下行速度控制####

	tc qdisc add dev eth0 root handle 1: htb r2q 1
	tc class add dev eth0 parent 1: classid 1:1 htb rate 30kbit ceil 60kbit
	tc  filter add dev eth0 parent 1: protocol ip prio 16 u32 match ip dst 192.168.1.2  flowid 1:1
	
注：限制192.168.1.2的下载速度为30kbit最高可以60kbit ,其中r2q是指没有default的root,使整个网络的带宽没有限制

####使用tc限制上行速度####

	tc qdisc del dev eth0 root
	tc qdisc add dev eth0 root handle 1: htb
	tc class add dev  eth0 parent 1: classid 1:1 htb rate  10kbit ceil 100kbit
	tc class add dev  eth0 parent 1:1 classid 1:10 htb rate 10kbit ceil 10kbit
	tc qdisc add dev  eth0 parent 1:10 sfq perturb 10
	tc filter add dev eth0 protocol ip parent 1: prio 2   u32 match ip dst 220.181.xxx.xx/32 flowid 1:1
	# 上面这台,让 220.181.xxx.xx/32 这台跑默认的,主要是为了让这个 ip 连接进来不被控制
	tc filter add dev eth0 protocol ip parent 1: prio 50 u32 match ip dst 0.0.0.0/0  flowid 1:10
	# 默认让所有的流量都从这个通过
	
注：只能向外发10kbit的数据

参考：[USING NETWORK LINK CONDITIONER IN IOS 6](http://www.neglectedpotential.com/2012/09/ios6-network-link-conditioner/)；[Linux内核流量控制TC详解](http://kevinleo.blog.51cto.com/341461/102680)
