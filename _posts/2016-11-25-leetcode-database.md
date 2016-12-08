---
date: 2016-11-25 18:41:30+00:00
layout: post
title: Leetcode中数据库题目小结
thread: 166
categories: database 
tags: database 

---

这篇小结下Leetcode中现有的数据库题目：

1. [Duplicate Emails](https://leetcode.com/problems/duplicate-emails/)

2. [Employees Earning More Than Their Managers](https://leetcode.com/problems/employees-earning-more-than-their-managers/)  

3. [Combine Two Tables](https://leetcode.com/problems/combine-two-tables/)

4. [Customers Who Never Order](https://leetcode.com/problems/customers-who-never-order/)

5. [Rising Temperature](https://leetcode.com/problems/rising-temperature/)

6. [Second Highest Salary](https://leetcode.com/problems/second-highest-salary/)

7. [Delete Duplicate Emails](https://leetcode.com/problems/delete-duplicate-emails/)

8. [Consecutive Numbers](https://leetcode.com/problems/consecutive-numbers/)

9. [Rank Scores](https://leetcode.com/problems/rank-scores/)

10. [Department Highest Salary](https://leetcode.com/problems/department-highest-salary/)

11. [Nth Highest Salary](https://leetcode.com/problems/nth-highest-salary/)

12. [Trips and Users](https://leetcode.com/problems/trips-and-users/)

13. [Department Top Three Salaries](https://leetcode.com/problems/department-top-three-salaries/)

### 1. Duplicate Emails ###

Write a SQL query to find all duplicate emails in a table named Person.

	+----+---------+
	| Id | Email   |
	+----+---------+
	| 1  | a@b.com |
	| 2  | c@d.com |
	| 3  | a@b.com |
	+----+---------+

For example, your query should return the following for the above table:

	+---------+
	| Email   |
	+---------+
	| a@b.com |
	+---------+

列出常用语句：

	select Email from Person group by Email having count(*) > 1;
	或
	select distinct a.Email from Person a join Person b 
		on (a.Email = b.Email) where a.Id <> b.Id;


### 2. Employees Earning More Than Their Managers ###

The Employee table holds all employees including their managers. Every employee has an Id, and there is also a column for the manager Id.

	+----+-------+--------+-----------+
	| Id | Name  | Salary | ManagerId |
	+----+-------+--------+-----------+
	| 1  | Joe   | 70000  | 3         |
	| 2  | Henry | 80000  | 4         |
	| 3  | Sam   | 60000  | NULL      |
	| 4  | Max   | 90000  | NULL      |
	+----+-------+--------+-----------+

Given the Employee table, write a SQL query that finds out employees who earn more than their managers. For the above table, Joe is the only employee who earns more than his manager.

	+----------+
	| Employee |
	+----------+
	| Joe      |
	+----------+

查询语句如下：

	select a.name as Employee from Employee a join Employee b 
		on a.ManagerId = b.Id where a.Salary>b.Salary;

### 3. Combine Two Tables ###

Table: Person

	+-------------+---------+
	| Column Name | Type    |
	+-------------+---------+
	| PersonId    | int     |
	| FirstName   | varchar |
	| LastName    | varchar |
	+-------------+---------+

PersonId is the primary key column for this table.
Table: Address

	+-------------+---------+
	| Column Name | Type    |
	+-------------+---------+
	| AddressId   | int     |
	| PersonId    | int     |
	| City        | varchar |
	| State       | varchar |
	+-------------+---------+

AddressId is the primary key column for this table.

Write a SQL query for a report that provides the following information for each person in the Person table, regardless if there is an address for each of those people:

	FirstName, LastName, City, State

查询语句如下：

	select FirstName, LastName, City, State from Person p 
		left join Address a on p.PersonId = a.PersonId;


### 4. Customers Who Never Order ###

Suppose that a website contains two tables, the Customers table and the Orders table. Write a SQL query to find all customers who never order anything.

Table: Customers.

	+----+-------+
	| Id | Name  |
	+----+-------+
	| 1  | Joe   |
	| 2  | Henry |
	| 3  | Sam   |
	| 4  | Max   |
	+----+-------+

Table: Orders.

	+----+------------+
	| Id | CustomerId |
	+----+------------+
	| 1  | 3          |
	| 2  | 1          |
	+----+------------+

Using the above tables as example, return the following:

	+-----------+
	| Customers |
	+-----------+
	| Henry     |
	| Max       |
	+-----------+

列出两种查询语句：

	select Name as Customers from Customers where Id not in
		(select distinct(CustomerId) from Orders);
	或
	select c.Name as Customers from Customers c left join
		Orders o on c.Id = o.CustomerId where o.Id is NULL;

### 5. Rising Temperature ###

Given a Weather table, write a SQL query to find all dates'Ids with higher temperature compared to its previous (yesterday's) dates.

	+---------+------------+------------------+
	| Id(INT) | Date(DATE) | Temperature(INT) |
	+---------+------------+------------------+
	|       1 | 2015-01-01 |               10 |
	|       2 | 2015-01-02 |               25 |
	|       3 | 2015-01-03 |               20 |
	|       4 | 2015-01-04 |               30 |
	+---------+------------+------------------+

For example, return the following Ids for the above Weather table:

	+----+
	| Id |
	+----+
	|  2 |
	|  4 |
	+----+

查询语句如下：

	select w1.Id from Weather as w1 inner join Weather as w2
		on TO_DAYS(w1.Date) = TO_DAYS(w2.Date)+1 and w1.Temperature>w2.Temperature;

### 6. Second Highest Salary ###

Write a SQL query to get the second highest salary from the Employee table.

	+----+--------+
	| Id | Salary |
	+----+--------+
	| 1  | 100    |
	| 2  | 200    |
	| 3  | 300    |
	+----+--------+

For example, given the above Employee table, the second highest salary is 200. If there is no second highest salary, then the query should return null.

查询语句如下：

	select max(Salary) from Employee where Salary < (select max(Salary) from Employee);

### 7. Delete Duplicate Emails ###

Write a SQL query to delete all duplicate email entries in a table named Person, keeping only unique emails based on its smallest Id.

	+----+------------------+
	| Id | Email            |
	+----+------------------+
	| 1  | john@example.com |
	| 2  | bob@example.com  |
	| 3  | john@example.com |
	+----+------------------+

Id is the primary key column for this table.
For example, after running your query, the above Person table should have the following rows:

	+----+------------------+
	| Id | Email            |
	+----+------------------+
	| 1  | john@example.com |
	| 2  | bob@example.com  |
	+----+------------------+

列出两种语句：

	delete p1 from Person p1, Person p2 where p1.Email = p2.Email and p1.Id > p2.Id;
	或
	delete p from Person as p where p.Id not in (select Id from 
		(select min(Person.Id) as Id from Person group by Person.Email) as NeedRemovedId);


### 8. Consecutive Numbers ###

Write a SQL query to find all numbers that appear at least three times consecutively.

	+----+-----+
	| Id | Num |
	+----+-----+
	| 1  |  1  |
	| 2  |  1  |
	| 3  |  1  |
	| 4  |  2  |
	| 5  |  1  |
	| 6  |  2  |
	| 7  |  2  |
	+----+-----+

For example, given the above Logs table, 1 is the only number that appears consecutively for at least three times.

列出三种查询语句：

	select distinct l1.Num from Logs l1, Logs l2, Logs l3
		where l1.Id = l2.Id -1 and l2.Id = l3.Id -1
		and l1.Num = l2.Num and l2.Num = l3.Num;
	或
	select distinct l1.Num from Logs l1 
		join Logs l2 on l1.Id = l2.Id - 1
		join Logs l3 on l1.Id = l3.Id - 2
		where l1.Num = l2.Num and l2.Num = l3.Num;
	或
	select distinct Num from (
	select Num, @count := IF(@pre = Num, @count+1, 1) as n, @pre :=Num
	from Logs, (select @count :=0, @pre := -1) as init
	) as t where t.n >= 3;


### 9. Rank Scores ###

Write a SQL query to rank scores. If there is a tie between two scores, both should have the same ranking. Note that after a tie, the next ranking number should be the next consecutive integer value. In other words, there should be no "holes" between ranks.

	+----+-------+
	| Id | Score |
	+----+-------+
	| 1  | 3.50  |
	| 2  | 3.65  |
	| 3  | 4.00  |
	| 4  | 3.85  |
	| 5  | 4.00  |
	| 6  | 3.65  |
	+----+-------+

For example, given the above Scores table, your query should generate the following report (order by highest score):

	+-------+------+
	| Score | Rank |
	+-------+------+
	| 4.00  | 1    |
	| 4.00  | 1    |
	| 3.85  | 2    |
	| 3.65  | 3    |
	| 3.65  | 3    |
	| 3.50  | 4    |
	+-------+------+

列出四种查询语句：

	select Score, (select COUNT(distinct Score) from Scores where Score>=s.Score) Rank
	from Scores s order by Score DESC;
	或
	select Score, (select COUNT(*) from (select distinct Score s from Scores) t where s>=Score) Rank
	from Scores order by Score DESC;
	或
	select s.Score, COUNT(distinct t.Score) Rank
	from Scores s join Scores t on s.Score <= t.Score
	group by s.Id order by s.Score DESC;
	或
	select Score, @rank := @rank +(@pre <> (@pre := Score)) Rank
	from Scores, (select @rank := 0, @pre := -1) init 
	order by Score DESC;

### 10. Department Highest Salary ###

The Employee table holds all employees. Every employee has an Id, a salary, and there is also a column for the department Id.

	+----+-------+--------+--------------+
	| Id | Name  | Salary | DepartmentId |
	+----+-------+--------+--------------+
	| 1  | Joe   | 70000  | 1            |
	| 2  | Henry | 80000  | 2            |
	| 3  | Sam   | 60000  | 2            |
	| 4  | Max   | 90000  | 1            |
	+----+-------+--------+--------------+

The Department table holds all departments of the company.

	+----+----------+
	| Id | Name     |
	+----+----------+
	| 1  | IT       |
	| 2  | Sales    |
	+----+----------+

Write a SQL query to find employees who have the highest salary in each of the departments. For the above tables, Max has the highest salary in the IT department and Henry has the highest salary in the Sales department.

	+------------+----------+--------+
	| Department | Employee | Salary |
	+------------+----------+--------+
	| IT         | Max      | 90000  |
	| Sales      | Henry    | 80000  |
	+------------+----------+--------+

列出三种查询语句：

	select d.Name as Department, e.Name as Employee, e.Salary from Employee e, Department d
	where e.DepartmentId = d.Id and e.Salary = (select MAX(Salary) from Employee e2 where
	e2.DepartmentId = d.Id);
	或
	select d.Name as Department, e1.Name as Employee, e1.Salary from Employee e1
	join Department d on e1.DepartmentId = d.Id where Salary in
	(select MAX(Salary) from Employee e2 where e1.DepartmentId = e2.DepartmentId);
	或
	select d.Name as Department, e.Name as Employee, e.Salary from Employee e, Department d
	where e.DepartmentId=d.Id and e.Salary >= ALL (select Salary from Employee e2 where
	e2.DepartmentId = d.Id);

### 11. Nth Highest Salary ###

Write a SQL query to get the nth highest salary from the Employee table.

	+----+--------+
	| Id | Salary |
	+----+--------+
	| 1  | 100    |
	| 2  | 200    |
	| 3  | 300    |
	+----+--------+

For example, given the above Employee table, the nth highest salary where n = 2 is 200. If there is no nth highest salary, then the query should return null.

	select MAX(Salary) from Employee e1 where N-1 = 
	(select COUNT(distinct(e2.Salary)) from Employee e2 where e2.Salary > e1.Salary);
	或
	select distinct Salary from Employee group by Salary 
	order by Salary DESC limit 1 offset N;


### 12. Trips and Users ###

The Trips table holds all taxi trips. Each trip has a unique Id, while Client_Id and Driver_Id are both foreign keys to the Users_Id at the Users table. Status is an ENUM type of (‘completed’, ‘cancelled_by_driver’, ‘cancelled_by_client’).

	+----+-----------+-----------+---------+--------------------+----------+
	| Id | Client_Id | Driver_Id | City_Id |        Status      |Request_at|
	+----+-----------+-----------+---------+--------------------+----------+
	| 1  |     1     |    10     |    1    |     completed      |2013-10-01|
	| 2  |     2     |    11     |    1    | cancelled_by_driver|2013-10-01|
	| 3  |     3     |    12     |    6    |     completed      |2013-10-01|
	| 4  |     4     |    13     |    6    | cancelled_by_client|2013-10-01|
	| 5  |     1     |    10     |    1    |     completed      |2013-10-02|
	| 6  |     2     |    11     |    6    |     completed      |2013-10-02|
	| 7  |     3     |    12     |    6    |     completed      |2013-10-02|
	| 8  |     2     |    12     |    12   |     completed      |2013-10-03|
	| 9  |     3     |    10     |    12   |     completed      |2013-10-03| 
	| 10 |     4     |    13     |    12   | cancelled_by_driver|2013-10-03|
	+----+-----------+-----------+---------+--------------------+----------+

The Users table holds all users. Each user has an unique Users_Id, and Role is an ENUM type of (‘client’, ‘driver’, ‘partner’).

	+----------+--------+--------+
	| Users_Id | Banned |  Role  |
	+----------+--------+--------+
	|    1     |   No   | client |
	|    2     |   Yes  | client |
	|    3     |   No   | client |
	|    4     |   No   | client |
	|    10    |   No   | driver |
	|    11    |   No   | driver |
	|    12    |   No   | driver |
	|    13    |   No   | driver |
	+----------+--------+--------+

Write a SQL query to find the cancellation rate of requests made by unbanned clients between Oct 1, 2013 and Oct 3, 2013. For the above tables, your SQL query should return the following rows with the cancellation rate being rounded to two decimal places.

	+------------+-------------------+
	|     Day    | Cancellation Rate |
	+------------+-------------------+
	| 2013-10-01 |       0.33        |
	| 2013-10-02 |       0.00        |
	| 2013-10-03 |       0.50        |
	+------------+-------------------+

列出两种查询语句：

	select Request_at Day, ROUND(COUNT(IF(Status != 'completed', TRUE, NULL))/COUNT(*), 2) 'Cancellation Rate'
	from Trips where (Request_at between '2013-10-01' and '2013-10-03') and Client_Id in
	(select Users_Id from Users where Banned = 'No') group by Request_at;
	或
	select t.Request_at Day, ROUND(SUM(CASE WHEN t.Status LIKE 'cancelled%' THEN 1 ELSE 0 END)/COUNT(*), 2) 'Cancellation Rate'
	from Trips t join Users u on t.Client_Id = u.Users_Id and u.Banned = 'No' where
	t.Request_at between '2013-10-01' and '2013-10-03' group by t.Request_at;


### 13. Department Top Three Salaries ###

The Employee table holds all employees. Every employee has an Id, and there is also a column for the department Id.

	+----+-------+--------+--------------+
	| Id | Name  | Salary | DepartmentId |
	+----+-------+--------+--------------+
	| 1  | Joe   | 70000  | 1            |
	| 2  | Henry | 80000  | 2            |
	| 3  | Sam   | 60000  | 2            |
	| 4  | Max   | 90000  | 1            |
	| 5  | Janet | 69000  | 1            |
	| 6  | Randy | 85000  | 1            |
	+----+-------+--------+--------------+

The Department table holds all departments of the company.

	+----+----------+
	| Id | Name     |
	+----+----------+
	| 1  | IT       |
	| 2  | Sales    |
	+----+----------+

Write a SQL query to find employees who earn the top three salaries in each of the department. For the above tables, your SQL query should return the following rows.

	+------------+----------+--------+
	| Department | Employee | Salary |
	+------------+----------+--------+
	| IT         | Max      | 90000  |
	| IT         | Randy    | 85000  |
	| IT         | Joe      | 70000  |
	| Sales      | Henry    | 80000  |
	| Sales      | Sam      | 60000  |
	+------------+----------+--------+


列出三种查询语句：

	select d.Name as Department, e.Name as Employee, e.Salary from Employee e 
	join Department d on e.DepartmentId = d.Id where (select COUNT(distinct Salary) from
	Employee where Salary>e.Salary and DepartmentId=d.Id)<3 order by d.Name, e.Salary DESC;
	或
	select d.Name as Department, e.Name as Employee, e.Salary from Employee e, Department d
	where (select COUNT(distinct Salary) from Employee where Salary > e.Salary and
	DepartmentId = d.Id) in (0, 1, 2) and e.DepartmentId=d.Id order by d.Name, e.Salary DESC;
	或
	select d.Name as Department, e.Name as Employee, e.Salary from
	(select e1.Name, e1.Salary, e1.DepartmentId from Employee e1 join Employee e2
	on e1.DepartmentId=e2.DepartmentId and e1.Salary<=e2.Salary group by e1.Id
	having COUNT(distinct e2.Salary)<=3) e join Department d on e.DepartmentId=d.Id
	order by d.Name, e.Salary DESC;