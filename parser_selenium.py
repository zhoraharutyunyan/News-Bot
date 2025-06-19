from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
import pandas as pd
from selenium.webdriver.chrome.options import Options




driver = webdriver.Chrome()
driver.fullscreen_window()
actions = ActionChains(driver)
wait = WebDriverWait(driver, 10)

news_list = []
news_target = []
categories = ['Քաղաքական', 'Իրավական', 'Սպորտ', 'Կրթություն']
pages = ['body > main > div > div > div.col-md-8 > div > div.post-pagination.clearfix > ul > li:nth-child(6) > a', # 1
         'body > main > div > div > div.col-md-8 > div > div.post-pagination.clearfix > ul > li:nth-child(8) > a', # 2
         'body > main > div > div > div.col-md-8 > div > div.post-pagination.clearfix > ul > li:nth-child(9) > a', # 3
         'body > main > div > div > div.col-md-8 > div > div.post-pagination.clearfix > ul > li:nth-child(10) > a', # 4
         'body > main > div > div > div.col-md-8 > div > div.post-pagination.clearfix > ul > li:nth-child(11) > a']# >5

try:
    driver.get('https://www.aravot.am/')
    time.sleep(3)
    for i in categories:
        if i == 'Քաղաքական':
            driver.find_element(By.CSS_SELECTOR, '#menu-item-964353 > a').click()
        elif i == 'Իրավական':
            driver.find_element(By.CSS_SELECTOR, '#menu-item-964354 > a').click()
        elif i == 'Սպորտ':
            driver.find_element(By.CSS_SELECTOR, '#menu-item-964359 > a').click()
        else:
            driver.find_element(By.CSS_SELECTOR, '#menu-item-964358 > a').click()
        time.sleep(3)

        for news_i in range(1, 11):
            try:
                news = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'body > main > div > div > div.col-md-8 > div > div:nth-child({news_i}) > div.col-9 > h6 > a'))).text
                news_list.append(news)
                news_target.append(i)
            except:
                print(f'News {news_i} not found on category {i}')

        for page in range(1, 6):  # You have only 5 page selectors
            try:
                page_selector = pages[page - 1]
                item = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, page_selector)))

                # Scroll to element
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", item)
                time.sleep(1)  # Optional: Let the scroll finish

                # Click safely
                item.click()
                time.sleep(3)

                # Scrape news on this page
                for news_i in range(1, 11):
                    try:
                        news = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'body > main > div > div > div.col-md-8 > div > div:nth-child({news_i}) > div.col-9 > h6 > a'))).text
                        news_list.append(news)
                        news_target.append(i)
                        print(news)
                    except:
                        print(f'News {news_i} not found on page {page} in category {i}')
            except Exception as e:
                print(f'Error on page {page}: {e}')
    df = pd.DataFrame(data=news_list, columns=['news'])
    df['target'] = news_target
    df.to_csv('news.csv', index=False, index_label=False)
except Exception as ex:
    print(f'Error: {ex.__class__.__name__}')
finally:
    driver.close()
    driver.quit()
