from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm

def save_img(img_url,id):
    # url_path = "https://farm6.staticflickr.com/3789/8804001147_d92eb75fff_o.jpg"  #
    try:
        response = requests.get(img_url)
        save_path = f'./src\\ver_img/{id}.png'
        with open(save_path, 'wb') as f:  # 以二进制写入文件保存
            f.write(response.content)
    except:
        return
    # 保存图片到本地
    


def visit(id,driver:webdriver.Chrome):
    time.sleep(0.1)
    url=f"https://bingli.iiyi.com/show/{id}-1.html"
    driver.get(url)
    elements=driver.find_elements(By.XPATH,'/html/body/div[7]/div/div[3]/img')
    save_img(elements[0].get_attribute('src'),id)

if __name__=='__main__':
    server_root='d:\\tools\\chromedriver.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_argument('log-level=3')
    option.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=option,executable_path=server_root)
    for id in tqdm(range(66000,66250,1)):
        visit(id,driver)

