---
date: 2014-1-1 12:18:30+00:00
layout: post
title: 利用Android APP监测Android应用程序的资源占用消耗
thread: 21
categories: android
tags: android
---

上个月做了个Android APP用来监测Android应用程序的资源占用消耗，在这小结下。

###Android APP的主要功能###

Android APP的主要功能如下：

- 在Android前台操作应用程序，后台实时测试当前应用程序的CPU占用、内存占用和流量消耗。

- 前台以悬浮框的形式显示后台得到的性能数据，性能数据以excel格式文件保存。

- 悬浮框中截图按钮能方便的截取当前应用程序界面的图片并保存到手机中。

- 可以设置记录数据的时间间隔和是否显示悬浮框等。

- 在APP中以曲线的方式显示应用程序的CPU占用和内存占用数据。

- 将获取的数据文件通过邮件以附件的方式发送到指定邮箱。

###获取Android设备中已安装应用程序的信息###

利用PackageManager类可以获取Android设备上已安装的应用程序包的信息，包括系统应用和非系统应用。我们关注的是非系统应用，可以只显示用户安装的应用程序信息。代码如下：

	public static List<PackageInfo> getInstalledApps(Context context) {  
	    List<PackageInfo> apps = new ArrayList<PackageInfo>();  
	    PackageManager pManager = context.getPackageManager();  
	    //获取Android设备中用户安装的APP
	    List<PackageInfo> paklist = pManager.getInstalledPackages(0);  
	    for (int i = 0; i < paklist.size(); i++) {  
	        PackageInfo pak = (PackageInfo) paklist.get(i);  
	        //判断是否为系统的应用程序，若不大于0，则为用户安装的应用程序 
	        if ((pak.applicationInfo.flags & pak.applicationInfo.FLAG_SYSTEM) <= 0) {  
	            apps.add(pak);  
	        }  
	    }  
	    return apps;  
	}  

获取应用程序列表后，我们可以继续获取应用程序的图标、应用程序大小等信息。选中待测试的应用程序后，利用Intent将待测试的应用程序的进程名、进程id和包名等信息传递给后台服务。

###性能数据的获取和保存###

在linux系统中，可以从/proc文件系统中获取系统硬件信息和当前正在运行进程的信息。/proc是一种伪文件系统（虚拟文件系统，只存在内存中，不占用外存空间）。一些linux程序如top、ps等实际上是从/proc文件中获取信息再组织显示。由于Android系统是基于linux内核，因此我们可以从/proc中获取计算CPU占用、内存占用和网络流量消耗信息。

####CPU占用数据的获取####

（1） 获取CPU核数

通过/proc/cpuinfo文件可以获取CPU的相关信息如型号、频率等。从/sys/devices/system/cpu/中获得CPU的核数。代码如下：

	 private int getNumCores() {
	        class CpuFilter implements FileFilter {
	            @Override
	            public boolean accept(File pathname) {
	                if(Pattern.matches("cpu[0-9]", pathname.getName())) {
	                    return true;
	                }
	                return false;
	            }      
	        }
	        try {
	            File dir = new File("/sys/devices/system/cpu/");
	            File[] files = dir.listFiles(new CpuFilter());
	            return files.length;
	        } catch(Exception e) {
	            e.printStackTrace();
	            return 1;
	        }
	    }

（2） 计算总的CPU占用率

根据CPU的时间来计算CPU占用率，/proc/stat文件包含了CPU活动信息。如下图所示。

![](/assets/blog_pic/proc_stat.PNG)

其中，第一行中的数值表示的是CPU从系统启动到当前时刻总的使用情况，如：

- 8860表示处于用户态的运行时间,但不包括nice值为负的进程所占用的CPU时间；

- 629表示nice值为负的进程所占用的CPU时间；

- 5176表示处于核心态的运行时间；

- 31923表示除IO等待外的其他等待时间。

通过第一行数据我们可以计算总的CPU时间：totalCPUTime = user + nice + system + idle + iowait + irq +softirq + stealstolen +guest。单位是jiffies（Jiffies为Linux核心变数，主要记录系统启动以来的节拍数tick）。

CPU总使用率= 100*((totalCPU2-totalCPU1)-(idleCPU2-idleCPU1))/(totalCPU2-totalCPU1).代码如下：

	public void getTotalCpuTime(){
	        String totalCpuPath = "/proc/stat";
	        try {
	            RandomAccessFile file = new RandomAccessFile(totalCpuPath, "r");
	            String[] toks = file.readLine().toString().split(" "); 
	            idleCPU = Long.parseLong(toks[5]);
	            totalCPU = Long.parseLong(toks[2]) + Long.parseLong(toks[3])
	                    + Long.parseLong(toks[4]) + Long.parseLong(toks[6])
	                    + Long.parseLong(toks[5]) + Long.parseLong(toks[7])
	                    + Long.parseLong(toks[8]);
	        } catch (FileNotFoundException e) {
	            e.printStackTrace();
	        } catch (IOException e) {
	            e.printStackTrace();
	        }
	    }
	
	    totalCPU2 = totalCpu;      
	    idleCPU2 = idleCpu;
	    //获取总体CPU占用率，其中CPUnum为CPU核心数
	    totalCpuRatio = fomart.format(100  *CPUnum *((double) ((totalCpu - idleCpu) 
	        - (totalCpu2 - idleCpu2)) / (double) (totalCpu - totalCpu2)));

（3）计算某个进程的CPU占用率

/proc/<pid>/stat文件包含了某个进程的CPU的所有活动信息。如下图所示。

![](/assets/blog_pic/proc_pid_stat.PNG)

其中980为邮件服务的进程id；325表示该任务在用户态的运行时间；150表示该任务在核心态的运行时间；后面的两个0分别表示已死线程在用户态和核心态的运行时间。时间单位为jiffies。

某进程CPU使用率= 100*(processCPU2-processCPU1)/(totalCPU2-totalCPU1)，代码如下：

	 public void getProcessCpuTime(){
	        String processCpuPath = "/proc/" + pid + "/stat";
	        try {
	            RandomAccessFile file = new RandomAccessFile(processCpuPath, "r");
	            String line = "";
	            StringBuffer sb = new StringBuffer();
	            sb.setLength(0);
	            while ((line = file.readLine()) != null) {
	                sb.append(line + "\n");
	            }
	            String[] toks = sb.toString().split(" "); 
	            processCPU = Long.parseLong(toks[13])+Long.parseLong(toks[14])
	                + Long.parseLong(toks[15]) + Long.parseLong(toks[16]);
	        } catch (FileNotFoundException e) {
	            e.printStackTrace();
	        } catch (IOException e) {
	            e.printStackTrace();
	        }
	    }
	processCpu2 = processCpu;
	    //获取某进程的CPU占用率，其中CPUnum为CPU核心数
	    processCpuRatio = fomart.format(100 * CPUnum*((double) (processCpu - processCpu2) 
	        / (double) (totalCpu - totalCpu2)));

（4） 利用Runtime类执行top命令来获取CPU占用情况

通过Android系统提供的Runtime类，执行adb 命令(top,procrank等命令)查询，通过对执行结果的标准控制台输出进行解析。执行adb命令的代码如下：

	final Process m_process = Runtime.getRuntime().exec("/system/bin/top -n 1");
	final StringBuilder sbread = new StringBuilder();
	BufferedReader bufferedReader = new BufferedReader(
	    new InputStreamReader(m_process.getInputStream()), 8192);
	
	Runtime.getRuntime().exec("/system/xbin/procrank");


####内存占用数据的获取####

内存占用有四种表现形式，分别如下：

- VSS（Virtual Set Size）虚拟内存占用；

- RSS（Resident Set Size）实际占用的物理内存（包含共享库占用的内存）；

- PSS（Proportional Set Size）实际占用的物理内存（包含比例分配共享库占用的内存）；

- USS（Unique Set Size）进程独自占用的物理内存（不包含共享库占用的内存）。	

其中VSS>=RSS>=PSS>=USS。在Android系统中利用procrank命令可以获得四类内存占用的数据。我们需要获得的就是实际内存占用PSS。

在内存获取的方法中，除了读取/proc文件和利用Runtime类执行adb命令外，还可以使用android.os.Debug来获取内存占用信息。代码如下：

	public int getPidMemorySize(int pid, Context context) 
	  {
	      ActivityManager am = (ActivityManager) context.getSystemService(Context.ACTIVITY_SERVICE);
	      int[] myMempid = new int[] { pid };
	      Debug.MemoryInfo[] memoryInfo = am.getProcessMemoryInfo(myMempid);
	      memoryInfo[0].getTotalSharedDirty();
	      int memSize = memoryInfo[0].getTotalPss();
	      return memSize;
	  }

####网络流量数据的获取####

获取Android单个进程的网络流量有两种方法：

（1）读取/proc/uid_stat/<uid>/tcp_send（上行数据）和/proc/uid_stat/<uid>/tpc_rcv（下行数据）两个文件，其中uid为进程的用户id；

（2）利用Android2.3及以后版本提供的android.net.TrafficStats类，这种方法实际上也是读取上述的两个文件来进行流量统计的，只是做了一个封装。

由于第二种方法只能在Android 2.3以上的版本使用，我们使用第一种方法来获取网络流量。代码如下：

	public void getNetInfo(){
	        String appNetRcvPath = "/proc/uid_stat/" + uid +"/tcp_rcv";
	        String appNetSndPath = "/proc/uid_stat/" + uid +"/tcp_snd";
	        try {
	            RandomAccessFile fileRcv = new RandomAccessFile(appNetRcvPath, "r");
	            RandomAccessFile fileSnd = new RandomAccessFile(appNetSndPath, "r");
	            tcp_rcv = Long.parseLong(fileRcv.readLine().toString());
	            tcp_snd = Long.parseLong(fileSnd.readLine().toString());
	        } catch (FileNotFoundException e) {
	            e.printStackTrace();
	        } catch (IOException e) {
	            e.printStackTrace();
	        }
	        tracffic = tcp_rcv + tcp_snd;
	    }

####性能数据的保存####

为了方便的进行性能数据的后续分析，我们将性能数据保存为CSV或excel文件。Java中操作excel文件可以使用jxl库或poi库。我们使用的是jxl，Jxl是一个开源的java Excel API项目。在Android项目中导入jxl的jar文件，即可使用jxl去操作Excel文件了。由于代码较长，在这就不列出了。性能数据存储后，我们便可读取Excel文件，将数据显示在悬浮窗和在app中绘制性能曲线了。

###避免后台服务被杀掉###

利用后台服务来测试Android手游的CPU占用、内存占用和网络流量消耗，但当Android设备的内存不够时，系统会杀掉一些没有用户交互的应用服务以释放资源，我们需要避免后台服务被杀掉。
Android有两类Services：

- startService(). 某组件启动该服务后，该类服务就会脱离组件独立运行，但当Android设备内存不够时，这类服务就会优先被杀掉；

- bindService(). 这类服务和某些组件进行绑定，组件可以利用这类服务来进行交互和通信（IPC）。当组件解除绑定时，这类服务被销毁。因此当创建的Services与当前交互的Activities绑定时，当Android设备内存不够时，也不会轻易的被杀掉（除非当前交互的Activities也被杀掉了）。为了更保险，我们可以将Services设置为前台运行（调用startForeground（）方法）。

因此，为了避免后台服务被杀掉，我们可以使用bindService()来实现，bindService（）有三种实现方法，这个留个下次再总结。

###邮件发送性能数据###

获取资源占用消耗数据文件后，我们可以调研Android的邮件客户端，通过邮件将数据文件发送到指定邮箱，便于在PC端进行进行查看分析。代码如下：

	btnEmail.setOnClickListener(new OnClickListener()
	{
	    @Override
	    public void onClick(View v){
	        File file = new File(PerformancetestService.resultFilePath); //附件文件地址
	        Intent email = new Intent(Intent.ACTION_SEND);
	        String[] emailReciver = new String[]{"gzzhangxiang@corp.netease.com"};
	        email.putExtra(android.content.Intent.EXTRA_EMAIL, emailReciver);
	        email.setType("application/octet-stream"); //设置为二进制数据
	        email.putExtra("subject","性能测试数据文件"); //标题
	        email.putExtra("body", "附件是资源占用信息文件"); //正文
	        //添加附件，附件为file对象 
	        email.putExtra(Intent.EXTRA_STREAM, Uri.fromFile(PerformancetestService.resultFile));               
	        startActivity(email); //调用系统的mail客户端进行发送
	    }
	});

###截屏功能和在Android APP中显示资源占用曲线###

这两部分在之前的文章中有介绍。可查看[利用android-screenshot-library(ASL)来实现截屏](http://gitzx.github.io/android-screenshot-library/)和[利用ichartjs库来实现Android上绘制报表](http://gitzx.github.io/android-ichartjs/)

今天是2014的第一天，希望自己在接下来的一年里更加努力，多总结和思考，加油~

