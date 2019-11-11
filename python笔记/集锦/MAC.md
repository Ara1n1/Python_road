#  MAC

## 1. Terminal

### 1.1 网络相关

```python
arp -a | wc -l
fping 192.168.12.0/24 -g -a
# 取消文件的 @ 权限
xattr -c -r *
# 文件权限
rwxrwxrwt
# t为粘贴位，一个目录既使它的所有权限都开放，如果是设置了粘帖位，除非目录的属主和root用户有权限删除它，除此之外其它用户不能删除这个目录。
```

### 1.3 端口相关

```python
# 查看9000端口占用情况
sudo lsof -i:9000 
# 手动结束某一进程
kill -9 pid号
```

```mysql
# for windows
# 查看端口号占用情况
netstat -ano | findstr '3306'
```

### 1.4 常用

1. 定时关机

```python
# 晚上给8点关机
sudo shutdown -h 20:00
  
sudo shutdown -h 1702231800
```

### 1.5 查看pip安装包路径

```python
pip3 list
pip3 show packagename
```

### 1.6 文件相关

```python
brew install tree
# 查看某一目录结构
tree
```

### 1.7 开发者工具

```python
xcode-select --install
# 为app开放权限
sudo spctl --master-disable  
```





##2. Homebrew 使用 

###2.1 brew 安装

```python
# 安装brew最新版本
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# 卸载当前版本并安装最新版本
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall)"

#继续报错：chown: /usr/local: Operation not permitted
这是Mac OS 10.13版本之后加强了权限的限制，尤其是对/usr/local目录，默认开通 SIP （System Intergrity Protection），它禁止了软件以root身份在Mac上运行（参考https://blog.csdn.net/shaobo8910/article/details/81121314）。
  
解决办法：关闭SIP
1.重启Mac，按住Command + R键直到Apple Logo出现，进入Recovery Mode模式
2.点击工具里的Terminal（终端）
3.执行 csrutil disable
4.重启Mac
5.重启完成后，执行 sudo chflags norestricted /usr/local && sudo chown -R fxp/usr/local

（如果想重新开启安全设置，则重复1、2步骤，输入csrutil enable就可以了）
```

###2.2 brew 常用命令

```python
brew list       列出已安装的软件
brew update     更新brew
brew home       用浏览器打开brew的官方网站
brew info       显示软件信息
brew deps       显示包依赖
# 更新brew
brew update
# 需要赋给/usr/local目录权限
sudo chown -R $(whoami) /usr/local

# 安装软件
brew install git
# 卸载软件
brew uninstall git
# 搜索软件
brew search git
# 显示已经安装软件列表
brew list
#查看软件信息
brew [info | home] [FORMULA...]
# 删除旧版本安装包缓存
brew cleanup git、brew cleanup
# 查看那些已安装的程序需要更新
brew outdated
# 更新软件，把所有的Formula目录更新，并且会对本机已经安装并有更新的软件用*标明
brew update
# 更新某具体软件
brew upgrade git
# 锁定某个软件禁止更新:
brew pin git
# 解除禁更锁定
brew unpin git
# 查看brew存放安装包的缓存地址:
brew --cache
```

###2.3 brew 安装与卸载其他软件

```python
brew install wget
brew uninstall wget
brew search /wge*/
```

### 2.4 brew 卸载

```python
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall)"
```

```python
# 删除brew库
cd `brew --prefix`
rm -rf Cellar
brew prune
rm -rf Library .git .gitignore bin/brew README.md share/man/man1/brew
rm -rf ~/Library/Caches/Homebrew
```

```python
# 删除brew库
cd `brew –prefix`
brew prune
rm `git ls-files`
rm -r /usr/local/Homebrew
rm -rf .git
rm -rf ~/Library/Caches/Homebrew
rm -rf /usr/local/opt
rm -rf /usr/local/Caskroom
rm -rf /usr/local/var/homebrew
```



## 3. byobu

```python
# 安装
# 因为byobu是基于Ubuntu开发的，其他一些操作太好使，待后续研究补充。
#Alpine Linux    
apk add byobu
# Arch    
pacman -Sy byobu
# Debian    
apt-get install byobu
# Fedora    
yum install byobu
# Gentoo    
emerge byobu
# Mac OS    
brew install byobu
# Mint    
sudo apt-get install byobu
# Ubuntu    
sudo apt-get install byobu
#以Mac为例，安装完成后打开终端，输入byobu进入会话，
按下ctrl + a后松开，再按下"|" 横向开启分屏。
按下ctrl + a后松开，再按下"%" 纵向开启分屏。
按下ctrl + a后松开，再按下方向键切换分屏，或者shift + 方向键切换。
按下ctrl + a后松开，再按下"k", 关闭会话，所用分屏也会关闭
```



## 4. brew 安装软件顺序

```python
# 安装zsh 语法高亮
brew install zsh-syntax-highlighting
```

###4.1 cmake

1. 什么是cmkae

   ​	CMake是一个跨平台的安装（编译）工具，可以用简单的语句来描述所有平台的安装(编译过程)。他能够输出各种各样的makefile或者project文件，能测试编译器所支持的C++特性,类似UNIX下的automake。只是 CMake 的组态档取名为 CMakeLists.txt。Cmake 并不直接建构出最终的软件，而是产生标准的建构档（如 Unix 的 Makefile 或 Windows Visual C++ 的 projects/workspaces），然后再依一般的建构方式使用。

2. cmake 没有依赖关系

###4.2 wget的依赖关系

```python
# wget 
libidn2 --> wget
gettext --> libidn2 and wget
libunistring --> libidn2 and wget
openssl --> libevent and wget 
```

![wget的依赖关系](/Users/henry/Documents/截图/Py截图/wget的依赖关系.png)

## 5. 环境变量

```python
# Mac下配置环境变量文件：bash_profile
# 生效
source  .bash_profile 
```

## 6. 文件的作用

###6.1 ~/.CFUserTextEncoding

```python
# ~/.CFUserTextEncoding存储用户的默认文本编码和首选语言。
以下是Mac OS X参考库技术说明2228的摘录有更多信息：
Core Foundation尝试访问用户的主目录以确定其默认文本编码（存储在文件〜/ .CFUserTextEncoding中）。如果将EUID切换为登录用户的UID然后调用CF，则Core Foundation访问此文件时可能会出现问题。您可以通过设置一个环境变量来阻止此访问，该变量告诉Core Foundation要使用的默认文本编码。环境变量名称为__CF_USER_TEXT_ENCODING。其值应使用格式字符串“0x％X：0：0”构造，其中％X由登录用户的UID替换。
# 默认情况下，我的~/.CFUserTextEncoding副本包含0：0。
#冒号左侧的第一个数字表示默认编码。我文件中的0代表kCFStringEncodingMacRoman。可以在CFString Reference
```

### 6.2 .DS_Store 是什么

​	使用 Mac 的用户可能会注意到，系统经常会自动在每个目录生成一个隐藏的 .DS_Store 文件。.DS_Store(英文全称 Desktop Services Store)是一种由苹果公司的Mac OS X操作系统所创造的隐藏文件，目的在于存贮目录的自定义属性。

```python
# 禁止.DS_Store 文件生成
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool TRUE
# 恢复生成
defaults delete com.apple.desktopservices DSDontWriteNetworkStores
```

### 6.3 缓存清理

```python
# 重启－开机看到白屏时，按command+option+r+p，电脑会黑屏然后重启。
# 重置下电脑的硬件设置，可以提高电脑的速度。
# 这四个键的作用是恢复系统的原始设置
# 会解决扬声器音量，花屏，触控板不灵，电脑启动慢，运行慢等一些列问题，
# 但这是通过软件解决的，若是硬件故障，只能维修了。
```

​	如果感觉系统越来越慢，或是iTunes怎么都无法和iOS设备同步。这时候你应该重置一下MAC的PRAM和NVRAM.

1. 彻底关闭电脑后连接上电源适配器；
2. 开机，在显示灰屏前同时按住Command+Option+P+R 键，
3. 直到听见三次以上启动声后松开这些键，速度就恢复

### 6.4 .idlerc 

```python
# python idle相关文件
```

### 6.5 macport相关

```python
1. .profile 
2. .macports 
```

###6.6 vim 插件管理

```python
# YouCompleteMe unavailable, 报错
dlopen(/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload/itertools.so, 0x0002): code signature in (/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload/itertools.so) not valid for use in process: mapped file has no cdhash, completely unsigned? Code has to be at least ad-hoc signed.
```

## 7. Mac 启用FTP服务

```python
# 启用FTP服务
sudo -s launchctl load -w /System/Library/LaunchDaemons/ftp.plist
# 关闭FTP服务
sudo -s launchctl unload -w /System/Library/LaunchDaemons/ftp.plist
```

```python
# 登录格式为 ftp://用户名@ip 
# 然后输入你在Mac上的用户名和密码就可以了
```

## 8. 彻底卸载pycharm

```python
1、打开访达，找到PyCharm应用，右键移到废纸篓；
2、清理缓存，参数，日志相关配置文件：(注：ls PyCharm关键字进行搜索，PyCharm2018.3是我的文件名称)
a、cd ~/Library/Preferences/           
		rm -rf PyCharm2018.3/         
b、cd ~/Library/Logs
		rm -rf PyCharm2018.3/
c、cd ~/Library/Application\ Support/
		rm -rf PyCharm2018.3/
d、cd ~/Library/Caches/
		rm -rf PyCharm2018.3/
```

## 9. 缩小图标

```python
# 默认是一行是 7 个，可以改成 8 或 9
defaults write com.apple.dock springboard-columns -int 9
# 重启生效
defaults write com.apple.dock ResetLaunchPad -bool TRUE;killall Dock
```

## 10. 卸载内置应用

```python
# 重启按住。command + r
# 选择实用工具 --> 终端
csrutil disable 								# 关闭系统保护
ls /Volumes/									# 查看磁盘
cd /Volumes/Macintosh HD/System/Applications	# 进入应用目录
rm -rf TV.app									# 删除应用
...
csrutil enable
reboot
```

