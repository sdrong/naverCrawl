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


def collect_reviews(args):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from time import sleep
    import pandas as pd

    next_list_count, first_page = args
    options = Options()
    options.headless = True  # 헤드리스 모드 활성화
    # 사용자 에이전트 설정
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    df = pd.DataFrame(columns=['num','summary', 'grade', 'review'])

    df_idx = 0  # 데이터프레임 인덱스 초기화

    try:
        url = "https://shopping.naver.com/window-products/brandfashion/9949176287?NaPm=ct%3Dlty029gf%7Cci%3Dshoppingwindow%7Ctr%3Dswhl%7Chk%3D02d395b67c73ad3d7fe701d6d0d5ef31f0938469%7Ctrx%3D"
        driver.get(url)
        sleep(2)  # 페이지 로딩 대기
        # 첫 번째 코드에서 제공된 선택자를 적용하여 리뷰 탭으로 이동
        driver.find_element(By.CSS_SELECTOR, '#_productTabContainer > div > ul > li:nth-child(2) > a').click()
        sleep(10)  # 리뷰 탭 로딩 대기
        print(first_page)
        driver.find_element(By.CSS_SELECTOR, f'#REVIEW > div > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a:nth-child({first_page+1})').click()
        print(first_page)
        sleep(5)  # 페이지 로딩 대기
        while next_list_count > 0:
            for page in range(1, 100):
                try:
                    driver.find_element(By.CSS_SELECTOR, '#_productTabContainer > div > ul > li:nth-child(2) > a').click()
                    sleep(3)
                    now_page_html = driver.find_element(By.CSS_SELECTOR, f'#REVIEW > div > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div').get_attribute('innerHTML')
                    soup = BeautifulSoup(now_page_html, 'html.parser')
                    target_elements  = soup.find('a', {'aria-current': 'true', 'role': 'menuitem'})
                    base_num = 0
                    num = 1
                    for elem in target_elements:
                        base_num = (((int)(elem.text))-1)*20
                        num+=1
                    print(num)
                    sleep(3)
                    df_idx = 0
                    for review_number in range(1, 21):
                        review_table = driver.find_elements(By.CSS_SELECTOR, f'#REVIEW > div > div > div._2LvIMaBiIO > div._2g7PKvqCKe > ul > li:nth-child({review_number}')
                        sleep(1)
                        for review in review_table:
                            summary = review.find_element(By.CSS_SELECTOR, f'div._2FXNMst_ak').text
                            grade = review.find_element(By.CSS_SELECTOR, f'div._2V6vMO_iLm > em').text
                            review_text = review.find_element(By.CSS_SELECTOR, f'div._3z6gI4oI6l').text
                            df.loc[base_num+df_idx] = [base_num+df_idx,summary, grade, review_text]
                            df_idx += 1
                    driver.find_element(By.CSS_SELECTOR, f'#REVIEW > div > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a:nth-child({num+4})').click()
                    
                except Exception as e:
                    print("페이지 로딩 중 오류 발생:", e)
                    break
            try:
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
    final_df.to_csv('shopping_crawling.csv', index=False, encoding='utf-8-sig')


    end_time = time.time()
    print("CSV 파일 저장 완료")
    print(f"크롤링 완료 시간: {end_time - start_time}초")
    print(final_df)

if __name__ == "__main__":
    main()


"""
<div class="_1HJarNZHiI _2UJrM31-Ry" role="menubar" style="padding-top: 50px; padding-bottom: 50px;">
<a href="#" class="fAUKm1ewwo _2PB8-gs2tG _nlog_click _nlog_impression_element" aria-hidden="false" role="button" data-shp-page-key="100393376" data-shp-sti="" data-shp-nsc="shoppingw.brand" data-shp-abt_exps="[]" data-shp-inventory="revlist" data-shp-area="revlist.pgprev" data-shp-area-type="action" data-shp-area-id="pgprev">이전</a>
<a href="#" class="UWN4IvaQza N=a:PROUDCT_REVIEW.npaypg _nlog_click _nlog_impression_element" aria-current="false" role="menuitem" data-shp-page-key="100393376" data-shp-sti="" data-shp-nsc="shoppingw.brand" data-shp-abt_exps="[]" data-shp-inventory="revlist" data-shp-area="revlist.pgn" data-shp-area-type="action" data-shp-area-id="pgn">2</a>
<a href="#" class="UWN4IvaQza N=a:PROUDCT_REVIEW.npaypg _nlog_click _nlog_impression_element" aria-current="false" role="menuitem" data-shp-page-key="100393376" data-shp-sti="" data-shp-nsc="shoppingw.brand" data-shp-abt_exps="[]" data-shp-inventory="revlist" data-shp-area="revlist.pgn" data-shp-area-type="action" data-shp-area-id="pgn">3</a><a href="#" class="UWN4IvaQza N=a:PROUDCT_REVIEW.npaypg _nlog_click _nlog_impression_element" aria-current="false" role="menuitem" data-shp-page-key="100393376" data-shp-sti="" data-shp-nsc="shoppingw.brand" data-shp-abt_exps="[]" data-shp-inventory="revlist" data-shp-area="revlist.pgn" data-shp-area-type="action" data-shp-area-id="pgn">4</a><a href="#" class="UWN4IvaQza N=a:PROUDCT_REVIEW.npaypg _nlog_click _nlog_impression_element" aria-current="false" role="menuitem" data-shp-page-key="100393376" data-shp-sti="" data-shp-nsc="shoppingw.brand" data-shp-abt_exps="[]" data-shp-inventory="revlist" data-shp-area="revlist.pgn" data-shp-area-type="action" data-shp-area-id="pgn">5</a><a href="#" class="UWN4IvaQza N=a:PROUDCT_REVIEW.npaypg _nlog_click _nlog_impression_element" aria-current="true" role="menuitem" data-shp-page-key="100393376" data-shp-sti="" data-shp-nsc="shoppingw.brand" data-shp-abt_exps="[]" data-shp-inventory="revlist" data-shp-area="revlist.pgn" data-shp-area-type="action" data-shp-area-id="pgn">6</a><a href="#" class="UWN4IvaQza N=a:PROUDCT_REVIEW.npaypg _nlog_click _nlog_impression_element" aria-current="false" role="menuitem" data-shp-page-key="100393376" data-shp-sti="" data-shp-nsc="shoppingw.brand" data-shp-abt_exps="[]" data-shp-inventory="revlist" data-shp-area="revlist.pgn" data-shp-area-type="action" data-shp-area-id="pgn">7</a><a href="#" class="UWN4IvaQza N=a:PROUDCT_REVIEW.npaypg _nlog_click _nlog_impression_element" aria-current="false" role="menuitem" data-shp-page-key="100393376" data-shp-sti="" data-shp-nsc="shoppingw.brand" data-shp-abt_exps="[]" data-shp-inventory="revlist" data-shp-area="revlist.pgn" data-shp-area-type="action" data-shp-area-id="pgn">8</a><a href="#" class="UWN4IvaQza N=a:PROUDCT_REVIEW.npaypg _nlog_click _nlog_impression_element" aria-current="false" role="menuitem" data-shp-page-key="100393376" data-shp-sti="" data-shp-nsc="shoppingw.brand" data-shp-abt_exps="[]" data-shp-inventory="revlist" data-shp-area="revlist.pgn" data-shp-area-type="action" data-shp-area-id="pgn">9</a><a href="#" class="UWN4IvaQza N=a:PROUDCT_REVIEW.npaypg _nlog_click _nlog_impression_element" aria-current="false" role="menuitem" data-shp-page-key="100393376" data-shp-sti="" data-shp-nsc="shoppingw.brand" data-shp-abt_exps="[]" data-shp-inventory="revlist" data-shp-area="revlist.pgn" data-shp-area-type="action" data-shp-area-id="pgn">10</a><a href="#" class="UWN4IvaQza N=a:PROUDCT_REVIEW.npaypg _nlog_click _nlog_impression_element" aria-current="false" role="menuitem" data-shp-page-key="100393376" data-shp-sti="" data-shp-nsc="shoppingw.brand" data-shp-abt_exps="[]" data-shp-inventory="revlist" data-shp-area="revlist.pgn" data-shp-area-type="action" data-shp-area-id="pgn">11</a><a href="#" class="fAUKm1ewwo _2Ar8-aEUTq _nlog_click _nlog_impression_element" aria-hidden="false" role="button" data-shp-page-key="100393376" data-shp-sti="" data-shp-nsc="shoppingw.brand" data-shp-abt_exps="[]" data-shp-inventory="revlist" data-shp-area="revlist.pgnext" data-shp-area-type="action" data-shp-area-id="pgnext">다음</a></div>
"""
#REVIEW > div > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a:nth-child(5)

#REVIEW > div > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a:nth-child(6)
