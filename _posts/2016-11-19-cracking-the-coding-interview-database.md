---
date: 2016-11-19 12:16:30+00:00
layout: post
title: 《Cracking the coding interview》中数据库小结
thread: 165
categories: database 
tags: database 

---

这篇小结下《Cracking the coding interview》中的数据库题目。


1. Write a method to find the number of employees in each department.

2. What are the different types of joins? Please explain how they differ and why certain types are better in certain situations.

3. What is denormalization? Explain the pros and cons.

4. Draw an entity-relationship diagram for a database with companies, people, and professionals (people who work for companies).

5. Imagine a simple database storing information for students’ grades. Design what this database might look like, and provide a SQL query to return a list of the honor roll students (top 10%), sorted by their grade point average.


### 1. 写一条SQL语句找到每一个部门中员工的数量 ###

Write a method to find the number of employees in each department.

	select Dept_Name, Departments.Dept_ID, count(*) as 'num_employees'
	from Departments
	left join Employees
	on Employees.Dept_ID = Departments.Dept_ID
	group by Departments.Dept_ID, Dept_Name


### 2. SQL的连接有哪些不同的类型？解释它们的不同点及在什么情况下用哪种连接 ###

What are the different types of joins? Please explain how they differ and why certain types are better in certain situations.


连接(JOIN)将数据库中的两个或多个表组合起来。为了使用连接，每个表至少要包含一个相同的字段(属性)。不同的连接类型决定了哪些记录会出现在结果集。SQL的连接(JOIN)可以分为：

1. 内连接（inner join）：默认的连接类型，找出满足连接谓词的组合，产生的结果集中，是表A和表B的交集。内部连接的各条件表达式既可以放在ON子句又可以放在WHERE子句中。

	（1）相等连接（equip join）：是比较连接的一种特例，它的连接谓词只用相等比较。USING结构不仅仅是语法糖，连接结果中只产生一个DepartmentID的列（无表名前缀）

	（2）自然连接（natural join）：自然连接比相等连接的进一步特例化，两表中的所有名称相同的列都会比较（隐式的），两表中名称相同的列只出现一次。

	（3）交叉连接（cross join）：交叉连接时所有内连接的基础，交叉连接返回两个集合的笛卡尔积。

内连接简单例子：

	内连接例子：
	SELECT *FROM   employee 
	  INNER JOIN department 
	     ON employee.DepartmentID = department.DepartmentID;

	相等连接：
	SELECT *FROM   employee 
       INNER JOIN department USING (DepartmentID);

	自然连接：
	SELECT *
	FROM   employee NATURAL JOIN department;

	显式的交叉连接：
	SELECT *
	FROM   employee CROSS JOIN department;

	隐式的交叉连接：
	SELECT *
	FROM   employee ,department;


.
2. 外连接（outer join）：外连接没有隐式的连接符号。返回满足谓词的两个表的并集。外部连接既包含ON子句又包含WHERE子句时，应当只把表之间的连接条件写在ON子句中，对表中数据的筛选必须写在WHERE子句中。（这是因为对于外部连接，保留表中被ON子句筛除掉的行要被添加回来，在此操作之后才会用WHERE子句去筛选连接结果中的各行。）

	（1）左外连接（left outer join）：左外连接会返回左表的所有记录和右表中匹配记录的组合(如果右表中无匹配记录, 来自于右表的所有列的值设为 NULL). 如果左表的一行在右表中存在多个匹配行, 那么左表的行会复制和右表匹配行一样的数量, 并进行组合生成连接结果.

	（2）右外连接（right outer join）：右连接操作返回右表的所有行和这些行在左表中匹配的行(没有匹配的, 来源于左表的列值设为 NULL)。右连接很少使用（可以通过换表为位置代替）。

	（3）全连接（full outer join）： 全连接是左右外连接的并集. 连接表包含被连接的表的所有记录, 如果缺少匹配的记录, 即以 NULL 填充。

外连接简单例子：

	左外连接：
	SELECT *  FROM   employee  LEFT OUTER JOIN department  
          ON employee.DepartmentID = department.DepartmentID;
	
	右外连接：
	SELECT * FROM   employee RIGHT OUTER JOIN department 
          ON employee.DepartmentID = department.DepartmentID;

	全连接：
	SELECT *  FROM   employee 
		FULL OUTER JOIN department 
          ON employee.DepartmentID = department.DepartmentID;

	一些数据库系统(如 MySQL)并不直接支持全连接, 但它们可以通过左右外连接的并集(参: union)来模拟实现：
	SELECT *FROM   employee 
       LEFT JOIN department 
          ON employee.DepartmentID = department.DepartmentID
	UNION
	SELECT *FROM   employee
       RIGHT JOIN department
          ON employee.DepartmentID = department.DepartmentID
	WHERE  employee.DepartmentID IS NULL;

	外连接查询得到的结果也可以通过关联子查询得到，例如：
	SELECT employee.LastName, employee.DepartmentID, department.DepartmentName 
		FROM   employee LEFT OUTER JOIN department 
          ON employee.DepartmentID = department.DepartmentID;
	等价于：
	SELECT employee.LastName, employee.DepartmentID,
  		(SELECT department.DepartmentName FROM department
   		WHERE employee.DepartmentID = department.DepartmentID )
	FROM   employee;
	

.
3. 自连接（self join）:自连接就是和自身连接。

自连接简单例子：

	SELECT F.EmployeeID, F.LastName, S.EmployeeID, S.LastName, F.Country
	FROM Employee F, Employee S
	WHERE F.Country = S.Country
	AND F.EmployeeID < S.EmployeeID
	ORDER BY F.EmployeeID, S.EmployeeID;


另外，连接的算法有：

1. 嵌套循环（Loop Join）：类似于C语言编程时的双重循环。

2. 合并连接（Merge Join）:类似于两个有序数组的合并。两个输入表都在合并列上排序；然后依序对两张表逐行做连接或舍弃。如果预先建好了索引，合并连接的计算复杂度是线性的。

3. 哈希连接（Hash Join）：适用于查询的中间结果，通常是无索引的临时表；以及中间结果的行数很大时。哈希连接选择行数较小的输入表作为生成输入，对其连接列值应用哈希函数，把其行（的存储位置）放入哈希桶中。


### 3. 什么是反范式？它优缺点是什么？ ###

What is denormalization? Explain the pros and cons.

先小结下数据库三大范式：

1. 第一范式（1NF）：无重复的列。数据库的所有字段值都是不可分解的原子值（每个列的值域都是有原子值组成）。只要在RDBMS中已经存在的数据表，一定是符合1NF的。

2. 第二范式（2NF）：属性完全依赖于主键（消除部分子函数依赖）。满足第二范式（2NF）必须先满足第一范式（1NF）。

3. 第三范式（3NF）：属性不依赖于其他非主属性（消除传递依赖）。满足第三范式（3NF）必须先满足第二范式（2NF）

范式化模型的优点是：优点是范式可以避免数据冗余，减少数据库的空间，减轻维护数据完整性的麻烦。

范式化模型的缺点是：按照范式的规范设计出来的表，等级越高的范式设计出来的表越多。当表的数量比较多，查询设计需要很多关联模型（join）时，会导致查询性能低下。

反范式是通过增加冗余数据或数据分组来提高数据库读性能的过程。本质上就是用空间来换取时间，把数据冗余在多个表中，当查询时可以减少或者是避免表之间的关联。

范式的应用是这样的变化的：

第三范式数据库的设计—–>当数据量越来越大，达到百万级时，经常要对一些多表数据进行大范围高频率进行操作——->范式数据库的设计———->网站的数据量再持续增长———->范式和反范式的数据库设计


### 4. 画出一个数据库的实体关系图(ER图)，其中的实体有公司(companies)，人(people)， 专业人士(professionals)。 ###

Draw an entity-relationship diagram for a database with companies, people, and professionals (people who work for companies).

 professionals和people间是ISA(is a)的关系，除了people的属性，每个professional还有自己额外的属性，如：级别，工作经验等。

一个professional只能去一家公司上班(一般情况下是这样)， 而一家公司可以雇佣很多的professional。因此，它们之间是多对一的关系。 “工作(work for)”关系可以有如下属性：加入公司的时间，工资等。 为什么这两个属性是关系的属性而不是professional的属性呢？ 因为只有当我们将professional和companies联系起来，才会有这些属性， 或是说这些属性才有意义。

ER图如下：

![](/assets/blog_pic/database-ER.png)


### 5. 有一个简单的数据库，存储学生的成绩信息。尝试设计这个数据库，它会是怎样的？ 提供一个SQL查询语句来返回光荣榜学生信息(前10%)，按照他们的GPA排序。 ###

Imagine a simple database storing information for students’ grades. Design what this database might look like, and provide a SQL query to return a list of the honor roll students (top 10%), sorted by their grade point average.

	SELECT StudentName, GPA
	FROM (
		SELECT 	top 10 percent Avg(CourseEnrollment.Grade) AS GPA,
		CourseEnrollment.StudentID
		FROM CourseEnrollment
		GROUP BY CourseEnrollment.StudentID
		ORDER BY Avg(CourseEnrollment.Grade)) Honors
	INNER JOIN Students ON Honors.StudentID = Students.StudentID



参考：[连接 (SQL)](https://zh.wikipedia.org/wiki/%E8%BF%9E%E6%8E%A5_(SQL))


