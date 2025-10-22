# databricks-flask-xray
> 脚本来自老王,稍作修改([`forked from eooce/python-xray-argo`](https://github.com/eooce/python-xray-argo))
> 
> 对于服务器脚本检测风险片段进行了base64编码
> 
> 如：NEZHA类、VMESS、Vless、Trogan 等相关配置
>
> 删减了TG通知（个人感觉部署项目不需要通知，保留在保活脚本中：健康检测、启动、停止）
>
> 方式1：一键部署，WEB无法公网访问；在面板中访问站点链接： /sub 获取节点
>
> 方式2：配置ARGO（节点8001和web8000两个隧道），默认启动时不开启节点服务，服务器不存在节点相关的程序和配置文件，安全
>
>>使用 /start 可以启动节点服务部署
>
>>使用 /stop 可以停止节点服务，关闭隧道（保留WEB隧道，确保自定义域名可用），并清理相关文件
>
>>使用 /sub-status 查看节点服务状态和节点信息
>
>>使用 /<SUB_PATH> 订阅节点

## ** 方式一. 一键部署，不修改任何内容，直接上传，通过/sub 获取订阅节点
> 优点：操作简单
> 
> 缺点：argo默认随机通道，每次重启节点会变，需要更新订阅
```bash
# 文件清单
./
  static/
    index.html      #默认网站页面
  app.py
  app.yml
  main.py
  env.conf
  requirements.txt
```

## ** 方式二、 配置环境变量**
> 环境变量配置文件：`env.conf`
>
> 配置后，进行base64编码，保存到`env.conf`中
```python
_SUB_PATH='sub'
_NAME='dbs-xray'
_UUID=''
_WEB_DOMAIN='' #databricks设置自定义域名
_WEB_ARGO_AUTH='' #databricks设置web隧道token
_ARGO_DOMAIN='' 
_ARGO_AUTH=''

WEB_ARGO_DOMAIN=os.environ.get('WEB_DOMAIN',_WEB_DOMAIN)
WEB_ARGO_AUTH = os.environ.get('WEB_ARGO_AUTH', _WEB_ARGO_AUTH)
FILE_PATH = os.environ.get('FILE_PATH', './.cache')    
SUB_PATH = os.environ.get('SUB_PATH', _SUB_PATH)           
UUID = os.environ.get('UUID', _UUID)  
NEZHA_SERVER = os.environ.get('NEZHA_SERVER', '')      
NEZHA_PORT = os.environ.get('NEZHA_PORT', '')          
NEZHA_KEY = os.environ.get('NEZHA_KEY', '')            
ARGO_DOMAIN = os.environ.get('ARGO_DOMAIN', _ARGO_DOMAIN)        
ARGO_AUTH = os.environ.get('ARGO_AUTH', _ARGO_AUTH)            
ARGO_PORT = int(os.environ.get('ARGO_PORT', '8001'))   
CFIP = os.environ.get('CFIP', 'www.visa.com.tw')       
CFPORT = int(os.environ.get('CFPORT', '443'))          
NAME = os.environ.get('NAME', _NAME)                   
PORT = int(os.environ.get('SERVER_PORT') or os.environ.get('PORT') or 3000)
```
