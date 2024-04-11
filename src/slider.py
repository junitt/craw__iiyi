import re
import requests
import time
from io import BytesIO
 
import cv2
import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
class CrackSlider():
    # 通过浏览器截图，识别验证码中缺口位置，获取需要滑动距离，并破解滑动验证码
 
    def __init__(self,driver):
        self.driver =driver
        self.wait = WebDriverWait(self.driver, 10)

    def save_img(self,img_url):
    # url_path = "https://farm6.staticflickr.com/3789/8804001147_d92eb75fff_o.jpg"  #
        try:
            response = requests.get(img_url)
            save_path = f'./src/target.png'
            with open(save_path, 'wb') as f:  # 以二进制写入文件保存
                f.write(response.content)
            return save_path
        except:
            return ''

    def slider_is_exist(self):
        return len(self.driver.find_elements(By.CLASS_NAME,'sliderS')) != 0
    
    def crack_slider(self, distance):
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sliderS')))
        ActionChains(self.driver).click_and_hold(slider).perform()
        ActionChains(self.driver).move_by_offset(xoffset=distance, yoffset=0).perform()
        time.sleep(1)
        ActionChains(self.driver).release().perform()
        return 0