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
import logging
import os
import tempfile  # 임시 파일을 위한 모듈

logging.basicConfig(level=logging.INFO)


def save_images_as_pdf(image_urls, pdf_filename):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    page_width, page_height = letter
    x_margin, y_margin = 50, 50
    x, y = x_margin, page_height - y_margin

    for url in image_urls:
        try:
            # 이미지 로드
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            if img.mode == 'P':
                img = img.convert('RGB')

            # 이미지 크기 조정 로직은 이전과 동일
            img_w, img_h = img.size
            aspect_ratio = img_w / img_h
            max_img_width = page_width - (2 * x_margin)
            max_img_height = page_height - (2 * y_margin)
            if aspect_ratio > 1:
                img_width = min(img_w, max_img_width)
                img_height = img_width / aspect_ratio
            else:
                img_height = min(img_h, max_img_height)
                img_width = img_height * aspect_ratio
            
            # 현재 페이지에 이미지가 맞는지 확인
            if y - img_height < y_margin:
                c.showPage()
                x, y = x_margin, page_height - y_margin
            
            # 임시 이미지 파일 생성 및 삭제
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmpfile:
                img_path = tmpfile.name
                img = img.resize((int(img_width), int(img_height)))
                img.save(img_path)
                c.drawImage(img_path, x, y - img_height, width=img_width, height=img_height)
                y -= img_height + y_margin
        except Exception as e:
            print(f"Error saving image {url}: {e}")
    
    c.save()


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
        url = "https://brand.naver.com/sidiz/products/7567795565?n_media=11068&n_query=%EC%8B%9C%EB%94%94%EC%A6%88&n_rank=4&n_ad_group=grp-a001-02-000000038783838&n_ad=nad-a001-02-000000274248140&n_campaign_type=2&n_mall_id=sidiz00&n_mall_pid=7567795565&n_ad_group_type=2&n_match=3&NaPm=ct%3Dlucouaa8%7Cci%3D0yG0001oJKnAlj0nV1iv%7Ctr%3Dpla%7Chk%3Df434f29bd98e182c3cceb71c24aa40b55d19945b"
        driver.get(url)
        sleep(2)  # 페이지 로딩 대기
        if first_page == 1:
            product_html = driver.find_element(By.CSS_SELECTOR, f'#SE-a88fac98-5767-11ee-808b-75e2306683b8 > div > div > div').get_attribute('innerHTML')
            soup = BeautifulSoup(product_html, 'html.parser')

            # data-src 속성을 가진 모든 img 태그 찾기
            images = soup.find_all('img', {'data-src': True})

            # 각 img 태그의 data-src 속성값 추출
            image_urls = [img['data-src'] for img in images]
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
                            print(f"리뷰 추가됨: {base_num+df_idx}, {summary}, {grade}, {review_text}")  # 리뷰가 추가될 때마다 출력
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
        if first_page == 1:
            for url in image_urls:
                print(url)
            save_images_as_pdf(image_urls, "product_images.pdf")

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
    print(final_df)

if __name__ == "__main__":
    main()