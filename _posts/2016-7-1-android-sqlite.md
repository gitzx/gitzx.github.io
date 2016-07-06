---
date: 2016-7-1 19:15:30+00:00
layout: post
title: Android中sqlite使用小结
thread: 149
categories: android
tags: android

---

Android系统提供了五种数据存储方式：（1）[Shared Preferences](https://developer.android.com/guide/topics/data/data-storage.html?hl=zh-cn#pref)；（2）[Internal Storage](https://developer.android.com/guide/topics/data/data-storage.html?hl=zh-cn#filesInternal)；（3）[External Storage](https://developer.android.com/guide/topics/data/data-storage.html?hl=zh-cn#filesExternal)；（4）[SQLite Databases](https://developer.android.com/guide/topics/data/data-storage.html?hl=zh-cn#db)；（5）[Network Connection](https://developer.android.com/guide/topics/data/data-storage.html?hl=zh-cn#netw)。在这篇中小结下Android中sqlite的使用。


Android系统中运行时集成了SQLite，因此每个Android应用程序都可以通过[android.database.sqlite](https://developer.android.com/guide/topics/data/data-storage.html?hl=zh-cn#netw)接口访问Android内置的SQLite数据库。


### SQLite基本命令 ###

在pc上安装SQLite后或者通过adb连接到Android设备后，可以通过命令来操作SQLite数据库，常用命令如下：

1. 创建数据库： `sqlite3 test.db`

2. 创建表： `create table testtable(id integer primary key,value text);`

3. 插入数据： 

		insert into testtable(id,value) value(1,"AAA");
		insert into testtable(id,value) value(2,"BBB");
		insert into testtable(id,value) value(3,"CCC");

4. 查询数据： `select * from test;`

5. 删除表： `drop table test.testtable;` 

6. 创建视图： `create view testview as select * from testtable;`

7. 创建索引: `create index testidx on testtable(value);`

8. 显示表结构： `.schema testtable`

9. 获取所有的表和视图： `.table`

10. 获取指定表的索引列表： `.indices testetable`

11. 导出数据到SQL文件：
	
		.output [filename]
		.dump
		.output stdout

12. 从SQL文件中导入数据库： `.read [filename]`

13. 格式化输出数据到CSV格式：

		.output [filename.csv]
		.separator
		select * from test;
		.output stdout

14. 从CSV文件中导入数据到表中

		create table new newtesttable (id integer primary key,value text);
		.import [filename.csv] newtesttable

15. 备份数据库： `sqlite3 test.db .dump > backup.sql`

16. 恢复数据库： `sqlite3 test.db < backup.sql`


### 在Android中操作SQLite ###

在Android中使用SQLite常用做法是创建一个继承[SQLiteOpenHelper](https://developer.android.com/reference/android/database/sqlite/SQLiteOpenHelper.html?hl=zh-cn)的子类并重写`onCreate()`，`onUpgrade()`或者`onOpen()`，`onDowngrade()`方法。

创建数据库和表：

	{% highlight java %}
	//ExampleDbSchema.java
	public class ExampleDbSchema
	{
	    public static final class ExampleDbTable
	    {
	        public static final String NAME="ExampleDbSchema";
	        public static final class Cols
	        {
	            public static final String UUID="uuid";
	            public static final String TITLE="title";
	        }
	    }
	}
	//ExampleDbHelper.java
	import android.content.Context;
	import android.database.sqlite.SQLiteDatabase;
	import android.database.sqlite.SQLiteOpenHelper;
	import com.etanote.android.ExampleDbSchema.ExampleDbTable;
	public class ExampleDbHelper extends SQLiteOpenHelper
	{
	    private static final int DATABASE_VERSION=1;
	    private static final String DATABASE_NAME="ExampleDb.db";
	    private static final String SQL_CREATE_ENTRIES=
	        "CREATE TABLE"+ExampleDbTable.NAME+"("+
	        "_id integer primary key autoincrement, " +
	        ExampleDbTable.Cols.UUID + "," +
	        ExampleDbTable.Cols.TITLE + "," +
	        ")"
	    );
	    private static final String SQL_DELETE_ENTRIES=
	        "DROP TABLE IF EXISTS "+ExampleDbTable.NAME;
	    public ExampleDbHelper(Context context)
	    {
	        super(context,DATABASE_NAME,null,DATABASE_VERSION);
	    }
	    //第一次创建表或者表初始化时会创建数据库
	    @Override
	    public void onCreate(SQLiteDatabase db)
	    {
	        db.execSQL(SQL_CREATE_ENTRIES);
	    }
	    public void onUpgrade(SQLiteDatabase db,int oldVersion,int newVersion)
	    {
	        db.execSQL(SQL_DELETE_ENTRIES);
	        onCreate(db);
	    }
	    public void onDowngrade(SQLiteDatabase db,int oldVersion,int newVersion)
	    {
	        onUpgrade(db,oldVersion,newVersion);
	    }
	}
	{% endhighlight %}


获取对数据库的引用，可以调用[getWritableDatabase()](https://developer.android.com/reference/android/database/sqlite/SQLiteOpenHelper.html?hl=zh-cn#getWritableDatabase())或[getReadableDatabase()](https://developer.android.com/reference/android/database/sqlite/SQLiteOpenHelper.html?hl=zh-cn#getReadableDatabase())。例如: 

	{% highlight java %}
	private CrimeLab(Context context) 
	{
	    mContext = context.getApplicationContext();
	    mDatabase = new CrimeBaseHelper(mContext)
	            .getWritableDatabase();
	}
	{% endhighlight %}

插入、查看、更新、删除数据操作：

	{% highlight java %}
	private static ContentValues getContentValues()
	{
	    ContentValues values=new ContentValues();
	    values.put(ExampleDbTable.Cols.UUID,"100");
	    values.put(ExampleDbTable.Cols.TITLE,"HELLO");
	    return values;
	}
	ContentValues values=getContentValues();
	long newRowId;
	//insert
	newRowId=mDatabase.insert(ExampleDbTable.NAME,null,values);
	//query  返回Cursor对象
	String[] projection={ExampleDbTable.Cols.UUID,ExampleDbTable.Cols.TITLE};
	String sortOrder=ExampleDbTable.Cols.UUID + " DESC";
	Cursor cursor = db.query(
	    ExampleDbTable.NAME,   // The table to query
	    projection,             // The columns to return
	    selection,              // The columns for the WHERE clause
	    selectionArgs,          // The values for the WHERE clause
	    null,                   // don't group the rows
	    null,                   // don't filter by row groups
	    sortOrder               // The sort order
	    );
	cursor.moveToFirst();
	long itemId=cursor.getLong(corsor.getColumnIndexOrThrow(ExampleDbTable.Clos.UUID));
	//update
	values.put(ExampleDbTable.Cols.TITLE,"World");
	String selection=ExampleDbTable.Cols.UUID+" LIKE ? ";
	String[] selectionArgs={String.valueOf(newRowId)};
	newRowId=mDatabase.update(ExampleDbTable.NAME,values,selection,selectionArgs);
	//delete
	mDatabase.update(ExampleDbTable.NAME,values,selection,selectionArgs);
	{% endhighlight %}

































参考：[SQLite Android Bindings
Documentation](https://www.sqlite.org/android/doc/trunk/www/index.wiki)

[android.database.sqlite](https://developer.android.com/reference/android/database/sqlite/package-summary.html)

[在SQL数据库中保存数据](https://developer.android.com/training/basics/data-storage/databases.html?hl=zh-cn#ReadDbRow)