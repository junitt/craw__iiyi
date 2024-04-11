from medical_record import medical_record_manager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from util import *
from tqdm import tqdm
from cv_mod.cv_puzzle_detect import detector
from slider import CrackSlider
tot=0


def parse_web(id,driver):
    url=f"https://bingli.iiyi.com/show/{id}-1.html"
    # time.sleep(0.1)
    # driver.get(url)
    # if 404==driver.execute_script("return window.performance.getEntries()[0].responseStatus;"):
    #     return None
    medical_record={"title": '',
        "department": '',
        "url": url,
        "id":str(id)
    }
    title=driver.find_elements(By.XPATH,'/html/body/div[2]/div[3]/div[2]/div[1]/h2')[0].text
    medical_record["title"]=title
    medical_record['department']=driver.find_elements(By.XPATH,'/html/body/div[2]/div[3]/div[2]/div[2]/a[1]')[0].text+' '+driver.find_elements(By.XPATH,'/html/body/div[2]/div[3]/div[2]/div[2]/a[2]')[0].text
    elements=driver.find_elements(By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[3]/div[1]/p[1]/span')
    patient_base=elements[0].text
    elements=driver.find_elements(By.TAG_NAME,'h3')
    raw_record_pair=extract_raw_record_from_eles(elements)
    raw_record_pair["一般资料"]=patient_base
    elements=driver.find_elements(By.TAG_NAME,'h2')
    for e in elements:
        if e.text=='【分析总结】':
            attr_cont=e.find_element(By.XPATH,'..').text
            raw_record_pair['分析总结']=attr_cont[len('【分析总结】')+2:]
    raw_record_pair=final_proc_record(raw_record_pair)
    raw_record_pair['查体']=raw_record_pair['查体'].replace('/分','/min').replace('℃','度').replace('：','是')
    medical_record['raw_medical_record']=raw_record_pair
    return medical_record

def solve(id,driver,slider_manager:CrackSlider,Detector:detector):
    url=f"https://bingli.iiyi.com/show/{id}-1.html"
    time.sleep(0.1)
    driver.get(url)
    if 404==driver.execute_script("return window.performance.getEntries()[0].responseStatus;"):
        return None
    if(slider_manager.slider_is_exist()):
        elements=driver.find_elements(By.XPATH,'/html/body/div[7]/div/div[3]/img')
        save_pt=slider_manager.save_img(elements[0].get_attribute('src'))
        if save_pt=='':
            return None
        distance=Detector.get_distance(save_pt)
        slider_manager.crack_slider(distance)
        time.sleep(2)
    return parse_web(id,driver)

def main():
    
    manager=medical_record_manager(root='.\\src\\data\\raw_patient.json')
    server_root='d:\\tools\\chromedriver.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_argument('log-level=3')
    option.add_argument("--user-data-dir="+r"C:/Users/liziyang/AppData/Local/Google/Chrome/User Data/")
    option.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=option,executable_path=server_root)
    slider_manager=CrackSlider(driver)
    Detect=detector()

    global tot
    #66450
    for id in tqdm(range(66150,66450,1)):
        # obj=parse_web(id,driver)
        obj=solve(id,driver,slider_manager,Detect)
        if obj is not None:
            tot+=1
            manager.load_record(obj)
    manager.save_file()
    print(tot)
    # time.sleep(30)

if __name__=='__main__':
    main()