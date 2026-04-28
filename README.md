# yanxi-info信息收集工具

## 介绍

[+]一款信息收集工具,目前支持功能:

​	  [-]子域名爆破&爬虫提取子域名

​	  [-]自动验活&超时二次检测	

​	  [-]端口存活扫描

​	  [-]403Bypass

[+]Version 0.0.2

————————————————————————————————————————————————————

## 配置

配置目录`\config\config.txt`

目前可自定义`线程`、 `域名访问超时时间`、`超时复检时间`

————————————————————————————————————————————————————

## 子域名扫描

通过爆破与爬虫来发现子域名；子域名超时复检。


#### <-使用说明->

    <u>举例：</u>想找`baidu.com的子域名，那就输入`baidu.com`
    
    程序会在当前文件夹生成`./URL/baidu.com/`，以及`存活子域名.txt`、`存活日志.txt`、`超时子域名.txt`
    
    [!]超时检测的时间可在/config/config.txt中自行配置

![image-20260428142524954](C:\Users\egie\AppData\Roaming\Typora\typora-user-images\image-20260428142524954.png)

————————————————————————————————————————————————————

## 端口扫描

可选择1000常见端口、全端口、自定义端口。

![image-20260428142346147](C:\Users\egie\AppData\Roaming\Typora\typora-user-images\image-20260428142346147.png)

————————————————————————————————————————————————————

## 403Bypass

需要将对应的数据包粘贴至 "请求包.txt"中

```
目前支持:请求头绕过、路由绕过、API版本绕过
```

#### <-使用说明->

```
将请求包复制到 "请求包.txt"之后选择"[3] 403bypass"即可
```

![image-20260428143236504](C:\Users\egie\AppData\Roaming\Typora\typora-user-images\image-20260428143236504.png)

![image-20260428143159625](C:\Users\egie\AppData\Roaming\Typora\typora-user-images\image-20260428143159625.png)

————————————————————————————————————————————————————

## 字典

**子域名**

    子域名爆破->`\dictionary\submins.txt`

**端口扫描**

    默认1000端口字典->`\dictionary\1000-port.txt`
    
    全端口字典->`\dictionary\all-port.txt`
    
    用户自定义端口->`\dictionary\user-define-port.txt`

