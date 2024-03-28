# -*- coding: utf-8 -*-#
import getpass
import random
from playwright.sync_api import sync_playwright, expect
import time
USER_DIR_PATH = f"C:\\Users\\{getpass.getuser()}\\AppData\Local\Google\Chrome\\User Data"


def get_ip():
    list_ip = []
    with open('proxy.txt', mode='r', encoding='utf-8') as f:
        ips = f.readlines()
    for ip in ips:
        ip = ip.strip()
        ip = ip.replace(":", "@", 1)
        list_ip.append(ip)
    sk_ip = random.choice(list_ip)
    user, pw, ip = sk_ip.split('@')
    proxy = {"server": f"http://{ip}",
             "username": user,
             "password": pw
             },
    print(proxy[0])
    return proxy[0], ip

def get_data_info():
    list_ip = []
    with open('data.txt', mode='r', encoding='utf-8') as f:
        ips = f.readlines()
    for ip in ips:
        ip = ip.strip()
        list_ip.append(ip)
    sk_ip = random.choice(list_ip)
    return sk_ip


def get_config(user, pwd, proxy, ip,data_info):
    i = 1
    while i < 4 :
        try:
            if proxy:
                with sync_playwright() as p:
                    browser = p.chromium.launch(
                        # 指定本机用户缓存地址
                        # user_data_dir=USER_DIR_PATH,
                        # 接收下载事件
                        # accept_downloads=True,
                        # 设置 GUI 模式
                        headless=False,
                        # bypass_csp=True,
                        slow_mo=500,
                        proxy=proxy,
                        args=['--disable-blink-features=AutomationControlled']
                    )
            else:
                with sync_playwright() as p:
                    browser = p.chromium.launch(
                        # 指定本机用户缓存地址
                        # user_data_dir=USER_DIR_PATH,
                        # 接收下载事件
                        # accept_downloads=True,
                        # 设置 GUI 模式
                        headless=False,
                        # bypass_csp=True,
                        slow_mo=500,
                        # proxy=proxy,
                        args=['--disable-blink-features=AutomationControlled']
                    )

                    page = browser.new_page()
                    page.context.clear_cookies()
                    page.goto("https://platform.openai.com/login?launch")
                    page.get_by_label("Email address").click(modifiers=["Control"])
                    page.get_by_label("Email address").fill(user)
                    page.locator("button[name=\"action\"]").click()
                    page.get_by_label("Password").click(modifiers=["Control"])
                    page.get_by_label("Password").fill(pwd)
                    page.get_by_role("button", name="Continue").click()
                    try:
                        locator_1 = page.locator('[id="error-element-password"]')
                        expect(locator_1).to_have_text("Wrong email or password", timeout=3000)
                        print('密码错误')
                        with open('密码错误.txt', mode='a', encoding='utf-8') as f:
                            f.write(f'{user}----{pwd}\n')
                        return
                    except:
                        page.goto("https://openai.com/waitlist/gpt-4-api")
                        with page.expect_popup() as popup_info:
                            page.get_by_role("link", name="account settings").click()
                        time.sleep(3)
                        page1 = popup_info.value
                        res1 = page1.locator("//div[2]/input")
                        key = res1.get_attribute("value")
                        page1.close()
                        page.get_by_label("Organization ID *").fill(key)
                        name = user.split('@')[0]
                        page.get_by_label("First name *").fill(name)
                        page.get_by_label("Last name *").fill(name)
                        page.get_by_label("Email *").fill(user)
                        page.get_by_label("Academic research").check()
                        page.get_by_placeholder(
                            "For use cases we tried, GPT-3.5 did not reliably handle multi-language text. We hope to explore GPT-4 for this use case.").fill(
                            data_info)

                        page.get_by_role("button", name="Join waitlist").click()
                        print(f'{user} 申请成功')
                        time.sleep(3)
                        with open('申请成功.txt', mode='a', encoding='utf-8') as f:
                            f.write(f'{user}----{pwd}\n')
                        page.close()
                        return
        except:
            i += 1
    else:
        with open('失败.txt', mode='a', encoding='utf-8') as f:
            f.write(f'{user}----{pwd}\n')
        print(f'{user} 失败....')



if __name__ == '__main__':
    # 调用函数 随机获取一个ip
    kg_ip = input('是否使用代理ip(y/n):')
    if kg_ip == 'y':
        proxy, ip = get_ip()
        with open('账号.txt', mode='r', encoding='utf-8') as f:
            data = f.readlines()
        for i in data:
            i = i.strip()
            user = i.split('----')[0]
            pwd = i.split('----')[1]
            data_info = get_data_info()
            get_config(user, pwd, proxy, ip,data_info)
    else:
        with open('账号.txt', mode='r', encoding='utf-8') as f:
            data = f.readlines()
        for i in data:
            i = i.strip()
            user = i.split('----')[0]
            pwd = i.split('----')[1]
            data_info = get_data_info()
            proxy = False
            ip = False
            get_config(user, pwd, proxy, ip,data_info)

