

# redis

## 1. 概念

1.  redis是内存型数据库，断电数据会丢失
3.  selenium操作浏览器时，需要注意浏览器资源释放，防止内存泄漏
4.  redis持久化：防止数据丢失，以文件形式存储
5.  Redis是vmware开发的开源免费的**KV型NoSQL缓存产品**

### 1. redis特性

2.  **redis是c语言编写的**，支持数据持久化，是key-value类型数据库。
2.  redis支持数据备份，高可用也就是master-slave模式
3.  性能极高 – Redis能读的速度是110000次/s,写的速度是81000次/s 。
4.  **原子 – Redis的所有操作都是原子性的**，意思就是要么成功执行要么失败完全不执行。单个操作是原子性的。多个操作也支持事务，即原子性，通过MULTI和EXEC指令包起来。

### 2. 应用场景

1.  Redis 是一个开源（BSD许可）的，内存中的数据结构存储系统，它可以用作**数据库**、**缓存**和**消息中间件**
2.  替代某些场景下的mysql，如社交类app
3.  大型系统中，可以存储session信息，购物车订单

## 2. redis安装

### 1. 安装方式

1.  yum安装，简单，需要配置yum源
2.  源码编译安装，可以指定安装路径，自定制第三方扩展模块功能
3.  rpm安装，需要手动解决依赖关系

### 2. 源码安装

#### 1. 环境准备

```shell
wget http://download.redis.io/releases/redis-4.0.10.tar.gz
tar xzvf redis-4.0.10.tar.gz
```

-   解决依赖包

```shell
yum install gcc patch libffi-devel python-devel  zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel openssl openssl-devel -y
```

#### 2. 释放makefile

-   告诉gcc编译器，redis安装路径
-   如果默认没有configure脚本，但有**makefile**，直接make && make install即可

```shell
make && make install
```

#### 3. 编译完成

-   即可使用redis，启动redis服务端

```shell
redis-server 			# 直接执行
redis-cli				# 测试，ping回显PONG
```

-   redis可执行文件

```shell
./redis-benchmark 		# 用于进行redis性能测试的工具
./redis-check-dump 		# 用于修复出问题的dump.rdb文件
./redis-cli 			# redis的客户端
./redis-server 			# redis的服务端
./redis-check-aof 		# 用于修复出问题的AOF文件
./redis-sentinel 		# 用于集群管理
```

-   云服务器中招了

```shell
kill -9 pid
# 查看定时任务，并编辑**文件的定时任务
crontab -l
crontab -e
# 全局搜索病毒文件，并删除(注意恶意病毒，篡改了文件名)
find / -name 病毒文件
# 找到后 rm -rf 删除
lsattr filename.txt
# 去掉文件的锁,即可删除
chattr -a  -i  filename.txt
```

#### 4. 指定配置文件

-   安全的启动redis服务端
    1.  更改启动端口
    2.  添加redis密码
    3.  开启redis安全模式
-   默认配置文件，redis.conf

```shell
# 过滤出配置文件的有益信息(去掉注释和空白行)
grep -v '^#' redis.conf | grep -v '^$' > myredis.conf
```

#### 5. 指定配置启动

-   test.py

```python
import redis
# redis默认有 16 个库，0-15
conn = redis.StrictRedis(host='172.16.44.142', port=6379, db=0, password='')
conn.set('name', 'henry')
```

-   myredis.conf

```shell
bind 172.16.44.142				# 绑定redis服务器地址
protected-mode yes				# 开启安全模式
port 6800						# 指定端口
requirepass xxx					# 设置密码
pidfile /var/run/redis_6379.pid	# 进程id文件
loglevel notice					# 日志等级
daemonize yes					# 后台运行 
```

-   启动

```shell
redis-server myredis.conf
# 测试
redis-cli -p 6800 -h 172.16.44.142
172.16.44.142:6800> ping
(error) NOAUTH Authentication required.
172.16.44.142:6800> AUTH test
OK
```

## 3. redis数据

### 1. 常用命令

```shell
keys *
type key						# 查看key对应的value类型

expire queue seconds			# 设置过期剩余时间
ttl queue						# 查看剩余时间
persist	queue					# 取消queue的过期时间

dump key						# 序列化 key
randomkey						# 随机返回一个 key
move key db						# 移动 key 到指定db
rename key newkey				# 重命名 key

exists key						# 判断key是否存在
del key							# 删除key，可以删除多个
dbsize 							# 当前库key的数量
flushdb							# 清除redis的所有key
flushall						# 清空所有数据库的所有 key
```

### 2. 数据类型(5)

-   redis是一种高级的key：value存储系统，其中value支持五种数据类型
    1.  字符串（strings）
    2.  散列（hashes）
    3.  列表（lists）
    4.  集合（sets）
    5.  有序集合（sorted sets）

#### 1. 字符串(string)(10)

-   string 类型的值最大能存储 512MB。

-   set系列：set、mset、getset（3）
-   get系列：get、mget、getrange（3）
-   len系列：strlen（1）
-   -+系列：incr、decr（2）
-   append：追加拼接到 value 中

```shell
# string 类型，通过set命令设置
set key value
set 'name' 'xixi'
# 获取指定的key
get 'name'
# key存在，则追加到该key原来值的末尾。
append 'name' 'haha'
# 批量设置和获取
mset 'name' 'henry' 'age' 18
mget 'name' 'age'
# 将已存在 key 的值设为value，并返回key的旧值(old value)
getset name echo
# 返回 key 中字符串值的子字符 value[start, end],包含end
getrange name 1 2
# 获取 name 值的长度
strlen name
# 自增1
incr 'prize'
# 自减1
decr 'prize'
```
#### 2. 散列(hashe)(11)

-   hash 是一个 string 类型的 field 和 value 的映射表，hash 特别适合用于**存储对象**。每个 hash 可以存储 2^32^ -1 键值对（40多亿）

-   set系列：hset、hmset、hsetnx（3）
-   get系列：hget、hmget（2）
-   del系列：hdel（1）
-   k/v系列：hkeys、hvals、hgetall（3）
-   其他：hlen、hexists（2）

```shell
# 将哈希表 key 中的字段 field 的值设为 value
hset stu name 'henry' age '18' height '180' 
# 获取存储在哈希表中指定字段的值
hget stu name
# 如果给定字段已经存在则没有操作被执行
hsetnx key field value

# 同时将多个 field-value (域-值)对设置到哈希表 key 中
hmset key field1 value1 field2 value2 ...
hmset stu name echo age 19
# 获取所有给定字段的值
hmget key field1 field2 ...
hmget stu name height

# 删除一个或多个哈希表字段
hdel key field1 field2 ...
# 查看哈希表 key 中，指定的字段是否存在
hexists key field

# 获取所有哈希表中的字段
hkeys key
# 获取哈希表中所有值
hvals key
# 获取在哈希表中指定 key 的所有字段和值
hgetall key
# 获取哈希表中字段的数量
hlen key
```

#### 3. 列表(list)(13)

-   列表最多可存储 2^32^ - 1 元素 (42 9496 7295, 每个列表可存储40多亿)。

-   push系列：lpush、rpush、lpushx、rpushx（4）
-   pop系列：lpop、rpop、blpop、brpop（4）
-   **range系列：lrange（1）**
-   **index系列：lset、lindex（2）**
-   **其他：ltrim、llen（2）**

```shell
# 双向队列
# 从list左边(右边)插入
lpush/rpush key value1 value2 ...
lpush/rpush test 1

# 索引查看list, [start, end]
lrange test start end	
# 通过索引设置列表元素的值
lset key index value
# 通过索引获取列表中的元素
lindex key index

# 移出并获取列表的第一个(最后一个)元素
lpop/rpop key
# 移出并获取列表的第一个(最后一个)元素，如果列表为空会阻塞直到等待超时或发现可弹出元素为止
blpop/brpop key1 [key2 ] timeout 

# 获取列表长度
llen key
# 对一个列表进行修剪(trim)，就是说，让列表只保留指定区间内的元素，不在指定区间之内的元素都将被删除
ltrim key start stop 						
# 将值插入到已存在的 列表 中
lpushx/rpushx key 
```

#### 4. 集合(set)(8)

-   Redis 的 Set 是 string 类型的无序集合。集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是 `O(1)`。

-   add系列：sadd（1）
-   查看：smembers（1）
-   删除：srem（1）
-   成员：sismember、scard（2）
-   交并集：sdiff、sinter、sunion（3）
-   redis的集合，是一种无序的集合，集合中的元素没有先后顺序。

```shell
# set 集合类型
# 默认是无序的
sadd url 'http://www.baidu.com' 'http://www.jd.com'
# 查看所有的成员
smembers url
# 删除
srem url 'http://www.jd.com'
# 判断是否是集合的元素
sismember url 'http://www.jd.com'

# 列出 url - url2
sdiff url url2
# 返回集合的交集
sinter url url2
# 返回集合的并集
sunion url url2

# 获取成员个数
scard key 
```

#### 5. 有序集合zset(sorted set)

-   和 set 一样也是string类型元素的集合，且不允许重复的成员。不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。zset的成员是唯一的,但分数(score)却可以重复。

```shell
# 向有序集合添加一个或多个成员，或者更新已存在成员的分数
zadd key score1 member1 [score2 member2] 
# 获取成员个数
zcard key 
# 查看成员，闭区间 []
zrange key start end
# 返回指定成员索引
zrank key member
# 删除一个或多个成员
zrem key member1 member2...
```

## 4. redis发布订阅

```shell
# 发布者
publish python 'hello python'
publish python 'hello go'
# 订阅者1
subscribe linux python
# 正则模式订阅
psubscribe python*
# 订阅者2
subscribe go
```

## 5. 持久化

-   **触发机制**
    	1. 手动执行save命令
     2.  或者配置触发条件  save  200   10   #在200秒中内,超过10个修改类的操作

### 1. 方式一：rdb

#### 1. 触发方式

2.  产生了一个经过压缩的二进制文件，保存到磁盘
3.  配置文件
    -   myredis_rdb.conf

```shell
dbfilename dbmp.conf
# 持久化文件保存位置
dir /data/6379
# 每900s只要有1个修改记录就保存一次
save 900 1
save 60 10000
```

```shell
# 启动
redis-server myredis_rdb.conf
```

-   手动触发

```python
save
```

#### 2. 基于快照的持久化

-   基于快照的持久化，速度更快，一般用作备份，主从复制也是依赖于rdb持久化功能

### 2. 方式二：aof

-   AOF（append-only log file），将修改类的操作命令,追加到日志文件中
-   AOF 文件中的命令全部以**redis协议的格式**保存，新命令追加到文件末尾。
-   优点：最大程度保证数据不丢
-   缺点：日志记录非常大

#### 1. aof配置文件

-   aof_redis.json

```python
daemonize yes
port 6379
logfile /data/6379/redis.log
dir /data/6379
dbfilename  dbmp.rdb
requirepass test
save 900 1
save 300 10
save 60  10000
appendonly yes
appendfsync always			# 总是修改类操作
			everysec		# 每秒保存
    		no				# 依赖于系统自带的缓存大小机制
```

#### 2. 基于aof的持久化

-   以追加的方式记录redis操作日志的文件。可以最大程度的保证redis数据安全，类似于mysql的binlog

### 3. rdb方式转换aof

#### 1. 环境准备

-   **确保redis版本在2.2以上**
-   本文在redis4.0中，通过**config set**命令，达到不重启redis服务，从RDB持久化切换为AOF

```shell
# 版本>4.0
redis -v 
# 准备rdb配置文件
daemonize yes
port 6379
logfile /data/6379/redis.log
dir /data/6379
dbfilename  myredis.rdb
bind  127.0.0.1
requirepass test
save 900 1
save 300 10
save  60  10000
# 启动redis
redis-server redis.conf
# 临时生效
redis-cli
# 开启 aof 持久化方式
config set appendonly yes
# 关闭 rdb 持久化方式
config set save ''
# 永久生效，修改配置文件，/etc/redis.conf
# 此时RDB已经正确切换AOF，注意还得修改redis.conf添加AOF设置，不然重启后，通过config set的配置将丢失
appendonly yes
```

## 6. redis主从复制

### 1. redis 支持多实例

-   一台机器可以同时运行多个redis数据库
-   环境准备：运行3个redis数据库，达到1主2从的配置
-   主库：6379.conf
-   从库
    -   6380.conf、6381.conf
    -   `sed 's/6379/6380/' 6379.conf > 6380.conf`
-   开启主从配置功能

#### 1. master库

-   redis.conf

```shell
daemonize yes
bind  127.0.0.1
port 6379
loglevel notice
logfile /data/6379/redis.log
dir /data/6379
pidfile /data/6379/redis.pid
dbfilename dump.rdb
```

#### 2. slave库

-   6380.conf 、6381.conf

```shell
# 6380和 6381配置主从
sed 's/6379/6380/g' redis.conf > 6380.conf
sed 's/6379/6381/g' redis.conf > 6381.conf
# 启动数据库
redis-server redis.conf
redis-server 6380.conf
redis-server 6381.conf
# 修改配置文件
echo 'slave of 127.0.0.1 6379' >> 6380.conf
echo 'slave of 127.0.0.1 6379' >> 6381.conf
# 查看数据库信息
redis-cli info replication
redis-cli -p 6380 slaveof 127.0.0.1 6379
redis-cli -p 6381 slaveof 127.0.0.1 6379
redis-cli info replication
# 主库用于插入数据、从库用于读取，实现读写分离
```

### 2. master故障切换

#### 1. 手动切换 6380 为主库

```shell
# 1. 关闭从库身份
redis-cli -p 6380 slaveof no one
# 2. 设置其他从库的主库
redis-cli -p 6381 slaveof 127.0.0.1 6380
# 3. 修改配置文件中的主从关系
sed -i 's/slaveof 127.0.0.1 6379//g' 6380.conf
sed -i 's/slaveof 127.0.0.1 6379/slaveof 127.0.0.1 6380/g' 6381.conf
```

#### 2. 实现细节

1.  在开启主从复制的时候，使用的是RDB方式的，同步主从数据的
2.  同步开始之后，通过**主库命令传播的方式**，主动的复制方式实现
3.  2.8以后实现PSYNC的机制，实现断线重连

### 3. redis-sentinel主从复制高可用

#### 1. 简介

1.  `Redis-Sentinel`是redis官方推荐的高可用性解决方案，当用redis作master-slave的高可用时，如果master本身宕机，redis本身或者客户端都没有实现主从切换的功能。
2.  `redis-sentinel`就是一个独立运行的进程，用于监控多个master-slave集群，自动发现master宕机，进行自动切换slave --> master。

#### 2. sentinel主要功能

1.  不时的监控redis是否良好运行，如果节点不可达就会对节点进行**下线标识**
2.  如果被标识的是主节点，sentinel就会和其他的sentinel节点“协商”，如果其他节点也认为主节点不可达，就会选举一个sentinel节点来完成自动故障转移
3.  在master-slave进行切换后，master_redis.conf、slave_redis.conf和sentinel.conf的内容都会发生改变，即`master_redis.conf 中会多一行slaveof的配置`，sentinel.conf的监控目标会随之调换

#### 3. 工作方式(8)

1. 每个Sentinel以**每秒钟一次的频率向它所知的Master，Slave以及其他 Sentinel 实例发送一个 PING 命令**

2. 如果一个实例（instance）距离最后一次有效回复 PING 命令的时间**超过 down-after-milliseconds** 选项所指定的值， 则这个实例会被 Sentinel **标记为主观下线**。

3. 如果一个**Master被标记为主观下线**，则正在监视这个Master的**所有 Sentinel 要以每秒一次的频率确认Master的确进入了主观下线状态**。

4. 当有足够数量的 Sentinel（大于等于配置文件指定的值）在指定的时间范围内确认Master的确进入了主观下线状态， 则**Master会被标记为客观下线**

5. 在一般情况下， 每个 Sentinel 会以**每 10 秒一次的频率**向它已知的所有Master，Slave**发送 INFO 命令**

6. 当Master被 Sentinel 标记为客观下线时，**Sentinel 向下线的 Master 的所有 Slave 发送 INFO 命令的频率会从 10 秒一次改为每秒一次**

7. 若没有足够数量的 Sentinel 同意 Master 已经下线， Master 的客观下线状态就会被移除。

8. 若 Master 重新向 Sentinel 的 PING 命令返回有效回复， Master 的主观下线状态就会被移除。

#### 4. 主观下线和客观下线

-   **主观下线**：**Subjectively Down**，简称 SDOWN，指的是当前 Sentinel 实例对某个redis服务器做出的下线判断。
-   **客观下线**：Objectively Down， 简称 ODOWN，指的是多个 Sentinel 实例在对Master Server做出 SDOWN 判断，并且通过 SENTINEL is-master-down-by-addr 命令互相交流之后，得出的Master Server下线判断，然后开启failover.
-   SDOWN**适合于Master和Slave**，只要一个 Sentinel 发现Master进入了ODOWN， 这个 Sentinel 就可能会被其他 Sentinel 推选出， 并对下线的主服务器执行自动故障迁移操作。
-   ODOWN**只适用于Master**，对于Slave的 Redis 实例，Sentinel 在将它们判断为下线前不需要进行协商， 所以Slave的 Sentinel 永远不会达到ODOWN。

### 4. redis-sentinel使用

#### 1. 环境准备

-   三个redis数据库实例，三个配置文件

```shell
# sentinel_6379.conf
port 6379
daemonize yes
logfile "6379.log"
dbfilename "dump-6379.rdb"
dir "/var/redis/data/"

# sentinel_6380.conf 
port 6380
daemonize yes
logfile "6380.log"
dbfilename "dump-6380.rdb"
dir "/var/redis/data/"
slaveof 127.0.0.1 6379

# sentinel_6381.conf 
port 6381
daemonize yes
logfile "6381.log"
dbfilename "dump-6381.rdb"
dir "/var/redis/data/"
slaveof 127.0.0.1 6379
```

#### 2. 启动数据库

```shell
redis-server 6379.conf
redis-server 6380.conf
redis-server 6381.conf
```

#### 3. 哨兵配置

-   三个哨兵监控，三个配置文件
-   sentinel-26379.conf、sentine-26380.conf、sentinel-26381.conf

```shell
# sentinel-26379.conf  
port 26379  
dir /var/redis/data/
logfile "26379.log"

# 当前Sentinel节点监控 127.0.0.1:6379 这个主节点
# 2 代表判断主节点失败至少需要 2 个Sentinel节点节点同意
# mymaster 是主节点的别名
sentinel monitor 127.0.0.1 6379 2

# 每个Sentinel节点都要定期 PING 命令来判断 Redis 数据节点和其余Sentinel节点是否可达，如果超30000毫秒30s且没有回复，则判定不可达
sentinel down-after-milliseconds mymaster 30000

# 当Sentinel节点集合对主节点故障判定达成一致时，Sentinel领导者节点会做故障转移操作，选出新的主节点，
# 原来的从节点会向新的主节点发起复制操作，限制每次向新的主节点发起复制操作的从节点个数为1
sentinel parallel-syncs mymaster 1

# 故障转移超时时间为180000毫秒，3分钟
sentinel failover-timeout mymaster 180000
#加一个后台运行
daemonize yes
```

```python
# sentinel-26380.conf、sentinel-26381.conf
sed 's/26379/26380/g' sentinel-26379.conf > sentinel-26380.conf
sed 's/26379/26381/g' sentinel-26379.conf > sentinel-26381.conf
```

#### 4. 启动哨兵

-   第一次启动后配置文件会自动修改
-   daemonize yes

```shell
redis-sentinel sentinel-26379.conf
redis-sentinel sentinel-26380.conf
redis-sentinel sentinel-26381.conf
# 测试哨兵是否启动成功
redis-cli -p 26379 info sentinel
redis-cli -p 26380 info sentinel
redis-cli -p 26381 info sentinel
```

#### 5. 测试

-   断掉主库检查主从状态

```shell
kill -9 主库的pid
redis-cli -p 6379 info replication
redis-cli -p 6380 info replication
redis-cli -p 6381 info replication
```



## 7. redis-cluster配置

### 0. 结局并发和数据量问题

#### 1. 简介

1.  redis官方生成可以达到 `10万/s`,每秒执行10万条命令
2.  一台服务器内存正常是`16~256G`，假如你的业务需要500G内存
3.  数据量过大
    -   一台服务器内存正常是16~256G，假如你的业务需要500G内存，新浪微博作为世界上最大的redis存储，就超过1TB的数据，去哪买这么大的内存条？
    -   各大公司有自己的解决方案，推出各自的集群功能，**核心思想都是将数据分片（sharding）**存储在多个redis实例中，每一片就是一个redis实例。
4.  各大企业集群方案：
    -   twemproxy由Twitter开源
    -   Codis由豌豆荚开发，基于GO和C开发
    -   redis-cluster官方3.0版本后的集群方案

#### 2. 客户端分片

-   **redis3.0集群采用P2P模式**，完全去中心化，将redis所有的key分成了**16384**个槽位，每个redis实例负责一部分slot，集群中的所有信息通过节点数据交换而更新。
-   redis实例集群主要思想是将redis数据的key进行散列，通过hash函数特定的key会映射到指定的redis节点上

#### 3. 数据分布理论

-   分布式数据库首要解决把整个数据集按照分区规则映射到多个节点的问题，即把数据集划分到多个节点上，每个节点负责整个数据的一个子集。
-   常见的分区规则有**哈希分区和顺序分区**。`Redis Cluster`采用**哈希分区规则**，因此接下来会讨论哈希分区规则。
    1.  节点取余分区
    2.  一致性哈希分区
    3.  **虚拟槽分区(redis-cluster采用的方式)**

#### 4. 哈希分区

-   节点取余

```shell
# 例如按照节点取余的方式，分三个节点
# 1~100的数据对3取余，可以分为三类
1. 余数为0
2. 余数为1
3. 余数为2

# 那么同样的分4个节点就是hash(key)%4
# 节点取余的优点是简单，客户端分片直接是哈希+取余
```

-   一致性哈希

    -   客户端进行分片，哈希+顺时针取余
-   **虚拟槽分区**
    1.  Redis Cluster采用虚拟槽分区
    2.  虚拟槽分区巧妙地使用了哈希空间，使用分散度良好的哈希函数把所有的数据映射到一个固定范围内的整数集合，整数定义为槽（slot）。
    3.  Redis Cluster槽的范围是`0 ～ 16383`。
    4.  槽是集群内数据管理和迁移的基本单位。采用大范围的槽的主要目的是为了方便数据的拆分和集群的扩展，
    5.  **每个节点负责一定数量的槽**。

### 1. 搭建redis cluster

#### 1. 环境准备

-   配置文件：redis-7000.conf、redis-7001.conf、redis-7002.conf、redis-7003.conf、redis-7004.conf、redis-7005.conf
-   仅仅是端口的区别

```shell
port 7000
daemonize yes
dir "/opt/redis/data"
logfile "7000.log"
dbfilename "dump-7000.rdb"

cluster-enabled yes   					#开启集群模式
cluster-config-file nodes-7000.conf		#集群内部的配置文件
# redis cluster需要16384个slot都正常的时候才能对外提供服务，换句话说，只要任何一个slot异常那么整个cluster不对外提供服务。 因此生产环境一般为no
cluster-require-full-coverage no　　	
```

```shell
sed 's/7000/7001/g' redis-7000.conf > redis-7001.conf
sed 's/7000/7002/g' redis-7000.conf > redis-7002.conf
sed 's/7000/7003/g' redis-7000.conf > redis-7003.conf
sed 's/7000/7004/g' redis-7000.conf > redis-7004.conf
sed 's/7000/7005/g' redis-7000.conf > redis-7005.conf
```

#### 2. 启动

```shell
redis-server redis-7000.conf
redis-server redis-7001.conf
redis-server redis-7002.conf
redis-server redis-7003.conf
redis-server redis-7004.conf
redis-server redis-7005.conf
```

#### 3. 分配redis slot 槽位

-   手动编写c语言，分配
-   使用ruby的一个redis 模块，自动分配
-   配置ruby脚本环境

```shell
# 安装
yum install -y ruby
# 使用 ruby和gem
```

-   下载ruby操作redis的模块

```shell
wget http://rubygems.org/downloads/redis-3.3.0.gem
```

-   使用ruby包管理工具安装gem

```shell
gem install -l redis-3.3.0.gem
```

-   通过ruby一键分配槽位

```shell
# 找到redis-trib.rb命令
find / -name redis-trib.rb
# 开启集群开启槽位
/opt/redis-4.0.10/src/redis-trib.rb create --replicas 1 127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005
# 分配好集群后，向集群中写入数据
redis-cli -c -p 7000
set name 'xiake'
```

-   如果执行时报如下错误：

    `[ERR] Node XXXXXX is not empty. Either the node already knows other nodes (check with CLUSTER NODES) or contains some key in database 0`

-   **解决方法**：是删除生成的配置文件`nodes.conf`，如果不行则说明现在创建的结点包括了旧集群的结点信息，需要删除redis的持久化文件后再重启redis，比如：`appendonly.aof、dump.rdb`

## 8. redis的过期策略

### 1. 定期删除

-   redis默认是每隔 100ms 就**随机抽取**一些设置了过期时间的key，检查其是否过期，如果过期就删除。注意这里是随机抽取的。为什么要随机呢？你想一想假如 redis 存了几十万个 key ，每隔100ms就遍历所有的设置过期时间的 key 的话，就会给 CPU 带来很大的负载！

### 2. 惰性删除

-   定期删除可能会导致很多过期 key 到了时间并没有被删除掉。所以就有了惰性删除。假如你的过期 key，靠定期删除没有被删除掉，还停留在内存里，除非你的系统去查一下那个 key，才会被redis给删除掉。这就是所谓的惰性删除，也是够懒的哈！

### 3. redis 提供 6种数据淘汰策略：

1.  volatile-lru：从已**设置过期时间**的数据集（server.db[i].expires）中挑选最近最少使用的数据淘汰
2.  volatile-ttl：从**已设置过期时间**的数据集（server.db[i].expires）中挑选将要过期的数据淘汰
3.  volatile-random：从**已设置过期时间**的数据集（server.db[i].expires）中任意选择数据淘汰
4.  allkeys-lru：当内存不足以容纳新写入数据时，在键空间中，移除`最近最少使用`的key（**这个是最常用的**）
5.  allkeys-random：从数据集（server.db[i].dict）中`任意选择数据淘汰`
6.  no-eviction：`禁止驱逐数据`，也就是说当内存不足以容纳新写入数据时，新写入操作会报错。这个应该没人使用吧

### 4. 4.0版本后增加以下两种：

1. volatile-lfu：从已设置过期时间的数据集(server.db[i].expires)中挑选最不经常使用的数据淘汰
2. allkeys-lfu：当内存不足以容纳新写入数据时，在键空间中，移除最不经常使用的key

# python操作redis

## 1. 安装

```python
# win
下载redis到指定目录，配置PATH即可
# mac
brew install redis
```

## 2. 使用

1.  redis使用 key:value 方式存储，**哈希存储结构{key:value}**
2.  **多次设置同一个key 会被覆盖**

```python
# 终端
redis-cli
# 总共 16 个库，0-15，用来数据隔离
select 8					# 切换 8 号库，默认 0 号库
set key value				# 设置一个健值对，哈希存储结构{key:value}
keys pattern				# 查询当前数据库中所有的key,如keys * 查询当前数据库中所有key
keys a*						# 查询以 a开头
keys *n*					# 包含 n
...
get key						# 查询 key 对应的 value
```

## 3. python操作redis

### 1. 操作单个库

-   --protected-mode no：测试使用，没有设置密码可以使用主机ip
-   安装redis

```python
pip install redis
```

-   使用

```python
from redis import Redis
redis_cli = Redis(host='127.0.0.1', port=6379, db=6)
redis_cli.set('name', 'echo')
```

### 2. 操作 redis-cluster

-   安装redis-py-cluster

```python
pip install redis-py-cluster
```

-    使用

```python
import rediscluster
nodes=[
    {"host":"172.16.44.142","port":7000},
    {"host":"172.16.44.142","port":7001},
    {"host":"172.16.44.142","port":7002},
    {"host":"172.16.44.142","port":7003},
    {"host":"172.16.44.142","port":7004},
    {"host":"172.16.44.142","port":7005}
]
# decode_responses：默认打印 bytes 类型数据
cluster = rediscluster.RedisCluster(startup_nodes=nodes,decode_responses=True)
print(cluster.get('name'))
```

