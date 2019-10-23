# Mogodb

-   port：27017，mysql：3306，redis：6379
-   NoSQL 不仅仅只是SQL

### 1. mongodb中概念

1.  使用不存在的对象即创建该对象
2.  Json结构存储。dict用法

#### table1-1 mysql和mongodb对比

| 称呼   | MySQL    | MongoDB               |
| ------ | -------- | --------------------- |
| 数据库 | database | database              |
| 数据表 | Tables   | Collections(本质是表) |
| 数据列 | Colum    | Field(字段)           |
| 数据行 | Row      | Documents             |


### 2. 数据类型(8)

-   F6：执行（nosqlbooster-for-mongodb）

```python
ObjecgtID : Documents 自动生成的 _id，时间戳+机器码(mac地址序列化结果)+PID+计数器(整个数据库的计数器，会共享给server中的其他Mongodb)
string							# 必须是 utf-8的字符
Boolean							# true/false
Integer							# 整数据(int32, int64)
Double							# 不指定默认是double，所有小数在mongo中都是double，mongodb不存在float
Array							# 类似python中的 list
Object							# python中的dict，其他语言都叫object
Null							# 空
Timestamp						# 时间戳

db.users.insert({data:ISODate()})
```

### 3. 常用操作

#### 1. 使用数据库

-   启动数据库

```python
mongod							# 启动mongodb服务
mongod --dbpath='/data/db'		# 指定数据库存放路径 /data/db
mongod --port=27017				# 指定使用的端口号
mogo							# 启动客户端
```

-   基本操作

```python
> show databases				# 查看当前数据库中磁盘中的数据库
> use dbname					# 切换当前使用的数据库
> db							# 查看当前使用的数据库，代指当前数据库名
> use xxx						# use不存在的库，在内存中创建数据库空间，只有数据时，才会存到磁盘中
> db.users						# users不存在时，在内存中创建数据表空间
> show tables					# 查看当前数据库中磁盘中的数据表
```

#### 2. 增删改查

```python
db.users.insert({})				# 增加数据
db.users.insert([{name:'henry',age:19}, {name:'echo',age:18}])
db.users.find()					# 查询当前数据表中的所有数据
```

#### 3. 条件查询(4)

-    $and：并列条件

```python
db.users.find({age:19})			# 查询所有符合条件的数据
db.users.find({name:'henry',age:19}) # 并列方式查询
```

```python
db.users.find({'$and':[{name:'henry'},{age:19}]})
```

-   $or：或条件 

```python
db.users.find({'$or':[{age:19}, {name:'echo'}]}) 
```

-   $in ：包含或者，同一字段或者条件，**必须是交集**

```python
# 或者
db.users.find({age:{'$in':[18, 19, 20]}}) 
```

-   $all：**必须是子集**

```python
db.users.find({hobby:[1,2,3,4,5]}) 
db.users.find({hobby:{'$all':[3,5,1]}}) 
```

#### d4. 范围查询

-   数学比较符($gt/lt/get/let/eq/ne)

```python
db.users.find(age{'$gt':19})
db.users.find(age{'$lt':19})
db.users.find(age{'$gte':19})
db.users.find(age{'$lte':19})
db.users.find(age{'$eq':19})	# 用在并列、或条件中
db.users.find(age{'$ne':19})	# 除了age=19的所有数据(没有age字段和age！=19)
```

-   Object查询可以直接使用**对象.属性**，作为key
    -   当Array中出现Object会自动遍历其中的属性

```python
db.users.find({hobby:2})
```

#### 5. 更改update()

1.  db.tablename.update({查询条件},` $修改器:{修改内容})`
2.  查询并修改符合条件的**第一条数据**
3.  $：**修改器**(单个字段进行修改)
    1.  $set：强制将某值修改覆盖，如果不存在则创建
    2.  $unset：强制删除一个字段
    3.  $inc：自增

-   **单个对象修改(3个修改器)**

```python
# $set：设置属性
db.users.update({'name':'echo'}, {'$set':{'name':'dean'}})
db.users.update({'name':'echo'}, {'$set':{'name':'dean','age':28, 'gender':1}})
# $unset：删除属性，任意值都会生效
db.users.update({'name':'echo'}, {'$unset':{'gender':任意值}})
# $inc：引用属性，增加(-1减少)
db.users.update({'name':'echo'}, {'$inc':{age:1}})
```

-   **针对`$array`的修改器，以及 $ 关键字用法和特殊性**
    -   array--> `$push $pull $pop $pushAll $pullAll`
    -   pop和push的方向是一致的
    -   pull 和 pullAll：删除一个值，批量删除

```python
# $push：追加
db.users.update({'name':'echo'}, {'$push':{'hobby':123}})
# $pop：只能删除array第一条(-1)或最后一条(1)的数据
db.users.update({'name':'echo'}, {'$pop':{'hobby':1/-1}})
```

```python
# $pushAll：批量增加 (3.6版本被废弃)
db.users.update({'name':'echo'}, {'$pushAll':{'hobby':[a,b,c]}})

# $pull：删除符合条件的所有元素(python的 remove)
db.users.update({name:'henry'}, {'$pull': {hobby:6}})
# $pullAll：批量删除符合条件的元素
db.users.update({'name':'echo'}, {'$pullAll':{'hobby':[3,4,5]}})
```

-   **$关键字的特殊用法：保存符合条件的下标。只能存储一层遍历的索引**
    -   array和object：会发生遍历
    -   此时：'hobby.$ '必须加引号

```python
db.users.update({'hobby':0}, {'$set':{'hobby.$':123}})
db.users.update({'hobby':0}, {'$set':{'hobby.9':123}})
```

#### 6. 删除

```python
# 删除所有数据
db.Tables.remove({})
# 删除一条数据，只删除第一一条
db.users.remove({}, {justOne: true})
db.users.remove({name:'oleg'}, {justOne:true})
```

#### 7. 官方推荐

-   插入：insertOne和insertMany

```python
db.tablename.insertOne({'name':'dianel'})
db.tablename.insertMany([{'name':'dianel'},{'name':'oleg'}])
```

-   查询：findOne和find

```python
# 查询符合条件的第一条数据
db.tablename.findOne({'name':'dianel'})
# 查询符合条件的所有数据
db.tablename.find({'name':'dianel'})
```

-   修改：updateOne和updateMany

```python
# 修改符合条件的第一条数据
db.tablename.updataOne({},{})
# 更新所有数据，没有则增加
db.tablename.updataMany({},{'inc':{age:1}})
```

-   删除：deleteOne和deleteMany

```python
# 删除符合条件的第一条数据，从头删除
db.tablename.deleteOne({age:19})
# 删除符合条件的所有数据
db.tablename.delete({age:1})
```

### 4. 高级函数

-   排序：sort > 跳过：skip > 筛选：limit (优先级次序，mongodb内部逻辑)
-   count()：计算查找到数据的条数

```python
# 升序排序，-1则为逆序
db.users.find({}).sort({age:1})
# 筛选前 -3(n) 条
db.users.find({}).limit(-3)
# 跳过前 3(n) 条
db.users.find({}).skip(3)
# 顺序任意
db.users.find({}).skip(4).limit(2)
db.users.find({}).limit(2).skip(4)
# 分页
page = 页码 = 1
count = 条目 = 2
db.users.find({}).limit(count).skip((page-1)*count).sort({字段:-1})
```

### 5. pymongo

#### 1. 下载pymongo

```python
pip install pymongo
```

#### 2. 使用

-   find_one：pep8规范，下划线命名
-   如果查询 _id：id值必须带上`ObjectId('xxxxxx')`

```python
from pymongo import MongoClient
from bosn import ObjectId
MC = MongoClinet('127.0.0.1', 27017)
MongoDB = MC['day93']
# 插入数据时，返回 inserted_id/inserted_ids
# 类型是：<class 'bson.objectid.ObjectId'>
res = MongoDB.Users.insert_one({'name':'iris', 'age':20})
print(res.inserted_id, type(res.inserted_id))
# 通过 _id 进行查找
res = MongoDB.Users.find_one({'_id':ObjectId(res)})
print(res)

# cursor是一个生成器
for row in res:
    print(row)
```

-   批量插入

```python
res = MongoDB.Users.insert_many([{'name':'iris', 'age':20},{'name':'oleg', 'age':20}])
# list类型[ObjectId(), ObjectId()...]
print(res.inserted_ids, type(res.inserted_ids))
```

-   更新数据

```python
# 只更新第一条数据
res = MongoDB.Users.update_one({}, {'$inc':{age:1}})
# 更新所有
res = MongoDB.Users.update_many({'age':20}, {'$inc':{age:1}})
```

-   删除数据

```python
# 删除第一条数据
res = MongoDB.Users.delete_one({})
# 删除所有数据
res = MongoDB.Users.delete_many({})
```

-   **高级函数**

```python
# 选择 3(n) 条数据
res = MongoDB.Users.find({}).limit(3)
for row in res: print(row)
    
# 跳过 3(n) 条数据
res = MongoDB.Users.find({}).skip(3)
for row in res: print(row)

# 排序
from pymongo import DESCENDING, ASCENDING
res = MongoDB.Users.find({}).sort('age', DESCENDING)
res = MongoDB.Users.find({}).sort({'age':-1}) # -1会报错
for row in res: print(row)
```

