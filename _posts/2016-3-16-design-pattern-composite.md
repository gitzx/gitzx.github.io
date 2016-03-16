---
date: 2016-3-16 8:51:30+00:00
layout: post
title: 组合模式
thread: 109
categories: design_pattern
tags: design_pattern
---

组合模式是将对象组合成树形结构以表示“部分-整体”的层次结构，组合模式使得用户对单个对象和组合对象的使用具有一致性。

### 组合模式三要素 ###

1. 抽象构件角色(Component)：组合中的对象声明接口，实现所有类共有接口的默认行为，声明一个接口用于访问和管理Component子部件；

2. 树叶构件组件(Leaf)：在组合树中表示叶节点对象，叶节点没有子节点，在组合中定义图元对象的行为；

3. 树枝构件角色(Composite)：定义有子部件的那些部件的行为，存储子部件，在Component接口中实现与子部件有关的操作。

### 组合模式两种实现方式 ###

1. 透明方式：在component中声明所有用于管理子对象的方法，如add、remove等，实现component接口的类都具备上述方法。好处是叶子节点和其他节点是一致的，但缺点是叶子节点不具备add、remove功能，实现它们是没有意义的。

2. 安全方式：不在component中声明所有用于管理子对象的方法，在composite接口中声明管理子对象的方法。

### 组合模式安全方式实现 ###

	{% highlight java %}
	//component
	public abstract class File
	{
		String name;
		public File(String name)
		{
			this.name = name;
		}
		public String getName()
		{
			return name;
		}
		public void setName(String name)
		{
			this.name = name;
		}
		public abstract void display();
	}
	//composite
	public class Folder extends File
	{
		private List<File> files;
		public Folder(String name)
		{
			super(name);
			files = new ArrayList<File>();
		}
		public void display()
		{
			for(File file : files)
			{
				file.display();
			}
		}
		public void add(File file)
		{
			files.add(file);
		}
		public void remove(File file)
		{
			files.remove(file);
		}
	}
	//leaf:text、image
	public class TextFile extends File
	{
		public TextFile(String name)
		{
			super(name);
		}
		public void display()
		{
			System.out.println("TextFile : " + super.getName());
		}
	}
	public class ImageFile extends File
	{
		public ImageFile(String name)
		{
			super(name);
		}
		public void display()
		{
			System.out.println("ImageFile: " + super.getName());
		}
	}
	//Client
	public class Client
	{
		public static void main(String[] args)
		{
			Folder folder = new Folder("Folder");
			TextFile textfile = new TextFile("1.txt");
			ImageFile imagefile = new ImageFile("1.png");
			Folder folderA = new Folder("folderA");
	
			folder.add(textfile);
			folder.add(imagefile);
			folder.add(folderA);
	
			TextFile textfile2 = new TextFile("2.txt");
			ImageFile imagefile2 = new ImageFile("2.png");
			folderA.add(textfile2);
			folderA.add(imagefile2);
	
			folderA.display();
			folder.display();
		}
	}
	{% endhighlight %}


### 适用场景 ###

1. 需表示对象-整体层次结构

2. 希望客户端忽略组合对象和单个对象的不同，统一的使用组合结构中的所有对象。