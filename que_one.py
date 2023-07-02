import requests
from lxml import html
from lxml import etree
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def search_text():
    with open("./data/mydata.txt", "r") as file:
        websites = file.readlines()
    # print(websites)
    for website in websites:
        # 去除换行符
        website = 'https:'+website.strip()
        print(website)
        try:
            # 发送GET请求获取网站内容
            response = requests.get(website)

            # 使用 lxml 解析网站内容
            get_content = html.fromstring(response.content)

            # 提取和处理网页内容
            # 1.收集索引号、发布机构、发布日期、政策标题、政策正文文本、政策正文附件链接，以上六项信息

            title, release_date = get_content.xpath("//td[@class='td-value']/span/text()")[2:]
            index, agency = get_content.xpath("//td[@class='td-value-xl']/span/text()")[:2]
            policy_text = "".join(get_content.xpath("/html/body/div[2]/div[4]/div[3]/div[3]/div[2]/p/text()"))
            att_link = get_content.xpath("/html/body/div[2]/div[4]/div[3]/div[3]/div[2]/p[21]/a/@href")
            print("[政策标题]:", title)
            print("[索引号]:", index)
            print("[发布机构]:", agency)
            print("[发布日期]:", release_date)
            print("[政策正文文本]:", policy_text)
            print("[政策正文附件]:", att_link)

        except requests.exceptions.RequestException as e:
            print(f"[Error]: Failed to fetch content from {website}: {e}")

def search_data(start_date, end_date):
    global driver
    driver = webdriver.Edge()
    driver.get('https://www.gd.gov.cn/gkmlpt/policy')
    # element = driver.find_elements_by_class_name("document-number").getText()
    # print(element)
    driver.implicitly_wait(10)
    page_text = driver.page_source
    tree = etree.HTML(page_text)
    # li_list = tree.xpath('//*[@id="postList"]/table/tbody/tr/td[2]/text()')
    li_list = tree.xpath('//*[@id="postList"]/div/a[6]/text()')
    flag = True
    # 写入文件
    filename = "./data/mydata.txt"
    # 打开文件以供写入（如果文件不存在会自动创建）
    file = open(filename, "w")

    for i in range(int(li_list[0])):
        if flag:
            page_text = driver.page_source
            tree = etree.HTML(page_text)
            start = tree.xpath('//*[@id="postList"]/table/tbody/tr/td[2]/text()')
            href = tree.xpath('//*[@id="postList"]/table/tbody/tr/td[1]/a/@href')
            for i in range(len(start)):
                if start_date < start[i] < end_date:
                    # print(start[i], ':', href[i])
                    file.write(href[i] + "\n")
                elif start[i] < start_date:
                    print('--------查询结束！---------')
                    flag = False
                    break
            # a = tree.xpath('//*[@id="postList"]/table/tbody/tr/td[1]/a/text()')
            wait = WebDriverWait(driver, 10)
            # sleep(5)

            next_button = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="next"]')))
            # 点击下一页按钮
            # next_button.click()
            driver.execute_script("arguments[0].click();", next_button)
            # sleep(5)
        else:
            break

    driver.quit()
    file.close()
    search_text()


if __name__ == "__main__":
    # 1.收集索引号、发布机构、发布日期、政策标题、政策正文文本、政策正文附件链接，以上六项信息
    # 2.可以收集特定时间区间内的全部政策信息
    # 测试代码
    start_date = '2023-01-01'
    end_date = '2023-06-01'
    result = search_data(start_date, end_date)
