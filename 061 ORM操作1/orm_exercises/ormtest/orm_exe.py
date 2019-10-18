#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_exercises.settings")
django.setup()

from app01 import models
from django.db.models import Max, Count

"""
1.查找所有书名里包含金老板的书
"""
# obj = models.Book.objects.filter(title__contains='金老板')
# for i in obj:
#     print(i)

# select * from app01_book where title like '%金老板%';

"""
2.查找出版日期是2018年的书
"""
# obj = models.Book.objects.filter(publish_date__year=2018)
# for i in obj:
#     print(i)

# select * from app01_book where year(publish_date)=2018;
"""
3.查找出版日期是2017年的书名
"""
# obj = models.Book.objects.filter(publish_date__year=2017).values_list('title')
# for i in obj:
#     print(i)

# mysql> select title from app01_book where year(publish_date)=2017;
"""
4.查找价格大于10元的书
"""
# obj = models.Book.objects.filter(price__gt=10).values('title')
# for i in obj:
#     print(i)

# mysql> select * from app01_book where price > 10;
"""
5.查找价格大于10元的书名和价格
"""
# obj = models.Book.objects.filter(price__gt=10).values('title', 'price')
# for i in obj:
#     print(i)

# mysql> select title,price from app01_book where price > 10;
"""
6.查找memo字段是空的书
"""
# obj = models.Book.objects.filter(memo__isnull=True)
# for i in obj:
#     print(i)

# mysql> select title from app01_book where memo is null;
"""
7.查找在北京的出版社
"""
# obj = models.Publisher.objects.filter(city='北京')
# for i in obj:
#     print(i)

# mysql> select name from app01_publisher where city='北京';
"""
8.查找名字以沙河开头的出版社
"""
# obj = models.Publisher.objects.filter(name__startswith='沙河')
# for i in obj:
#     print(i)

# mysql> select name from app01_publisher where name like '沙河%';
"""
9.查找“沙河出版社”出版的所有书籍
"""
# obj = models.Book.objects.filter(publisher__name='沙河出版社').values('title')
# for i in obj:
#     print(i)

# select * from (select title, name from app01_publisher t1 inner join app01_book t2 on t1.id=t2.publisher_id) t3 where t3.name='沙河出版社';

"""
10.查找每个出版社出版价格最高的书籍价格  ?
"""
obj = models.Book.objects.values('publisher_id').annotate(maxprice=Max('price')).values('publisher_id', 'maxprice')
# obj = models.Publisher.objects.annotate(max=Max('book__price')).values('max', 'id', 'name', 'book__title')
# print(obj)
# for i in obj:
#     print(i)


# select title, max(price),name from (select title,price,name from app01_book t1 inner join app01_publisher t2 on t1.publisher_id = t2.id) t3 group by name;
"""
11.查找每个出版社的名字以及出的书籍数量  ?
"""
# obj = models.Book.objects.values('publisher__name').annotate(nums=Count('id')).values('publisher__name', 'nums')
# for i in obj:
#     print(i)


# select title,count(title),name from (select title,price,name from app01_book t1 right join app01_publisher t2 on t1.publisher_id = t2.id) t3 group by name;

"""
12.查找作者名字里面带“小”字的作者
"""
# obj = models.Author.objects.filter(name__contains='小')
# for i in obj:
#     print(i)

# select * from app01_author where name like '%小%'
"""
13.查找年龄大于30岁的作者
"""
# obj = models.Author.objects.filter(age__gt=30)
# for i in obj:
#     print(i.name)

# select * from app01_author where age > 30;
"""
14.查找手机号是155开头的作者
"""
# obj = models.Author.objects.filter(phone__startswith='155')
# for i in obj:
#     print(i.name)

# select * from app01_author where phone like '155%';
"""
15.查找手机号是155开头的作者的姓名和年龄
"""
# obj = models.Author.objects.filter(phone__startswith='155').values('name', 'age')
# for i in obj:
#     print(i)


# select name,age from app01_author where phone like '155%'
"""
16.查找每个作者写的价格最高的书籍价格 ?
"""
# obj = models.Author.objects.annotate(maxprice=Max('book__price')).values('name', 'maxprice')
# for i in obj:
#     print(i)


# select name, max(price) from (select t1.id,t1.name, t2.book_id from app01_author t1 inner join app01_book_author t2 on t1.id=t2.author_id) t3 inner join app01_book t4 on t3.book_id=t4.id group by name;
"""
17.查找每个作者的姓名以及出的书籍数量 ?
"""
# obj = models.Author.objects.annotate(nums=Count('book__id')).values('name', 'nums')
# for i in obj:
#     print(i)
# select name, count(book_id) from (select t1.id,t1.name, t2.book_id from app01_author t1 inner join app01_book_author t2 on t1.id=t2.author_id) t3 inner join app01_book t4 on t3.book_id=t4.id group by name;

"""
18.查找书名是“跟金老板学开车”的书的出版社
"""
# obj = models.Book.objects.get(title='跟金老板学开车').publisher.name
# print(obj)

# select name from ((select publisher_id from app01_book where title='跟金老板学开车')  t1  inner join app01_publisher t2 on t1.publisher_id=t2.id) ;
"""
19.查找书名是“跟金老板学开车”的书的出版社所在的城市
"""
# obj = models.Book.objects.get(title='跟金老板学开车').publisher.city
# print(obj)

# select name,city from ((select publisher_id from app01_book where title='跟金老板学开车')  t1  inner join app01_publisher t2 on t1.publisher_id=t2.id) ;
"""
20.查找书名是“跟金老板学开车”的书的出版社的名称
"""
# obj = models.Book.objects.get(title='跟金老板学开车').publisher.name
# print(obj)


# select name from ((select publisher_id from app01_book where title='跟金老板学开车')  t1  inner join app01_publisher t2 on t1.publisher_id=t2.id) ;
"""
21.查找书名是“跟金老板学开车”的书的出版社出版的其他书籍的名字和价格
"""

# books = models.Book.objects.filter(publisher_id=models.Book.objects.get(title='跟金老板学开车').publisher_id)
# for i in books:
#     if i.title != '跟金老板学开车':
#         print(i)


# select * from app01_book where publisher_id not in  (select publisher_id from app01_book where title='跟金老板学开车');
"""
22.查找书名是“跟金老板学开车”的书的所有作者
"""
# obj = models.Book.objects.get(title='跟金老板学开车').author.all().values('name')
# print(obj)

# authors = models.Author.objects.filter(book__title='跟金老板学开车')
# for i in authors:
#     print(i)


# select * from (select author_id from (select id bid from app01_book where title='跟金老板学开车') t1 inner join app01_book_author t2 on t1.bid=t2.book_id) t3 inner join app01_author on t3.author_id=app01_author.id;
"""
23.查找书名是“跟金老板学开车”的书的作者的年龄
"""
# authors = models.Author.objects.filter(book__title='跟金老板学开车').values('age')
# print(authors)


# select name,age from (select author_id from (select id bid from app01_book where title='跟金老板学开车') t1 inner join app01_book_author t2 on t1.bid=t2.book_id) t3 inner join app01_author on t3.author_id=app01_author.id;
"""
24.查找书名是“跟金老板学开车”的书的作者的手机号码
"""
# authors = models.Author.objects.filter(book__title='跟金老板学开车').values('phone')
# print(authors)

# select name,phone from (select author_id from (select id bid from app01_book where title='跟金老板学开车') t1 inner join app01_book_author t2 on t1.bid=t2.book_id) t3 inner join app01_author on t3.author_id=app01_author.id;

"""
25.查找书名是“跟金老板学开车”的书的作者们的姓名以及出版的所有书籍名称和价钱
"""
# author = models.Author.objects.filter(book__title='跟金老板学开车')
# books = models.Book.objects.filter(author__id__in=author)
# for i in author:
#     print(i)
# for i in books:
#     print(i)


# select name,price from (select name,book_id  from (select name, id nid from (select author_id from (select id bid from app01_book where title='跟金老板学开车') t1 inner join app01_book_author t2 on t1.bid=t2.book_id) t3 inner join app01_author on t3.author_id=app01_author.id) t4  inner join app01_book_author t5 on t4.nid=t5.author_id) t6 inner join app01_book on t6.book_id=app01_book.id;

# f = models.Author.objects.filter(pk=1).exists()
# print(f)

obj = models.Author.objects.filter(book__title='跟金老板学开车').values('name', 'book__title', 'book__publisher__name')
for i in obj:
    print(i)