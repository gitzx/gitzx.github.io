---
date: 2014-1-4 14:19:30+00:00
layout: post
title: ios安全机制
thread: 22
categories: ios
tags: ios
---

IOS的安全架构分为两层，低层次的硬件和固件安全抵御恶意软件和病毒，高层次的系统级安全保护个人信息和企业数据，防止未授权访问和渗透攻击。iOS安全架构图如下：

![](/assets/blog_pic/ios-Security.PNG)

上部分是软件系统，整个文件系统都被加密，文件系统分为系统分区和用户分区，应用程序运行在用户分区并被限制在一个“沙盒”中。下部分是硬件和固件，文件系统通过系统内核与硬件通信，系统内核直接调用固化加密引擎加解密文件数据，固化加密引擎密钥依赖烧制在设备上的设备key、组key和苹果根认证证书。

###系统结构###

####安全启动链（Secure Boot Chain）####

系统启动过程中每一步包含的所有组件都已经过苹果签名，并且只有在验证了信任链后才会被执行。这包括引导加载程序、内核、内核扩展、基带固件。

当iOS设备启动后，应用处理器立刻执行引导只读存储器（Boot ROM）中的代码。引导ROM中的不可变代码是在集成电路制作过程中放置进去的，引导ROM代码包含了苹果的根认证中心公共密钥（Root CA public key），该密钥用来验证引导加载程序[Low-Level Bootloader (LLB)]是否被苹果签名，验证通过才允许它加载。这是信任链中的第一步，每一步都需要确保下一步执行的代码是经过苹果签名的。当LLB完成工作时，会执行下一步引导加载程序（iBoot），会依次证实并运行iOS内核。

这个安全引导链确保最低层次的软件不会被篡改，允许iOS只运行在通过验证的苹果设备上。如果在引导过程中的某一步不能载入或不能验证下一步，启动就会终止并在设备上显示“Connection iTunes”。这叫做恢复模式。如果Boot ROM不能载入或不能验证LLB，会进入设备固件更新[DFU (Device Firmware Upgrade)]模式。两种情况下，设备必须通过USB连接到iTunes并恢复到出厂设置。

Ios有三种启动模式：

- 正常模式

　　Boot ROM ---> Low Level boot loader（LLB）---> iBoot（2 stageboot loader ---> OS（kernel/Application）

- 恢复模式

　　Boot ROM ---> Low Level boot loader（LLB）---> iBoot（2 stageboot loader ---> Kernel （Ramdisk，can be restored）

- DFU（Development Firmware Upgrade）模式

也可长按Home和Sleep/Wake按钮8秒进入该模式，该启动模式存在安全漏洞被利用进行越狱。
　　Boot ROM ---> iBSS ---> iBec ---> Kernel （Ramdisk，can be restored）	

####系统软件个性化（System Software personalization）####

iOS设备的系统升级之后是不允许降级的（官方没有提供接口）。iOS系统在升级过程需要联网进行验证，系统升级之前，设备会将LLB、iBoot、内核、镜像，外加一个随机的不可重复的值发送到苹果的服务器进行验证，服务器端对所有这些进行验证，如果通过验证，将会返回一个通过的结果，结果加入了与设备唯一相关的ECID。这样做的好处是此值是无法重用的，只能对应与一台设备，且只能使用一次。通过这种机制，保证了系统升级过程都是符合苹果要求的。提高了较高的安全性。

####应用签名（App Code Signing）####

iOS系统在升级过程需要联网进行验证，系统升级之前，设备会将LLB、iBoot、内核、镜像，外加一个随机的不可重复的值发送到苹果的服务器进行验证，服务器端对所有这些进行验证，如果通过验证，将会返回一个通过的结果，结果加入了与设备唯一相关的ECID。这样做的好处是此值是无法重用的，只能对应与一台设备，且只能使用一次。同过这种机制，保证了系统升级过程都是符合苹果要求的。提高了较高的安全性。

####运行时安全（Runtime　Process　Security)####

所有的第三方应用都在沙盒中运行。每个应用是隔离的，都有一个唯一的home路径用来存放自己的文件，这个路径是在安装时随机分配的。如果要访问另一个应用的数据，只能通过iOS提供的API或services。

系统文件和资源也是跟用户应用隔离开来。各个应用之间无法共享文件，如要互相通信，只能通过URLSchema或shared key chain。对应用需要的特别操作可以授权，授权是键值对的形式，签名后打包进应用程序。

采用ASLR技术。地址空间布局随机化[Address space layoutrandomization (ASLR)], )是一种针对缓冲区溢出的安全保护技术，通过对堆、栈、共享库映射等线性区布局的随机化，以及增加攻击者预测目的地址的难度，防止攻击者直接定位攻击代码位置，达到阻止溢出攻击的目的。

XN (execute never) 标志位在ARMv6中被引入，不可以在此区执行指令，从而在硬件上支持执行保护。

###数据加密和保护###

安全启动链、代码签名、运行时安全等确保受信任的代码和应用才能在设备上运行。iOS还提供额外的安全功能来保护用户的数据，即使是在其他的安全机制遭到破坏时（如设备被未经授权修改）。就像系统架构一样，加密和数据保护整合了硬件和软件技术提供保护能力。

####硬件安全特性（Hardware Security Features）####

加解密是耗时耗能源的操作。而iOS内所有用户数据都是强制加密的，加密功能不能关闭。所以，苹果的AES加解密引擎都是硬件级的，位于存储与系统之间的DMA内，所有进出存储的数据都啊要经过硬件的加密与解密，这样提供了较高的效率与性能。

加密解密使用的KEY主要来自unique ID(UID)以及Group ID(gid)，UID与唯一设备相关，GID与某种特定型号的CPU相关，一台设备的UID及GID全部被烧制到芯片内部，除了AES加密引擎，没有其他方法直接读取，能看到的只有使用UID及GID加密后的数据。这样，不同设备的加密结果是不同的，同一套密文只能在加密的机器上进行解密。

除了GID及UID，其他加密使用的KEY全部来自系统自带的随机数生成器，具体使用的算法为Yarrow。

####文件数据保护（File Data Protection）####

每当一个文件在数据分区创建时，数据保护就创建一个新的256位的key。该key被交给硬件AES引擎，AES引擎使用该key加密要写入闪存的文件。

文件的内容用File key加密，File key被class key加密存储在文件的元数据Metadata中。文件的元数据被file system key加密。file system key是一个随机数，在iOS第一次安装时创建或在设备被抹除时重建。该key存在Effaceable Storage中，删除该key会导致所有文件无法访问，这就是苹果实现快速抹除设备数据的根源。Class key受UID保护，有些class key还受开机密码保护。Key的等级层次提供灵活性和高性能。如，改变文件的保护类型，只需要对File key用对应的class key重新加密；改变了开机密码，只需重新加密class key。

prefile的访问需要进行解密的key，这些key包括：

- File System Key: 系统安装时生成的一个随即的key，远程删除数据时，其实不用真正的删除磁盘上的数据，只要删除此key，那么所有文件的prefile key 将不能访问，也就是所有文件将无法读取。

- Class Key，另一个key，与UID相关，如果用户设置了锁屏密码，那么此Class Key将的来源将同时包括锁屏密码。

只有有了这两个key，一个文件的prefilekey才能被读取出来，此加密的文件才能被揭秘，也就是说，当锁屏之后，或存储位于不同的设备之上，数据是无法读取的。

![](/assets/blog_pic/file-protect.PNG)

当一个文件打开时，它的元数据首先被解密（使用file system key）。元数据包括加密了的file key和文件的保护类型class，根据文件保护类型找到对应的加密的class key，利用开机密码和UID可解密class key，再利用class key解密file key，最后把file key提供给AES引擎，当从闪存读取文件时由它来解密文件类容。

####开机密码（Passcodes）####

锁屏密码为了防止暴力破解，增加了三个限制：

- 将其与uid绑定，也就是只能在该密码生成的设备上进行尝试；

- 两次尝试的时间间隔强制设成80ms，机器暴力破解的时间将大大加长；

- 增加选项，若连续输错次数超过10次，可选择删除设备内数据。

####数据保护类型（Classes）####

在iOS设备上，当一个文件创建时，它被应用（app）分配了一个类型（class）。不同的类型在数据被访问时会应用不同的策略。

####密钥链的数据保护（Keychain Data Protection）####

应用的小量极敏感数据如密码，最好存储与KeyChain内，而不是应用自己管理。Keychain是以No Protection保护类型存储在文件系统中的SQLite数据库实现的。它提供了与文件保护key层次对应的key等级。只有一个数据库，一个叫securityd的安全守护进程决定哪一个keychain的项可以被哪个进程或应用访问。Keychain访问API要求调用securityd框架，securityd框架会查询应用的“keychain-access-groups”和 “application-identifier”授权。access groups允许Keychain的项在不同的应用之间共享数据。

####密钥包（Keybags)####

文件和keychain的两种数据保护类型的key都通过密钥包存储和管理。iOS有四个密钥包：System、Backup、Escrow、iCLoud Backup。

###网络安全###

IOS提供了大量的标准网络安全协议。iOS不像其他平台，它不需要防火墙，因为iOS限制了监听端口的数量，移除了一些不需要的网络应用，如telnet、shells、web server。通过使用iMessge、FaceTime和苹果推送提醒服务来通信，有完整的加密和认证。

- SSL TLS

- VPN

- WIFI

- Bluetooth

###设备权限控制###

- Passcode Protection

- Configuration Enforcement

- Mobile Device Management

- Apple Configurator

- Device Restrictions

- Supervised Only Restrictions

- Remote Wipe


参考：[ios Security](http://www.apple.com/ipad/business/docs/iOS_Security_Oct12.pdf)