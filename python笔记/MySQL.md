# 数据库mysql

## 1.1 数据库

### 1. 概念

1. 用户认证

   - 注册：用户名不能重复
   - 登陆

2. 只是通过文件操作，改变数据是非常繁琐的

3. 解决对于**多台机器**或**多个进程**操作同一份数据我们需要自己**解决并发**和**安全问题**比较麻烦

4. 自己处理数据备份，容错措施

5. c/s架构的操作数据文件的一个**管理软件**

   - 解决并发问题
   - 实现用更简单快速的方式完成数据的增删改查
   - 提供一些容错、高可用的机制
   - 权限的认证

6. 数据操作

   1. 连接server
   2. 指令

7. 专有名词

   1. 数据库管理系统(DBMS)：专门用来管理数据文件，帮助用户更简洁的操作数据的软件
   2. 数据(data)、文件
   3. 数据库(database, DB)：每一个项目都有一个数据库
   4. 数据库管理员(DBA)

8. 常见的数据库

   - 关系型数据库

     - Relational Database Management System：(RDBMS)是指包括**相互联系的逻辑组织**和**存取这些数据的一套程序** (数据库管理系统软件)。关系数据库管理系统就是管理关系数据库，并将数据逻辑组织的系统。

     1. sql server/ sqlite/ db2/ access/ 
     2. oracle：收费，比较严谨，安全性高（国企、事业单位银行、金融行业）
     3. mysql：开源（小公司互联网公司）
     4. 注意：sql语句通用

   - 非关系型数据库(key:value结构)eg：快递单号（redis、mongodb、memcache）

   - 在 WEB 应用方面，MySQL是最好的 **RDBMS**(关系数据库管理系统) 应用软件。

### 2. mysql的安装

1. win，路径必须是**全英文**
2. bin目录
3. **my.ini文件**（文件名必须是这个）

```python
# 客户端
[mysql]
# 设置mysql客户端默认字符集
default-character-set=utf8 

# server端
[mysqld]
#设置3306端口
port = 3306
# 设置mysql的安装目录
basedir=C:\Program Files\mysql-5.6.39-winx64 
# 设置mysql数据库的数据的存放目录
datadir=C:\Program Files\mysql-5.6.39-winx64\data 
# 允许最大连接数
max_connections=200
# 服务端使用的字符集默认为8比特编码的latin1字符集
character-set-server=utf8mb4
# 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB
```

1. 安装路径：不能有空格，不能有中文，**不能带着转义特殊字符开头的文件夹名**
2. 安装之后发现配置有问题：再修改配置文件往往不能生效
   - 卸载之后重装
   - mysqld remove，把所有配置、PATH修改正确
   - 重启计算机—清空注册表
   - 重新安装：mysqld install

### 3. mysql的cs架构

```mysql
# windows
mysqld install
net start mysql
#  server net stop mysql
mysql -u'用户名' -p'密码'
# 客户端，可以是python代码也可以是一个程序
# mysql.exe是一个客户端
```

```mysql
# mac
sudo mysql.server status
sudo mysql.server start/stop/restart
```

#### 3.1 mysql中的用户和权限

- 在安装数据库之后，有一个最高权限的用户root
- mysql server端的ip 用户名/密码
- mysql -h192.168.12.87 -uroot -p123

#### Note1

1. 可以连接网络上的某一个数据库

#### 3.2 数据库中的概念

- 库、表、数据
  - **描述事物的符号记录称为数据**，如：一条数据data(一行数据)
  - **表就相当于文件，表中的一条记录就相当于文件的一行内容**，多条数据组成一个表
  - **数据库即存放数据的仓库**，多个表组成一个库
  - 一般情况下：一个项目占用一个或以上个库

#### 3.3 mysql的操作

- sql语句(structure query language)

  - SQL : 结构化查询语言(**Structured Query Language)**简称SQL(发音：/ˈes kjuː ˈel/ "S-Q-L")，是一种特殊目的的编程语言，是一种数据库查询和程序设计语言，用于存取数据以及查询、更新和管理关系数据库系统。
  - SQL语言主要用于存取数据、查询数据、更新数据和管理关系数据库系统，SQL语言由IBM开发。**SQL语言分为3种类型**：

  1. **DDL**语句 数据库定义语言：数据库，表，视图，索引，存储过s s程
  2. **DML**语句 数据库操纵语言：插入数据insert，delete，update，alter
  3. **DCL**语句 数据库控制语言：创建用户。grant    revoke 取消授权

```mysql
# 查看当前用户
select user(); 
# 设置密码，password 表示密文存储
set password for root@localhost = password('123');
# 创建用户
create user 用户名@'网段.%' identified by '密码';
# 查看用户状态，用户信息都存储在mysql中的user表中
select host,user from mysql.user;
# 查看当前库
show databases;
# 创建文件夹henry
create database henry；
# 查看指定用户权限
show grants for 用户名(@'网段.%');
show grants for 用户名;
# 授权 * 表示所有
grant all(select/insert) on henry.* to 用户名@'ip网段.%';
# 设置立即生效
flush privileges
# 创建账号并授权,必须有密码
grant all on 库名.* to 用户名@'%' identified by  '123';
#select, insert, update, delete, create, drop, index, alter, grant, references, reload, shutdown, process, file等14个权限

# 取消用户权限
revoke all on test.* from henry@'%';
# 删除用户
delete from mysql.user where host='192.168.12.%' and user='test';
drop user test@'192.168.12
# 修改指定用户密码
update mysql.user set password=pssword('新密码') where User='test' and Host='%';
```

- 库的操作

```mysql
# 创建库
create database demo;
# 查看库
show databases;
# 删除库，demo
drop database demo
# 查看当前使用的库
select database();
# 切换库，到demo库下
use demo；
```

- **表操作(4)**

```mysql
# 创建表,char()默认一个字符
create table student(id int, name char(10));
# 查看当前文件夹中的表
show tables;
# 删除表
drop table student;
# 查看表结构
desc student;
# 删除多个表
drop tables s2,s3,s4;
```

- **操作表中数据(4)**

```mysql
# 数据插入
insert into student values(1, 'henry');
# 数据查看
select * from student;
# 修改数据，必须设置条件，确定为一条数据data
update 表 set 字段名 =值 where id=2;
# 删除数据
delete from 表 where id=1；
```

## 1.2 表的介绍

### 1. 存储引擎

- 选择**如何存储和检索**数据的这种**灵活性**是MySQL为什么如此受欢迎的主要原因。其它数据库系统(包括大多数商业选择)仅支持一种类型的数据存储。
- mysql5.6/5.7支持的存储引擎包括**InnoDB**、 **MyISAM**、 **MEMORY**、 **CSV**、 **BLACKHOLE**、 **FEDERATED**、 **MRG_MYISAM**、 **ARCHIVE**、 **PERFORMANCE_SCHEMA**。其中**NDB**和**InnoDB**提供**事务安全表**，其他存储引擎都是非事务安全表。

#### 1.1 表的存储方式(3)

1. 方式1：**MyISAM**
   1. mysql5.5- 默认存储方式
   2. 存储的文件个数：**表结构**、**表数据**、**索引**
   3. **不支持**行级锁、事务和外键
2. 方式2：**InnoDB** 
   1. mysql5.6+ 默认存储方式
   2. 存储文件个数：**表结构**、**表数据**
   3. 支持**事务**：把多句操作，变成原子操作
   4. 支持**外键**：通过外键(**有约束**)在其他表(**有约束**)中查找信息
   5. 支持**行级锁**(默认)：脏数据（+表级锁），支持数据并发
3. 方式3：**MEMORY**
   1. 存储在内存：**表结构**存储到硬盘中， 表数据存储到内存上
   2. **优势**：增删改查速度快
   3. **劣势**：重启数据消失、容量有限

#### 1.2 存储引擎介绍

- **InnoDB**
  1. 用于**事务**处理应用程序，支持**外键**和**行级锁**。
  2. 如果应用**对事物的完整性**有比较高的要求，在**并发条件下要求数据的一致性**
  3. 数据操作除了**插入**和**查询**之外，还包括很多**更新**和**删除**操作，那么InnoDB存储引擎是比较合适的。
  4. InnoDB除了有效的降低由删除和更新导致的锁定，还可以确保事务的**完整提交和回滚**，对于类似**计费系统**或者**财务系统**等对数据准确要求性比较高的系统都是合适的选择。
- **MyISAM**
  1. 如果应用是以**读操作**和**插入操作**为主
  2. 只有**很少的更新和删除**操作，并且对**事务的完整性、并发性要求不高**，那么可以选择这个存储引擎。
- **Memory**
  - 将所有的数据保存在**内存**中，在需要快速定位记录和其他类似数据的环境下，可以提供极快的访问。Memory的**缺陷是对表的大小有限制**，虽然数据库因为异常终止的话数据可以正常恢复，但是一旦数据库关闭，存储在内存中的数据都会丢失。

**其他存储引擎**

1. InnoDB
   - MySql 5.6 版本默认的存储引擎。InnoDB 是一个事务安全的存储引擎，它具备提交、回滚以及崩溃恢复的功能以保护用户数据。InnoDB 的行级别锁定以及 Oracle 风格的一致性无锁读提升了它的多用户并发数以及性能。InnoDB 将用户数据存储在聚集索引中以减少基于主键的普通查询所带来的 I/O 开销。为了保证数据的完整性，**InnoDB 还支持外键约束**。
2. MyISAM
   - MyISAM既不支持事务、也不支持外键、其优势是访问速度快，但是**表级别的锁**限制了它在读写负载方面的性能，因此它经常应用于**只读**或者**以读为主**的数据场景。
3. Memory
   - 在内存中存储所有数据，应用于对非关键数据由快速查找的场景。Memory类型的表访问数据非常快，因为它的数据是存放在内存中的，并且默认使用**HASH**索引，但是一旦服务关闭，表中的数据就会丢失
4. BLACKHOLE
   - 黑洞存储引擎，类似于 Unix 的 /dev/null，Archive 只接收但却并不保存数据。对这种引擎的表的查询常常返回一个空集。这种表可以应用于 DML 语句需要发送到从服务器，但主服务器并不会保留这种数据的备份的主从配置中。
5. CSV
   - 它的表真的是以逗号分隔的文本文件。CSV 表允许你以 CSV 格式导入导出数据，以相同的读和写的格式和脚本和应用交互数据。由于 CSV 表没有索引，你最好是在普通操作中将数据放在 InnoDB 表里，只有在导入或导出阶段使用一下 CSV 表。
6. NDB
   - (又名 NDBCLUSTER)——这种**集群数据引擎**尤其适合于需要最高程度的正常运行时间和可用性的应用。注意：NDB 存储引擎在标准 MySql 5.6 版本里并不被支持。
   - MySql 集群的版本有：基于 MySql 5.1 的 MySQL Cluster NDB 7.1；基于 MySql 5.5 的 MySQL Cluster NDB 7.2；基于 MySql 5.6 的 MySQL Cluster NDB 7.3。同样基于 MySql 5.6 的 MySQL Cluster NDB 7.4 目前正处于研发阶段。
7. Merge
   - 允许 MySql DBA 或开发者将一系列相同的 MyISAM 表进行分组，并把它们作为一个对象进行引用。适用于超大规模数据场景，如数据仓库。
8. Federated
   - 提供了从多个物理机上联接不同的 MySql 服务器来创建一个逻辑数据库的能力。适用于分布式或者数据市场的场景。
9. Example
   - 这种存储引擎用以保存阐明如何开始写新的存储引擎的 MySql 源码的例子。它主要针对于有兴趣的开发人员。这种存储引擎就是一个啥事也不做的 "存根"。你可以使用这种引擎创建表，但是你无法向其保存任何数据，也无法从它们检索任何索引。

#### 1.3 查看mysql所有的配置

```mysql
# 查看与存储引擎相关配置
show variables like '%engine%';
show variables like "default_storage_engine";
# 查看当前数据库支持的存储引擎
show engines \g
show engines;
# 修改已经存在表的存储引擎
alter table 表名 engine = innodb;
# 查看与编码相关的配置
show variables like '%chara%';
# 查看
show variables like '%关键字%';
```

- 指定存储引擎

```mysql
# 创建表
create table t1(id int, name char(10)) engine=innodb;
# 查看表的结构，包括存储引擎和编码 \G 格式化输出，带 \G 不能使用分号
show create table t1 \G
# 只查看表字段基础信息
describle t1;

t1.frm frame 表结构
t1.ibd innoDB 存储引擎
```

```mysql
# 指定engine为myisam
create table t2(id int, name char(10)) engine=MyISAM;

t2.frm 表结构
t2.MYD 数据
t2.MYI 索引
```

```mysql
# 指定engine为memory
create table t2(id int, name char(10)) engine=memory;
t2.xxx 数据
```

### 2. mysql数据类型(4)

```mysql
# 语法：
create table 表名(
字段名1 类型[(宽度) 约束条件],
字段名2 类型[(宽度) 约束条件],
字段名3 类型[(宽度) 约束条件]);

# 注意：
1. 在同一张表中，字段名是不能相同
2. 宽度和约束条件可选
3. 字段名和类型是必须的
```

- 数值：
  - TINYINT(1byte)，SMALLINT(2byte)，MEDIUMINT(4byte)，**INT**(4byte)，BIGINT(8byte)
- 日期时间
- 字符
- **ENUM**和**SET**类型

#### 2.1数值

1. MySQL支持所有标准SQL数值数据类型。这些类型包括严格数值数据类型(**INTEGER**、 **SMALLINT**、 **DECIMAL**和**NUMERIC**)，以及近似数值数据类型(**FLOAT**、 **REAL**和**DOUBLE PRECISION**)。
2. 关键字INT是INTEGER的同义词，关键字DEC是DECIMAL的同义词。
3. MySQL支持的整数类型有**TINYINT**、**MEDIUMINT**和**BIGINT**。
4. 对于小数的表示，MYSQL分为**两种方式**：**浮点数和定点数**。浮点数包括float(单精度)和double(双精度),而**定点数**只有**decimal**一种，在mysql中**以字符串的形式存放**，比浮点数更精确，适合用来表示货币等精度高的数据。
5. BIT数据类型保存位字段值，并且支持MyISAM、MEMORY、InnoDB和BDB表。

- 整数(int)

```mysql
# 创建无符号int型表
create table t3(id1 int, id2 int unsigned);
```

- 小数(float/double)

```mysql
# 一共有5位，小数2位
float(5, 2)/ double(5, 2)
# 创建表
create tables t4(f1 float(5,2), double(5,2));
# 不指定长度，单精度和双精度
create tables t4(f1 float, double);
# decimal精度,默认存储（10，0）整数
create table t5(d1 decimal, d2 decimal(25, 20));
# decimal内部存储是按照字符串存的
```

#### Note2(4)

1. 默认int类型有符号
2. int类型数据范围不被**宽度**约束
3. 5.6版只能约束数字的显示宽度，5.7不受限制
4. 5.6版插入数据超过最大长度会默认显示最大值，5.7版直接会提示：Out of range value

#### 2.2 时间和日期(5)

1. **date**：年月日
2. **time**：时分秒
3. **year**：年份值
4. **datetime**：年月日时分秒
5. **timestamp**：年月日时分秒
   - 1970-01-01 00:00:00/2038结束时间是第 **2147483647** 秒，北京时间 **2038-1-19 11:14:07**，格林尼治时间 2038年1月19日 凌晨 03:14:07

```mysql
# 创建表
create table t6(d1 date, y year, ts timestamp);
insert into t6(now(), now(), now());
# 指定传y,datetime默认为更新时间
insert into t6(y) values(2019);
# 指定datetime更新方式
create table t6(d1 date, y year, 
                dt datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);
# 可以使用字符串，纯数字
# 5.7版本，插入参数不全，会报错，5.6版不会
```

#### 2.3 字符串

1. 字符串类型指**CHAR**、**VARCHAR**、BINARY、VARBINARY、BLOB、TEXT、**ENUM**和**SET**。该节描述了这些类型如何工作以及如何在查询中使用这些类型。
2. BINARY 和 VARBINARY 类似于 CHAR 和 VARCHAR，不同的是它们包含二进制字符串而不要非二进制字符串。也就是说，它们包含字节字符串而不是字符字符串。这说明它们没有字符集，并且排序和比较基于列值字节的数值值。
3. BLOB 是一个二进制大对象，可以容纳可变数量的数据。有 4 种 BLOB 类型：TINYBLOB、BLOB、MEDIUMBLOB 和 LONGBLOB。它们区别在于可容纳存储范围不同。
4. 有 4 种 TEXT 类型：TINYTEXT、TEXT、MEDIUMTEXT 和 LONGTEXT。对应的这 4 种 BLOB 类型，可存储的最大长度不同，可根据实际情况选择。

- char：定长字符串(3)
  - 补齐指定长度的
  - 长度变化小的情况使用、浪费空间，存储效率较高
  - 用户名、密码、身份证、手机号
- varchar：变长字符串(3)
  - 存储输入长度的+1 eg.alex    则存储alex4
  - 节省空间、存储效率s相对低
  - 评论、微博、说说、微信状态

```mysql
create table t7(name1 char(5), name2 varchar(5));
# 分别存储 'echo ' 和 'echo4'
insert into t7 values('echo', 'echo')
select concat(name1, '---') from t7;
select concat(name2, '---') from t7;
```

#### 2.4 enum和set类型

1. ENUM中文名称叫枚举类型，它的值范围需要在创建表时通过枚举方式显示。ENUM**只允许从值集合中选取单个值，而不能一次取多个值**。
2. SET和ENUM非常相似，也是一个**字符串对象**，里面可以包含**0-64**个成员。根据成员的不同，存储上也有所不同。set类型可以**允许值集合中任意选择1或多个元素进行组合**。对超出范围的内容将不允许注入，而对重复的值将进行自动去重。

- ENUM('male', 'female')：单选框
- set('')：多选框
- 5.6版本取交集，5.7版本插入的数据必须和指定数据一致，不然会报错

```mysql
create table t8(name char(12), 
                gender ENUM('male', 'female'),
               hobby set('play', 'drink', 'eat'));
```

### 3. mysql工作流程

![sql工作流程](/Users/henry/Documents/%E6%88%AA%E5%9B%BE/Py%E6%88%AA%E5%9B%BE/sql%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B.png)

- MySQL架构总**共四层**，在上图中以虚线作为划分。 
  1. 最上层的服务并不是MySQL独有的，大多数给予网络的客户端/服务器的工具或者服务都有类似的架构。比如：**连接处理**、**授权认证**、**安全等**。 
  2. 第二层的架构包括大多数的MySQL的**核心服务**。包括：查询解析、分析、优化、缓存以及所有的内置函数（例如：日期、时间、数学和加密函数）。同时，所有的跨存储引擎的功能都在这一层实现：**存储过程**、**触发器**、**视图等**。
  3. 第三层包含了**存储引擎**。**存储引擎负责MySQL中数据的存储和提取**。服务器通过API和存储引擎进行通信。这些接口屏蔽了不同存储引擎之间的差异，使得这些差异对上层的查询过程透明化。存储引擎API包含十几个底层函数，用于执行“开始一个事务”等操作。但存储引擎一般不会去解析SQL（InnoDB会解析外键定义，因为其本身没有实现该功能），不同存储引擎之间也不会相互通信，而只是简单的响应上层的服务器请求。
  4. 第四层包含了**文件系统**，所有的表结构和数据以及用户操作的日志最终还是以文件的形式存储在硬盘上。

## 1.3 表的完整性约束

### 1. 约束(5)

- unsigned：设置无符号

1. **NOT NULL** ：非空约束，指定某列不能为空； 
2. **DEFAULT**：默认值，当同一数据大量出现时使用；
3. **UNIQUE** : 唯一约束，指定某列或者几列组合不能重；
4. **PRIMARY KEY** ：**主键**，指定该列的值可以唯一地标识该列记；
5. **FOREIGN KEY** ：外键，指定该行记录从属于主表中的一条记录，主要用于参照完整性。

#### 1.1 not null

- 非空

```mysql
create table t1(id int not null,
               name char(12) not null,
               age int);
insert into t1(id, name) values(1, 'henry');
```

#### 1.2 default

- 默认值，创建列时可以指定默认值，当插入数据时如果未主动设置，则自动添加默认值

```mysql
create table t2(id int not null,
               name char(12) not null,
               gender enum('male', 'female') not null default 'male'
               );       
insert into t2(id, name) values(1, 'henry');
```

#### 1.3 unique

- 不重复(**key UNI**)，所有的非空数据不重复
- 唯一约束，指定某列或者几列组合不能重复

```mysql
create table t3(id int unique,
               username char(12) not null unique,
               pwd char(18)
               );
```

- **联合唯一**(**key MUL**)

```mysql
create table t4(id int not null unique,
               ip char(15),
               server char(10),
               port int,
               unique(ip, port))  # 联合唯一,不能同时重复
```

#### 1.4 auto_increment

1. 自增(只能用于数值)，**自带非空 唯一属性**
2. 约束字段为自动增长，被约束的字段必须同时被key约束
3. 如果事务**rollback**了这个**auto_increment**值就会浪费掉，从而造成间隙
4. AUTO_INCREMENT数据列序号的最大值受该列的数据类型约束，一旦达到上限，**AUTO_INCREMENT**就会**失效**。

```mysql
create table t5(id int unique auto_increment,
               username char(10),
               pwd char(18));

insert into t5(username, pwd) values('henry', '123');
# 自增大小只增不减
# 对于自增的字段，在用delete删除后，再插入值，该字段仍按照删除前的位置继续增长
```

- 应该用**truncate清空表**，比起delete一条一条地删除记录，truncate是直接清空表，在删除大表时用它 mysql> truncate student;

```mysql
# 也可以创建表时指定auto_increment的初始值，注意初始值的设置为表选项，应该放到括号外
create table student(id int primary key auto_increment,
                     name varchar(20),
                     gender enum('male','female') default 'male'
                    ) auto_increment=3;
```

- **mysql自增步长**

```mysql
#设置步长
# sqlserver：自增步长
# 基于表级别,指定步为2，从0开始计数
create table t1（id int unique auto_increment, age int
    ）engine=innodb,auto_increment=2 default charset=utf8;
# mysql自增的步长：
show session variables like 'auto_inc%'; 
# 基于会话级别
set session auto_increment_increment=2;# 修改会话级别的步长
# 基于全局级别的
set global auto_increment_increment=2; # 修改全局级别的步长（所有会话都生效）
# 查看设置，重新登陆5.7版本直接失效
show variables like 'auto_incre%'; 
```

- If the value of **auto_increment_offset(起始偏移量)** is greater than that of **auto_increment_increment(步长)**, the value of auto_increment_offset is ignored. 
- **比如**：设置auto_increment_offset=3，auto_increment_increment=2

#### 1.5 primary key

1. 一张表**只能**设置**一个主键,innodb**表中最好设置一个主键
2. 主键约束这个字段，非空且唯一即：**not null unique**

```mysql
create table t6(id int not null unique,
               name char(10) not null unique);
# 第一个指定为not null nuique 字段被定义为主键
```

```mysql
create table t7(id int primary key,
               name char(10) not null unique);
```

- **联合主键**

```mysql
create table t8(id int,
               ip char(15),
               server char(10),
               port int,
               primary(ip, port))  # 联合主键
```

#### Note(4)

1. 主键为了保证表中的每一条数据的**该字段**都是表格中的**唯一值**。换言之，它是用来独一无二地确认一个表格中的每一行数据。 
2. 主键可以包含**一个**字段或**多个字段**。当主键包含多个栏位时，称为**组合键** (Composite Key),也可以叫**联合主键**。
3. **主键**可以在建新表格时设定 (运用 CREATE TABLE 语句)，或是以改变现有的表格架构方式设定 (运用 ALTER TABLE)。
4. **主键必须唯一**，主键值**非空**；可以是单一字段，也可以是多字段组合。

#### 1.6 foreign key

1. 外键，涉及到两张表
2. 关联的数据类型必须一致
3. 被关联的表**必须唯一**，mysql最好关联主键
4. 先创建**外表**，再创建**关联表**

```mysql
create table staff(id int primary key auto_increment,
                   age int,
                   gender enum('male', 'female'),
                   salary float(10,2),
                   hire_date date,
                   post_id int,
                   foreign key(post_id) references dept(pid);
                   
create table dept(pid int primary key, name char(10) not null nuique);
```

- 级联删除和更新
- foreign key(post_id) references dept(pid) **on update cascade on delete cascade**

```mysql
create table staff(id int primary key auto_increment,
                   age int,
                   gender enum('male', 'female'),
                   salary float(10,2),
                   hire_date date,
                   post_id int,
                   foreign key(post_id) references dept(pid) 
                   on update cascade 
                   on delete set null);
                   
create table dept(pid int primary key, name char(10) not null nuique);
```

### 2. 修改表结构

- 创建项目之前
- 项目开发、运行过程中

#### 2.1 修改表名

```mysql
# 修改表名
alter table 表名 rename 新表名;
```

#### 2.2 增加/删除字段

```mysql
# 添加字段
alter table 表名 add 添加字段名 数据类型(宽度)  约束;
# 删除字段
alter table 表名 drop 删除字段名;
```

#### 2.3 修改字段

```mysql
# 修改已经存在字段的类型、宽度 约束，不能修改字段名字
alter table 表名 modify 字段名 类型() 约束
# 修改已经存在字段的类型、宽度 约束、字段名字
alter table 表名 change 字段名 新字段名 类型() 约束
```

#### 2.4 修改字段顺序

```mysql
# 把字段放在第一列
alter table 表名 modify age 类型+约束 first；
# 把字段放在id之后
alter table 表名 modify age int not null after id；
# 也可以与 add、change 连用
```

#### 2.5 修改字段约束

```mysql
#去掉null约束
alter table t modify name char(10) null;
# 添加null约束
alter table t modify name char(10) not null;
```

```mysql
# 去掉unique约束,特殊
alter table 表名 drop index 字段名;
# 添加unique约束
alter table 表名 modify 字段名 int unique;
```

#### 2.6 修改库的默认编码

```mysql
alter database 库名 CHARACTER SET utf8;
```

#### 2.7 操作主键add/drop

```mysql
# 先删除主键，删除一个自增主键会报错
# 需要先去掉主键的自增约束，然后再删除主键约束
alter table 表名 drop primary key;
# 增加主键
alter table 表名 add primary key(id);
```

#### 2.8 操作外键add/drop

```mysql
# 添加外键
alter table 表名 add constraint 外键名 foreign key(字段) references press(字段);
# 删除外键
alter table 表名 drop foreign key 外键名;
```

#### 2.9 删除表

```mysql
drop table 表名；
```

### 3. 操作数据

两张表的数据关系：**多对一**、**一对一**、**多对多**(书、作者)

#### 3.1 多对一

- 永远在多的表中设置外键
- **例如**：一对多（或多对一）：一个出版社可以出版多本书

```mysql
create table press(id int primary key auto_increment,
                   name varchar(20));

create table book(id int primary key auto_increment,
                  name varchar(20),
                  press_id int not null,
                  foreign key(press_id) references press(id)
                  on delete cascade
                  on update cascade);

insert into press(name) values('henry publisher'),
('echo publisher'),('dean publisher');

insert into book(name,press_id) values('henry',1),('echo',2),
('dean',2),('brad',3),('dianel',2),('oleg',3);

```

#### 3.2 一对一

- 外键+unique   
- **后出现**的表中字段作为**外键**

```mysql
# 两张表：学生表和客户表
create table customer(id int primary key auto_increment,
                      name varchar(20) not null,
                      qq varchar(10) not null,
                      phone char(16) not null);

create table student(id int primary key auto_increment,
                     class_name varchar(20) not null,
                     customer_id int unique, #该字段一定要是唯一的
                     foreign key(customer_id) references customer(id) 
                     on delete cascade
                     on update cascade);
# 增加客户
insert into customer(name,qq,phone) values('henry', '12345', 12312312311), ('echo','123123123',12312312311),('dean', '283818181', 12312312311), ('brad','283818181',12312312311), ('oleg', '888818181', 12312312311), ('dianel','112312312',12312312311);
# 增加学生
insert into student(class_name,customer_id) values('1班',3),('2班',4),('3班',5);

```

#### 3.3 多对多

- 利用第三张表，把两个关联关系的字段作为第三张表的外键

```mysql
create table author(id int primary key auto_increment,
                    name varchar(20));
create table book(id int primary key auto_increment,
                    name varchar(20));
# 这张表就存放作者表与书表的关系，即查询二者的关系查这表就可以了
create table author_book(id int not null unique auto_increment,
                         author_id int not null,
                         book_id int not null,
                         constraint fk_author foreign key(author_id) references author(id)
                         on delete cascade
                         on update cascade,
                         constraint fk_book foreign key(book_id) references book(id)
                         on delete cascade
                         on update cascade,
                         primary key(author_id,book_id));

# 插入作者和书籍信息
insert into author(name) values('henry'),('echo'),('dean'),('diane');
insert into book(name) values('1'),('2'),('3'),('4'),('5'),('6')
insert into author_book(author_id,book_id) values(1,1),(1,2),(1,3）,(1,4),(1,5),(1,6),(2,1),(2,6),(3,4),(3,5),(3,6),(4,1);

```

#### 3.4 on delete/update

```mysql
# 在父表上update/delete记录时，同步update/delete掉子表的匹配记录
cascade方式	

# 在父表上update/delete记录时，将子表上匹配记录的列设为null要注意子表的外键列不能为not null  
set null方式 

# 如果子表中有匹配的记录,则不允许对父表对应候选键进行update/delete操作
No action方式

# 同no action, 都是立即检查外键约束
Restrict方式

# 父表有变更时,子表将外键列设置成一个默认的值 但Innodb不能识别
Set default方式
```

### 4. 记录操作

#### 4.1 数据增加

1. insert into 表名 values(值…)：一次性可以写入**多行**数据
2. insert into 表名(字段名) values(值...)
3. insert into 表名 value(值…)：一次性只可以写入**一**行数据

```mysql
# 写入一行数据
insert into t1 values(1, 'henry', 19);
insert into t1 value(1, 'henry', 19);
# 写入多行数据
insert into t1 values(1, 'henry', 19), (2, 'echo', 18);
# 指定字段写入
insert into t1(name, age) value('henry', 19);
```

#### 4.2 删除

```mysql
# 删除条件匹配到的数据
delete form 表 where 条件;
```

#### 4.3 修改

```mysql
# 修改表中数据， set 后的字段可以为一个或多个
update 表 set 字段=值 where 条件;
# 注意null只能使用 is 匹配
where name is null;
```

## 1.4 查询

- select 语法

```mysql
SELECT DISTINCT 字段1,字段2... FROM 表名
                              WHERE 条件
                              GROUP BY field
                              HAVING 筛选
                              ORDER BY field
                              LIMIT 限制条数
```

### 1. 基本查询

```mysql
# 查看表中所有数据
select * from 表
# 查看指定字段
select 字段1,字段2... from 表
# 查看指定字段，自动去重
select distinct 字段1,字段2... from 表
# 数值型四则运算，并名别名显示
select name,salary*12 (as) annual_salary form 表
# 数值型四则运算，并名别名， 拼接显示
select concat ('姓名：',name,'薪资：',salary*12) (as) annual_salary form 表
# 使用':'进行拼接
select concat_ws (':', name,salary*12 (as) annual_salary) form 表
```

```mysql
# 结合CASE语句：
SELECT(CASE
       WHEN emp_name = 'henry' THEN
           emp_name
       WHEN emp_name = 'echo' THEN
           CONCAT(emp_name,'_prefect')
       ELSE
           concat(emp_name, '_nice')
       END
       ) as new_name FROM employee;
```

### 2 . where

- **逐行过滤**

1. 比较运算：<>/!= 不等于，> ，< ，>=，<=
2. 范围筛选
   - 多选一个
   - 在一个模糊的范围里
     - 在一个数值区间
     - 字符串模糊查询
     - 正则匹配
3. 逻辑运算—条件拼接
   - 与、或、非

#### 2.1 比较/逻辑/身份运算

- **in / not in / is / is not** 

```mysql
select * from t1 where salary>1000;
# 和数值类型无关
select * from t1 where salary=20000 or slary=30000;
# 逻辑运算
select * from t1 where gender='male' and age=18;
# 多选一,可以使用 in
select 字段名，... from t1 where salary in (20000, 30000, 19000);
# not in 
select 字段名，... from t1 where salary not in (20000, 30000, 19000);
# is /is not 
select 字段名 from t1 where 字段 is null;
```

#### 2.2 模糊查找(3)

1. **between…and...**

```mysql
# between ... and ...
select  name,salary from t1 where salary between 10000 and 20000
```

2. **字符串**模糊匹配，**like**

```mysql
# like ， % 通配符，匹配任意长度，任意内容
select * from t1 where name like '程%';
# like ， _ 通配符，匹配一个任意字符
select * from t1 where name like '程_';
# like ， 以 n 结尾
select * from t1 where name like '%n';

```

3. 正则匹配，**regexp**

```mysql
select * from t1 where name regexp 正则表达式;
SELECT * FROM employee WHERE emp_name REGEXP 'on$';
```

### 3. 分组聚合

#### 3.1 group by

- group by 后的这个字段，也就是post字段中的每一个不同的项目保留下来
- 并且把值是这一项的所有行归为一组，并**只显示组中第一个**

```mysql
# 显示一个组的第一个,必须有group的字段
select post from employee group by post;
# distinct 基于group by完成
```

#### 3.2 聚合函数(5)

- 把多行的同一字段进行一些统计，最终得到一个结果

1. count(字段)：统计这个字段有多少项
2. sum(字段)：统计这个字段对应的数值和，数值类型
3. avg(字段)：平均值
4. **min、max**：
   - 只能取到最小、最大值，但不能取到对应的其他项(名字)，显示组中第一项
   - 使用多表查询

- **count**

```mysql
select count(*/ 主键) from employee;
# 只算id不为空的字段个数
select count(id) from employee;
```

- **avg/sum**

```mysql
select avg(salary) from employee;
select sum(salary) from employee;
```

#### 3.3 分组聚合

- group by

```mysql
# 分别对各个组,统计人数
select post,count(*) from employee group by post;
# 对某一组进行统计人数
select post,count(*) from employee where post='teacher';
# 各部门的平均薪资
select post,avg(salary) from employee group by post;
```

```mysql
# 最晚入职
select max(hire_date) from employee group by post;
# 最早入职
select min(hire_date) from employee group by post;
```

- **查询分组内所有成员名**
  - **group_concat()**

```mysql
# 查询岗位名以及岗位包含的所有员工名字
select post, group_concat(emp_name) from employee group by post;
# 查询岗位名以及各岗位内包含的员工个数
select post, count(id) from employee group by post;
# 查询公司内男员工和女员工的个数
select gender, count(id) from employee group by gender;
```

#### Note3(2)

1. 总是根据会重复的项进行分组
2. 分组总是和聚合函数一起使用

#### 3.4 having

- having 条件，**组过滤**， 一般与**group**一起使用
- **Where** 发生在分组**group by之前**，因而Where中可以有任意字段，但是**绝对不能**使用聚合函数。
- **Having**发生在分**组group by之后**，因而Having中可以使用分组的字段，**无法直接取到其他字段**,可以使用**聚合函数**

```mysql
# 部门人数大于3
select post from employee group by post having count(*) > 3;
# 平均薪资大于10000
select post from employee group by post having avg(salary) > 10000;
# 过滤整张表,必须有 age 字段，否则报错
select emp_name, age from employee having avg(age)>18;
```

- having 过滤示例

```mysql
# 查询各岗位内包含的员工个数小于2的岗位名、岗位内包含员工名字、个数
select post, group_concat(emp_name), count(*) from employee group by post having count(id) < 2;
# 查询各岗位平均薪资大于10000的岗位名、平均工资
select post,avg(salary) from employee group by post having avg(salary) > 10000;
# 查询各岗位平均薪资大于10000且小于20000的岗位名、平均工资
select post,avg(salary) from employee group by post having avg(salary) > 10000 and avg(salary) < 20000;
# 使用 between ... and...
select post,avg(salary) from employee group by post having avg(salary) between 10000 and 20000;
```

#### 3.5 order by

```mysql
# desc 表示降序排
# asc 表示生序排列，默认值
select * from employee order by salary desc;
# 多个个字段排序，先根据第一个字段排列后，再根据第二个字段排列
select * from employee order by age asc, salary desc;
```

- having 和 order by综合使用示例

```mysql
# 查询各岗位平均薪资大于10000的岗位名、平均工资,结果按平均薪资升序排列
select post, avg(salary) from employee group by post having avg(salary) > 10000 order by avg(salary) asc;
# 查询各岗位平均薪资大于10000的岗位名、平均工资,结果按平均薪资降序排列
select post, avg(salary) from employee group by post having avg(salary) > 10000 order by avg(salary) desc;
```

#### 3.6 limit

```mysql
# 分页显示
# 默认从0开始，显示前5个
select * from employee limit 5;
# 显示下5个, 5+1 位置开始取
# limit m,n 表示从m+1开始取到5个
limit n offset m等价于limit m,n

select * from employee limit 5,5;
# 显示下5个
select * from employee limit 10,5;
```

#### Note3(3)

1. **关键字执行的优先级(8)**
   - **join优先级要高于from**
   - **from**—> **where** —> **group by** —> **select** —> **distinct** —> **having** —> **order by** —>**limit**
2. 用户认证—>解析、优化、执行sql、找到存储引擎
3. select之前把行数限制在小的范围

![sql语句执行顺序](/Users/henry/Documents/%E6%88%AA%E5%9B%BE/Py%E6%88%AA%E5%9B%BE/sql%E8%AF%AD%E5%8F%A5%E6%89%A7%E8%A1%8C%E9%A1%BA%E5%BA%8F.png)

### 4. 多表查询

- 数据准备

```mysql
# 建表
create table department(id int, name varchar(20) );

create table staff(id int primary key auto_increment,
                   name varchar(20),
                   gender enum('male','female') not null default 'male',
                   age int,
                   dep_id int);
#插入数据
insert into department values(200,'技术'),(201,'人力资源'),(202,'销售'),(203,'运营');
insert into staff(name,gender,age,dep_id) values
('henry','male',18,200), 
('echo','female',48,201),
('dean','male',38,201),
('diane','female',28,202),
('oleg','male',18,200),
('iris','female',18,204);

#查看表结构和数据
mysql> desc department;
mysql> desc employee;

mysql> select * from department;
mysql> select * from employee;
```

#### 4.1 连表查询

- **通常使用内连接和左外连接**

```mysql
select 字段列表
    FROM 表1 INNER|LEFT|RIGHT JOIN 表2
    ON 表1.字段 = 表2.字段;
```

1. **交叉连接：不适用任何匹配条件。生成笛卡尔积**

```mysql
# 笛卡尔积
select 字段 from t1,t2 where 字段1=字段2;
# 连表查询,staff,department 两个表，和 inner join 效果一致
select * from staff, department as dept where dep_id=dept.id;
```

2. **内连接(inner join)**
   - 两张表条件不匹配的项不出现结果中

```mysql
select 字段 from t1 inner join t2 on t1(字段1) = t2(字段2);
```

3. **外连接**
   1. **左外连接(left join)：全量显示左边的表中数据**
      - **本质**就是：在内连接的基础上增加**左边有右边没有**的结果
   2. 右外连接(right join)：全量显示右边的表中数据
      - **本质**就是：在内连接的基础上增加**右边有左边没有**的结果
   3. 全外连接**(左外连接 union 右外连接)**：mysql没有全外连接
      - **在内连接的基础上增加左边有右边没有的和右边有左边没有的结果**
   4. **sqlserver**中有全外连接(**full join**)，没有右外连接

```mysql
# t1连接t2，显示全量的左表，只显示匹配到的t2
select 字段 from t1 left join t2 on t1(字段1) = t2(字段2);
select 字段 from t1 right join t2 on t1(字段1) = t2(字段2);
# 全连接
select 字段 from t1 left join t2 on t1(字段1) = t2(字段2) union
select 字段 from t1 right join t2 on t1(字段1) = t2(字段2);
```

```mysql
# 通过左外、和右外连接实现全外连接示例
select * from staff left join department as dept on dep_id = dept.id union select * from staff right join department as dept on dep_id = dept.id;
```

- **注意 union与union all的区别：union会去掉相同的纪录**

4. **连表查询示例**
   - **连表查询效率更高**

```mysql
# 以内连接的方式查询staff和department表，并且staff表中的age字段值必须大于25,即找出年龄大于25岁的员工以及员工所在的部门
# 此时括号可以省略
select staff.name, dept.name from staff left join department as dept on dep_id = dept.id where age > 25;
# 以内连接的方式查询staff和department表，并且以age字段的升序方式显示
select * from staff inner join department as dept on dep_id = dept.id order by age;
```

#### 4.2 子查询

1. 基本语法

```mysql
1：子查询是将一个查询语句嵌套在另一个查询语句中。
2：内层查询语句的查询结果，可以为外层查询语句提供查询条件。
3：子查询中可以包含：IN、NOT IN、ANY、ALL、EXISTS 和 NOT EXISTS等关键字
4：还可以包含比较运算符：= 、 !=、> 、<等
```

```mysql
# 子表中匹配到唯一值
select name from emp where dep_id = (select id from department where name='技术');
# 子表中匹配到多个值
select name from emp where dep_id in (select id from department where name in ('技术', '销售'));
```

2. **带in关键字的查询**

- 使用in时，后面的表中字段只能有一个字段

```mysql
# 查询平均年龄在25岁以上的部门名
select name from department where id in (select dep_id from staff group by dep_id having avg(age) > 25);
# 查看技术部员工姓名
select name from staff where dep_id in (select id from department where name = '技术' )
# 查看不足1人的部门名(子查询得到的是有人的部门id)
select name from department where id not in (select dep_id from staff group by dep_id);
```

3. **带比较运算符**

```mysql
# 查询大于所有人平均年龄的员工名、年龄
select name, age from staff where age > (select avg(age) from staff);
# 查询大于部门内平均年龄的员工名、年龄
select name, age from staff t1 inner join (select dep_id, avg(age) avg_age from staff group by dep_id) t2 on t1.dep_id = t2.dep_id where t1.age > t2.avg_age;
```

4. 带EXISTS关键字的子查询

- **EXISTS关字键字表示存在**。在使用EXISTS关键字时，**内层查询语句**不返回查询的记录。而是**返回一个真假值**。
- 当返回True时，外层查询语句将进行查询；当返回值为False时，外层查询语句不进行查询

```mysql
# exists后为真
select * from staff where exists (select id from department where id=200);
# 输出staff中所有数据
# exists后为假
select * from staff where exists (select id from department where id=200);
# 输出为空
```

5. **示例**
   - **查询每个部门最新入职的那位员工**

```mysql
# 连表查询
select t1.emp_name, t1.hire_date, t1.post from employee as t1 inner join (select depart_id, max(hire_date) as max_date from employee group by depart_id) as t2 on t1.depart_id = t2.depart_id where t1.hire_date = t2.max_date;
```

```mysql
# 子查询
select t3.emp_name,t3.post,t3.hire_date from employee as t3 where id in (select (select id from employee as t2 where t2.depart_id=t1.depart_id order by hire_date desc limit 1) from employee as t1 group by depart_id);
```

## 1.5 mysql索引

### 1. 存储过程

```mysql
# 1.准备表
create table s_test(id int,
                name varchar(20),
                gender char(6),
                email varchar(50));
# 2.创建存储过程，实现批量插入记录
delimiter $$ #声明存储过程的结束符号为$$
create procedure auto_insert()
BEGIN
    declare i int default 1;
    while(i<3000000)do
        insert into s_test values(i,'henry','male',concat('henry',i,'@qq.com'));
        set i=i+1;
    end while;
END$$ #$$结束
delimiter ; #重新声明分号为结束符号
# 3.查看存储过程
show create procedure auto_insert\G 
# 4.调用存储过程
call auto_insert();
# 在写入的时候不更新索引表，只针对myisam生效
ALTER TABLE table_name DELAY_KEY_WRITE= 1;
# 删除
drop procedure if exists auto_insert;
```

### 2. 初识索引

- **索引**是应用程序设计和开发的一个重要方面。**若索引太多**，应用程序的性能可能会受到影响。而索引太少，对查询性能又会产生影响，要找到一个平衡点，这对应用程序的性能至关重要。
- **场景**：某台MySQL服务器iostat显示磁盘使用率一直处于100%，经过分析后发现是由于开发人员添加了**太多的索引**，在删除一些不必要的索引之后，磁盘使用率马上下降为20%。可见索引的添加也是非常有技术含量的。

#### 2.1 概念

- **索引在MySQL中也叫是一种“键”，是存储引擎用于快速找到记录的一种数据结构**
- 建立起的一个在存储表阶段的一个存储结构能够在查询的时候加速
- 出于效率方面的考虑，InnoDB数据表的**数据行级锁定实际发生在它们的索引上**，而不是数据表自身上。显然，数据行级锁定机制只有在有关的数据表有一个合适的索引可供锁定的时候才能发挥效力

#### 2.2 索引的重要性

1. 读写比例：10:1，读的速度是数据库的关键
   - 读取硬盘的io操作时间要远远长于cpu执行指令的时间
   - 尽量减少io次数才是关键
   - 索引对性能的影响随着数据量的增加愈发重要
   - 访问磁盘的成本大概是访问内存的**十万倍左右**
2. 磁盘IO与预读性原理，一次读取一个**block**块
   - 访问磁盘，那么这里先简单介绍一下磁盘IO和预读，磁盘读取数据靠的是**机械运动**，每次读取数据花费的时间可以分为**寻道时间**、**旋转延迟**、**传输时间**三个部分，寻道时间指的是磁臂移动到指定磁道所需要的时间，主流磁盘一般在**5ms**以下；旋转延迟就是我们经常听说的磁盘转速，
   - 一台500 -MIPS（Million Instructions Per Second）的机器每秒可以执行5亿条指令。
   - 考虑到磁盘IO是非常高昂的操作，计算机操作系统做了一些优化，**当一次IO时，不光把当前磁盘地址的数据，而且把相邻的数据也都读取到内存缓冲区内**，因为局部预读性原理告诉我们，当计算机访问一个地址的数据的时候，与其相邻的数据也会很快被访问到。每一次IO读取的数据我们称之为**一页(page)**。具体一页有多大数据跟操作系统有关，一般为4k或8k，也就是我们读取一页内的数据时候，实际上才发生了一次IO，这个理论对于索引的数据结构设计非常有帮助。
   - 4096bytes, 4k(linux)
   - oracle会一次读取2个block块
   - mysql会一次读取4个block块

#### 2.3 索引原理

- **本质都是：通过不断地缩小想要获取数据的范围来筛选出最终想要的结果，同时把随机的事件变成顺序的事件，也就是说，有了这种索引机制，我们可以总是用同一种查找方式来锁定数据。**
- 索引会加速搜索的速度，但写的速度很慢。每次写入数据时都必须整理树形结构。

#### 2.4 数据库存储方式

1. **平衡树 balance tree b树**

   1. 写入数据：速度较慢，需要整理数据

   2. **b树**在范围查询b树不占优势(root、leaf、branch)演变成双向链式结构

   3. **在b树基础上的改良**：b+树(innodb 默认结构)（**2**）

      - **目的**：每次查找数据时把磁盘IO次数控制在一个很小的数量级，最好是常数数量级。

      1. 分支节点和根节点不在存储实际数据
         - 让分支和根节点能存储更多的索引信息
      2. 在叶子节点之间加入**双向的链式结构**方便在查询中的范围条件

   

   4. **索引字段要尽量的小**：通过上面的分析，我们知道IO次数取决于b+数的高度h，假设当前**数据表的数据为N**，每个**磁盘块的数据项的数量是m**，则有**h=㏒(m+1)N**，当数据量N一定的情况下，m越大，h越小；而**m = 磁盘块的大小 / 数据项的大小**，磁盘块的大小也就是一个数据页的大小，是固定的，如果数据项占的空间越小，数据项的数量越多，树的高度越低。这就是为什么每个数据项，即索引字段要尽量的小，比如int占4字节，要比bigint8字节少一半。这也是为什么b+树要求把真实的数据放到叶子节点而不是内层节点，一旦放到内层节点，磁盘块的数据项会大幅度下降，导致树增高。当数据项等于1时将会退化成线性表。

   - B-Tree中一次检索最多需要h-1次I/O（**根节点常驻内存**），渐进复杂度为O(h) = O(logdN) 。一般实际应用中，出度**d**是非常大的数字，通常超过**100**，因此h非常小（通常不超过3）。（h表示树的高度 & 出度d表示的是树的度，即树中各个节点的度的最大值）

   5. **索引的最左匹配特性**：当b+树的数据项是**复合的数据结构**，比如(name,age,sex)的时候，b+树是按照从左到右的顺序来建立搜索树的，比如当(张三,20,F)这样的数据来检索的时候，b+树会优先比较name来确定下一步的所搜方向，如果name相同再依次比较age和sex，最后得到检索的数据；但当(20,F)这样的没有name的数据来的时候，b+树就不知道下一步该查哪个节点，因为建立搜索树的时候**name就是第一个比较因子**，必须要先根据**name来搜索才能知道下一步去哪里查询**。比如当(张三,F)这样的数据来检索时，b+树可以用name来指定搜索方向，但下一个字段age的缺失，所以只能把名字等于张三的数据都找到，然后再匹配性别是F的数据了， 这个是非常重要的性质，即**索引的最左匹配特性**。

2. **树的高度**会影响索引的效率

   - 对哪一列创建索引，选择尽量**短的列做索引**
   - 对**区分度高的列**建索引，重复率超过10%就不适合创建索引
   - 尽量选择区分度高的列作为索引,区分度的公式是**count(distinct 字段)/count(\*)**，表示字段不重复的比例。

3. 索引特点(2)

   - 加速读取，但牺牲了写的速度
   - 每个节点存储**数据的地址**

4. mysql中所有的b+树索引的高度都基本上控制在**3**层

   - io操作的次数非常稳定(3)
   - 有利于通过范围查询
   - 在数据库中，**B+树的高度一般都在2~4层**，这也就是说查找某一个键值的行记录时最多只需要2到4次IO，这倒不错。因为当前一般的机械硬盘每秒至少可以做100次IO，2~4次的IO意味着查询时间只需要0.02~0.04秒。

#### 2.4 聚集索引和辅助索引

1. **数据库中的B+树索引可以分为聚集索引（clustered index）和辅助索引（secondary index）**

2. **聚集索引**：数据直接存储在树结构的叶子节点

   - 如用户需要查找一张表，查询最后的10位用户信息，由于B+树**索引是双向链表**，所以用户可以快速找到最后一个数据页，并取出10条记录

   ```mysql
   # InnoDB存储引擎表是索引组织表，即表中数据按照主键顺序存放。
   1. 而聚集索引（clustered index）就是按照每张表的主键构造一棵B+树，同时叶子结点存放的即为整张表的行记录数据，也将聚集索引的叶子结点称为数据页。
   2. 聚集索引的这个特性决定了索引组织表中数据也是索引的一部分。同B+树数据结构一样，每个数据页都通过一个双向链表来进行链接。
   # 如果未定义主键，MySQL取第一个唯一索引（unique）而且只含非空列（NOT NULL）作为主键，InnoDB使用它作为聚簇索引。  
   1. 如果没有这样的列，InnoDB就自己产生一个这样的ID值，它有六个字节，而且是隐藏的，使其作为聚集索引。
   # 由于实际的数据页只能按照一棵B+树进行排序，因此每张表只能拥有一个聚集索引。
   1. 在多数情况下，查询优化器倾向于采用聚集索引。因为聚集索引能够在B+树索引的叶子节点上直接找到数据。
   2. 此外由于定义了数据的逻辑顺序，聚集索引能够特别快地访问针对范围值得查询。
   ```
   
- 可以通过添加主键的方式完成索引的建立
  
```mysql
   alter table t1 add primary key(id);
   alter table t1 modify id not null unique;
```

- **聚集索引的好处之一：**它对主键的排序查找和范围查找速度非常快，叶子节点的数据就是用户所要查询的数据。
   - **聚集索引的好处之二：范围查询（range query）**，即如果要查找主键某一范围内的数据，通过叶子节点的上层中间节点就可以得到页的范围，之后直接读取数据页即可。
   
3. **辅助索引**：数据不直接存储在树中

   - **需要回表**
   - 表中除了**聚集索引外**其他索引都是**辅助索引（Secondary Index，也称为非聚集索引）**，与聚集索引的区别是：**辅助索引的叶子节点不包含行记录的全部数据**。叶子节点除了包含键值以外，每个叶子节点中的索引行中还包含一个书签（**bookmark**）。该书签用来告诉InnoDB存储引擎去哪里可以找到与索引相对应的行数据。

   ![innodb辅助索引](/Users/henry/Documents/%E6%88%AA%E5%9B%BE/Py%E6%88%AA%E5%9B%BE/innodb%E8%BE%85%E5%8A%A9%E7%B4%A2%E5%BC%95.png)

   - **辅助索引**的存在并**不影响数据在聚集索引中的组织**，因此每张表上可以有多个辅助索引，但**只能有一个聚集索引**。当通过辅助索引来寻找数据时，InnoDB存储引擎会遍历辅助索引并通过叶子级别的指针获得索引的主键，然后再通过主键索引来找到一个完整的行记录。

4. **聚集和辅助索引对比**

   1. **聚集索引与辅助索引相同的是**：不管是聚集索引还是辅助索引，其内部都是B+树的形式，即**高度是平衡的**，叶子结点存放着所有的数据。**聚集索引与辅助索引不同的是**：叶子结点存放的是否是一整行的信息
   2. **聚集索引**
      - 纪录的索引顺序与顺序相同，因此更适合between and和order by操作
      - 叶子结点直接对应数据从中间级的索引页的索引行直接对应数据页
      - 每张表只能创建一个聚集索引
   3. 非聚集索引
      - 索引顺序和物理顺序无关
      - 叶子结点不直接指向数据页
      - 每张表可以有多个非聚集索引，需要更多磁盘和内容
      - 多个索引会影响insert和update的速度

5. innodb**中聚集索引和辅助索引**并存（都是b+树）

   - 数据和索引存在一起
   - 除了**主键**之外所有的索引都是**辅助索引**

6. myisam中只有**辅助索引**

   - 叶子节点存储数据的**主键**的值
   - 通过主键再查找数据

7. **需要注意的是**：**innodb**表的索引会存放于**s1.ibd**文件中，而**myisam**表的索引则会有单独的索引文件**table1.MYI**

8. MySAM索引文件和数据文件是分离的，**索引文件仅保存数据记录的地址**。而在innodb中，表数据文件本身就是按照B+Tree（BTree即Balance Tree）组织的一个索引结构，这棵树的叶节点data域保存了完整的数据记录。这个索引的key是数据表的主键，因此**innodb表数据文件本身就是主索引**。因为inndob的数据文件要按照主键聚集，所以innodb要求表必须要有主键（Myisam可以没有），如果没有显式定义，则mysql系统会自动选择一个可以唯一标识数据记录的列作为主键，如果不存在这种列，则mysql会自动为innodb表生成一个隐含字段作为主键，这字段的长度为6个字节，类型为长整型.


### 3. 使用索引

#### 3.1 索引两大类型

1. 我们可以在创建上述索引的时候，为其指定索引类型，**分两类**：
   - **hash类型的索引**：查询单条快，范围查询慢
     - **只有memory（内存）存储引擎支持哈希索引**，哈希索引用索引列的值计算该值的hashCode，然后在hashCode相应的位置存执该值所在行数据的物理位置，因为使用散列算法，因此访问速度非常快，但是一个值只能对应一hashCode，而且是散列的分布方式，因此哈希索引不支持范围查找和排序的功能。
   - **btree类型的索引**：b+树，层数越多，数据量指数级增长（我们就用它，因为innodb默认支持它）
2. 不同的存储引擎支持的索引类型也不一样
   - InnoDB 支持事务，**支持行级别锁定**，支持 B-tree、Full-text 等索引，不支持 Hash 索引；
   - MyISAM 不支持事务，**支持表级别锁定**，支持 B-tree、Full-text 等索引，不支持 Hash 索引；
   - Memory 不支持事务，支持表级别锁定，支持 B-tree、Hash 等索引，不支持 Full-text 索引；
   - NDB 支持事务，支持行级别锁定，支持 Hash 索引，不支持 B-tree、Full-text 等索引；
   - Archive 不支持事务，支持表级别锁定，不支持 B-tree、Hash、Full-text 等索引；
3. 除此之外还有全文索引，即**FULLTEXT**用于搜索**很长一篇文章**的时候，效果最好。用在比较短的文本，如果就一两行字的，普通的 INDEX 也可以。但其实对于全文搜索，我们并不会使用MySQL自带的该索引，而是会选择**第三方软件如Sphinx**，专门来做全文搜索。
4. 其他的如空间索引SPATIAL，了解即可，几乎不用。

#### 3.2 索引的种类

1. **primary key** 主键    **自带聚集索引** 和约束：非空+唯一
   - 联合主键
2. **unique** 区分度最高  **自带辅助索引** 和约束：唯一
   - 联合唯一
3. **index 辅助索引**         辅助索引        没有约束
   - 联合索引，根据两个字段建立索引

#### 3.3 使用索引

- **添加主键会自动添加为索引**
- 添加unique也会自动添加为索引

```mysql
# 方法一：创建表时
create table 表(字段...,
               index|unique|fulltext|spatial|key 
               索引名称 on 表(字段1,字段2...));
# 方法二：CREATE在已存在的表上创建索引,常用方法
create index(索引类型，通常使用index) 索引名称 on 表(字段1,字段2...);
# 方法三：ALTER TABLE在已存在的表上创建索引
alter table 表名 add index 索引名称 on 表(字段1,字段2...);
# 删除索引
drop index 索引名 on 表名字;
# 查看表s1的索引
show index from s1;
```

- 不添加索引的时候肯定慢
- 查询的字段不是索引字段也慢

#### 3.4 索引不生效

- 范围、条件字段是否参与计算、列的区分度、列的长度、条件 and/or，联合索引的前缀问题

1. 要查询的范围越大，索引效果越不明显，越费时
   - 和比较运算符有关的，大于、小于、不等于、between … and ...
   - like，结果范围大，like **abc%可以生效**，**%abc索引不生效**

```mysql
select * from 表 where id between 1000000 and 1000005;
# 使用like
select * from 表 where emial like '%abc';
```

2. 一列的区分度不高
   - 即范围过大

```mysql
# 而对于区分度低的字段，无法找到大小关系，因为值都是相等的，毫无疑问，还想要用b+树存放这些等值的数据，只能增加树的高度，字段的区分度越低，则树的高度越高。
```

3. 索引列不能参与计算，不能包含函数

```mysql
select * from s1 where id*10 = 1000000;
```

4. 对两列内容进行条件查询
   - and：**优先选择有索引且树形结构更好的进行查找**，快速缩小范围
   - or：如果存在没有索引项，索引效果不生效，只是根据条件从左到右依次筛选
     - 条件中带有or的想要命中索引，这些条件中所有列都是索引列
5. **最左前缀匹配原则**，非常重要的原则，对于**组合索引**mysql会一直向右匹配直到遇到范围查询(>、<、between、like)就停止匹配(指的是范围大了，有索引速度也慢)，比如a = 1 and b = 2 and c > 3 and d = 4 如果建立(a,b,c,d)顺序的索引，d是用不到索引的，如果(a,b,d,c) 的索引则都可以用到，a,b,d的顺序可以任意调整。
6. 其他情况
   1. 索引字段使用函数
   2. 排序条件为索引，则select字段必须也是索引字段，否则无法命中
      - 如果对主键排序，则还是速度很快：
   3. 联合索引：不能使用or连接条，从左到右第一个使用范围的条件后的所有列索引失效、在条件中使用了or

**小结：索引不生效情况**

1. 在联合索引中如果使用**or**条件索引不生效
2. 条件必须含有创建索引的第一个字段(**最左前缀原则**)
   - id列可以命中索引
3. 整个条件中，一开始**出现模糊匹配的那一刻，索引就失效**

#### 3.5 联合索引

- 查找总是两个(多)个条件
- **从本质上来说**，联合索引就是一棵B+树，不同的是联合索引的键值得数量不是1，而是>=2
- **在第一个键相同的情况下，已经对第二个键进行了排序处理**

```mysql
create index ind_mix on s1(id, email);
# 对于联合索引（a,b）,下述语句可以直接使用该索引，无需二次排序
select ... from table where a=xxx order by b;
# 然后对于联合索引(a,b,c)来首，下列语句同样可以直接通过索引得到结果
select ... from table where a=xxx order by b;
select ... from table where a=xxx and b=xxx order by c;
# 但是对于联合索引(a,b,c)，下列语句不能通过索引直接得到结果，还需要自己执行一次filesort操作，因为索引（a，c)并未排序
select ... from table where a=xxx order by c;
```

2. 应用场景
   1. 只对a，b，c条件进行索引
   2. **不**对b，对c**进行单列索引**
3. 单列索引
   1. 区分度高的列，建立索引，条件的范围尽量小
   2. 条件中的列不参与计算，使用and 作为条件连接
   3. 使用or连接多个条件，在满足上述条件的基础上，对or相关的所有列创建索引

#### 3.6 覆盖/合并索引

1. **InnoDB存储引擎支持覆盖索引（covering index，或称索引覆盖）**，即从**辅助索引中就可以得到查询记录**，而不需要查询聚集索引中的记录。
2. **覆盖索引的一个好处是**：辅助索引不包含整行记录的所有信息，故其大小要远小于聚集索引，因此可以减少大量的IO操作

- 如果使用索引作为条件查询，查询完毕之后，不需要回表查**即覆盖索引**
- 对两个字段分别创建索引，由于sql让两个索引同时生效，那么这个时候这两个索引就成为了**合并索引**。

```mysql
# 合并索引
create index name on users;
create index age on users;
select * from users where name='henry' or age='18';
```

#### 3.7 执行计划

```mysql
# 执行计划，并不会真正执行sql语句，给出一个执行计划
explain select id from s1 where id = 1000000;
```

- 执行计划使用场景
  1. 测试sql语句是否可以满足数据量多的情况下的效率

![ ](/Users/henry/Documents/%E6%88%AA%E5%9B%BE/Py%E6%88%AA%E5%9B%BE/sql%20explian%E5%8F%82%E6%95%B0.png)

- 建表、使用sql需要注意
  - char代替varchar
  - 连表代替子查询
  - 创建表的时候，固定长度的字段在前面

#### 3.8 慢查询优化流程

![sql 慢日志流程](/Users/henry/Documents/%E6%88%AA%E5%9B%BE/Py%E6%88%AA%E5%9B%BE/sql%20%E6%85%A2%E6%97%A5%E5%BF%97%E6%B5%81%E7%A8%8B.png)

1. 先运行看看是否真的很慢，注意设置SQL_NO_CACHE
2. where条件单表查，锁定最小返回记录表。这句话的意思是把查询语句的where都应用到表中返回的记录数最小的表开始查起，单表每个字段分别查询，看哪个字段的区分度最高
3. explain查看执行计划，是否与1预期一致（从锁定记录较少的表开始查询）
4. order by limit 形式的sql语句让排序的表优先查
5. 了解业务方使用场景
6. 加索引时参照建索引的几大原则
7. 观察结果，不符合预期继续从0分析

### 4. 库的备份与恢复

```mysql
# 语法：
mysqldump -h服务器 -u用户名 -p密码 数据库名 > 备份文件.sql
# 示例：
# 单库备份
mysqldump -uroot -p123 库名 > 备份文件名(路径)
mysqldump -uroot -p123 db1 table1 table2 > db1-table1-table2.sql
# 多库备份,导入时不需要指定库名，会覆盖库名相同的库
mysqldump -uroot -p123 --databases db1 db2 mysql db3 > db1_db2_mysql_db3.sql
# 备份所有库
mysqldump -uroot -p123 --all-databases > all.sql 
```

```mysql
# 方法一：不使用 --databases 参数
mysql -u用户名 -p密码  库名 < 备份文件名 
# 方法二：
mysql> use db1;
# 关闭二进制日志，只对当前session生效
mysql> SET SQL_LOG_BIN=0;  
mysql> source /root/db1.sql
```



## 1.6 pymysql模块

### 1. 第三方模块

```mysql
mysql -uroot -p
mysql.exe              # mysql的一个客户端
```

- **ip port 用户名 密码 使用的库** 连接mysqld的server端

```python
import pymysql
con = pymysql.connect(host='127.0.0.1', user='root', password='123', database='test')
# 数据库操作符，游标，dict取值，默认元组
cur = con.cursor(pymysql.cursors.DictCursor)
# 操作
cur.execute('sql语句')
# 获取返回值，cur类似操作文件的游标指针
ret = cur.fetchone()/ fetchmany(n)/ fetchall()
con.commit()
con.close()
```

- localhost：不过网卡，127.0.0.1过网卡

### 2. 事务和锁

```mysql
# 开启事务
begin; 或者 start transction;
# 查询id值，for update添加行锁；
select * from emp where id = 1 for update;
# 完成更新
update emp set salary=10000 where id = 1;
# 提交事务
commit;
```

### 3. sql注入

```mysql
-- 表示注释掉之后的sql语句
select * from userinfo where name = 'alex' ;-- and password = '792164987034';
select * from userinfo where name = 219879 or 1=1 ;-- and password = 792164987034;
select * from userinfo where name = '219879' or 1=1 ;-- and password = '792164987034';    
```

1. 怎么避免sql注入问题

```python
sql = 'select * from 表'
# 参数为可迭代对象，使用execut拼接
cur.execute(sql, (username, password))
cur.close()
con.close()
```

2. **回滚操作**
   - 修改表中数据必须使用commit() 方法

```mysql
import pymysql
# 打开数据库连接
db = pymysql.connect("localhost","testuser","test123","TESTDB" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
# SQL 插入语句
sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
try:
   cursor.execute(sql) # 执行sql语句
   db.commit()         # 提交到数据库执行
except:
   db.rollback()       # 如果发生错误则回滚
# 关闭数据库连接
db.close()
```

3. **查询操作**
   - Python查询Mysql使用 fetchone() 方法获取单条数据, 使用fetchall() 方法获取多条数据。
   - **fetchone():** 该方法获取下一个查询结果集。结果集是一个对象
   - **fetchall():** 接收全部的返回结果
   - **rowcount:** 这是一个**只读属性**，并返回执行execute()方法后影响的行数。

```mysql
import pymysql
# 打开数据库连接
db = pymysql.connect("localhost", "root", "root", "day40")
# 使用cursor()方法获取操作游标
cur = db.cursor()
# SQL 查询语句
sql = "SELECT * FROM employee \
       WHERE salary > %s" % (1000)
try:
    ret = cur.execute(sql)           # 执行SQL语句
    print(ret)                       # ret为数据行数
    results = cur.fetchall()         # 获取所有记录列表
    for row in results:
        id = row[0]
        name = row[1]
        gender = row[2]
        age = row[3]
        hire_date = row[4]
        print("id=%s,name=%s,gender=%s,age=%s,hire_date=%s"%(id, name, gender, age, hire_date))
except:
    print("Error: unable to fetch data")
# 关闭数据库连接
db.close()
```

## 1.7 数据库优化

- sql优化：索引、尽量那个把条件范围都写在where里，尽量用连表查
- 如何创建表：把固定长度的字段放在前面、分库分表
- innodb中的外键是特有的
- 符合条件的数据，每次都会执行一次select语句

## 数据库平台

### 1. 数据库平台

-   关系型和非关系型
-   如果没有，谁来维护
-   公司有多少台服务器、哪些业务

### 2. mysql

-   5.6、5.7或8.0
-   新业务在尝试使用 5.7 / 8.0
-   表结构设计：资深开发、DBA、架构师带领团队设计、合作完成
-   表之间的关联和多少张表，对应哪些业务，常用的sql
-   数据量

### 3. 设计表结构

-   建立约束和关联
-   查询sql的角度
    -   是否用到了索引，哪里用到了，为什么要用

### 4. sql的查询

### 5. 优化

1.  架构，建表(数据量非常大的时候，千万级)
    1.  分库分表、读写分离(mysql server集群)：select语句执行效率慢，数据量大
        1.  主库：用于修改数据
        2.  从库：读取数据
        3.  一般是从库多，主库少
        4.  默认是异步复制的
            -   binlog：sql语句历史
            -   把binlog日志交给从库
            -   **异步**：不关心复制的结果
            -   **同步**：需要等待复制结果，从ralylog中取出sql二进制命令执行，并写入binlog中，返回结果
            -   **半同步**：ralylog记录主库推过来的binlog，只要写入ralylog就返回结果
        5.  分表
            -   **水平分表**：大表从中间分开，拆分成小表
            -   **垂直分表**：经常查的数据和不常查的数据分开
    2.  尽量把定长的字段放在前面，尽量多使用定长字段
    3.  建立索引
    4.  把固定长度的字段放在前面、分库分表
2.  sql语句
    -   尽量那个把条件范围都写在where里，尽量用连表查
    -   多表查，尽量用连表查代替子查询
    -   命中索引
3.  细节
    -   char 和 varchar 区别
    -   搜索的时候创建一个唯一索引和只创建普通索引index的区别
        -   唯一索引更快