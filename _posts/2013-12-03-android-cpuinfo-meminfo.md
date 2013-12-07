---
date: 2013-12-03 18:45:30+00:00
layout: post
title: 获取Android设备上的资源占用消耗信息
thread: 09
categories: android
tags:  android
---

最近在做Android的资源占用信息监控，需要获取单个进程的cpu、内存占用信息，在这总结下常用的方法。

###Android的API函数###

- ActivityManager类

该类可以实现许多系统级别的Activity管理和监控功能，常用的内部类：

(1)ActivityManager.MemoryInfo 系统内存使用情况;
(2)ActivityManager.ProcessErrorStateInfo 错误状态的进程;
(3)ActivityManager.RecentTaskInfo 近期用户打开的任务信息;
(4)ActivityManager.RunningAppProcessInfo 正在运行应用程序进程信息;
(5)ActivityManager.RunningServiceInfo 正在运行的服务信息;
(6)ActivityManagerRunningTaskInfo 正在运行的任务信息;
	
	public long getFreeMemorySize(Context context) 
	{
		ActivityManager.MemoryInfo outInfo = new ActivityManager.MemoryInfo();
		ActivityManager am = (ActivityManager) context.getSystemService(Context.ACTIVITY_SERVICE);
		am.getMemoryInfo(outInfo);
		long avaliMem = outInfo.availMem;
		return avaliMem / 1024;
	}

- 利用android.os.Debug查看单个进程的内存信息

		public int getPidMemorySize(int pid, Context context) 
		{
			ActivityManager am = (ActivityManager) context.getSystemService(Context.ACTIVITY_SERVICE);
			int[] myMempid = new int[] { pid };
			Debug.MemoryInfo[] memoryInfo = am.getProcessMemoryInfo(myMempid);
			memoryInfo[0].getTotalSharedDirty();
			// int memSize = memoryInfo[0].dalvikPrivateDirty;
			// TODO PSS
			int memSize = memoryInfo[0].getTotalPss();
			// int memSize = memoryInfo[0].getTotalPrivateDirty();
			return memSize;
		}


###解析Android的设备信息文件###

- proc/cpuinfo获取

		private String ReadCPUinfo()
		 {
		  ProcessBuilder cmd;
		  String result="";
		  try{
		   String[] args = {"/system/bin/cat", "/proc/cpuinfo"};
		   cmd = new ProcessBuilder(args);		
		   Process process = cmd.start();
		   InputStream in = process.getInputStream();
		   byte[] re = new byte[1024];
		   while(in.read(re) != -1){
		    System.out.println(new String(re));
		    result = result + new String(re);
		   }
		   in.close();
		  } catch(IOException ex){
		   ex.printStackTrace();
		  }
		  return result;
		 }

- proc/meminfo获取

		public long getTotalMemory() {
			String memInfoPath = "/proc/meminfo";
			String readTemp = "";
			String memTotal = "";
			long memory = 0;
			try {
					FileReader fr = new FileReader(memInfoPath);
					BufferedReader localBufferedReader = new BufferedReader(fr, 8192);
					while ((readTemp = localBufferedReader.readLine()) != null) {
						if (readTemp.contains("MemTotal")) {
							String[] total = readTemp.split(":");
							memTotal = total[1].trim();
						}
					}
					String[] memKb = memTotal.split(" ");
					memTotal = memKb[0].trim();
					Log.d(LOG_TAG, "memTotal: " + memTotal);
					memory = Long.parseLong(memTotal);
				} catch (IOException e) {
					Log.e(LOG_TAG, "IOException: " + e.getMessage());
				}
			return memory;
		}


- proc/[pid]/stat 获取某个进程的信息；proc/stat获取所有进程信息
	
		public void readCpuStat() {
			String processPid = Integer.toString(pid);
			String cpuStatPath = "/proc/" + processPid + "/stat";
			try {
				// monitor cpu stat of certain process
				RandomAccessFile processCpuInfo = new RandomAccessFile(cpuStatPath,
						"r");
				String line = "";
				StringBuffer stringBuffer = new StringBuffer();
				stringBuffer.setLength(0);
				while ((line = processCpuInfo.readLine()) != null) {
					stringBuffer.append(line + "\n");
				}
				String[] tok = stringBuffer.toString().split(" ");
				processCpu = Long.parseLong(tok[13]) + Long.parseLong(tok[14]);
				processCpuInfo.close();
			} catch (FileNotFoundException e) {
				Log.e(LOG_TAG, "FileNotFoundException: " + e.getMessage());
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
	
			try {
				// monitor total and idle cpu stat of certain process
				RandomAccessFile cpuInfo = new RandomAccessFile("/proc/stat", "r");
				String[] toks = cpuInfo.readLine().split(" ");
				idleCpu = Long.parseLong(toks[5]);
				totalCpu = Long.parseLong(toks[2]) + Long.parseLong(toks[3])
						+ Long.parseLong(toks[4]) + Long.parseLong(toks[6])
						+ Long.parseLong(toks[5]) + Long.parseLong(toks[7])
						+ Long.parseLong(toks[8]);
				cpuInfo.close();
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}

###通过Android系统提供的Runtime类，执行adb 命令(top,procrank,ps...等命令)查询。###
	
	final Process m_process = Runtime.getRuntime().exec("/system/bin/top -n 1");
	final StringBuilder sbread = new StringBuilder();
	BufferedReader bufferedReader = new BufferedReader(
	    new InputStreamReader(m_process.getInputStream()), 8192);
	    
	# procrank  
	Runtime.getRuntime().exec("/system/xbin/procrank");

procrank命令可以获得当前系统中各进程的内存占用，从/proc/pid/maps中读取信息来进行统计，包含PSS，USS，VSS，RSS。

也可以使用smem强大的工具来监控手机内存，可以监控系统lib，生成饼图或者柱形图

###利用adb shell命令在pc端查看Android设备的资源占用消耗信息###

- 通过adb shell进入Android系统的proc目录，查看proc/cpuinfo、proc/meminfo、proc/[pid]/stat和proc/stat信息。

- 通过adb shell的top命令查看cpu、内存占用信息。

- 通过adb shell的tcpdump命令查看Android设备网络流量消耗信息。由于tcpdump不是Android中自带的命令，需要安装[tcpdump](http://www.tcpdump.org/)。安装tcpdump的命令如下：

		C:\Users\Administrator>adb shell
		shell@android:/ $ su
		su
		shell@android:/ # chmod 777 /data/local
		chmod 777 /data/local
		shell@android:/ # ^C
		C:\Users\Administrator>adb push tcpdump /data/local

启动tcpdump服务的命令如下：

	C:\Users\Administrator>adb shell
	shell@android:/ $ su
	su
	shell@android:/ # chmod 6755 /data/local/tcpdump
	chmod 6755 /data/local/tcpdump
	shell@android:/ # /data/local/tcpdump -p -s 0 -w /sdcard/net.pcap

可以在sd卡中得到net.pcap文件（或adb shell pull命令获得），利用wireshark即可分析。



参考：[查看基于Android 系统单个进程内存、CPU使用情况的几种方法](http://blog.csdn.net/kieven2008/article/details/6445421)

