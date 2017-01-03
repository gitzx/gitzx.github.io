---
date: 2016-12-17 14:21:30+00:00
layout: post
title: MySQL数据库操作(python)
thread: 170
categories: database 
tags: database 

---

这篇用python语言小结下数据库的连接及对记录字段的各种操作。

### 利用_mysql模块连接 ###

`_mysql`模块直接封装实现了MySQL的C语言API函数。它与Python标准的数据库API接口不兼容。

	import _mysql
	import sys
	
	con = none
	
	try:
		con = _mysql.connect('localhost','gitzx','123456','test')
		con.query("SELECT VERSION()")
		result = con.use_reulst()
		print "MySQL VERSION: %s " % result.fetch_row()[0]
	except _mysql.Error, e:
		print "Error %d: %s " % (e.args[0], e.args[1])
	finally:
		if con:
			con.close()


### 利用MySQLdb模块连接 ###

MySQLdb是在_mysql模块的基础上进一步进行封装，并且与Python的标准数据库API接口兼容。使用这个模块是操作MySQL数据库的首选方法。

主要步骤有：

1. 用db.connect()创建数据库连接，连接对象为conn；

2. 如果不需要返回查询结果，就直接调用conn.execute();

3. 如果需要返回查询结果，则需要首先通过conn.cursor()创建游标对象cur，并使用cur.fetchone()等函数获取查询结果；

4. 根据数据库隔离级别的不同，修改数据库后，可能需要使用conn.commit()手动提交事务；

5. 调用相应的close()方法关闭cur及conn。

例如：

	import MySQLdb as mdb 
	import sys
	
	con = none 
	try:
		con = mdb.connect('localhost','gitzx','123456','test')
		cur = con.cursor()
		cur.execute("SELECT VERSION()")
		data = cur.fetchone()
		print "Database VERSION: %s " % data
	
	    cur.execute("CREATE TABLE IF NOT EXISTS \
	        Writers(Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25))")
	    cur.execute("INSERT INTO Writers(Name) VALUES('Jack London')")
	    cur.execute("INSERT INTO Writers(Name) VALUES('Honore de Balzac')")
	    con.commit()
	except mdb.Error, e:
		print "Error %d: %s " % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		if con:
			con.close()


### python数据库连接池包DBUtils ###

python中使用MySQLdb进行数据库请求时，都是独立的去请求访问，相当浪费资源，且当访问数量达到一定数量时，会对MySQL性能会产生较大的影响。在实际使用过程中，常会使用数据库的连接池技术如([DBUtils包](https://pypi.python.org/pypi/DBUtils)和ORM框架)，达到访问数据库时资源复用的目的。

DBUtils提供了两个外部接口：

1. `DBUtils.PersistentDB `：提供线程专用的数据库连接，并自动管理连接；

2. `DBUtils.PooledDB`：提供线程间可共享的数据库连接，并自动管理连接。

相关参数配置：

1. dbapi ：数据库接口

2. mincached ：启动时开启的空连接数量

3. maxcached ：连接池最大可用连接数量

4. maxshared ：连接池最大可共享连接数量

5. maxconnections ：最大允许连接数量

6. blocking ：达到最大数量时是否阻塞

7. maxusage ：单个连接最大复用次数

简单例子：

	import MySQLdb as mdb
	import time
	import string
	from DBUtils.PooledDB import PooledDB
	pool = PooledDB(mdb, user="gitzx",passwd="123456",host="localhost",\
		port=3306,db="test",mincached=2,maxcached=2,maxshared=2,maxconnections=2)
	
	for i in range(1000):
		time.sleep(1)
		conn = pool.connection()
		cursor = conn.cursor()
		cursor.execute("""SELECT * from student""")
		result = cursor.fetchall()
		print cursor.description
		conn.close()


### ORM框架使用 ###

除了上述方法连接操作数据库，也可以使用ORM(Object-relational mappers)来进行数据库操作。ORM框架建立在数据库API之上，使用关系对象映射进行数据库操作，即将对象转换成SQL，然后使用数据API执行SQL并获取执行结果。

在python中，常用的ORM框架有SQLAlchemy和Django ORM。之前用flask做过一些web网站，在这简单介绍下SQLAlchemy。

	from sqlalchemy import create_engine
	import MySQLdb
	
	engine = create_engine('mysql+mysqldb://gitzx:123456@127.0.0.1:3306/test',max_overflow=5)
	# method_a starts a transaction and calls method_b
	def method_a(connection):
	    trans = connection.begin() # open a transaction
	    try:
	        method_b(connection)
	        trans.commit()  # transaction is committed here
	    except:
	        trans.rollback() # this rolls back the transaction unconditionally
	        raise
	
	# method_b also starts a transaction
	def method_b(connection):
	    trans = connection.begin() # open a transaction - this runs in the context of method_a's transaction
	    try:
	        connection.execute("insert into mytable values ('bat', 'lala')")
	        connection.execute(mytable.insert(), col1='bat', col2='lala')
	        trans.commit()  # transaction is not committed yet
	    except:
	        trans.rollback() # this rolls back the transaction unconditionally
	        raise
	
	# open a Connection and call method_a
	conn = engine.connect()
	method_a(conn)
	conn.close()


参考：[MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/)

[SQLAlchemy 1.1 Documentation](http://docs.sqlalchemy.org/en/latest/core/tutorial.html)