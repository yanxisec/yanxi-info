# yanxi-info信息收集工具

[+]一款(开发中)的综合信息收集工具,当前功能:

​	  [-]子域名爆破&爬虫提取子域名

​	  [-]验活&超时二次检测	

​	  [-]端口存活扫描

[+]Version 0.0.1​

<img width="1480" height="760" alt="image" src="https://github.com/user-attachments/assets/3db4f7a8-ef94-4724-9e94-b53ccedc8dbe" />
<img width="1480" height="760" alt="image" src="https://github.com/user-attachments/assets/33ffd8c8-badb-4238-bba5-4cb07e3c3d41" />


————————————————————————————————————————————————————

## 配置

配置目录`\config\config.txt`

目前可自定义`线程`、 `超时时间`、`子域名超时复检时间`

————————————————————————————————————————————————————

## 子域名扫描

通过爆破与爬虫来发现子域名；子域名超时复检。


#### <-使用说明->

    <u>举例：</u>想找`google.cn`的子域名，那就输入`google.cn`

    程序会在当前文件夹生成`./URL/google.cn/`，以及`存活子域名.txt`、`存活日志.txt`、`超时子域名.txt`

————————————————————————————————————————————————————

## 端口扫描

可选择1000常见端口、全端口、自定义端口。

————————————————————————————————————————————————————

## 字典

**子域名**

    子域名爆破->`\dictionary\submins.txt`

**端口扫描**

    默认1000端口字典->`\dictionary\1000-port.txt`

    全端口字典->`\dictionary\all-port.txt`

    用户自定义端口->`\dictionary\user-define-port.txt`

