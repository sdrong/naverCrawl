import requests
from bs4 import BeautifulSoup
import csv

# 크롤링할 URL
url = 'https://www.techpowerup.com/gpu-specs/radeon-rx-7600-xt.c4190'

# 웹 페이지의 HTML을 가져옴
response = requests.get(url)
html_content = response.text

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
    specs = "\n".join([f"{spec.find('dt').text.strip()}: {spec.find('dd').text.strip()}" for spec in section.find_all("dl", class_="clearfix")])
    if specs:
        additional_specs += f"{section_title}:\n{specs}\n\n"

# 'Retail boards based on this design' 정보 추출
retail_boards_section = soup.find("section", class_="details customboards")
retail_boards_rows = retail_boards_section.find("tbody").find_all("tr")
retail_boards_data = ""
for row in retail_boards_rows:
    cols = row.find_all("td")
    board_name = cols[0].text.strip()
    gpu_clock = cols[1].text.strip()
    boost_clock = cols[2].text.strip()
    memory_clock = cols[3].text.strip()
    other_changes = cols[4].text.strip()
    retail_boards_data += f"{board_name}: GPU Clock: {gpu_clock}, Boost Clock: {boost_clock}, Memory Clock: {memory_clock}, Other Changes: {other_changes}\n"

# CSV 파일에 저장
csv_file_path = 'gpu_specs_extended.csv'

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Product Name', 'Main Specs', 'Additional Specs', 'Derived Models'])
    writer.writerow([product_name, main_specs, additional_specs, retail_boards_data])

print(f'Data has been saved to {csv_file_path}')
