# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

def getData():
    cookies = {
        "sessionid_admin": "NDM3ZWNiNzktNDI4Ni00MmM3LTgxNTUtMDFlOTMyNzIwYjU2"
    }
    headers = {
        "Referer": "http://192.168.134.130:30869/gathering-code",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
    }
    ans = []
    for i in range(1,2):
        url = f"http://192.168.134.130:30869/gatheringCode/findGatheringCodeByPage?pageSize=9867&pageNum={i}&state=&gatheringChannelId=&userName=&exceptionFlag=&auditStatus="
        s = requests.get(url=url,cookies=cookies, headers=headers)
        s.encoding = "utf-8"
        html = s.text
        html = html.replace("true", "True").replace("false", "False").replace("null", "False")
        html = eval(html)
        print(html["data"]["content"][0]["id"])
        for con in html["data"]["content"]:
            temp = []
            temp.append(con["gatheringChannelName"] + "/" + con["userName"])
            if con["gatheringChannelName"] in ["银行卡", "微信转银行卡"]:
                temp.append("银行/开户人:" + con["openAccountBank"]+"/"+con["accountHolder"]+"卡号:"+con["bankCardAccount"])
            elif con["gatheringChannelName"] in ["微信", "支付宝"]:
                temp.append("收款人:"+con["account"])
            elif con["gatheringChannelName"] in ["支付宝id转账"]:
                temp.append("账号:"+con["account"]+"支付宝id:"+con["alipayId"])
            elif con["gatheringChannelName"] in ["微信手机转账"]:
                temp.append("手机号/姓名:"+con["mobile"]+"/"+con["realName"])
            elif con["gatheringChannelName"] in ["支付宝转账"]:
                temp.append("账号:"+con["account"]+"姓名:"+con["realName"])
            temp.append("通过")
            if con["deleteFlag"] == False:
                temp.append("正常")
            else:
                temp.append("已删除")
            if con["exceptionFlag"] == False:
                temp.append("正常")
            else:
                temp.append("收款异常")
            temp.append(con["createTime"])
            temp.append(f"{con['totalTradeAmount']}元/{con['totalPaidOrderNum']}次/{con['totalOrderNum']}次/{con['totalSuccessRate']}%")
            temp.append(f"{con['todayTradeAmount']}元/{con['todayPaidOrderNum']}次/{con['todayOrderNum']}次/{con['todaySuccessRate']}%")
            if con["storageId"] == False:
                temp.append("接单记录彻底删除")
            else:
                temp.append("接单记录查看二维码彻底删除")
            ans.append(temp)
    return ans

def writeCSV(result):
    f = open("fuck.txt", "w", encoding="utf8")
    f.write("通道/所属账号,详细信息,审核状态,删除状态,收款状态,创建时间,累计收款/收款次数/接单次数/成功率,今日收款/收款次数/接单次数/成功率,操作" + "\n")
    for i in range(len(result)):
        f.write(",".join(result[i]) + "\n")
    f.close()

def getImage():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    cookies = {
    "domain": "192.168.134.130",
    "name": "sessionid_admin",
    "path": "/",
    "value": "NDM3ZWNiNzktNDI4Ni00MmM3LTgxNTUtMDFlOTMyNzIwYjU2",
}
    browser.get("http://192.168.134.130:30869/login")
    browser.add_cookie(cookie_dict=cookies)
    browser.get("http://192.168.134.130:30869/gathering-code")
    bot_10 = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="gathering-code"]/div[2]/div[3]/div[1]/span[2]/span/button/span[1]')))
    bot_10.click()
    bot_100 = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="gathering-code"]/div[2]/div[3]/div[1]/span[2]/span/div/a[4]')))
    bot_100.click()
    ele = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="gathering-code"]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[1]')))
    time.sleep(2)
    height = browser.execute_script(
        "return  document.body.offsetHeight;")
    print(height)
    browser.set_window_size(1489, height-2300)
    time.sleep(2)
    browser.save_screenshot("./png1/1.png")
    print("1.png is ok")
    for i in range(99):
        next_page = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="gathering-code"]/div[2]/div[3]/div[2]/ul/li[9]/a')))
        next_page.click()
        time.sleep(3)
        height = browser.execute_script(
            "return  document.body.offsetHeight;")
        print(height)
        browser.set_window_size(1489, height)
        browser.save_screenshot(f"./png1/{i+2}.png")
        print(f"{i+2}.png is ok")
    browser.close()

if __name__ == '__main__':
    ans = getData()
    writeCSV(ans)
    getImage()
