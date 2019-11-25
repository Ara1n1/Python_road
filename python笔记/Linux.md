1u and 2u

2. top500.org
3. CPU：Central Processing Unit
4. DDR2：240-pin DDR 184-pin
5. Graphic Processing Unit
6. Hot swap
7. 1U = 44.45mm
8. BSD：tcp/ip, unix
9. kernel.org
10. 5.2.4：主版本号、次版本号、末版本号
11. GPL
12. aliyun

# 1. Centos简介

服务器密码要求：

- 12位及其以上
- 必须包含大写字母，小写字母，数字，特殊字符
- 3个月或者半年更换一次

## 1. 虚拟机

- vmware
- virturl box(orcle)
- 作用：通过软件模拟生成硬件信息

1. 桥接：会跟主机获取同一网段ip地址
2. net：会进行地址转换

## 2. 终端

1. 图形终端：/dev/tty7
2. 虚拟终端(ctrl+alt+f1-6) /dev/tty#
3. 伪终端：/dev/pts/id
4. 物理终端
5. 设备终端
6. 串行终端

```SHELL
# chvt N 命令切换到前台终端 N，这与按CTRL+ALT+Fn相同。如果它不存在，则创建相应的屏幕。
# 进入/dev/tty2
chvt 2
chvt 1    # 退出
fgconsole # 查看活动虚拟控制台的总数
fgconsole --next-available # 查看下一个未分配的虚拟终端
deallocvt # 移除未使用的虚拟终端
```

```SHELL
# 查看主机地址
ifconfig
ip a/addr
# 查看终端
tty
```

- 交互式接口
- 启动终端后，在终端设备上会打开一个接口
- GUI：图形接口
- 命令行CLI：shell、powershell
- Shell
  - sh、csh、tcsh
  - ksh、bash（linux、mac上的shell）、zsh
  - 用来在linux系统上的一个接口，用来将用户的输入发送给操作系统执行，并把得到的结果输出出来
- **linux定义变量不能有空格**

```SHELL
# 查看系统支持的shell
cat /etc/shells
# 切换shell
chsh -s /bin/bash
# 查看当前shell
echo $SHELL
# #号表示root用户
# 用户@主机名 当前目录 身份
[root@localhost /]# 
# $号表示普通用户
[henry@localhost /]$
```

## 3. 修改提示符格式

```SHELL
PS1="\[\e[1;5;41;33m\][\u@\h \W]\\$\[\e[0m\]"
\e 
\h 主机名简称
\w 当前工作目录 \t 24小时时间格式 \! 命令历史数
\u 当前用户
\H 主机名
\W 当前工作目录基名 \T 12小时时间格式
\# 开机后命令历史数
1表示字体加粗， 0表示默认字体。4表示给字体加上下划线。5表示字体闪烁。7表示用亮色突出显示，来让你的文字更加醒目
31表示字符颜色。
可选颜色：红色、绿色、黄色、蓝色、洋红、青色和白色。他们对应的颜色代码是：30（黑色）、31（红色）、32（绿色）、 33（黄色）、34（蓝色）、35（洋红）、36（青色）、37（白色）
40表示字符背景色。可选颜色 40、41、42、43、44、45、46、47
```

```SHELL
# 查看主机信息
[root@localhost ~]# echo $PS1
[\u@\h \W]\$
# 更改用户
[root@localhost ~]# PS1="\[\e[1;30;35m\][\u@\h \W]\\$\[\e[0m\]"
# 更改用户信息的配置文件,即永久生效
# 向文件中追加信息
echo 'PS1="\[\e[1;30;35m\][\u@\h \W]\\$\[\e[0m\]"'>> /etc/profile.d/ps.sh(自定义名称,后缀必须是.sh)
```

## 4. Linux基础命令

1. 内部命令：安装完系统以后自带的命令
2. 外部命令：第三方命令，在某些地方可以直接找到执行文件

```SHELL
# 获取内部命令列表
[root@3ad30f522613 ~]# help
# 查看是命令类别
[root@3ad30f522613 ~]# type echo
echo is a shell buildin
# 查找命令的路径，在PATH变量中寻找
which cp
# 列出所有别名
alias
# 定制、取消别名
alias ce='cd /etc'
unalias ce
# 修改 ～/.bashrc 文件，当前用户有效
echo 'alias ce='cd /etc' >> ~/.bashrc
# 所有用户生效
echo 'alias ce='cd /etc' >> /etc/bashrc
# 执行本身含义
"ls"  'ls'	\ls
# 单双引号的区别
echo "$name"  # 打印name变量
echo ${name}	# 打印name变量
echo '$name'	# 打印name变量名
```

## 5. 常用命令

### 0. 格式

```SHELL
# 选项：启用或禁用某些功能(短选项-a和长选项--all)
# 参数：命令的作用对象，一般为目录、用户等
command [options] [args...]
# 注意
1. 多个选项及参数和命令之间需要空格隔开
2. ctrl + c：取消命令执行
3. 同时执行多个命令，用分号隔开
4. 换行command + \，使用\将命令切换成多行s
```

### 1. 时间相关

#### 1. date

1. F：年月日
2. H/I：小时(24/12)
3. y/m/d/H/M/S
4. a/A：二/星期二
5. T：时分秒
6. s：时间戳
7. W：第几周

```SHELL
# 显示完整时间
date 
# 显示年月日
date +%F
# 显示24小时
date +%H
# 显示12小时
date +%I
# 年月日，时分秒
data +%y
data +%m
data +%d
date +%H
data +%M
data +%S
# 星期
date +%a
date +%A
# 打印完整时间
date +%T
# 自定义格式
date +%Y-%m-%d
date +%Y-%m-%d\ %H:%M   # 可以使用\ 表示转义
# unix元年，1970.01.01 0:0:0，时间戳
date +%s
# 显示多少周
date +%W
```

#### 2. timedatectl

```shell
# 显示时区
timedatectl
# 设置时区
timedatectl set-timezone Asia/Shanghai
timedatectl set-timezone UTC
timedatectl set-time 15:58:30
timedatectl set-time 20151120
timedatectl set-time '16:10:40 2015-11-20'
# 查看所有时区
timedatectl list-timezones
# 将你的硬件时钟设置为本地时区
timedatectl set-local-rtc 1
# 将你的硬件时钟设置为协调世界时（UTC）
timedatectl set-local-rtc 0
```

#### 3. cal

```SHELL
# 查看日历，一个月
cal
# 查看日历，当前月以及上个月和下个月
cal -3
# 显示一年日历
cal -y
# 显示2018年日历
cal -y 2018
```

### 2. 关机、重启

```SHELL
# 默认一分钟后关机
shutdown # 所有用户都会收到此消息
# 重启，一分钟之后
shutdown -r 
# 取消
shutdown -c
# 指定时间关机
shutdown -r now/hh:mm/+6(6分钟之后)

# 直接重启
reboot
# -p表示切断电源
reboot -p 
# 重启
init 6

# 关机
init 0
# 关机
poweroff
```

### 3. xshell

```SHELL
# 快速退出
ctrl + d 
```

# 2. 常用命令1

```shell
cat /etc/redhat-release 			# 查看redhat发行版本
cat	/etc/os-release					# 查看linux发行版本
```

-   通过vmware esxi企业版虚拟化技术，创建虚拟机

## 1. 终端操作

### 1. 终端快捷键(13)

- 需要注意，alt会跟别的快捷键冲突

```SHELL
control + L  # 清屏
control + s  # 锁定屏幕 !
control + q  # 解锁 !
control + c  # 终止命令
control + a  # 移动 cursor 到行首
control + e  # 移动 cursor 到行尾
control + xx # 移动 cursor 到上次位置 !
control + u  # 删除到行首
control + k  # 删除到行尾
control + d  # delete
alt + r		 # 删除整行
alt+f        # 光标向右移动一个单词尾
alt+b        # 光标向左移动一个单词首
```

### 2. 补全功能

1. 外部变量/命令补全：**cp**
   - Shell 会根据**环境变量**从左到右依次查找，找到第一个匹配的则返回
   - 如果部分命令只能搜索到一个则可以使用tab 补全
   - 如果有多个则使用两次tab提示
2. 目录补全
   - 把用户给定的目录字符串只能搜索到一个则直接补全
   - 如果匹配到多个则使用两次tab显示所有文件目录列表
3. 回显echo
   - 输入什么就输出什么，并加入一个换行符

```SHELL
# 获取环境变量
$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

### 3. 帮助

#### 1. 内部命令

- help command
- man bash

#### 2. 外部命令

- `command --help/-h`
- man command(**q退出**)
- 官方文档

#### 3. Man

- 9个章节

```SHELL
# 显示man
man man
1 用户命令
2 系统调用(内核提供的功能)
3 c库调用
4 设备文件
5 配置文件
6 游戏
7 其他
8 管理类命令
9 linux内核api
```

## 2. 目录结构

### 1. 结构(4)

1. 树形结构
2. 目录严格区分大小写
3. 隐藏文件以 . 开头
4. 路径分隔符为 /

### 2. 文件命令规范(4)

1. 文件名最长为255个字符
2. 包括路径在内最长4095个字符
3. 除了 / 和 NULL 以外，其他字符都生效
4. 大小写敏感

### 3. 颜色表示(6)

1. 蓝色：表示目录
2. 绿色：表示可执行文件
3. 红色：表示压缩文件
4. 蓝绿色：表示链接文件
5. 白色：普通文件
6. 灰色：其他文件
7. 蓝底白字：硬链接
8. 红底黑字：软链接，原文件被删除

### 4. 文件系统结构(20)

```SHELL
/			# 根目录
/boot   	# 存放系统引导文件(内核文件、引导加载器)
/run		# 服务或系统启动后生成的文件
/etc    	# 配置文件
/home   	# 普通用户的家目录
/root 		# root用户家目录

/bin    	# 所有用户均可使用的命令
/sbin   	# 管理员可以使用的命令，管理类命令
/lib		# 基本库文件，win的 *.dll, linux的 *.so
/lib64  	# 专门用于64位操作系统的一些辅助库文件

/media		# 便携式文件的挂载点
/mnt		# 临时文件的挂载，光盘、u盘
/tmp		# 存放临时文件
/srv		# 系统上允许的服务用到的数据
/opt		# 一般第三方的安装程序
/usr		# 安装程序
/var		# 存放经常变化的数据，如：日志(/var/log), message:系统启动日志，sssd:链接的用户信息，secure:其他用户登录信息
/proc		# 存放内核和进程的虚拟文件
/dev	    # 存放设备信息
/sys		# 存放硬件相关的虚拟文件
```

| 二进制文件      | 库文件           | 配置文件         | 帮助文件             |
| --------------- | ---------------- | ---------------- | -------------------- |
| /bin            | /lib             | /etc/*           | /usr/share/man       |
| /sbin           | /lib/64          | /usr/local/etc/* | /usr/share/doc       |
| /usr/bin        | /usr/lib         |                  | /usr/local/share/man |
| /usr/sbin       | /usr/lib64       |                  | /usr/local/share/doc |
| /usr/local/bin  | /usr/local/lib   |                  |                      |
| /usr/local/sbin | /usr/local/lib64 |                  |                      |

### 5. 相对路径和绝对路径

- 绝对路径：从根开始，完整路径，可以找到任何存在的文件
- 相对路径：相对于某个文件或目录开始，可以使用简短的形式
  - .. 代表父目录， . 代表当前路径

```SHELL
# esc . 获取上条命令的参数
# 获取文件名
basename /etc/sysconfig/network-scripts/ifcfg-ens33
# 获取文件目录
dirname /etc/sysconfig/network-scripts/ifcfg-ens33
```

## 3. 常用命令

### 1. cd pwd

- 可以使用相对路径也可以使用绝对路径

```SHELL
cd /opt
cd ../etc
# 直接回到用户家目录
cd
# 回到上次目录
cd -
# 查看当前目录的绝对路径，print working directory
pwd
```

### 2. ls

#### 1. 参数

1. -a / —all：表示所有(-A除了 . 和 ..)
2. -l：使用长格式显示，显示**mtime**
3. -R：递归显示指定文件中的所有文件
4. -S：根据文件大小降序显示
5. -u
   - with -lt 按照atime排序，the newest first
   - with -l 不排序，显示atime
   - 按照atime排序显示
6. -t：根据修改时间排序，the newest first
7. -c
- with -lt 表示按照ctime排序显示
   - with -l 不排序，显示ctime
   - 按照ctime排序
8. -d：只显示目录文件
9. -h：自动调节文件大小的单位(一般和l连用)

```SHELL
# 查看所有文件
ls -a / --all
# 长格式显示文件
ls -l
# ls -la
# 递归查看某个目录下的文件
ls -R /etc
# 长格式显示目录本身
ls -ld 目录名
# 竖着显示文件
ls -1 /etc
# 根据文件的大小进行排序
ls -lS /    # 降序
ls -lSr /   # 升序
# 只能显示当前目录下的目录
ls -d */
# 自动调节文件大小的单位(一般和l连用)
ls -h /
```

### 3. touch

- 创建新文件、修改文件的时间戳

#### 1. 用法

- touch [选项]... 文件...

#### 2. 参数

- -a 仅改变atime 和ctime
- -m 仅改变mtime和ctime

```SHELL
touch a.txt			# 文件不存在创建，存在则修改时间戳
touch a{1..10}  	# 命令的展开
touch a{a..z}
touch a{1..10..2}
touch a{a..z..2}
echo a{1..10}
```

### 4. history

- 命令保存在 ～/.bash_history中
- 当用户登录系统后，会去读取 ～/.bash_history的内容，在正常退出后会把历史保存到改文件中

```SHELL
键盘上上下键查找
# 查找所有执行过的命令
history
# 重复执行 第242 个命令
!242
# 重复执行最后一次命令
!! / !-1
# 重复执行倒数第二个命令
!-2
# 调出最后一次命令
ctrl + p

# 只执行命令，去掉参数(如：cd)
!:0
# 查找最近一次包含 echo 的命令
!echo
# 搜索之前执行过命令 control + d/g 退出
control + r
# 调用最后一次命令的参数
ls + esc .
# 只显示最后10条命令
history 10
# 清空命令历史
history -c
```

### 5. seq

- 用法：seq [选项]... 尾数
- 或：seq [选项]... 首数 尾数
- 或：seq [选项]... 首数 增量 尾数

```SHELL
seq 10
seq 1 10
touch a`seq 1 2 10`
# 命令的引用
ehco $(date +%T) >> filename
echo `date`
```

- 文件通配符
  1. `*`代表任意个字符
  2. ？表示任意单个字符
  3. [0-9] 表示数字
  4. [a-z]字母：从a-z，**并且包括A-Y**
  5. [A-Z]字母：从A-Z，**并且包括b-z**
  6. [abcde]：其中一个
  7. [^abcde]：取反
  8. [:lower:]/[:upper:]：表示小写字符
  9. [:digit:]：表示数字
  10. [a-zA-z] / [:alpha:]：所有字母
  11. [a-zA-Z0-9]/ [:alnum:]：所有**单个**数字和字母

```SHELL
ll a[0-9]
# 查看以 a 开头的所有文件
ls /etc/a*
ls a[abcde] or ls a{a..e}
ls a[^abcde]
ls a[[:lower:]]/ ls a[[:upper:]]
ls a[[:digit:]]
```

### 6. stat

- 查看文件状态

```SHELL
[root@localhost test]#stat aa
  文件："aa"
  大小：0         	块：0          IO 块：4096   普通空文件
设备：fd00h/64768d	Inode：17652659    硬链接：1
权限：(0644/-rw-r--r--)  Uid：(    0/    root)   Gid：(    0/    root)
环境：unconfined_u:object_r:admin_home_t:s0
最近访问：2019-07-30 11:58:56.110953195 +0800
最近更改：2019-07-30 11:58:56.110953195 +0800
最近改动：2019-07-30 11:58:56.110953195 +0800
创建时间：-
# access:访问时间，（读取文件内容，touch） atime
# modify:修改时间，（修改文件内容，touch） mtime，
# change:改动时间，（修改文件内容，touch） ctime，改变状态或属性如：mv，chown等
```

### 7. copy

#### 1. 用法

- cp [选项]... [-T] 源文件 目标文件
- 或：cp [选项]... 源文件... 目录
- 或：cp [选项]... -t 目录 源文件...

#### 2. 参数(9)

1. -i：覆盖之前提示，交互
2. -n：不覆盖已存在的文件，i失效
3. -ni：会提示，谁在后谁有效
4. -r：递归复制
5. -rf：强制覆盖
6. -rfv：显示详细的复制过程
7. -b：覆盖之前对源文件做备份 **目标文件名~**
8. —backup=numbered：覆盖之前对源文件做备份 文件名~1~，~2~...
9. -p：复制文件完全一样，保留原来的属性

```SHELL
cp 1.txt 2.txt
cp 1.txt test
cp 1.txt 2.txt 目录
cp -r test test2
```

- 如果source是文件
  - 如果目标不存在则新建并写入数据，存在则直接覆盖，提示使用`-i`选项
  - 如果目标是目录，则直接在目标文件夹中新建一个同名的文件
  - 如果复制多个文件，则目标必须是**目录(存在)**
- 如果source是目录
  - 如果目标不存在，则创建指定的目录，使用 `-r`选项
  - 如果目录存在
    - 目标是一个文件，则报错
    - 目标是一个目录，则在目标目录中创建同名目录

### 8. mv

- 移动、重命名

#### 1. 用法

- mv [选项]... [-T] 源文件 目标文件
- 或：mv [选项]... 源文件... 目录
- 或：mv [选项]... -t 目录 源文件...

#### 2. 参数

1. -i：交互式
2. -f：强制移动
3. -b：备份和copy一样
4. -v：显示进度

### 9. rm

- Remove (unlink) the FILE(s).

#### 1. 用法

- rm [选项]... 文件...

#### 2. 参数

1. -i：交互（ctrl+backspace）
2. -f：强制删除
3. -r：递归删除



# 3. 常用命令2

## 1. 文件操作

### 1. mkdir

#### 用法

`Usage: mkdir [OPTION]... DIRECTORY…`

#### 参数(2)

1. -p：创建多层目录
2. -v：显示创建的过程如：-pv

```SHELL
mkdir test1 test2 ...
mkdir test{1..10}
mkdir -p test/test1/test2...
# 递归创建目录,都好之间没有空格，否则报错
mkdir -pv {s1,s2}/{ss1,ss2}/{sss1,sss2}
```

- 删除**空目录**

```SHELL
# 只能删除空目录
rmdir test1
# 递归删除空目录
mkdir -p s1/s2/s3
rmdir -p s1/s2/s3
```

### 2. tree

#### 参数(2)

1. -L：指定查看目录层级
2. -d：只显示目录

```SHELL
yum install -y tree		# 需要配置yum源
tree 目录
tree -L 2
tree -d
```

### 3. 链接文件

#### 1. 软链接

1. 相当于快捷方式
2. 文件大小为：链接文件路径的字符数
3. 删除源文件：软链接不能用
4. 可以对目录做软链接
5. 可以跨越分区

```SHELL
ln -s 源文件 目标文件	# 生成软链接
ln -s b c
```

#### 2. 硬链接

1. 指向同一磁盘位置
2. 将文件的引用次数+1
3. 删除源文件：硬链接只是该文件引用次数 -1，目标文件不受影响
4. 不能对目录做硬链接
5. 不能跨越分区

```SHELL
ln 源文件 目标文件	# 生成硬链接
```

- **目录引用次数一般为2，其内部有一个链接 .** 
- 目录引用次数 = 2 + 目录中的文件数(目录和文件)

#### 3. 查看文件类型

```SHELL
file 文件名
```

## 2. 输入输出

### 1. 输入、输出

1. 标准输入：接收键盘的输入 **stdin 0**
2. 标准输出：默认输出到终端 **stdout 1**
3. 错误输出：默认输出到终端 **stderr 2**

### 2. I/O重定向

- 把输出和错误信息重定向到文件或其他位置
- `>` 覆盖，把**stdout**重定向到文件中
- 2> 覆盖，把**stderr**重定向到文件中
- &> 覆盖，把**stdout /stderr**重定向到文件中
- `>>`追加
- 2>>
- &>>

```SHELL
# hhhhh不存在，默认显示到文件，
ls /hhhhh 2> err.log
# 把所有输出重定向到data.log文件
(ls ; ls /hhhhh) &> data.log
# 把所有输出重定向到data.log文件
ls / /hhhhh &> data.log
# 分开输出执行信息和错误信息
ls / /hhhhh >info.log 2> error.log
ls / /hhhhh >info.log 2> &1
# 无限接收，输出信息不显示
ls / /hhhhh &> /dev/null
# 无限输出
if = /dev/zero

echo 哈哈哈哈 > a.log
echo 嘻嘻嘻嘻 > a.log
echo 嘻嘻嘻嘻 >> a.log
# a.log文件不存在会新建，存在会清空
>a.log
```

- 多行输入

```SHELL
# EOF结束，多行输入，结束时生成(保存)该文件
cat > f1 <<EOF(自定义)
# ctrl + c/d 结束，只要回车立即生成(保存)文件
cat > f4
# EOF：约定俗成的，end of file
```

### 3. tr

- 替换、压缩和删除字符

#### 1. 参数

1. -t：截断替换
2. -d：删除
3. -s：压缩，去重
4. -c：取反

```SHELL
# 输入ab显示12
tr ab 12
# 输入abc显示122，不足位数取最后一位去补
tr abc 12
# 截断替换
tr -t abcd 12
# 循环删除
tr -d abcd
# 此时重定向不能为原文件，如果为原文件，则文件会被清空
tr -d abc < issue > issue
tr -d abc < issue > issue2
# 压缩，去重
tr -s a
# 取反去重
tr -sc abc
# 取反去重，ctrl + d 结束
tr -dc abc
or tr -dc "abc\n"
# seq 1 10 > f1
tr '\n' ' ' < f1 > f2
tr ' ' '\n' < f2

# 文件小写转为大写
tr 'a-z' 'A-Z' < /etc/issue
```

### 4. 管道 ｜

- 使用 ｜连接多个命令
- 命令1 ｜ 命令2 ｜...
  - 将命令1的stanout发送给命令2的stdin ...
  - stderr默认不能通过管道传递

```SHELL
ls | tr 'a-z' 'A-Z'
```

## 3. 文件权限

### 1. 文件类型

```SHELL
lrwxrwxrwx.		# 链接文件l
-....					# 文件
d....					# 目录文件
s....					# socket 套接字
b....					# 块文件
c....					# 字符文件
```

```SHELL
-rw-r--r--.   1      root root   14   Jul 30 16:24  1.cfg
权限				引用次数    属主 属组   大小	   mtime时间   文件名
```

### 2. 更改属主、组

- chown：change ower

#### 1. 用法

`Usage: chown [OPTION]... [OWNER][:[GROUP]] FILE…
  or:  chown [OPTION]... --reference=RFILE FILE…`

#### 2. 参数

1. -R：递归更改属主
2. `--reference=源文件`：指定组或主和源文件一样

```SHELL
chown 属主 filename
chown 属主:属组 filename    # :和. 都可以
chown 属主.属组 filename
chown :属组 filename       # 只改变属组
chown -R henry test       # 递归更改属主，不使用-R子文件属主不变
```

```SHELL
# 修改组
chgrp henry fielname
# 指定filename1的组别和filename一样
chgrp --reference=filename1 filename 
```

### 3. 权限操作

#### 1. drwxr-xr-x

1. 第一位：代表文件类型
2. 三位为一组：属主(u)、属组(g)、其他的权限(o)
3. rwx：读、写、执行
4. root用户不受权限控制

```SHELL
# 设置不覆盖原文件
set -C
> a.txt
# 允许覆盖原文件
set +C
> a.txt
```

```SHELL
# 查看当前登录的用户
[root@localhost ~]# whoami
root
[root@localhost ~]# who am i
root     pts/3        2019-07-31 11:01 (172.16.44.1)
# 查看当前所有用户正在执行的命令
[root@localhost ~]# w
```

#### 2. 更改权限

1. 文件
   - r / 4：可以查看
   - w / 2：可以写
   - x / 1：可以执行
2. 目录的权限：一般是r和x一起存在
   - r / 4：可以使用ls查看
   - w / 2：可以创建或删除文件
   - x / 1：可以 cd 进文件夹，如果没有x权限w权限不生效，r生效只能查看哪些文件**权限看不到**

```SHELL
# 更改文件权限
chmod o-r filename   # 给其他去掉r权限
chmod +x filename    # 给所有加上x权限
chmod ug-x filename  # 给u和g去掉x权限
# 更改目录权限
chmod o-x dirname
chmod o+w dirname
chmod o=w dirname    # 其他权限只有
# 使用数字更改权限
chmod 644 文件名
chmod 755 目录
- 建议：不要给777权限
```

```SHELL
# 执行a.py文件
echo '#!/usr/bin/python' > a.py
echo '#coding:utf-8' >> a.py
echo 'print(123)' >> a.py
chmod +x a.py
./a.py
# 或者
chmod -x a.py
python a.py
```

#### 3. 特殊权限chattr

**参数**：

1. i：不能修改、删除、改名
2. a：只能追加内容

```SHELL
# 设置 i 属性
chattr +i a.txt
# 查看特殊权限
lsattr a.txt
```

## 4. 文本操作

### 1. cat(4)

参数：

1. -E：在每行结束处显示"$"
2. -n： 对输出的所有行编号
3. -b：对非空输出行编号
4. -s：折叠空行为一行

```SHELL
cat -E /etc/passwd
cat -n /etc/passwd
cat -b /etc/passwd
cat -sn /etc/passwd
```

### 2. tac

- 倒叙显示文件内容

```SHELL
tac /etc/passwd
```

### 3. less

- 分屏显示，空格一屏，回车一行
- /搜索， n：先后搜索 N：向前搜索
- q：退出

```SHELL
less /etc/passwd
# 搜索
/root 回车
```

### 4. more

- 分屏显示(百分比)，空格一屏，回车一行
- -d：显示翻页和退出信息
- 输出完自动退出，也可使用q提前退出

```SHELL
more -d /etc/passwdt
```

### 5. head

- 显示前多少行，默认显示10行
- -n：指定显示前 n 行

```SHELL
head /etc/passwd
# 显示前 3 行
head -3 /etc/passwd
```

### 6. tail

- 显示后多少行，**默认后10行**
- -n：指定显示后 n 行
- -f：追踪显示文件新加入的内容，一般用于查看日志
- tailf：相当于 tail -f

```SHELL
# 文件更改时访问
tail /etc/passwd
# 显示后 3 行
tail -3 /etc/passwd
```

```SHELL
# 实时访问文件
tailf /etc/passwd
```

### 7. cut

- 抽取文件

#### 参数(3)

1. -d：指定切割符，**必须与-f一起连用**
2. -f：指定显示指定列的数据(3中方法可以混用)
3. -c：按照字符切割，直接输出结果

```SHELL
cut -d: -f3 /etc/passwd
cut -d: -f3,5,6 /etc/passwd
cut -d: -f3-6 /etc/passwd
cut -d: -f3-5,7,9 /etc/passwd
# 按字符切割
cut -c2-5 /etc/passwd
```

### 8. paste

- -d：指定合并的符号
  - 指定多个字符时，只选择第一个字符作为连接符
- -s：把所有行合并一行显示

```SHELL
# 合并 b 和 d
paste -d: b d
# 默认是tab
paste b d
```

## 5. 分析文本

### 1. wc (word count)

- 空格和换行都认为是单词结束

#### 参数(5)

1. -l：行数
2. -w：单词个数
3. -c：字节数
4. -m：字符数
5. -L：文件中最长行长度

```SHELL
[root@localhost ~]# wc /etc/passwd
  43   86  2238 /etc/passwd
 行数  字数 字节数    文件
 wc -l /etc/passwds
```

### 2. sort

- 把文本显示在stdout中，不该变原文件

#### 参数(7)

1. 默认按照字母排序
2. -n：按照数字排序
3. -r：倒叙
4. -R：随机排
5. -f：忽略大小写
6. -t：指定分割符
7. -k：指定排序依据

```SHELL
sort b
sort -n b
sort -r b
sort -R b
# 先切割，根据第 3 列排序
sort -t: -k3 /etc/passwd
```

### 3. uniq

- 从输入中删除**前后相接**的重复行

#### 参数

1. -c：显示重复次数
2. -d：只显示重复行
3. -u：只显示不重复行

```SHELL
echo '1' >> b
echo '1' >> b
echo '2' >> b
echo '1' >> b
echo '1' >> b
uniq b
uniq -c b
uniq -d b
uniq -u b
```

```SHELL
# 应用
sort -n b | uniq -c
w|sort|cut -d\  -f1|uniq -c
ss -tnp| cut -d: -f2|tr -s ' '| cut -d' ' -f2|sort|uniq -c
```

### 4. diff

- 对比两个文件

```SHELL
diff a.txt b.txt
```

# 4. vi/vim

## 1. 打开、关闭文件

### 1. 打开文件

```SHELL
vim [option] filename
+n：光标定位到第n行
+/henry：光标到第一个匹配到的行首
-m：只读方式打开
-e：直接进入扩展命令行模式
-b：以二进制方式打开
```

### 2. 关闭文件

```SHELL
:q		# 退出
:q!		# 不保存，强制退出
:w		# 保存
:wq		# 保存退出
:wq!	# 强制的保存退出
:x		# 保存退出
```

```SHELL
ZZ		# 保存退出
ZQ		# 不保存退出
```

## 2. 模式的切换和操作(4)

- 命令模式：打开后的默认模式
- 插入模式：编辑文件
- 扩展命令模式（末行模式）：保存或退出等
- 可视化模式：配合鼠标使用

### 1. 命令模式和插入模式

- 进入插入模式

```SHELL
i		# cursor所在位置前插入
I		# cursor行首插入
a		# cursor所在位置后插入
A		# cursor行尾插入
o		# cursor下一行
O		# cursor上一行
```

- 回到命令模式：**Esc键**

### 2. 命令模式和扩展命令模式

- 进入扩展命令模式

```SHELL
:		# shifit + :
```

- 命令模式的操作

```SHELL
:w				 # 保存文件到磁盘
:r filename      # 读入filename，在cursor的下一行插入其内容
:w filename  	 # 另存为
:! command		 # 执行终端命令
:r! command		 # cursor下一行插入执行结果
```

- 到命令模式：**两次Esc键**或者**Esc + Enter**

## 3. cursor移动

### 1. 字符间移动

```SHELL
h j k l				# 左 下 上 右
```

### 2. 单词间移动

```SHELL
w 						# 下一个单词词首
e							# 当前或下一个单词词尾，除了下划线(_) 都是单词分隔符
b							# 当前或下一个单词词首
num command   # 配合数字键使用，表示跳转 n 个字符或单词
```

### 3. 行间移动

```SHELL
H							# cursor跳到，当前页第一行行首
M							# cursor跳到，当前页中间行首
L							# cursor跳到，当前页最后一行行首

zt						# 当前行移动到屏幕的顶端
zz						# 当前行移动到屏幕的中间
zb						# 当前行移动到屏幕的底端

0							# 跳转到行首
$							# 跳转到行尾
^							# 跳转到行首第一个非空白字符
gg/1G					# 跳转到文件第一行
G							# 跳转到文件末行
:10						# 跳转到第10行
10gg/10G			# 同上
```

### 4. 段落间移动

```SHELL
{							# 上一段
}							# 下一段
[[						# 文本开头
]]						# 文本结尾
```

### 5. 翻屏

```SHELL
ctrl + f			# 下一屏
ctrl + d			# 下半屏
ctrl + u			# 上半屏
ctrl + b			# 上一屏
```

## 4. 操作

### 1.字符编辑

```SHELL
nx							# 删除cursor之后的文本(n个字符，默认一个)
xp							# 两个字符交换位置
p								# 黏贴到cursor所在后一个字符后
~								# 大小写转化
nJ							# 合并下 n 行，删除下 n 行换行符

rx							# 用 x 替换cursor所在位置后的单个字符
R								# 切换为 Replace 模式，可以连续替换
```

### 2. 删除d

```SHELL
dl							# 删除右边的一个字符，根据cursor移动删除
d0
d$/D
3dd							# 删除当前行和下2行
d^							# 从cursor位置删除到当前行第一个非空字符
dw							# 删除一个单词
de							# 删除到当前单词或下一个单词词尾
db							# 删除到当前单词或上一个单词词首
dG							# 删除到文件行尾
dgg							# 删除到文件行首
```

### 3. 复制y

```SHELL
y$							# 结合cursor跳转使用
5yy							# 复制5行
p 							# 粘贴到cursor位置(类似a)，如果是整行则粘贴到下一行
P(大写)					 # 粘贴到cursor位置前，如果是整行则粘贴到上一行
```

- 改变c(**直接切换到插入模式**)

```SHELL
cw							# 结合cursor跳转使用
cc							# 删除整行，并进入insert模式
ncc							# 删除 n 行
c$/C
```

- 插入n次henry

```SHELL
nihenry					# 插入n个henry
```

- 撤销u：最近的更改

```SHELL
nu							# 撤销之前的 n 次更改
U								# 撤销当前行的更改
ctrl+r					# 撤销 撤销
3.							# 重复上次操作，3次
```

- 搜索/（**可以使用正则**）

```SHELL
/pattern				# 向下搜索指定pattern
?pattern			  # 向上搜索指定pattern
n								# 和搜索命令相同方向跳转cursor
N								# 和搜索命令相反方向跳转cursor
```

## 5. 扩展的命令模式补充

### 1. 地址定界

```SHELL
:start,end			# 从start行到end行
:start,+n				# 从start行到 start+n 行
:2,5						# 2-5行
:2,+5						# 2-7行
:n							# 具体到第n行
:.							# 当前行
:$							# 最后一行
:$-2						# 倒数第 $-2 行
:%							# 全部
:n,/pattern/		# 从第n行到第一次pattern匹配行
:/pat1/,/pat2/	# 从第一次pat1匹配行到第一次pat2匹配行
:/pattern/,n		# 从第一次pattern匹配行到第 n 行
```

### 2. 使用方法(d/y/w/r)

```SHELL
:/pattern/,n w newfile		
:4 r b				# 在第4行，插入
d								# 删除
y								# 复制
w newfile				# 将指定范围内的文件另存为
r filename			# 将文件内容插入指定位置
```

### 3. 查找替换

1. :地址定位符s/pattern(正则)/替换的内容/装饰器

- 查找的内容可以使用正则表达式和分组，**替换的内容可以引用，即\1, \2 等**
- 也可以使用**&代替查找的内容**(不需要分组)

```SHELL
# 替换第一个匹配字符
:%s/s..c/abc  	
# 使用向后引用，正则的分组
:%s/\(sy.c\)/abc\1/
```

2. 装饰器
   - i：忽略大小写
   - g：全部替换
   - gc：替换之前要确认(y,n,a,l,...)
   - / @ #：都可以作为查找替换的分隔符

## 6. 其他操作

### 1. 可视化模式

- 配合移动键使用
- 选中的文字可以被删除、复制、变更、过滤和替换等

1. v：面向字符
2. V：面向行
3. ctrl + v：面向块

```SHELL
# 批量加入注释
1. ctrl + v
2. 移动光标选中需要注释的行
3. 按下 I 并输入注释
4. esc结束
```

### 2. 多文件操作

- 保存之后再切换否则更改的内容会丢失

```SHELL
vim f1 f2 f2		# 打开多个文件
:next						# 切换下一个文件
:prev						# 切换下一个文件
:last
:first
# 退出
:wqall
:wall
:qall
```

### 3. 使用多个窗口

- 多个文件

```SHELL
vim -o f1 f2 f3	# 水平分屏
vim -O f1 f2 f3 # 垂直分屏
ctrl + w(hjkl)	# 切换窗口
```

- 单个文件

```SHELL
ctrl + w, s			# 水平分屏
ctrl + w, v			# 垂直分隔
ctrl + w,hjkl 	# 跳转
ctrl + w, q			# 取消相邻的屏幕
ctrl + w, o			# 取消全部窗口
```

### 4. 定制vim

- 全局配置文件：/etc/vimrc
- 当前用户配置文件：~/.vimrc
- 扩展命令模式(临时生效)
- nu, ic, ai, hls, cul,
- syntax 

```SHELL
:set nu					# 设置行号
:set nonu				# 取消行号
:set ic					# 忽略大小写，搜索
:set noic
:set ai					# 自动缩进,与上一样对齐
:set noai
:set hls				# 搜索高亮
:set nohls
:syntax on			# 语法高亮
:syntax off
:set cul				# 设置光标所在行的标志符(下划线)
:set nocul
:set all				# 获取帮助
```

- 文件转换

```SHELL
# 转换为 windows 格式
:set fileformat=dos
# 转换为 Linux/unix
:set fileformat=unix
```

### 5. vim帮助信息

- :help    :help topic
- vimtutor
- vim + enter

# 5. 搜索

## 1. find

### 1. 用法

1. `find [option]... [查找路径][查询条件][处理动作]`
2. 查找路径：可以指定目录，默认当前目录
3. 查找条件：用来指定文件查找的标准，文件名、大小、权限、类型等
4. 处理动作：对符合条件文件进行的操作，默认直接输出到屏幕

### 2. 查找条件

#### 1. -name：可以配合通配符使用

- 文件名：完全匹配
- 通配符：？、* 需要转义

```shell
# 使用名称查找，文件目录和文件只要符合都可以
find . -name a.txt		# 完全匹配
find -name a\?				# 所有以a开头后面有一个字母的文件或文件夹
find -name a\*				# 所有以a开头的文件或文件夹
find -anme 'a*'				# 所有以a开头的文件或文件夹
find -anme a[ab]			# 以a开头，后面字母是a/b的文件或文件夹
```

#### 2. -i ：忽略大小写

```shell
find -iname a					# 忽略大小写
```

#### 3. `-maxdepth/-mindepth`

- 指定查找深度，搜索层数，指定目录为第一层

```shell
find -maxdepth 2 -name a
# 最小层数， 包括第二层
find -mixdepth 2 -name a
```

#### 4. -type：指定文件类型(7)

1. f：**文件**
2. d：**目录**
3. l：链接
4. s：套接字
5. b：块设备
6. c：字符设备文件
7. p：管道文件

```shell
find -type f -name a
find -type d -name a
find -type l -name a
find -type s /run -name *
# 指定搜索层数
find -maxdepth 1 -type d
# 搜索块文件，如：/dev/sda
find / -type b -ls
# 搜索字符文件
find / -type c -ls
# 搜索管道文件
find / -type p -ls
```

#### 5. -empty：空文件夹

```shell
find -empty -type d      # 查找所有空目录
```

#### 6.  -user/-group：属主和组

```shell
find -user henry
find -group henry
```

#### 7. -uid/-gid：uid或gid的文件和目录

- id  username  ：**查看用户的 uid，gid**

```shell
id henry								# 查看用户uid
find -uid 1000
find -gid 1000
```

#### 8. -nouser/-nogroup：没有属主的

- linux通过uid进行识别用户

```shell
find / -nouser 					# 用户被删除时，属主变成数字表示没有属主
find / -nogroup
```

#### 9. 组合条件

- 与：-a
- 或：-o
- 非：-not / ！
- **摩根定律**
  - 非A或非B=非(A 且 B)
  - 非A且非B=非(A 或 B)

```shell
find -type f -o -nouser
find -not -user henry -a -not -user dean ll
find -not \( -user henry -o -not -user dean \) -ll
```

#### 10. -path：排除目录

```shell
# 排除指定目录下的其他文件
find -path "./*a1" -prune -o -print
# 以下命令等效
find -path "./*a1"
find -path "./*a1" -prune -a -print
find -path "./*a1" -prune -not -print
```

#### 11. -size：文件大小

- -n：[0, n-1]
- n：查找在大小在(n-1 n ] 的文件且不等0的文件
- +n：(n, )
- c：字节，K：kb，M：mb，G：gb

```shell
find -size 1c/K/M/G
# 生成 1M 文件
dd if=/dev/zero of =ccc bs=1M count=1
ll ccc
# 查找文件大小在[0, 1]的文件和目录
find -size -2M
# 查找文件大小在(1, 2]的文件和目录
find -size 2M
# 查找文件大小在(2,...)2M以上的文件和目录
find -size +2M
```

#### 12. 文件时间戳

- 默认时间戳以天为单位
  1. atime [+|-]/ mtime / ctime
  2. time：[time,time+1)时间为 time 天到 time+1 天之间的文件
  3. +time：[time+1….]
  4. -time：[0, tim)
- 以分钟为单位(和天一样)
  1. -amin
  2. -mmin
  3. -cmin

```shell
# 查找访问时间为[0, 1)天内的文件和目录
find -atime -1 -ls
# 查找访问时间为[1,2)天内的文件和目录
find -atime 1 -ls
# 查找访问时间为[2，....),2天以上的文件和目录
find -atime +1 -ls
```

#### 13. -perm：权限

```shell
# 普通文件一般为
find -perm 644 -ls
# 软链接为 777 
find -perm 777 -ls
```

### 3. 处理动作(5)

#### 1. -print：默认

- 把搜索结果打印到屏幕上

```shell
find -perm 644 -print
```

#### 2. -ls：类似ll

```shell
find -perm 644 -ls
```

#### 3. -delete：删除

```shell
find -perm 644 -delete
```

#### 4. -fls ls.txt：写入文件

```shell
# 将查找结果写入到文件中
find -perm 644 -fls ls.txt
```

#### 5. -ok/exec command {} \;

- 对查找到的文件执行 command 命令
- {}：表示搜索到的内容
- \;  ：为固定格式
- ok：需要确认，exec：不需要确认
- find传递内容时一次性传递的

```shell
# 需要确认
find -perm 644 -ok rm -rf {} \;
# 不需要确认
find -perm 644 -exec rm -rf {} \;
```

## 2. xargs

- xargs：可以将命令的输出，一个个交给管道之后的命令
- 解决好多命令不支持管道，但工作中会用到的问题
- 有些命令不支持太多字符，也可以使用xargs

```shell
touch a{1..1000000}
echo a{1..1000000}|xargs touch
find -name * | xargs ls -l
ls a* | xargs rm -f
```

## 3. grep

- **从文件中查找符合条件行，使用正则时需要对 +、 ?、 {、 }、 (、 )**
- Global search REgular expression and pring out the line，全局用正则搜索，并打印符合条件行
- 三剑客：grep、sed、awk，用于处理文本，都可以使用正则

#### 1. 用法 

- gerp [option]… pattern [filename]

```shell
# 只要行内容包行 pattern 整行就会被输出
grep 'root' /etc/passwd
```

#### 2. 参数

1. `--color=auto`
   - `alias grep = 'grep --color'`
   - 将匹配到的文本添加颜色显示
2. -v：取反
3. -i：忽略大小写
4. -n：显示匹配行行号
5. -c：显示匹配的行数
6. -o：显示匹配的字符串
7. -q：静默模式，不输出内容，判断执行是否成功，echo $?
8. -A n：输出匹配和后 n 行
9. -B n：输出匹配和前 n 行
10. -C n：输出匹配和前后 n 行
11. -e：或关系
12. -E：扩展正则表达式
13. -r：递归查找，**用于在目录中查找**

```shell
# 显示没有匹配到的行
grep -v 'root' /etc/passwd

grep -q 'root' /etc/passwd
# $?上次命令结果的返回值，成功表示0，不成功为非0(1-255)
echo $?
# 输出匹配行以及其下 2 行
grep -nA 2 'root' /etc/passwd
# 输出匹配行以及其上 2 行
grep -nB 2 'root' /etc/passwd
# 输出匹配行以及前后 2 行
grep -nC 2 'root' /etc/passwd
# 或者
grep -e 'root' /etc/passwd -e 'mail' /etc/passwd
# 递归查找
grep -r 'root' /etc/
```

## 4. 正则

- **注意和文件通配符区分**

### 1. 字符匹配(9)

1. .：任意
2. [abc]：abc的一个
3. [^abc]：取反
5. [:alpha:]：字母
6. [:upper:]：大写字母A-Z
7. [:lower:]：小写字母a-z
8. [:digit:]：数字
8. [:alnum:]：数字字母
9. [:punct:]：标点

```shell
grep "[[:alnum:]]*" b
grep "\W*" b

grep "a*.c" b
abc
ac
bc
dc
...
```

### 2. 量词

1. `*`：任意次，默认时贪婪匹配
2. ？：0 或 1次，使用时需要转义 \?
3. `+`：至少1次，使用时需要转义 \+
4. {n}：匹配n次，使用时需要转义` \{n\}`
5. {m, n}：匹配n次，使用时需要转义` \{m, n\}`
6. {,n}：至多n次，使用时需要转义` \{,n\}`

```shell
grep "a\?c" b
grep "a\+c" b
```

### 3. 位置锚定

1. ^：开头
2. $：结尾
3. ^$：空行

```shell
grep "^$" b
```

### 4. 向后引用

- \1：表示前面第一个分组的引用

```shell
grep "\(.\+\) is \1" b
grep "\(l..e\).*\1" b
# 外边的是1，里面的是2分组
grep "\(l(..)e\).*\1\2" b
```

### 5. egrep

- egrep = grep -E
- 标准正则需要转义此时不用转义

```shell
# 以下写法等价
grep -E "(l..e).*\1" b
egrep "(l..e).*\1" b
```

# 6.压缩和归档

## 1. 压缩

### 1. gzip

#### 1. 用法

- gzip [option]… [file]...

#### 2. 参数

1. -c：保留源文件，必须指定导出路径
2. -d：解压
3. -9：**指定压缩比为 9，默认为9， 范围[1-9]** 

```shell
# 删除源文件压缩
gzip /etc/passwd
# 解压zip包，默认删除压缩包
gunzip /etc/passwd.gz

# 解压，删除压缩包
gzip -d /etc/passwd.gz
# 压缩，解压保留原文件
gzip -c /etc/passwd.gz > /etc/passwd
gzip -dc /etc/passwd.gz > /etc/passwd

# 值越大，压缩比越大
gzip -9 /etc/passwd 
gzip -1 /etc/passwd 

# 查看压缩包,可以输出到一文件，即变相解压
zcat /etc/passwd.gz > /etc/passwd
```

### 2. bzip2

- 生成 .bz2 文件

#### 参数

1. -k：保留源文件
2. -d：解压缩
3. -9：指定压缩比

```shell
bzip2 /etc/passwd
# 指定压缩比默认9
bzip2 -9 /etc/passwd
bzip2 -d /etc/passwd.bz2
bunzip2 /etc/passwd.bz2
# 保留源文件
bzip2 -k /etc/passwd.bz2
# 查看bz2文件
bzcat /etc/passwd.bz2
```

### 3. xz

- 生成 .xz 文件

#### 1. 参数

1. -k：保留源文件
2. -d：解压
3. -9：指定压缩比

```shell
xz /etc/passwd
xz -d /etc/passwd.xz
unxz /etc/passwd.xz
# 指定压缩比为 9
xz -9 /etc/passwd
# 查看.xz 文件
xzcat /etc/passwd.xz
```

## 2. tar 归档

- 只放进包里不压缩
- 参数 - 可省略

### 1. 参数

1. c：创建
2. v：显示过程
3. f：指定文件
4. r：追加
5. x：解包
6. -C：指定解压位置
7. z：使用 gzip 压缩
8. j：使用 bzip2 压缩
9. J：使用 xz 压缩
10. `--exclude=filename`：排除指定文件

```shell
# 打包
tar cvf a.tar b c
# 追加 d 到 a.tar
tar -r -f a.tar d

# 使用 gzip 压缩，和解压
tar zcvf a.tar.gz f1 f2 f3
tar zxvf a.tar.bz
# 使用 bzip2 压缩，和解压
tar jcvf a.tar.bz f1 f2 f3
tar jxvf a.tar.bz
# 使用 xz 压缩，和解压
tar Jcvf a.tar.xz f1 f2 f3
tar Jxvf a.tar.xz

# 不指定压缩格式的解压， 默认解压到当前目录
tar xvf a.tar.xz
tar xf a.tar -C /opt
# 排除指定文件
tar zcf etc.tar.gz --exclude=/etc/yum.repos.d --exclude=yum.conf /etc/
```

### 2. split 分卷压缩

- 只能压缩文件

#### 1. 用法

`split -b size filename -d tarfile`

`cat tarfile* > tarfile`

#### 2. 参数

1. -b：指定分卷大小
2. -d：指定数字为后缀，默认是字母

```shell
# 大文件切分压缩
split -b 1M b -d b.tar.gz  
# 合并
cat b.tar.gz0* > b.tar.gz
```

# 7. 用户和用户组

## 1. motd

- message of the day
- 登录提示内容
- /etc/motd

## 2. 用户

### 1.用户分类

1. root：id为 0
2. 普通用户：
   - 系统用户：一般情况下启动服务或者运行进程，不可以登录，id 为 1-999/centos 7, 1-499/centos6。
   - 可登录用户：可以登录系统的，1000-65535/centos7，500-65535/cenos6。

### 2. useradd

- 只能root用户执行

#### 1. 参数(10)

1. -d：指定用户的家目录，默认在/home，不可以指定为 /temp 目录
2. -u：指定用户id
3. -g：指定用户的用户组，可以使用 gid / name
4. -G：指定用户的附加组
5. -M：不创建用户家目录
6. -N：不创建组，默认继承自 users 
7. -r：创建系统用户，id 从1000依次递减
8. -s：指定用户登录后使用的 shell，/sbin/nologin（可以登录看到提示信息，会立马踢掉）
9. -D：显示默认配置(可以和 -b，-s，-g连用)
10. -b：修改默认的家目录

```shell
useradd echo
useradd -d /opt/echo echo
# gid：有且只能有一个，—G：指定附加组，可以有多个
useradd -G root,echo dean
# 默认继承自， users
useradd -N dean1
# 创建系统用户
useradd -r henry
# 指定用户登录使用的shell
useradd -s /sbin/nologin dean2
passwd dean2						# 给dean2 设置登录密码

# 如果不指定uid，则系统会找到最大的 uid 进行递增
useradd -u 3000 dean3
useradd dean4
```

- 修改默认配置

```shell
# 修改默认登录shell
useradd -D -s /sbin/nologin
# 修改默认的家目录
useradd -D -b /opt
# 修改默认组
useradd -D -g 3000
```

#### 2. 配置文件

```shell
cat /etc/default/useradd
# 用户家目录的模版
ll -a /etc/skel/.
```

- 存放用户位置：/etc/passwd(7部分)

```shell
henry:   x:    1000:1000:henry: /home/henry:/bin/bash
用户名 密码占位符 uid  gid  描述信息   家目录     使用shell
```

### 3. usermod

#### 参数

1. -L：锁定用户，用户无法登录，默认情况下：修改用户密码即解锁
2. -U：解锁用户
3. -m：移动家目录
4. -d：新的家目录，不会自己创建，要使用-m选项
5. -g：修改主组
6. -G：修改附加组
7. -a：追加附加组，**需要和G一起连用**
8. -l：改名
9. -s：改shell

```shell
# 登录会进入 / 目录
usermod -d /usr/henry henry 
# -d 一般和 -m 连用
usermod -md /usr/local/henry henry 
# 追加附加组，需要和G一起连用
usermod -aG dean henry
```

### 4. userdel

#### 参数(1)

1. -r：删除用户以及家目录和mail pool

```shell
# 删除用户和家目录和mail pool
userdel -r dean2
```

### 5. passwd

- root only

#### 参数(9)

1. -d：删除用户密码
2. -l：锁定用户
3. -u：解锁用户
4. -e：强制用户下次登录时，修改密码
5. -x maxdays：密码最长有效期，默认是 day
6. -n mindays：密码最短有效期
7. -w days：提前通知用户密码到期时间
8. -i days：密码过期多少天禁用
9. `-—stdin`：从标准输入读取密码，不需要二次确认

```shell
passwd -i 7 dean
# 用于脚本，自动修改，交互的内容获取不到
echo 'xxx' ｜ passed --stdin username
```

### 6. chage

#### 参数(7)

1. -d：将密码修改时间设置为指定时间
2. -E：设置用户过期时间
3. -I：密码过期多长时间以后账户被禁用
4. -l：list用户密码策略
5. -m days：密码最多使用期
6. -M days：密码最长使用期
7. -W days：密码过期的警告天数

```shell
# 交互式更改用户密码策略
chage dean
```

- 配置文件
  1. 用户名
  2. 密码
  3. 18106：从unix元年到密码最近一次修改的时间
  4. 0：密码最小使用期限
  5. 99999：密码最大使用期限
  6. 7：密码过期前提前 7 天通知用户，默认是 7 天
  7. 20：密码过期 20 天被锁定，
  8. 最后一个：从unix元年，多少天账户失效

```shell
cat /etc/shadow
# $6$ ： sha-512，6表示加密方式，ahzn7peGcStDon3：加盐，剩下的为加密字符串
henry:$6$.ahzn7peGcStDon3$kI8HHtL5V0CHFS4VMb9.8yag5Qyq2a9CqjA3zyqFwnEHJYtzAOgDdDr7JzEiABusYOpZG.6BGvfyqjZvxABHk/:18106:0:99999:7:20::
```

### 7. su和sudo

#### 1. su

- su username，**从root切换，不需要密码**
- su - username，**完全切换，切换用户家目录和环境变量**

```shell
su username
# 完全切换，切换用户家目录和环境变量
su - username
# 获取用户权限，执行命令
su - root -c 'useradd dean3'
```

#### 2. sudo

- **/etc/sudoers**
  - 添加用户：henry  ALL=(ALL)    [NOPASSWD:]ALL
  - 添加用户组：%wheel    ALL=(ALL)   [NOPASSWD:] ALL
  - (ALL)：允许执行的命令
  - NOPASSWD：不需要输入密码
- visudo：提供语法检测

```shell
vim /etc/sudoers
添加：henry  ALL=(ALL) ALL
sudo useradd dean
```

## 3. 用户组

### 1. 分类

- gid取值和uid相同

1. root组：root ID为0
2. 普通用户组
   - 系统组
   - 可登录用户组

### 2. groupadd(2)

#### 1. 参数(2)

1. -g：指定gid
2. -r：指定系统组

```shell
groupadd oleg
cat /etc/group
```

#### 2. 配置文件

- /etc/group
- /etc/gshadow

1. henry：组名
2. x：密码占位符
3. 1000：gid
4. dean：以当前组为附加组的用户列表

```shell
# /etc/group
henry:x:1000:dean
# /etc/gshadow

```

### 3. groupmod(2)

- -g：修改gid
- -n：修改gname

```shell
groupmod -g henry 3000
groupmod -n henry henryboos
```

### 4. groupdel

```shell
groupdel dean
```

## 4. 两种认证方式

- 用户名和密码
- 用户名和key

```shell
# 生成key
ssk-keygen
# 公钥和私钥，非对称加密
Your identification has been saved in /root/.ssh/id_rsa.
# 公钥
Your public key has been saved in /root/.ssh/id_rsa.pub.
+---[RSA 2048]----+
|        .o+      |
|        .= .     |
|       .. = o .  |
|  . . .. = o +   |
| o o + .S O .    |
|  + = = o@ o     |
|   = B..=.*      |
|    E+.  +o+     |
|    .++   ++     |
+----[SHA256]-----+
# copy公钥到远程服务器
ssh-copy-id root@ip
# 直接登录，公加密私解密
ssh root@ip
```

# 8. 磁盘相关

### 1. df

- 查看磁盘空间占用率

```shell
df -h
```

### 2. mount

- 查看挂载信息

```shell
mount
```

### 3. du

- 显示目录的占用空间大小

#### 参数

1. -h：自动调节显示单位
2. -s：显示当前目录占用情况

```shell
du -h file
# 显示根目录的占用情况
du -sh /
# 显示指定目录下的每一个文件
du -sh /*
```

### 4. dd

1. 复制文件生成文件
2. if：表示来源，input file
3. of：表示输出，output file
4. bs：block size，**只能用整数**，单位可以是K M G T

```shell
dd if=/dev/zero of=/dev/null bs=10M count=10
```

### 5. RAID

#### 1. RAID0

- 数据分开存储
- 一般用于装系统

1. 读写速度提升磁盘个数N-1倍
2. 可用空间: 单个磁盘容量*磁盘个数N
3. 没有容错能力
4. 最少需要2块磁盘

#### 2. RAID1 

- 数据备份存储
- 保存数据

1. 读取速度提升，写的速度稍下降
2. 可用空间：单个磁盘容量
3. 有容错能力
4. 最少需要2块磁盘

#### 3. RAID5

- 数据分开存储，并存储校验值，校验值存储随机选取一个磁盘存储
- 目前较为流行

1. 读写速度提升
2. 可用空间，磁盘容量*磁盘个数N-1
3. 有容错能力：最多坏1块
4. 最少需要3块磁盘

#### 4. RAID6

- 新技术

1. 读写性能提升
2. 可用空间：单个磁盘容量*磁盘个数N-2
3. 有容错能力：最多可以坏2块
4. 至少需要4块磁盘

#### 5. RAID10

- 先做RAID 1 在做RAID 0

1. 读写性能提升
2. 可用空间：单个磁盘容量*磁盘个数N/2
3. 有容错能力：一个组中只能坏1块
4. 至少需要4块

#### 6. RAID01

- 先做RAID 0 在做RAID 1

1. 有容错能力：一个组中只能坏1块

#### 7. 软RAID

- 磁盘分区做RAID

# 9. 包管理工具

## 1. 介绍

- Cnetos/redhat：rpm / redhat package manager

## 2. yum

- -q：静默模式
- -y

### 1. 会解决包依赖关系

```SHELL
# 配置aliyun的yum源
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
# 清空缓存
yum clean all
yum makecache
```

```shell
# 1.使用YUM查找软件包 
yum search 
# 2.列出所有可安装的软件包 
yum list 
# 3.列出所有可更新的软件包 
yum list updates 
# 4.列出所有已安装的软件包 
yum list installed 
# 5.列出所有已安装但不在 Yum Repository 内的软件包 
yum list extras 
# 6.列出所指定的软件包 
yum list 包名
# 7.使用YUM获取软件包信息，安装和未安装的都可以查看
yum info 包名
# 8.列出所有可更新的软件包信息 
yum info updates 
# 9.列出所有已安装的软件包信息 
yum info installed 
# 10.列出所有已安装但不在 Yum Repository 内的软件包信息 
yum info extras 
# 11.搜索命令由哪个包生成，如果有filename则是以安装命令
yum provides 命令名
# 12.列出yum仓库信息
yum repolist
# 13.重新安装
yum reinstall
# 14.卸载包
yum remove 包名
```

- 包组

```shell
# 1.列出yum的包组，如：Development Tools(开发包信息api数据)
yum grouplist
yum install python3-devel
# 2.安装/卸载包组
yum group install/remove 包名
# 3.查看包组的info
yum group info 包名
# 4.检查包的依赖关系
yum deplist 包名
```

### 2. rpm命令

-   需要手动安装依赖关系

```shell
[root@localhost ~]# rpm -q python
python-2.7.5-68.el7.x86_64
# 检查包是否安装
rpm -q 包名
# 列出所有已安装的包
rpm -qa
# 查看指定文件是由那个包生成
rpm -qf /etc/ssh/sshd_config
# 查询安装 python 生成的文件
rpm -ql python
# 查询包的详细信息
rpm -qi python
# 查询 python 包的配置文件
rpm -qc python
# 查询 python 依赖的库文件
rpm -qR python
# 显示帮助信息
rpm -qd python
# 卸载 python 包，不会卸载依赖，yum会卸载依赖
rpm -e pyhon
```

- 包命名规范

```shell
# el7是redhat 7 系列
python-2.7.5-68.el7.x86_64
name-version(大版本.小版本.修订版)-作者修订次数.适用操作系统.架构
# noarch：不区分架构
# x86_64
# Amd64
# x86 i3/4/5/686  32位架构
# ppc(power pc), IBM
```

## 3. yum配置

- 配置文件目录：/etc/yum.repo.d
- 后缀：repo
- $release：当前os的发行的主版本号
- $basearch：基础平台，架构

```shell
[epel]			# 名字
name				# 描述信息
# 包的路径，可以是http://，https://，ftp://，file://(本地)
baseurl=http://mirrors.aliyun.com/epel/7/$basearch
# 设置访问规则
failovermethod=priority
# 是否开启该配置，0:禁用
enabeled=1
# 是否进行检查 gpgkey ，0:不检查，1检查
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7 
```

## 4. yum源

- 清华
- aliyun
- mirrors.163.com
- mirrors.huaweicloud.com
- mirrors.cloud.tencent.com

# 10. 系统相关

## 1. corntab

-   /etc/crontab

### 1. 说明

1.  计划任务
2.  同步时间、备份、日志
3.  *：代表所有
4.  2,4,5：代表或关系
5.  2-5：代表范围
6.  /2：间隔时间

```shell
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

# For details see man 4 crontabs

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu, fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed
  分 时 日 月 周    用户名 	   命名
```

### 2. 编辑/etc/crontab文件

```shell
# * 代表所有,每分钟的任务
* * * * * root echo 123 >> /tmp/a.txt 
# 每天 4点整的任务
0 4 * * * root echo 04 >> /tmp/a.txt
# 每个月的 3号
0 4 3 * * root echo 043 >> /tmp/a.txt
# 每周四的 4点 
0 4 3 * * 4 root echo 043**4 >> /tmp/a.txt
# 每天 4，6，8点的任务
0 4,6,8 * * *  root echo 4,6,8 >> /tmp/a.txt
# 每天8-22点的任务
0 8-22 * * * root echo 8-22 >> /tmp/a.txt
# /3表示每隔多长时间
0 8-22/3 * * * root echo 8-22/3>> /tmp/a.txt
# 每个月的3，10，15，25，30并且是周六，或关系
0 * 3,10,15,25,30 * 6 root echo 8-22 >> /tmp/a.txt
```

```shell
# 切分日志
/etc/cron.daily/logrotate
```

### 3. crontab命令创建

-   定时任务文件：**/var/spool/cron/user**，为指定用户创建定时任务文件
-   recommandations：分钟不要用 * 

#### 1. options

1.  -u：指定用户(默认 )
2.  -e：编辑
3.  -l：列出用户定时任务
4.  -ru：删除用户任务

```shell
# 编辑当前用户的计划任务
crontab -e
01 * * * * echo 'dadada' >> /tmp/aa.txt
# 只能读出/var/spool/cron/henry中的定时任务
crontab -lu henry
```

## 2. 网络相关

### 1.分类

| 类别 | 最大网络数           | IP地址范围                | 单个网段最大主机数 | 私有IP地址范围              |
| ---- | -------------------- | ------------------------- | ------------------ | --------------------------- |
| A    | 126（2^7-2)          | 1.0.0.1-127.255.255.254   | 16777214           | 10.0.0.0-10.255.255.255     |
| B    | 16384(2^14)          | 128.0.0.0-191.255.255.255 | 65534              | 172.16.0.0-172.31.255.255   |
| C    | 2097152(2^21)        | 192.0.0.0-223.255.255.255 | 254                | 192.168.0.0-192.168.255.255 |
| D    | 前四位位必须为 1110  | 224-239                   | 广播和多播使用     | -                           |
| E    | 前五位位必须为 11110 | 240-254                   | 留作科研使用       | -                           |

-   主机位全为 0 ，表示一个网段，全为1 表示广播地址 
-   127网段为保留地址，用于本地测试使用

### 2. CIDR(Classless Inter-Domain Routing))

-   网络位向主机位借位 
-   子网掩码：网络位全为1，主机位全为0
-   异或 ^：相同为 0
-   取反-(n+1)：~n
-   左移 << ：n*2^位移数
-   右移 >>：n/ (n*2^位移数) 向下取整

### 3. ip获取方式

-   手动
-   dhcp服务器(Dynamic Host Configuration Protocol)

### 4. ip配置

#### 1. 使用ip命令

```shell
# 添加ip，测试使用
ip addr add 192.168.182.200/24 dev ens33
# 添加label：ens33:0
ip a add 192.168.182.201/24 dev ens33 label ens33:0
ip a (show)
# 删除 ip 地址 
ip a del 192.168.182.200/24 dev ens33
ip a del 192.168.182.201/24 dev ens33:0
```

#### 2. 网卡配置文件

-   编辑配置文件

```shell
# /etc/sysconfig/network-scripts/ifcfg-ens33
TYPE=Ethernet				# 网卡接口类型，Ethernet Bridge
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static			# none，dhcp，static
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=ens33
UUID=22b1dd9a-aa5f-4f01-a652-b558bac89148 
DEVICE=ens33				# 设备
ONBOOT=yes					# 开机是否自启
IPADDR=172.16.44.143		# 配置静态ip
NETMASK=255.255.255.0		# 配置子网掩码
GATEWAY=172.16.44.2			# 网关一般是1/255，虚拟机是 2
DNS1=114.114.114.114
DNS2=8.8.8.8				# google
```

-   生效

```shell
# 重启网络
systemctl restart network
```

-   配置dns文件

```shell
# /etc/resolv.conf
# Generated by NetworkManager
nameserver 114.114.114.114
nameserver 8.8.8.8
# 域名解析
nslookup
114.114.114.114			# 114
119.29.29.29			# 腾讯
8.8.8.8					# google
```

-   浏览器访问域名时
    1.  读取本地hosts文件，寻找是否有对应的域名和ip记录
    2.  读取dns缓存
    3.  dns服务器查找

### 5. hostname

-   查看/设置主机名

```shell
hostname
# 重启终端生效，重启主机失效
hostname henry
```

-   配置文件

```shell
# /etc/hostname
localhost.localdomain
# 永久生效
hostnamectl set-hostname echo
```

### 6. 本地解析

-   主机和ip的映射关系
-   ip  +  域名

```shell
# /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
```

### 7. ss/netstat

-   打印网络系统的状态

#### 1. options

1.  -t：tcp协议
2.  -u：udp协议
3.  -x：unix socket，指的是 s类型文件
4.  -l：处于监听中的
5.  -p：相关程序及pid
6.  -n：显示端口

```shell
ss -t
ss -u
ss -x
# 常用组合
ss -tnlp ｜ gerp 22
ss -aulp
ss -tan
```

-   常用服务的端口号

```shell
ssh：22
http：80，https：443
mysql：3306
redis：6379
mongodb：27017
windows远程桌面：3389
oracle：1521
ftp：20/21
```

### 8. wget

-   下载命令

#### 1. options

1.  -O：指定下载后的文件路径
2.  -P：指定文件下载路径
3.  -q：静默模式
4.  -r：递归下载
5.  -p：下载所有的html元素

```shell
wget -O /tmp/filename url
wget -P /tmp url
wget -p url
```

## 3. 进程相关

### 1. ps

-   默认显示当前终端上的进程

#### 1. 支持的格式

-   unix：-h -a
-   BSD：aux
-   GNU：--help

#### 2. options

1.  -a：显示所有终端的进程
2.  -x：显示不连接终端的进程
3.  -u：显示不连接终端的进程
4.  f：显示进程数信息
5.  o：指定输出项
6.  L：显示所有的属性
7.  K 属性：从小到大排序，默认升序，倒叙：-属性
8.  -e：显示显示所有的进程
9.  -U username：显示指定用户的进程

```shell
ps -a		# 显示所有
ps -x		# 显示不连接终端的进程
ps -u		# 显示不连接终端的进程
ps o %cpu,%mem,pid,cmd K %mem
ps L
ps -ef		# 显示完整信息
ps -U henry
```

#### 3. 常用组合

-   与grep组合使用

```shell
ps aux | grep ssh
ps -ef
pidof sshd		# 根据名称查进程
kill pid		# 杀掉进程
killall sshd	# 杀死所有 sshd 进程
pkill sshd		# 按照模式杀死所有 sshd 进程
```

### 2. kill

-   向进程发送信号，实现对进程的管理，每个信号都有不同的数字对应

```shell
kill -l			# 查看系统支持的所有信号
# 常用信号
1 sighup		# 重读配置文件，平滑重启
2 sigint		# 终止正在运行的进程，相当于 ctrl+c
9 sigkill		# 强制杀死进程
18 sigcont		# 继续运行
19 sigstop		# 后台休眠

# 启动sshd服务
systemctl start sshd
systemclt daemon-reload 
```

## 4. 系统工具

### 1. uptime

-   显示当前时间	系统开启时长	当前在线人数	系统平均负载：1min，5min，15min的负载
-   平均负载：在特定的时间内，cpu等待运行的进程数
-   如果不超过cpu核心数的2倍则认为是良好的

```shell
uptime
15:34:54 up  1:18,  	1 user,  	load average: 0.00, 0.01, 0.05
# 当前时间	系统开启时长	当前在线人数	系统平均负载：1min，5min，15min的负载
```

### 2. top

-   实时显示系统进程的详细信息

#### 1. 排序

-   T：按照占用cpu时长
-   M：按照mem占用率排序
-   P：按照cpu占用率排序

#### 2. 首部信息显示

-   uptime信息：l（1+1种模式）
-   tasks和cpu信息：t（3+1种模式）
-   mem和swap：m （3+1种模式）
-   分别显示cpu：1（2种）
-   修改刷新时间：s
-   杀死正在执行的进程：k
-   退出：q

#### 3. options

1.  -d：指定刷新时间
2.  -b：显示所有的进程
3.  -n：指定刷新多少次退出

```shell
top				# 查看
top -d n		# 指定刷新时间
top -n n
```

#### 4. htop

-   在epel源中，升级版的top

```shell
yum install htop 
htop			# 支持鼠标，和空格
```

## 5. 性能分析

### 1. free

-   查看内存信息

#### 1. options

1.  -m/g/h
2.  -s：指定刷新时间
3.  -c：刷新次数

```shell
free -k/m/g/h		# 以mb/gb/自适应方式显示
free -c n			# 刷新 n 次退出
```

### 2. vmstat

1.  procs
    -   r可运行(正在运行或等待运行)的进程个数
    -   b处于不可中断的进程个数(被阻塞的队列长度)
2.  memory
    -   swpd：v交换内存的使用量
    -   free：空闲的
    -   buff/cache：buff和cache内存总量
3.  swap
    -   si：从磁盘到内存的数据速率(kb/s)
    -   so：从内存到磁盘的数据速率(kb/s)
4.  io
    -   bi：从块设备读入数据到系统的速率
    -   bo：从系统到块设备
5.  cpu
    -   us：用户空间
    -   sy：系统空间

```shell
procs -----------memory-----  ---swap-- ---io-- -system- ------cpu-----
 r  b   swpd  free  buff cache  si so    bi  bo   in  cs us sy id wa st
 2  0   0  130272    172 450452    0    0    72   8   55  75  0  1 99  0  0
```

### 3. iostat

-   查看磁盘读写信息

### 4. dstat

-   yum search/provides dstat
-   -c：显示cpu信息
-   -m：显示mem信息
-   -n：显示网卡信息

## 6. 作业管理

### 1. 后台运行

```shell
ctrl + z
dstat &				# 输出到屏幕
nohup dstat &		# 输出到文件
```

### 2. systemctl

-   管理服务

```shell
systemctl start/stop/restart sshd nginx redis   
systemctl reload sshd		# 重新加载配置文件
systemctl enable sshd 		# 开机自启
systemctl disenable sshd 	# 关闭关机自启
systemctl status firewalld	# 查看服务状态
# 查看开机自启
systemctl list-unit-files ｜ grep enabled
```

### 3. iptables

-   firewalld

```shell
iptables -F 				# 清空防火墙规则
iptables -L 				# 查看防火墙规则
systemctl stop iptables
systemctl status firewalld
```

### 4. selinux

```shell
setenforce 0				# 临时关闭selinux
getenforce					# 查看selinux状态
```

-   配置文件

```shell
# /etc/selinux/config
SELINUX = disabled/endforcing
```

## 7. 编译安装

-   传输文件

```python
# 传送文件
scp filename  henry@ip:/Users/henry/
# 下载
scp henry@ip:/tmp/test.txt /tmp
```

-   优点：可以自定义功能
-   缺点：安装耗时

```shell
wget url
# 安装lrzsz包，上传文件到centos
yum install lrzs
# 接收文件
rz -E
# 发送文件
sz a.txt 
# 解压
tar -xf xxx.xxx.tar.xz
# 进入包文件
# 查阅 INSTALL / REDEME.rst
./configure --help
```

-   源码编译安装流程

```shell
# 解决编译python3的基础环境依赖
yum install gcc patch libffi-devel python-devel  zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel -y
# 下载python3源码包
wget https://www.python.org/ftp/python/3.6.7/Python-3.6.7.tar.xz
# 指定安装路径，检查环境预处理
./configure --prefix=/opt/python36
# 释放 makefile 编译文件 
make 
# 执行make指令执行编译，安装完成
make install
# 配置环境变量
# 临时生效
PATH=$PATH:/opt/ptyhon/bin
# 永久生效，添加python3的环境变量,注意,要添加到开头
vim /etc/profile
PATH='/opt/ptyhon36/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin'
source /etc/profile
```

-   安装pip，安装之后，pip3位于/usr/local/bin目录下

```shell
yum install -y python36-setuptools
easy_install pip
```

-   python里的随机数是根据cpu中的时间片计算出来

## 8. 虚拟环境

-   通过yum安装的软件都可以使用systemctl启动
-   安装扩展的epel源

### 1. python3

```shell
# 下载 virtualenv 模块
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple virtualenv
#			不继承原来环境的包	 指定使用的解释器   自定义的虚拟环境
virtualenv --no-site-packages --python=python3   虚拟环境名称
```

```shell
python3 -m venv 路径如:django
# 激活进入虚拟环境
source django/bin/active
pip3 install django==1.11
# 退出
deactivate
```

```shell
# 在虚拟环境中启动项目
1. 安装包
# 导出python环境包
pip freeze > requirements.txt
# 安装虚拟环境，先切换虚拟环境
pip install -r requirements.txt -i https://pypi.douban.com/simple
2. 启动项目
python manager.py runserver 0.0.0.0:8000
```

### 2. python2

```shell
# 安装好之后会生成virtualenv命令
pip3 install virtualenv
# 生成虚拟环境
# --no-site-packages：生成一个干净的虚拟环境
# --python=python：指定python版本
virtualenv --no-site-packages --python=python3 test
```

### 3. 确保环境一致

```shell
# 导出python环境包
pip freeze > requirements.txt
# 安装虚拟环境，先切换虚拟环境
pip install -r requirements.txt
```

### 4. virtualenvwrapper

1.  ls virtualenv：查看虚拟环境
2.  workon test：直接切换虚拟环境
3.  cdvirtualenv：直接切换到当前env
4.  cdsitepackages：直接切换到当前的site-packags中
5.  lssitepackages：列出当前虚拟环境的site-packags
6.  rmvirtualenv 虚拟环境名
7.  deactive：退出

```shell
pip3 install virtualenvwrapper
vim .bashrc
# 创建虚拟环境
makevirtualenv django3
```
