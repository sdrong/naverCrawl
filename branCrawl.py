from bs4 import BeautifulSoup

def extract_gpu_urls(html_content):
    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(html_content, 'html.parser')

    # 'table class="processors"' 태그를 찾고, 그 안의 모든 'a' 태그를 찾기
    table = soup.find('table', class_='processors')

    # 제품명과 해당 URL을 저장할 딕셔너리
    product_urls = {}

    # 테이블 내의 모든 행(tr)을 순회
    for tr in table.find_all('tr'):
        # 각 행 내의 첫 번째 'td' 태그를 찾기 (제품명이 있는 칸)
        td = tr.find('td', class_='vendor-AMD')
        if td:
            a_tag = td.find('a')  # 'a' 태그 찾기
            if a_tag:
                product_name = a_tag.text.strip()  # 제품명 추출
                product_url = 'https://www.techpowerup.com' + a_tag['href']  # 제품 페이지 URL 추출
                product_urls[product_name] = product_url  # 딕셔너리에 저장

    return product_urls

# 사용 예시
html_content = """
여기에 <table class="processors"> 부터 시작하는 HTML 내용 전체를 붙여넣으세요.
"""
product_urls = extract_gpu_urls(html_content)
for name, url in product_urls.items():
    print(f"{name}: {url}")