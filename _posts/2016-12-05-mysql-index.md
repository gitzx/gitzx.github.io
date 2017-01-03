---
date: 2016-12-04 19:03:30+00:00
layout: post
title: MySQL索引小结
thread: 168
categories: database 
tags: database 

---

索引(Index)是帮助MySQL高效获取数据的数据结构。

### 索引的存储分类 ###

1. B-Tree索引：MyISAM引擎、InnoDB引擎、Memory引擎等都支持B树索引；

（1）普通索引：最基本的索引类型；

（2）唯一索引：字段信息不允许重复的索引；

（3）主键索引：主键是一种唯一性索引，必须指定为“Primary KEY”。

2. Hash索引： 只有Memory引擎支持，使用场景简单；

3. R-Tree索引(空间索引)：空间索引是MyISAM的一种特殊索引类型，主要用于地理空间的数据类型；

4. Full-text索引(全文索引)：全文索引也是MyISAM的一种特殊索引类型，InnoDB从MySQL5.6版本对全文索引的支持。


### 索引操作 ###

设置索引：

	//ALTER TABLE用来创建普通索引、UNIQUE索引或PRIMARY KEY索引
	ALTER TABLE table_name ADD INDEX index_name (column_list)
	ALTER TABLE table_name ADD UNIQUE (column_list)
	ALTER TABLE table_name ADD PRIMARY KEY (column_list)
	
	//CREATE INDEX 可对表增加普通索引或UNIQUE索引
	CREATE INDEX index_name ON table_name (column_list)
	CREATE UNIQUE INDEX index_name ON table_name (column_list)

删除索引：

	DROP INDEX index_name ON table_name
	ALTER TABLE table_name DROP INDEX index_name 
	ALTER TABLE table_name DROP PRIMARY KEY

查看索引：

	mysql> show index from table_name;
	mysql> show keys from table_name;


### 索引选择 ###

索引选择的原则：

1. 较频繁的作为查询条件的字段应该创建索引；

2. 唯一性太差的字段不适合单独创建索引；

3. 更新频繁的字段不适合创建索引；

4. 不会出现在`WHERE`子句中的字段不该创建索引。






