import requests
from bs4 import BeautifulSoup
import csv
import re
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 크롤링할 URL
url = 'https://www.techpowerup.com/gpu-specs/geforce-rtx-4090.c3889'

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(url)
html_content = driver.page_source

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_content, 'html.parser')

# 제품명 추출
product_name = soup.find("h1", class_="gpudb-name").text.strip()

# 메인 스펙 추출
main_specs_div = soup.find("dl", class_="gpudb-specs-large")
main_specs = "\n".join([f"{spec.find('dt').text.strip()}: {spec.find('dd').text.strip()}" for spec in main_specs_div.find_all("div", class_="gpudb-specs-large__entry")])

# 추가 스펙 추출
additional_specs_sections = soup.find_all("section", class_="details")
additional_specs = ""
for section in additional_specs_sections:
    section_title = section.find("h2").text.strip()
    specs = []
    for spec in section.find_all("dl", class_="clearfix"):
        dt_text = spec.find("dt").text.strip()
        # 'dd' 태그 안의 모든 텍스트를 추출하되, 줄바꿈과 불필요한 공백 처리
        dd_text = ' '.join(spec.find("dd").stripped_strings)
        dd_text = re.sub(r'\s+', ' ', dd_text)  # 연속된 공백을 하나의 공백으로 변환
        specs.append(f"{dt_text}: {dd_text}")
    if specs:
        additional_specs += f"{section_title}:\n" + "\n".join(specs) + "\n\n"


# 'Retail boards based on this design' 정보 추출
retail_boards_section = soup.find("section", class_="details customboards")
if retail_boards_section is not None:
    retail_boards_rows = retail_boards_section.find("tbody").find_all("tr")
    retail_boards_data = ""
    for row in retail_boards_rows:
        cols = row.find_all("td")
    # cols 리스트에 최소 5개의 요소가 있는지 확인
        if len(cols) != 5:
            print("형식이 다름")
            break
        board_name = cols[0].text.strip()
        gpu_clock = cols[1].text.strip()
        boost_clock = cols[2].text.strip()
        memory_clock = cols[3].text.strip()
        other_changes = cols[4].text.strip()
        retail_boards_data += f"기반 제품명:{board_name} -해당 제품의 바뀐 사항 GPU Clock: {gpu_clock}, Boost Clock: {boost_clock}, Memory Clock: {memory_clock}, 외의 바뀐 사항: {other_changes}\n"
else:
    retail_boards_data = "없음"
# CSV 파일에 저장
csv_file_path = 'Gpu\AMD\AMD_2020.csv'

with open(csv_file_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    ##writer.writerow(['Product Name', 'Main Specs', 'Additional Specs', 'Derived Models'])
    writer.writerow([product_name, main_specs, additional_specs, retail_boards_data])
print(product_name)
print(f'Data has been saved to {csv_file_path}')
