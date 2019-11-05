```mysql
4.查询有课程成绩小于60分的同学的学号、姓名
先查再连表
select distinct student_id from score where num< 60;
select sid,sname from student right join (
		    select distinct student_id from score where num< 60) as t
			  on student.sid = t.student_id;
			  
先连表再查询
select * from score left join student on student.sid = score.student_id;
select distinct student_id,sname from score 
	               left join 
								 student 
								 on student.sid = score.student_id 
								 where num<60;

5.查询至少有一门课与学号为1的同学所学课程相同的同学的学号和姓名；
select course_id from score where student_id = 1;
select distinct student_id from score where course_id in(
	select course_id from score where student_id = 1)
	and student_id !=1;
	
select student_id,sname from student right join(select distinct student_id from score where course_id in(
	select course_id from score where student_id = 1)
	and student_id !=1) as t1 on t1.student_id = student.sid;

7.查询各科成绩最高和最低的分：以如下形式显示：课程ID，最高分，最低分
select course_id,max(num),min(num) from score group by course_id;

8.查询课程编号“2”的成绩比课程编号“1”课程低的所有同学的学号、姓名；
# 找到课程2的所有人的学号，成绩
select student_id,num num2 from score where course_id = 2;
# 找课程1的所有人的学号，成绩
select student_id,num num1 from score where course_id = 1;
# 连表
select sid1 from (select student_id sid1,num num1 from score where course_id = 1) as t1
		inner join
		(select student_id sid2,num num2 from score where course_id = 2) as t2
		on sid1=sid2 where num1>num2;
# 和student表连表获取学生的姓名
select sid,sname from student right join (
		select sid1 from (select student_id sid1,num num1 from score where course_id = 1) as t1
		inner join
		(select student_id sid2,num num2 from score where course_id = 2) as t2
		on sid1=sid2 where num1>num2
	) as tmp
	on sid1 = sid;
	
9、查询“生物”课程比“物理”课程成绩高的所有学生的学号；
# 连表course 和score
select * from course right join score on score.course_id = course.cid;
select student_id s2,num as bnum from course right join score on score.course_id = course.cid 
		where cname = '生物';
select student_id s1,num as pnum from course right join score on score.course_id = course.cid 
		where cname = '物理';
# 连接同一个学生的物理和生物成绩
select s1 from (select student_id s1,num as bnum from course right join score on score.course_id = course.cid 
		where cname = '生物') as t1 
		inner join
		(select student_id s2,num as pnum from course right join score on score.course_id = course.cid 
		where cname = '物理') as t2
		on t1.s1 = t2.s2 where bnum>pnum;
		
13、查询没学过“张磊老师”课的同学的学号、姓名；
# 连表 课程和老师表，查看张磊老师所教课程
select cid from course inner join teacher on teacher.tid = course.teacher_id where tname='张磊老师';
# 学过张磊老师课程的人
select student_id from score where course_id in (
	select cid from course inner join teacher on teacher.tid = course.teacher_id where tname='张磊老师');
# 找没学过张磊老师课程的人
select sid,sname from student where sid not in (select student_id from score where course_id in (
	select cid from course inner join teacher on teacher.tid = course.teacher_id where tname='张磊老师'));
	
15.查询学过“李平老师”所教的所有课的同学的学号、姓名;
select count(cid) from course inner join teacher on teacher.tid = course.teacher_id where tname='李平老师';

select student_id from score right join 
			(select cid from course 
						inner join 
						teacher on teacher.tid = course.teacher_id where tname='李平老师') as tmp
			on cid = course_id 
			group by student_id having count(sid)=(
							select count(cid) from course inner join teacher 
							on teacher.tid = course.teacher_id where tname='李平老师');
# 获取学生的名字
select sid,sname from student right join (
	select student_id from score right join 
			(select cid from course 
						inner join 
						teacher on teacher.tid = course.teacher_id where tname='李平老师') as tmp
			on cid = course_id 
			group by student_id having count(sid)=(
							select count(cid) from course inner join teacher 
							on teacher.tid = course.teacher_id where tname='李平老师')
) as t on t.student_id = student.sid;

16、查询选修“李平老师”所授课程的学生中，成绩最高的学生姓名及其成绩
# 先知道李平老师所教课程id
select cid from  course left join teacher on teacher.tid =course.teacher_id where tname = '李平老师';

select * from score right join (select cid from  course left join teacher 
								on teacher.tid =course.teacher_id where tname = '李平老师') as courset
			  on courset.cid = course_id
# 取出最高的成绩
select max(num) from score right join (select cid from  course left join teacher 
								on teacher.tid =course.teacher_id where tname = '李平老师') as courset
			  on courset.cid = course_id;
# 
select student_id,mnum from (select * from score right join (select cid from  course left join teacher on teacher.tid =course.teacher_id where tname = '李平老师') as courset
		  on courset.cid = course_id) as stu_num
		right join 
		(select max(num) mnum from score right join (select cid from  course left join teacher 
							on teacher.tid =course.teacher_id where tname = '李平老师') as courset
		  on courset.cid = course_id) max_num
		on max_num.mnum = stu_num.num;

# 查出名字
select sname,mnum from student right join(
	select student_id,mnum from (select * from score right join (select cid from  course left join teacher on teacher.tid =course.teacher_id where tname = '李平老师') as courset
			on courset.cid = course_id) as stu_num
			right join 
			(select max(num) mnum from score right join (select cid from  course left join teacher 
								on teacher.tid =course.teacher_id where tname = '李平老师') as courset
			  on courset.cid = course_id) max_num
			on max_num.mnum = stu_num.num
	) as maxt on maxt.student_id = student.sid;

17、查询各个课程及相应的选修人数；
select course_id,count(sid) from score group by course_id;
select cid,cname,cnum from course right join (select course_id,count(sid) cnum from score group by course_id) as t
		on t.course_id = course.cid;

18、查询不同课程但成绩相同的学生的学号、课程号、学生成绩；
select distinct s1.student_id,s2.student_id,s1.course_id,s2.course_id,s1.num from score as s1,score as s2 where s1.num = s2.num and s1.course_id != s2.course_id;

19、查询每门课程成绩最好的前两名；
# 方法一
select course_id,max(num)from score s2 group by course_id;

select score.course_id,max(num) from score left join (select course_id,max(num) max_num from score s2 group by course_id) as tmp
			 on score.course_id = tmp.course_id where max_num != num group by score.course_id;
# 方法二
select t1.course_id,num1,num2 from(
select course_id,(select concat(student_id,':',num) from score as s1 where s1.course_id=s2.course_id order by s1.num desc limit 0,1) as num1
	from score s2 group by course_id) as t1
	inner join(select course_id,(select concat(student_id,':',num) from score as s1 where s1.course_id=s2.course_id order by s1.num desc limit 1,1) as num2
	from score s2 group by course_id) as t2
	on t1.course_id = t2.course_id;

22、查询没学过“张磊老师”讲授的任一门课程的学生姓名；
SELECT DISTINCT sid, sname FROM student RIGHT JOIN 
	(SELECT student_id FROM score LEFT JOIN 
		(select cid from teacher inner join course on course.teacher_id = teacher.tid where tname = '张磊老师') 
		t1 ON course_id=cid WHERE cid is NULL
	) t2 ON sid = student_id;
```

