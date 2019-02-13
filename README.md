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
```

### com.binghe.hacker.tools.script.scanner 包下的脚本
```
1. scan_host_ports.py: 端口扫描器  
2. scan_nmap.py: 使用nmap进行扫描
```