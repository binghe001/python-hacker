# 作者简介: 
冰河，高级软件架构师，Java编程专家，大数据架构师与编程专家，信息安全高级工程师，开源分布式消息引擎Mysum发起者、首席架构师及开发者，Android开源消息组件Android-MQ独立作者，国内知名开源分布式数据库中间件Mycat核心架构师、开发者，精通Java, C, C++, Python, Hadoop大数据生态体系，熟悉MySQL、Redis内核，Android底层架构。多年来致力于分布式系统架构、微服务、分布式数据库、大数据技术的研究，曾主导过众多分布式系统、微服务及大数据项目的架构设计、研发和实施落地。在高并发、高可用、高可扩展性、高可维护性和大数据等领域拥有丰富的经验。对Hadoop、Spark、Storm等大数据框架源码进行过深度分析并具有丰富的实战经验。

# 作者联系方式
QQ：2711098650

# 工具简述
本项目均为冰河亲自编写并整理的Python渗透脚本集合，可直接拿来用于实战渗透

# 脚本说明
### com.binghe.hacker.tools.script.attack.crypt 包下的脚本：
```
1.crypt_attack.py: 利用字典破解Unix/Linux口令 
``` 
  
### com.binghe.hacker.tools.script.attack.ssh 包下的脚本
```
1. pxssh_connection.py: 使用pexpect中的pxssh模块连接ssh， 需要在Linux下执行  
2. ssh_attack.py: 暴力破解SSH  
3. ssh_botnet.py: 构建SSH僵尸网络,批量向多个SSH终端发送执行命令，达到批量控制目标主机的目的  
4. ssh_connection.py: 连接ssh，需要在Linux下执行  
5. ssh_dsa_attack.py: 利用ssh密钥暴力破解SSH 
``` 
  
### com.binghe.hacker.tools.script.attack.zip 包下的脚本
```
1. attack_zip.py: 暴力破解zip文件  
2. attack_zip_input_args.py: 暴力破解zip文件  
```
### com.binghe.hacker.tools.script.attack.ftp 包下的脚本
```
1. ftp_anonymous.py: 确定一个FTP服务器是否允许匿名登录，允许则返回True,不允许返回False
2. ftp_brute.py: 根据用户名:密码字典暴力爆破FTP服务器
3. ftp_web_page.py: 在FTP服务器上搜索网页
4. ftp_inject.py: 感染FTP上的网页
5. ftp_attack_web_page.py: 完整的感染FTP服务器上的网页脚本
```
### com.binghe.hacker.tools.script.attack.metasploit 包下的脚本
```
1. conficker.rc: Metasploit脚本，在Kali命令行中运行msfconsole -r conficker.rc 即可运行该脚本
2. metasploit_attack.py: 利用Metasploit实施攻击的脚本，主要针对Windows系统
```
### com.binghe.hacker.tools.script.attack.0day 包下的脚本
```
1.zeroday_ftp_attack.py: 0day漏洞利用脚本，针对FreeFloat FTP
2.zeroday_ftp_attack2.py: 0day漏洞利用脚本，针对FreeFloat FTP
```
### com.binghe.hacker.tools.script.net 包下的脚本
```
1. windows_reg_net.py: 列举Windows注册表中存储的网络名和默认网关的Mac
2. windows_reg_net_location.py: 列举Windows注册表中存储的网络名和默认网关的Mac,并通过https://wigle.net查询物理位置
3. windows_net_location.py: 测试Mac地址的地理位置
```
### com.binghe.hacker.tools.script.recycle 包下的脚本
```
1. windows_recycle_recovery.py: 查找系统中所有用户对应的回收站中的文件，并打印出来
```
### com.binghe.hacker.tools.script.meta 包下的脚本
```
1. meta_pdf.py: 分析PDF文件中的元数据信息
2. meta_image.py: 下载链接中的所有图片，并检查每张图片中的GPS元数据，若存在GPS元数据，在打印此文件存在GPS元数据
3. meta_skype_sqlite3.py: 检查Skype数据库，把账户信息、联系人地址、通话记录以及存放在数据库中的消息打印出来
4. meta_firefox_sqlite3.py: 查询火狐浏览器存储的上网记录
```
### com.binghe.hacker.tools.script.scanner 包下的脚本
```
1. scan_host_ports.py: 端口扫描器  
2. scan_nmap.py: 使用nmap进行扫描
```

# 出现率高的密码
```
aaa
academia
anything
coffee
computer
cookie
oracle
password
secret
super
unknown
```