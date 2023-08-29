import ctypes, json, os, time, random, string, getpass, threading, re, sys

try:
    import pystyle
    import colorama
    import tls_client
    import httpx
    import user_agent
    import datetime
except ModuleNotFoundError:
    os.system("pip install pystyle")
    os.system("pip install colorama")
    os.system("pip install tls_client")
    os.system("pip install httpx")
    os.system("pip install user_agent")
    os.system("pip install datetime")

from pystyle import Write, System, Colorate, Colors
from colorama import Fore, Style, init

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT

success = 0
failed = 0
generated_agents = 0
total = 1

start = time.time()
ctypes.windll.kernel32.SetConsoleTitleW(f'[ Tiktok MassReport ] By H4cK3dR4Du & 452b')

def save_proxies(proxies):
    with open("proxies.txt", "w") as file:
        file.write("\n".join(proxies))

def get_proxies():
    with open('proxies.txt', 'r', encoding='utf-8') as f:
        proxies = f.read().splitlines()
    if not proxies:
        proxy_log = {}
    else:
        proxy = random.choice(proxies)
        proxy_log = {
            "http://": f"http://{proxy}", "https://": f"http://{proxy}"
        }
    try:
        url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
        response = httpx.get(url, proxies=proxy_log, timeout=60)

        if response.status_code == 200:
            proxies = response.text.splitlines()
            save_proxies(proxies)
        else:
            time.sleep(1)
            get_proxies()
    except httpx.ProxyError:
        get_proxies()
    except httpx.ReadError:
        get_proxies()
    except httpx.ConnectTimeout:
        get_proxies()
    except httpx.ReadTimeout:
        get_proxies()
    except httpx.ConnectError:
        get_proxies()
    except httpx.ProtocolError:
        get_proxies()

def check_proxies_file():
    file_path = "proxies.txt"
    if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
        get_proxies()

with open(f"config.json") as f:
    data = json.load(f)
    if data["proxy_scraper"] == "y" or data["proxy_scraper"] == "yes":
        check_proxies_file()
    else:
        pass

def update_console_title():
    global success, failed, generated_agents, total
    success_rate = round(success/total*100,2)
    ctypes.windll.kernel32.SetConsoleTitleW(f'[ Tiktok MassReport ] By H4cK3dR4Du & 452b | Reports Sent : {success} ~ Failed : {failed} ~ Success Rate : {success_rate}%')

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def check_ui():
    output_lock = threading.Lock()
    while True:
        success_rate = round(success/total*100,2)
        System.Clear()
        with output_lock:
            Write.Print(f"""
\t\t\t▄▄▄▄▄▪  ▄ •▄ ▄▄▄▄▄      ▄ •▄     ▄▄▄  ▄▄▄ . ▄▄▄·      ▄▄▄  ▄▄▄▄▄
\t\t\t•██  ██ █▌▄▌▪•██  ▪     █▌▄▌▪    ▀▄ █·▀▄.▀·▐█ ▄█▪     ▀▄ █·•██  
\t\t\t ▐█.▪▐█·▐▀▀▄· ▐█.▪ ▄█▀▄ ▐▀▀▄·    ▐▀▀▄ ▐▀▀▪▄ ██▀· ▄█▀▄ ▐▀▀▄  ▐█.▪
\t\t\t ▐█▌·▐█▌▐█.█▌ ▐█▌·▐█▌.▐▌▐█.█▌    ▐█•█▌▐█▄▄▌▐█▪·•▐█▌.▐▌▐█•█▌ ▐█▌·
\t\t\t ▀▀▀ ▀▀▀·▀  ▀ ▀▀▀  ▀█▄▀▪·▀  ▀    .▀  ▀ ▀▀▀ .▀    ▀█▄▀▪.▀  ▀ ▀▀▀ 

----------------------------------------------------------------------------------------------------------------------
\t\t\tSent Reports : [ {success} ] ~ Failed : [ {failed} ] ~ Success Rate : [ {success_rate}% ]
----------------------------------------------------------------------------------------------------------------------
""" , Colors.blue_to_red, interval=0.000)
            time.sleep(10)

def mass_report():
    global success, total, failed, generated_agents
    proxy = random.choice(open("proxies.txt", "r").readlines()).strip() if len(open("proxies.txt", "r").readlines()) != 0 else None

    session = tls_client.Session(
        client_identifier="chrome_113",
        random_tls_extension_order=True
    )

    if "@" in proxy:
        user_pass, ip_port = proxy.split("@")
        user, password = user_pass.split(":")
        ip, port = ip_port.split(":")
        proxy_string = f"http://{user}:{password}@{ip}:{port}"
    else:
        ip, port = proxy.split(":")
        proxy_string = f"http://{ip}:{port}"

    session.proxies = {
        "http": proxy_string,
        "https": proxy_string
    }
    with open(f"config.json") as f:
        data = json.load(f)
        url = data['report_url']
        report_types = data['report_types']

        if report_types["Violence"] == "y" or report_types["Violence"] == "yes":
            report_type = 90013
        elif report_types["Sexual Abuse"] == "y" or report_types["Sexual Abuse"] == "yes":
            report_type = 90014
        elif report_types["Animal Abuse"] == "y" or report_types["Animal Abuse"] == "yes":
            report_type = 90016
        elif report_types["Criminal Activities"] == "y" or report_types["Criminal Activities"] == "yes":
            report_type = 90017
        elif report_types["Hate"] == "y" or report_types["Hate"] == "yes":
            report_type = 9020
        elif report_types["Bullying"] == "y" or report_types["Bullying"] == "yes":
            report_type = 9007
        elif report_types["Suicide Or Self-Harm"] == "y" or report_types["Suicide Or Self-Harm"] == "yes":
            report_type = 90061
        elif report_types["Dangerous Content"] == "y" or report_types["Dangerous Content"] == "yes":
            report_type = 90064
        elif report_types["Sexual Content"] == "y" or report_types["Sexual Content"] == "yes":
            report_type = 90084
        elif report_types["Porn"] == "y" or report_types["Porn"] == "yes":
            report_type = 90085
        elif report_types["Drugs"] == "y" or report_types["Drugs"] == "yes":
            report_type = 90037
        elif report_types["Firearms Or Weapons"] == "y" or report_types["Firearms Or Weapons"] == "yes":
            report_type = 90038
        elif report_types["Sharing Personal Info"] == "y" or report_types["Sharing Personal Info"] == "yes":
            report_type = 9018
        elif report_types["Human Exploitation"] == "y" or report_types["Human Exploitation"] == "yes":
            report_type = 90015
        elif report_types["Under Age"] == "y" or report_types["Under Age"] == "yes":
            report_type = 91015
    
    output_lock = threading.Lock()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62"
    }

    try:
        match_reason = re.search(r'reason=(\d+)', url)
        match_nickname = re.search(r'nickname=([^&]+)', url)
        match_owner_id = re.search(r'owner_id=([^&]+)', url)
        if match_nickname:
            username = match_nickname.group(1)
        if match_owner_id:
            iduser = match_owner_id.group(1)
        if match_reason:
            reason_number = match_reason.group(1)
            new_url = url.replace(f"reason={reason_number}", f"reason={report_type}")
            report = session.get(new_url)
            if "Thanks for your feedback" in report.text:
                with output_lock:
                    time_rn = get_time_rn()
                    print(f"[ {magenta}{time_rn}{reset} ] | ( {green}+{reset} ) {blue}Reported with successfull to ", end='')
                    sys.stdout.flush()
                    Write.Print(f"{username} ~ {iduser}\n", Colors.purple_to_red, interval=0.000)
                    success += 1
                    total += 1
                    update_console_title()
                    mass_report()
            elif report.status_code == 200:
                with output_lock:
                    time_rn = get_time_rn()
                    print(f"[ {magenta}{time_rn}{reset} ] | ( {green}+{reset} ) {blue}Reported with successfull to ", end='')
                    sys.stdout.flush()
                    Write.Print(f"{username} ~ {iduser}\n", Colors.purple_to_red, interval=0.000)
                    success += 1
                    total += 1
                    update_console_title()
                    mass_report()
            else:
                with output_lock:
                    time_rn = get_time_rn()
                    print(f"[ {magenta}{time_rn}{reset} ] | ( {red}-{reset} ) {yellow}Cannot report to ", end='')
                    sys.stdout.flush()
                    Write.Print(f"{username} ~ {iduser}\n", Colors.purple_to_red, interval=0.000)
                    failed += 1
                    total += 1
                    update_console_title()
                    mass_report()
        else:
            mass_report()  
    except Exception as e:
        failed += 1
        total += 1
        update_console_title()
        mass_report()

def mass_report_thread():
    mass_report()

def check_ui_thread():
    check_ui()

num_threads = data['threads']
threads = []

with threading.Lock():
    for _ in range(num_threads - 1):
        thread = threading.Thread(target=mass_report_thread)
        thread.start()
        threads.append(thread)

    check_ui_thread = threading.Thread(target=check_ui_thread)
    check_ui_thread.start()
    threads.append(check_ui_thread)

    for thread in threads:
        thread.join()
