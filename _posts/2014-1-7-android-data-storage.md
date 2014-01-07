---
date: 2014-1-7 19:34:30+00:00
layout: post
title: Android中的数据存储
thread: 25
categories: android
tags: android
---

Android提供了提供了五种选择用于Android应用程序数据存储：

- Shared Preferences

	用于存储私有简单的键值对数据，实质是xml文件；

- Internal Storage

	用于在设备内部存储器上存储私有数据；

- External Storage 

	用于在设备外边存储器上存储公共数据；

- SQLite Databases

	在SQLite数据库上存储结构化数据；

- Network Connection

	将数据存储在网络服务器上

Android还提供了Content Provider用于对外共享数据，即将私有数据共享给其他应用访问。

Content Provider不能算是一种数据存储方式。它只是给我们提供操作数据的接口，Content Provider背后其实还是SQLite、File I\O等其他方式。

###Shared Preferences###

Shared Preferences是一种轻型的数据存储方式，它的本质是基于XML文件存储key-value键值对数据，通常用来存储一些简单的配置信息。其存储位置在/data/data/<包名>/shared_prefs目录下。SharedPreferences对象本身只能获取数据而不支持存储和修改，存储修改是通过Editor对象实现。实现SharedPreferences存储的步骤如下：

 （1）根据Context获取SharedPreferences对象

 （2）利用edit()方法获取Editor对象。

 （3）通过Editor对象存储key-value键值对数据。

 （4）通过commit()方法提交数据。

实现代码如下：

	public class MainActivity extends Activity {    
	 @Override
	     public void onCreate(Bundle savedInstanceState) {
	        super.onCreate(savedInstanceState);
	        setContentView(R.layout.main);
	        //获取SharedPreferences对象
	        Context ctx = MainActivity.this;       
	        SharedPreferences sp = ctx.getSharedPreferences("SP", MODE_PRIVATE);
	        //存入数据
	        Editor editor = sp.edit();
	        editor.putString("STRING_KEY", "string");
	        editor.putInt("INT_KEY", 0);
	        editor.putBoolean("BOOLEAN_KEY", true);
	        editor.commit();
	        //返回STRING_KEY的值
	        Log.d("SP", sp.getString("STRING_KEY", "none"));
	        //如果NOT_EXIST不存在，则返回值为"none"
	        Log.d("SP", sp.getString("NOT_EXIST", "none"));
	     }
	}

执行过后，即在/data/data/<包名>/shared_prefs目录下生成了一个SP.xml文件，一个应用可以创建多个这样的xml文件。 

###Internal Storage###

当应用程序被卸载时，存储在Android设备内部存储空间的数据相应的也会被删除。

写数据实现如下：

	String FILENAME = "hello_file";
	String string = "hello world!";
	FileOutputStream fos = openFileOutput(FILENAME, Context.MODE_PRIVATE);
	fos.write(string.getBytes());
	fos.close();

读取数据则使用openFileInput()、read().

###External Storage ###

####声明读写权限####

	<manifest ...>
	    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="18"/>  
	</manifest>

在Android4.4及以后版本中，访问应用程序私有的存储数据，不需要声明读写权限。

####检测外部存储可用性####

	/* Checks if external storage is available for read and write */
	public boolean isExternalStorageWritable() {
	    String state = Environment.getExternalStorageState();
	    if (Environment.MEDIA_MOUNTED.equals(state)) {
	        return true;
	    }
	    return false;
	}
	
	/* Checks if external storage is available to at least read */
	public boolean isExternalStorageReadable() {
	    String state = Environment.getExternalStorageState();
	    if (Environment.MEDIA_MOUNTED.equals(state) ||
	        Environment.MEDIA_MOUNTED_READ_ONLY.equals(state)) {
	        return true;
	    }
	    return false;
	}

####创建目录存储数据####

对其他应用程序公开数据的实现如下：

	public File getAlbumStorageDir(String albumName) {
	    // Get the directory for the user's public pictures directory.
	    File file = new File(Environment.getExternalStoragePublicDirectory(
	            Environment.DIRECTORY_PICTURES), albumName);
	    if (!file.mkdirs()) {
	        Log.e(LOG_TAG, "Directory not created");
	    }
	    return file;
	}

若不对其他应用程序公开，则使用getExternalFilesDir()方法。

###Databases（SQLite）###

Android 集成了 SQLite 数据库,数据库存储在 data/< 项目文件夹 >/databases/ 下。 Android 开发中使用 SQLite 数据库 Activites 可以通过 Content Provider 或者 Service 访问一个数据库。

创建数据库 Android 不自动提供数据库。在 Android 应用程序中使用 SQLite，必须自己创建数据库，然后创建表、索引，填充数据。

	Android 提供了 SQLiteOpenHelper 帮助你创建一个数据库

	public class DictionaryOpenHelper extends SQLiteOpenHelper {
	
	    private static final int DATABASE_VERSION = 2;
	    private static final String DICTIONARY_TABLE_NAME = "dictionary";
	    private static final String DICTIONARY_TABLE_CREATE =
	                "CREATE TABLE " + DICTIONARY_TABLE_NAME + " (" +
	                KEY_WORD + " TEXT, " +
	                KEY_DEFINITION + " TEXT);";
	
	    DictionaryOpenHelper(Context context) {
	        super(context, DATABASE_NAME, null, DATABASE_VERSION);
	    }
	
	    @Override
	    public void onCreate(SQLiteDatabase db) {
	        db.execSQL(DICTIONARY_TABLE_CREATE);
	    }
	}

###Network Connection###

网络存储使用java.net.*和android.net.*这两个包，技术比较多，在这就不总结了。


参考：[Storage Options](http://developer.android.com/guide/topics/data/data-storage.html)

