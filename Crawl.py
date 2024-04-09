import re
import time
from time import sleep
import re, requests, csv
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
import konlpy
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import PIL
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Pool
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from PIL import Image
import requests
from io import BytesIO
from docx import Document
import logging
import io
import os
import tempfile  # 임시 파일을 위한 모듈
import pytesseract
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/sindarong/Downloads/cap-pj-877bb00de996.json"

logging.basicConfig(level=logging.INFO)

def save_texts_to_txt(texts, filename):
    """텍스트 리스트를 .txt 파일로 저장하되, 특정 형식에 맞게 변환"""
    with open(filename, 'w', encoding='utf-8') as file:
        for text in texts:
            # 여기서 변환 로직을 적용합니다
            # '. /'를 찾아서 '. '으로 변경합니다.
            text = text.replace(". /", ". ")
            file.write(text + "\n")  # 각 텍스트 뒤에 줄바꿈을 추가합니다.
    logging.info(f".txt document saved: {filename}")

def extract_text_from_images(image_urls):
    """이미지 URL 목록에서 텍스트를 추출하여 반환합니다."""
    all_texts = []  # 추출된 텍스트들을 저장할 리스트
    client = vision.ImageAnnotatorClient()

    for url in image_urls:
        try:
            image = vision.Image()
            image.source.image_uri = url

            response = client.text_detection(image=image)
            annotations = response.text_annotations
            if annotations:
                text = annotations[0].description  # 첫 번째 텍스트 어노테이션에는 이미지 전체의 텍스트가 포함되어 있습니다.
            else:
                text = "No text found"
            all_texts.append(text + ". /")
            print(text)
        except Exception as e:
            print(f"Error extracting text from {url}: {e}")

    return all_texts

def collect_reviews(args):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from time import sleep
    import pandas as pd

    next_list_count, first_page = args
    options = Options()
    options.headless = True 
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    df = pd.DataFrame(columns=['num','summary', 'grade', 'review'])

    df_idx = 0  # 데이터프레임 인덱스 초기화
    
    try:
        url = "https://brand.naver.com/microsoftshop/products/8978087157"
        driver.get(url)
        sleep(2)  # 페이지 로딩 대기
        
        if first_page == 4:
            product_html = driver.find_element(By.CSS_SELECTOR, 'div.se-main-container').get_attribute('innerHTML')
            print(product_html)
            soup = BeautifulSoup(product_html, 'html.parser')

            # data-src 속성을 가진 모든 img 태그 찾기
            images = soup.find_all('img', {'data-src': True})

            # 각 img 태그의 data-src 속성값 추출
            image_urls = [img['data-src'] for img in images]
            all_texts = extract_text_from_images(image_urls)
            print(all_texts)
            save_texts_to_txt(all_texts, "extracted_texts.txt")
            sleep(2)
        driver.find_element(By.CSS_SELECTOR, '#content > div > div.z7cS6-TO7X > div._27jmWaPaKy > ul > li:nth-child(2) > a').click()
        sleep(3)  # 리뷰 탭 로딩 대기
        while next_list_count > 0:
            for page in range((first_page-1)*3+2, (first_page-1)*3+5):  # 리뷰 페이지를 설정하여서 처음페이지는 프로세스의 번호가 first_page가 된다 즉 1번프로세스면 1+1부터 2부터 시작하게 시작한다.  그후에 page+4를 하여 프로세스수만큼 증가하면서 서로 다른 페이지를 돌면서 리스트에 저장하게 된다.
                try:
                    driver.find_element(By.CSS_SELECTOR, f'#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a:nth-child({page})').click()
                    sleep(1)
                    now_page_html = driver.find_element(By.CSS_SELECTOR, f'#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div').get_attribute('innerHTML')
                    soup = BeautifulSoup(now_page_html, 'html.parser')
                    target_elements = soup.find_all('a', {'aria-current': 'true', 'role': 'menuitem'})
                    base_num = 0
                    for elem in target_elements:
                        base_num = (((int)(elem.text))-1)*20
                    df_idx = 0
                    for review_number in range(1, 21):
                        review_table = driver.find_elements(By.CSS_SELECTOR, f'#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > ul > li:nth-child({review_number})')
                        for review in review_table:
                            summary = review.find_element(By.CSS_SELECTOR, 'div._2FXNMst_ak').text
                            grade = review.find_element(By.CSS_SELECTOR, 'div._2V6vMO_iLm > em').text
                            review_text = review.find_element(By.CSS_SELECTOR, 'div._3z6gI4oI6l').text
                            df.loc[base_num+df_idx] = [base_num+df_idx,summary, grade, review_text]
                            df_idx += 1
                except Exception as e:
                    print("페이지 로딩 중 오류 발생:", e)
                    break
            try:
                driver.find_element(By.CSS_SELECTOR, '#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a.fAUKm1ewwo._2Ar8-aEUTq').click()
                next_list_count -= 1
                sleep(1)
            except Exception as e:
                print("다음 페이지 목록으로 이동 중 오류 발생:", e)
                break

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        driver.quit()

    return df

def main():
    start_time = time.time()
    tasks = [(10, i) for i in range(1, 5)]

    with Pool(processes=4) as pool:
        results = pool.map(collect_reviews, tasks)
    
    final_df = pd.concat(results)
    final_df.sort_values(by=['num'], inplace=True)
    final_df.drop_duplicates(subset=['num'], keep='first', inplace=True)
    final_df.reset_index(drop=True, inplace=True)
    final_df.to_csv('brand_crawling.csv', index=False, encoding='utf-8-sig')
    

    end_time = time.time()
    print("CSV 파일 저장 완료")
    print(f"크롤링 완료 시간: {end_time - start_time}초")

if __name__ == "__main__":
    main()
    