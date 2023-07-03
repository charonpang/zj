import lxml.html
import requests
from lxml import html
from lxml import etree
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from io import BytesIO

# class CrackSlider():
#     # 通过浏览器截图，识别验证码中缺口位置，获取需要滑动距离，并破解滑动验证码
#
#     def __init__(self):
#         super(CrackSlider, self).__init__()
#         self.opts = webdriver.ChromeOptions()
#         self.opts.add_experimental_option('excludeSwitches', ['enable-logging'])
#         self.driver = webdriver.Edge()
#
#         self.url = 'https://icas.jnu.edu.cn/cas/login'
#         self.wait = WebDriverWait(self.driver, 10)
#
#     def get_pic(self):
#         self.driver.get(self.url)
#         time.sleep(5)
#         target_link = self.driver.find_element(By.CLASS_NAME, "yidun_bg-img").get_attribute('src')
#         template_link = self.driver.find_element(By.CLASS_NAME, "yidun_jigsaw").get_attribute('src')
#
#         target_img = Image.open(BytesIO(requests.get(target_link).content))
#         template_img = Image.open(BytesIO(requests.get(template_link).content))
#         target_img.save('target.jpg')
#         template_img.save('template.png')
#
#     def crack_slider(self, distance):
#         slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'yidun_slider')))
#         ActionChains(self.driver).click_and_hold(slider).perform()
#         ActionChains(self.driver).move_by_offset(xoffset=distance, yoffset=0).perform()
#         time.sleep(2)
#         ActionChains(self.driver).release().perform()
#         return 0
#
#
# def add_alpha_channel(img):
#     """ 为jpg图像添加alpha通道 """
#
#     r_channel, g_channel, b_channel = cv2.split(img)  # 剥离jpg图像通道
#     alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255  # 创建Alpha通道
#
#     img_new = cv2.merge((r_channel, g_channel, b_channel, alpha_channel))  # 融合通道
#     return img_new
#
#
# def handel_img(img):
#     imgGray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)  # 转灰度图
#     imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # 高斯模糊
#     imgCanny = cv2.Canny(imgBlur, 60, 60)  # Canny算子边缘检测
#     return imgCanny
#
#
# def match(img_jpg_path, img_png_path):
#     # 读取图像
#     img_jpg = cv2.imread(img_jpg_path, cv2.IMREAD_UNCHANGED)
#     img_png = cv2.imread(img_png_path, cv2.IMREAD_UNCHANGED)
#     # 判断jpg图像是否已经为4通道
#     if img_jpg.shape[2] == 3:
#         img_jpg = add_alpha_channel(img_jpg)
#     img = handel_img(img_jpg)
#     small_img = handel_img(img_png)
#     res_TM_CCOEFF_NORMED = cv2.matchTemplate(img, small_img, 3)
#     value = cv2.minMaxLoc(res_TM_CCOEFF_NORMED)
#     value = value[3][0]  # 获取到移动距离
#     return value
#
#
# # 1. 打开chromedriver，试试下载图片
# cs = CrackSlider()
# cs.get_pic()
# # 2. 对比图片，计算距离
# img_jpg_path = 'target.jpg'  # 读者可自行修改文件路径
# img_png_path = 'template.png'  # 读者可自行修改文件路径
# distance = match(img_jpg_path, img_png_path)
# distance = distance / 480 * 345 + 12
# # 3. 移动
# cs.crack_slider(distance)
class TianYan():
    def __init__(self):
        self.driver = webdriver.Edge()
        self.ac = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 10)

    def Log_in(self):
        driver = self.driver
        self.driver.get('https://www.tianyancha.com/')
        # element = driver.find_elements_by_class_name("document-number").getText()
        # print(element)
        self.driver.implicitly_wait(10)
        # page_text = driver.page_source
        # tree = etree.HTML(page_text)
        # li_list = tree.xpath('//*[@id="page-container"]/div[1]/div/div[1]/div[2]/div/div[5]/span/text()')
        # print(li_list)

        self.ac.click(driver.find_element(By.CLASS_NAME, "treasure_nav-link__7ErdH")).perform()
        sleep(10)
        # ac.click(driver.find_element(By.CLASS_NAME,"login-toggle -scan")).perform()
        # sleep(5)
        try:
            # 点击短信/密码登录
            next_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="login-toggle -scan"]')))
            driver.execute_script("arguments[0].click();", next_button)
            # 点击密码登录
            log_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="title-password"]')))
            #<div class="title-password">密码登录</div>
            driver.execute_script("arguments[0].click();", log_button)
            # //*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[3]/input
            # 点击已阅读并同意
            agree_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[3]/input')))
            driver.execute_script("arguments[0].click();", agree_button)
        except:
            print("ERROR!")
        # 填入用户名和密码
        username = driver.find_element(By.XPATH, '//*[@class="phone _e3f88 _7c380"]/input')
        username.send_keys('15065549745')
        pwd = driver.find_element(By.XPATH, '//*[@class="password _e3f88 _7c380"]/input')
        pwd.send_keys('ty123456')
        # 点击登录
        log_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="sign-password"]/button')))
        driver.execute_script("arguments[0].click();", log_button)
        # 滑块验证
        # target_link = driver.find_element(By.XPATH, '//*[@class="gt_cut_bg gt_show"]').get_attribute('src')
        # template_link = driver.find_element(By.XPATH, "//*[@class='gt_slice gt_show']").get_attribute('style')
        # print(template_link)
        # <a class="gt_fullbg gt_show" style="cursor: default; background-image: none;">
        # target_img = Image.open(BytesIO(requests.get(target_link).content))

        # template_img = Image.open(BytesIO(requests.get(template_link).content))
        # target_img.save('target.jpg')
        # template_img.save('template.png')
        sleep(5)
        company = input("请输入公司名：")
        self.search_data(company)



    def search_data(self, company):
        filename = "./data/Intellectual_property.txt"
        # 打开文件以供写入（如果文件不存在会自动创建）
        file = open(filename, "w")
        file.write(company+"知识产权：\n")

        driver = self.driver
        sear = driver.find_element(By.XPATH, '//*[@class="_cc76e _7c380 _03321"]')
        sear.send_keys(company)
        # 点击搜索
        s_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="_50ab4 index_home-suggest-button__GuWyT _52bf6"]')))
        driver.execute_script("arguments[0].click();", s_button)
        # 再次搜索
        s2_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="_50ab4 tyc-header-suggest-button _52bf6"]')))
        driver.execute_script("arguments[0].click();", s2_button)
        # 点击知识产权
        z_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="index_filter-type__O4uav"]/a[5]')))
        driver.execute_script("arguments[0].click();", z_button)
        #//*[@id="search_query"]/div[1]/div[4]/div[2]/div[1]/div/div[1]/span[1]
        # mytext = driver.find_elements(By.XPATH, '//*[@id="search_query"]/div[1]/div[4]/div[2]/div/div/div[1]/span[1]/text()')
        while True:
            try:
                mytext = driver.find_elements(By.CLASS_NAME, 'link-hover')
                # print(mytext)
                for i in mytext:
                    print(i.text)
                    file.write(i.text + "\n")
                next_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//i[@class="tic tic-icon-arrow-right"]')))
                # 点击下一页按钮
                driver.execute_script("arguments[0].click();", next_button)
            except:
                print('END!')
                driver.quit()
                file.close()
                return
        driver.quit()
        file.close()

if __name__ == "__main__":
    # 测试代码
    # company = '光年之外'
    # result = Log_in()
    t = TianYan()
    company = '华为技术有限公司'
    t.Log_in()
    #https://www.tianyancha.com/search/t402?key=[公司名称]