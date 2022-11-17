from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from info_tool import get_user_rating_total
from tqdm.notebook import tqdm
import time
import math
import os


# 點擊「評論」按鈕
def click_on_comment_button(driver):
    # 等待「評論」button 元素加載
    button_XPATH = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]'
    
    print('載入評論頁面中...')
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, button_XPATH)))
    
    # 找到「評論」按鈕並點擊之
    driver.find_element(By.XPATH, button_XPATH).click()


def scroll_comment_section(driver):
    # 等待評論區塊加載
    comment_section_XPATH = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, comment_section_XPATH)))
    time.sleep(10)
    
    # 下滑評論區塊，加載更多評論
    comment_section = driver.find_element(By.CLASS_NAME, 'm6QErb.DxyBCb.kA9KIf.dS8AEf')
    user_ratings_total = get_user_rating_total(driver)
    
    scroll_times = math.ceil(user_ratings_total/10)
    # google map 最多能顯示 1130 則，無論再怎麼滑動都不會回傳新的評論。
    if scroll_times >= 112:
        scroll_times = 112

    # 滑動進度條
    print('滑動評論中...')
    scroll_process = tqdm(total=scroll_times)
    for i in range(scroll_times):
            
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", comment_section)
        time.sleep(1.2)
        
        scroll_process.update(1)


def expand_full_comment(driver):
    # 點擊展開評論全文的按鈕
    time.sleep(6)
    comment_section = driver.find_element(By.CLASS_NAME, 'm6QErb.DxyBCb.kA9KIf.dS8AEf')
    driver.execute_script("arguments[0].scrollTop = arguments[1]", comment_section, 0)
    comment_section = driver.find_element(By.CLASS_NAME, 'm6QErb.DxyBCb.kA9KIf.dS8AEf')
    open_full_comment_button = driver.find_elements(By.CLASS_NAME,"w8nwRe.kyuRq")
    
    # 展開全文進度條
    print('展開評論全文中...')
    button_process = tqdm(total=len(open_full_comment_button))
    
    for button in open_full_comment_button:
        button.click()
        button_process.update(1)
        
