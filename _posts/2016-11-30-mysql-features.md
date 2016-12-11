---
date: 2016-11-30 10:12:30+00:00
layout: post
title: MySQL一些特性小结
thread: 167
categories: database 
tags: database 

---

这篇小结下MySQL中的一些特性：

1. 视图

2. 存储程序（存储过程、存储函数、触发器、事件）

3. 游标

4. 约束

5. 分区表

6. 事务和锁 

7. 索引

8. 复制


### 1. 视图 ###

视图是一个虚拟表，不存放任何数据，包含的是数据的查询。有利于封装。

视图和表在同一命名空间，大多数地方视图和表是同样对待，但不能对视图创建触发器，也不能使用`Drop`命令删除视图。例如：

	CREATE TABLE t (qty INT, price INT);
	INSERT INTO t VALUES(3, 50), (5, 60);
	CREATE VIEW v AS SELECT qty, price, qty*price AS value FROM t;
	SELECT * FROM v WHERE qty = 5;
	UPDATE v SET qty = qty + 1;
	DELETE v WHERE qty = 4;


使用`WITH CHECK OPTION`关键字：

创建视图时添加`WITH CHECK OPTION`关键字，该子句要求数据库服务器对插入或更新的每一行进行测试，以确保其符合视图的`WHERE`子句设置的条件。如果不符合条件，那么数据库服务器将拒绝该操作，并显示错误。

其中，当视图定义中包含`UNION`运算符时，不能包括`WITH CHECK OPTION`关键字。

例如：

	CREATE TABLE t1 (a INT);
	CREATE VIEW v1 AS SELECT * FROM t1 WHERE a < 2
	WITH CHECK OPTION;
	CREATE VIEW v2 AS SELECT * FROM v1 WHERE a > 0
	WITH LOCAL CHECK OPTION;
	CREATE VIEW v3 AS SELECT * FROM v1 WHERE a > 0
	WITH CASCADED CHECK OPTION;

在MySQL 5.7.6及以后，插入会报如下错：

	mysql> INSERT INTO v2 VALUES (2);
	ERROR 1369 (HY000): CHECK OPTION failed 'test.v2'
	mysql> INSERT INTO v3 VALUES (2);
	ERROR 1369 (HY000): CHECK OPTION failed 'test.v3'

视图中的算法类型：

1. MERGE，会将引用视图的语句的文本与视图定义合并起来，使得视图定义的某一部分取代语句的对应部分。

2. TEMPTABLE，视图的结果将被置于临时表中，然后使用它执行语句。


3. UNDEFINED，MySQL将选择所要使用的算法。如果可能，它倾向于MERGE而不是TEMPTABLE，这是因为MERGE通常更有效，而且如果使用了临时表，视图是不可更新的。

如果视图中包含`GROUP BY`、`DISTINCT`、`UNION`、聚合函数、子查询等，只要无法在原表记录和视图记录中建立一一映射的场景中，MySQL都使用临时表算法来实现视图。

例如：

	CREATE ALGORITHM = MERGE VIEW v_merge (vc1, vc2) AS
	SELECT c1, c2 FROM t WHERE c3 > 100;

通过`explain select * from <view> `如果返回的`select_type`为`DERIVED`，则表示是使用临时表算法的，否则`select_type`的值为`SIMPLE`。 

### 2. 存储程序（存储过程、存储函数、触发器、事件） ###

存储程序泛指各种类型的存储对象（存储函数、存储过程、触发器、事件）。存储例程(stored routine)特指存储函数和存储过程：

1. 存储函数(stored function)：返回一个计算结果，该结果可以用在表达式里；

2. 存储过程(stored procedure)：不直接返回一个结果，但可以用来完成一半的运算或是生成一个结果传递回客户；

3. 触发器(trigger)：与数据表相关联的存储过程，当那个数据表被`INSERT`、`DELETE`、`UPDATE`语句修改时，触发器将自动执行；

4. 事件(event)：根据时间表在预定时刻自动执行。它是由一个特定的线程（“事件调度器”）来管理。


存储程序中包含复合语句时，语句必须以分号(;)隔开，但分号也是MySQL默认的语句分割符，因此需要利用`delimiter`命令把MySQL程序的语句分隔符符重新定义为存储程序中未出现过的字符或字符串。

在定义完存储程序之后，需要将语句终止符重新定义为分号。

存储过程例子：

	mysql> delimiter //
	mysql> CREATE PROCEDURE dorepeat(p1 INT)
	    -> BEGIN
	    ->   SET @x = 0;
	    ->   REPEAT SET @x = @x + 1; UNTIL @x > p1 END REPEAT;
	    -> END
	    -> //
	Query OK, 0 rows affected (0.00 sec)
	mysql> delimiter ;
	mysql> CALL dorepeat(1000);
	Query OK, 0 rows affected (0.00 sec)
	mysql> SELECT @x;
	+------+
	| @x   |
	+------+
	| 1001 |
	+------+
	1 row in set (0.00 sec)


存储函数(不包含分号，所有不使用`delimiter`)的例子：

	mysql> CREATE FUNCTION hello (s CHAR(20))
	mysql> RETURNS CHAR(50) DETERMINISTIC
	    -> RETURN CONCAT('Hello, ',s,'!');
	Query OK, 0 rows affected (0.00 sec)
	
	mysql> SELECT hello('world');


存储过程的参数类型：

1. IN参数：调用者将一个值传递给过程，过程可以对这个值进行修改，但任何修改在过程返回后对调用者是不可见的。如果没有指定参数类型，默认是IN参数类型；

2. OUT参数：过程把一个值赋值给OUT参数，这个值在过程返回后可以用调用者访问。

3. INOUT参数：允许调用者向过程传递一个值，然后再取一个值。


触发器可以设置成在这几种语句处理每个数据行之前或之后触发，触发器的定义包括一条将在触发器被触发时执行的语句。

例如：

	mysql> CREATE TABLE account (acct_num INT, amount DECIMAL(10,2));
	Query OK, 0 rows affected (0.03 sec)
	
	mysql> CREATE TRIGGER ins_sum BEFORE INSERT ON account
	    -> FOR EACH ROW SET @sum = @sum + NEW.amount;
	Query OK, 0 rows affected (0.06 sec)

可以使用`Drop TRIGGER`命令删除触发器。


事件和触发器类似，都是在某些事情发生的时候启动。

创建事件：

	CREATE
	    [DEFINER = { user | CURRENT_USER }]
	    EVENT
	    [IF NOT EXISTS]
	    event_name
	    ON SCHEDULE schedule
	    [ON COMPLETION [NOT] PRESERVE]
	    [ENABLE | DISABLE | DISABLE ON SLAVE]
	    [COMMENT 'comment']
	    DO event_body;
	
	schedule:
	    AT timestamp [+ INTERVAL interval] ...
	     | EVERY interval
	    [STARTS timestamp [+ INTERVAL interval] ...]
	    [ENDS timestamp [+ INTERVAL interval] ...]
	interval:
	  quantity {YEAR | QUARTER | MONTH | DAY | HOUR | MINUTE |
	              WEEK | SECOND | YEAR_MONTH | DAY_HOUR |
	DAY_MINUTE |DAY_SECOND | HOUR_MINUTE |
	HOUR_SECOND | MINUTE_SECOND}

DEFINER: 定义事件执行的时候检查权限的用户。

ON SCHEDULE schedule: 定义执行的时间和时间间隔。

ON COMPLETION [NOT] PRESERVE: 定义事件是一次执行还是永久执行，默认为一次执行，即NOT PRESERVE。

ENABLE | DISABLE | DISABLE ON SLAVE: 定义事件创建以后是开启还是关闭，以及在从上关闭。如果是从服务器自动同步主上的创建事件的语句的话，会自动加上DISABLE ON SLAVE。

COMMENT 'comment': 定义事件的注释。


删除事件语法：`DROP EVENT [IF EXISTS] event_name;`

更改事件语法：

	ALTER
	    [DEFINER = { user | CURRENT_USER }]
	    EVENT event_name
	    [ON SCHEDULE schedule]
	    [ON COMPLETION [NOT] PRESERVE]
	    [RENAME TO new_event_name]
	    [ENABLE | DISABLE | DISABLE ON SLAVE]
	    [COMMENT 'comment']
	    [DO event_body]

查看事件是否开启：

	//方式一
	SHOW VARIABLES LIKE 'event_scheduler';
	//方式二
	SELECT @@event_scheduler;
	//方式三
	SHOW PROCESSLIST;
	
	//查看事件状态
	SHOW EVENTS;

开启事件功能：

	//方式一：动态参数修改
	SET GLOBAL event_scheduler = ON;
	//方式二：更改my.cnf配置文件中[mysqlId]部分增加：
	event_scheduler=ON;

例如：创建一个每隔10分钟后清空test表数据的事件：

	DROP EVENT IF EXISTS event_example;
	CREATE EVENT event_example
	ON SCHEDULE
	AT CURRENT_TIMESTAMP + INTERVAL 10 MINUTE
	DO TRUNCATE TABLE test;


### 3. 游标 ###

在使用存储程序时经常会用到游标，游标的作用就是用于对查询数据库所返回的记录进行遍历，游标有如下特点：

1. 游标是只读的，不能更新它；

2. 游标是不能滚动的，只能在一个方向上遍历，也不能再记录间跳过进退等；

3. 避免在已经打开游标的表上更新数据。

游标的使用：

声明游标：

	DECLARE cursor_name CURSOR FOR SELECT_statement;  

打开游标

	OPEN cursor_name; 

获取下一行数据：

	FETCH cursor_name INTO variable list;  

释放游标，释放游标使用的所有内部内存和资源：

	CLOSE cursor_name; 

例如（过程定义一个局部变量和游标， 该游标返回了用户表得所有用户名组成的集合）：

	create procedure simplecursor()
	begin
		declare done boolean default 0;
		declare temp int; --定义局部变量
	    declare cursorDemo cursor for select name from user;
	    -- 当出现02000错误时把局部变量的值设为true
	    declare continue handler for sqlstate '02000' set done 1;
	    open cursorDemo; 
	    REPEAT
	    	fetch cursorDemo into temp;
	    until done end REPEAT;
	    
	    close cursorDemo; 
	end;


### 4. 约束 ###

关系型数据库有三大完整性：

1. 实体完整性：实体属性中的标识属性不能为空，不能重复，该约束通过制定的主键实现，其约束有系统强制实施；

2. 参照完整性：实体中的外键可以为空，但不能是错的；

3. 用户定义完整性：某一具体的实际数据库的约束条件，由应用环境所决定，反映某一具体应用所涉及的数据必须满足的要求(例如定义某一行不能为空);

约束主要完成对数据的校验和限制，从而保证数据库的完整性。

约束包括：（1）主键约束；（2）外键约束；（3）唯一约束；（4）非空约束；（5）默认约束。

主键约束（PRIMARY KEY）：主键约束列不允许重复，即任意两行的主键值都不相同，每行都具有一个主键值，也不允许出现空值；

单列主键创建方式：

	//方式一：
	CREATE TABLE student(id INT PRIMARY KEY, name VARCHAR(2O));
	//方式二：
	CREATE TABLE student(id INT NOT NULL, name VARCHAR(20),
	CONSTRAINT PK_STUD_ID PRIMARY KEY(id));

联合主键：有时候一个列的字段可能有重复，可以联合多个列设为主键：

	CREATE TABLE student(name VARCHAR(20), calss VARCHAR(20),
	CONSTRAINT CONSTRAINT_NAME PRIMARY KEY(name, class));

其他操作：

	//删除主键约束  
	ALTER TABLE table_name DROP PRIMARY KEY;    
	//添加主键  
	ALTER TABLE table_name ADD PRIMARY KEY(列名);    
	//修改列为主键
	ALTER TABLE table_name MODIFY 列名 数据类型 PRIMARY KEY;

外键约束（FOREIGN KEY）：外键约束是保证一个或两个表之间的参照完整性，保持数据一致性。表的外键可以是另一个表的主键（也可以是索引）；外键可以有重复，可以是空值，实现一对一或一对多关系。

	CREATE TABLE classes(
	          id INT AUTO_INCREMENT PRIMARY KEY,
	          name VARCHAR(20) 
	          );  
	//第一种：添加关键字
	CREATE TABLE student(
	          id INT AUTO_INCREMENT,         
	          name VARCHAR(20),          
	          CONSTRAINT PK_ID PRIMARY KEY(id),                        
	          class_id INT REFERENCES classes(id) 
	          )
	//第二种：额外声明
	CREATE TABLE student(
	          id INT AUTO_INCREMENT,         
	          name VARCHAR(20),          
	          CONSTRAINT PK_ID PRIMARY KEY(id),                        
	          class_id INT,
	          CONSTRAINT fk_class_id FOREIGN KEY(classe_id) REFERENCES classes(id)
	          )

外键约束的要求：

1. 父表和子表必须使用相同的存储引擎，而且禁止使用临时表

2. 数据表的存储引擎只能为InnoDB,default-storage-engine-INNODB

3. 外键列和参照列必须具有相似的数据类型，数字的长度或是有符号位必须相同，而字符 的长度可以不同

4. 外键列和参照列必须创建索引，如果外键列不存在索引的话，MySQL将自动创建索引。

5. 设定参照列:FOREIGN KEY(id) PEFERENCES provinces(id)

外键约束的参照操作

1. CASCADE：从父表删除或更新且自动删除或更新子表中匹配的行

2. SET NULL：从父表删除或更新行，并设置子表中的外键列为NULL，如果使用该选项，必须保证子表列没有指定NOT NULL

3. RESTRICT：拒绝对父表的删除或更新操作

4. NO ACTION：标准SQL的关键字，在MySQL中与RESTRICT相同

其他操作：

	//删除外键约束
	 ALTER TABLE 表名 DROP FOREIGN KEY 外键约束名;
	(创建外键的方法没有指定约束名称，系统会默认给外键约束分配外键约束名称，命名为student_ibfk_n)
	
	//增加外键约束 
	 ALTER TABLE 表名 ADD FOREIGN KEY 列名 REFERENCES 父表(对应列名);

唯一约束（UNIQUE）：唯一约束是指定表中的某一列或多个列中不能有相同的两行或两行以上的数据存在。唯一约束可以保证记录的唯一性；唯一约束的字段可以为空值；每张数据表可以存在多个唯一约束。主要是用来防止数据插入的时候重复。

	CREATE TABLE student(name CHAR(20) UNIQUE KEY);

其他操作：

	ALTER TABLE student MODIFY CHAR(20) UNIQUE KEY;

非空约束（NOT NULL）：非空约束是指输入值必须是非空的。

	CREATE TABLE student(name CHAR(20) NOT NULL);

默认约束（DEFAULT）：默认约束中定义的常量必须与该列的数据类型、精度等匹配；每个列只能定义一个DEFAULT约束；DEFAULT约束会在使用INSERT语句。

	CREATE TABLE student
	(joinTime DATETIME DEFAULT CURRENT_TIMESTAMP);


### 5. 分区表 ###

分区表对用户来说是一个独立的逻辑表，但底层是由多个物理子表组成。

实现分区的代码实际上是对一组底层表的句柄的封装，对分区表的请求，都会通过句柄对象转化成存储引擎的接口调用。

分区表的限制因素：

1. 一个表最多只能有1024个分区；

2. MySQL5.1中，分区表达式必须是整数，或者返回整数的表达式。在MySQL5.5中提供了非整数表达式分区的支持；

3. 如果分区字段中有主键或唯一索引的列，那么所有主键列和唯一索引列都必须包含进来；

4. 分区表中无法使用外键约束。

分区类型包括：

1. RANGE分区：按照数据的区间范围分区，区间要连续且不能相互重叠；

2. LIST分区：按照List中的值分区。是建立离散的值列表告诉数据库特定的值属于哪个分区；

3. HASH分区：按照HASH值来分区。MySQL支持两种HASH分区：（1）常规HASH分区,使用取模算法；（2）线性HASH分区,分区函数是一个线性的2的幂的运算规则。

4. KEY分区：在MySQL5.1版本中，RANGE,LIST,HASH分区要求分区键必须是INT类型，或者通过表达式返回INT类型。但KEY分区的时候，可以使用其他类型的列（BLOB，TEXT类型除外）作为分区键。

5. COLUMNS分区：MySQL5.5中支持。支持所有的整数类型，日期类型，字符串类型。

简单例子如：

	//RANGE分区
	CREATE TABLE student(id INT NOT NULL, store_id iNT NOT NULL)
	PARTITION BY RANGE(store_id)(
		PARTITION p0 VALUES LESS THAN(10), 
		PARTITION p1 VALUES LESS THAN(20)  /*大于等于10，小于20*/
	);
	//LIST分区
	CREATE TABLE student(id INT NOT NULL, store_id iNT NOT NULL)
	PARTITION BY LIST(store_id)(
		PARTITION p0 VALUES in (3, 5), 
		PARTITION p1 VALUES in (2, 8, 9)  
	);
	//HASH分区
	CREATE TABLE student(id INT NOT NULL, store_id iNT NOT NULL)
	PARTITION BY HASH(store_id)(
		PARTITION 4  //根据store_id对4取模
	);
	CREATE TABLE student(id INT NOT NULL, store_id iNT NOT NULL)
	PARTITION BY LINER HASH(store_id)(
		PARTITION 4 
	);
	//KEY分区
	CREATE TABLE student(id INT NOT NULL, store_id iNT NOT NULL)
	PARTITION BY LINER KEY(store_id)(
		PARTITION 4  
	);
	//COLUMNS分区
	CREATE TABLE student(id INT NOT NULL, store_time DATETIME)
	PARTITION BY RANGE|LIST COLUMN(store_time)(
		PARTITION p0 VALUES LESS THAN('2012-01-01'), 
		PARTITION p2 VALUES LESS THAN('2016-01-01')
	);

分区的优点：

1. 分区可以分在多个磁盘，存储更大一些；

2. 根据查找条件，只用查找对应的分区，不用全部查找；

3. 进行大数据搜索时可以进行并行处理。


剩余的（1）事务和锁；（2）索引；（3）复制。再另外小结。

参考：[MySQL 5.7 Reference Manual](http://dev.mysql.com/doc/refman/5.7/en/)

[高性能MySQL]()



