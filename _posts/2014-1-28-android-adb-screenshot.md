---
date: 2014-1-28 15:35:30+00:00
layout: post
title: 利用adb对Android进行截屏
thread: 34
categories: android
tags: android
---

之前介绍了利用adl在Android上对Android进行截屏,可见[利用android-screenshot-library(ASL)来实现截屏](http://gitzx.github.io/android-screenshot-library/).

在这介绍下利用Android debug Bridge来截屏，由于Android上没有`java.awt.Image`, 因此只能在PC端对连接的Android设备进行截屏，具体代码如下：
	
	import java.io.File;
	import java.io.IOException;
	import com.android.ddmlib.AndroidDebugBridge;
	import com.android.ddmlib.IDevice;
	import com.android.ddmlib.RawImage;
	import com.android.ddmlib.AndroidDebugBridge.IDeviceChangeListener;
	import java.awt.Dimension;
	import java.awt.image.BufferedImage;
	import javax.imageio.ImageIO;
	
	public class Screenshot implements IDeviceChangeListener {
		
		private static boolean mConnected = false;
	
		public static void main(String[] args) {
			try {
				// 创建Android Debug Bridge
				AndroidDebugBridge.init(false);
				AndroidDebugBridge adb = AndroidDebugBridge.createBridge();
				
				// 监听设备连接
				Screenshot ss = new Screenshot();
				AndroidDebugBridge.addDeviceChangeListener(ss);
				System.out.print("Waiting for device connection...\n");
				synchronized (ss) {
					ss.wait();
				}
				
				// 获取连接的Android设备列表
				IDevice[] devices = adb.getDevices();
				if(devices.length > 0) {
					// 对第一个连接的Android设备进行截屏
					getScreenshots(ss, devices[0]);
				}
				System.out.print("Done\n");
			} catch (InterruptedException e) {
	
			} finally {
				// 关闭Android Debug Bridge
				AndroidDebugBridge.terminate();
			}
		}
		
		private static void getScreenshots(Screenshot ss, IDevice device) {
			// 获取连接的Android设备编号
			String thisDevice = device.getSerialNumber();
			String dir = String.format("%s", thisDevice);
			
			// Set up the directory
			if (new File(dir).exists()){
				System.out.printf("Writing files to an existing directory %s\n", dir);
			} else if (new File(dir).mkdir() == false) {
				System.out.printf("Couldn't create directory %s\n", dir);
				return;
			} else {
				System.out.printf("Writing files to directory %s\n", dir);
			}		
			
			if (mConnected) {			
				RawImage raw = null;
				try {
					//截屏
					raw = device.getScreenshot();
				} catch (IOException e) {
					System.out.printf("Error getting image: %s\n", e.getMessage());
				}
				
				//获取合适大小的图形
				Boolean landscape = false; 
				BufferedImage image = null;
		        
				Dimension size = new Dimension();
				int width2 = landscape ? raw.height : raw.width;
				int height2 = landscape ? raw.width : raw.height;
		        if (image == null) {
					image = new BufferedImage(width2, height2,
							BufferedImage.TYPE_INT_RGB);
					size.setSize(image.getWidth(), image.getHeight());
				} else {
					if (image.getHeight() != height2 || image.getWidth() != width2) {
						image = new BufferedImage(width2, height2,
								BufferedImage.TYPE_INT_RGB);
						size.setSize(image.getWidth(), image.getHeight());
					}
				}
				int index = 0;
				int indexInc = raw.bpp >> 3;
				for (int y = 0; y < raw.height; y++) {
					for (int x = 0; x < raw.width; x++, index += indexInc) {
						int value = raw.getARGB(index);
						if (landscape)
							image.setRGB(y, raw.width - x - 1, value);
						else
							image.setRGB(x, y, value);
					}
				}
				
				String filename = String.format("%s%soutput.png", dir, File.separator);
				
		        try {
					ImageIO.write(image, "png", new File(filename));
					System.out.printf("Saved picture as %s\n", filename);
				} catch (IOException e) {
					System.out.println("Failed to find png writer");
				}
				
			}
		}
	
		//设备连接
		@Override
		public void deviceConnected(IDevice device) {
			System.out.printf("Device %s connected\n", device.getSerialNumber());
			mConnected = true;
			synchronized (this) {
				notify();
			}
		}
	
	 	//设备断开连接
		@Override
		public void deviceDisconnected(IDevice device) {
			System.out.printf("Device  %s disconnected\n", device.getSerialNumber());
			mConnected = false;
			synchronized (this) {
				notify();
			}
		}
	 
		@Override
		public void deviceChanged(IDevice device, int changeMask) {
			// 
		}
	}