import requests
from bs4 import BeautifulSoup
import csv
import re
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def extract_gpu_details(url):
    try:
        # 웹 페이지의 HTML을 가져옴
    #    response = requests.get(url, timeout=10)
    #    sleep(10)  # 요청 사이에 1초 대기
    #    if response.status_code != 200:
    #        print(f"{url}")
    #        return None, None, None, None
    #    html_content = response.text
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        html_content = driver.page_source
        driver.quit()  # 웹드라이버 사용 후 종료
        
        # BeautifulSoup 객체 생성
        soup = BeautifulSoup(html_content, 'html.parser')

        product_name_tag = soup.find("h1", class_="gpudb-name")
        if not product_name_tag:
            print(f"Product name tag not found for URL: {url}")
            return None, None, None, None

        product_name = product_name_tag.text.strip()
        # 메인 스펙 추출
        main_specs_div = soup.find("dl", class_="gpudb-specs-large")
        main_specs = "\n".join([f"{spec.find('dt').text.strip()}: {spec.find('dd').text.strip()}" for spec in main_specs_div.find_all("div", class_="gpudb-specs-large__entry")])

        # 추가 스펙 추출
        additional_specs = ""
        additional_specs_sections = soup.find_all("section", class_="details")
        for section in additional_specs_sections:
            section_title = section.find("h2").text.strip()
            specs = []
            for spec in section.find_all("dl", class_="clearfix"):
                dt_text = spec.find("dt").text.strip()
                dd_text = ' '.join(spec.find("dd").stripped_strings)
                dd_text = re.sub(r'\s+', ' ', dd_text)
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
        return product_name, main_specs, additional_specs, retail_boards_data
    except Exception as e:
        print(f"An error occurred while processing URL: {url} - {e}")
        return None, None, None, None

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
<table class="processors">
				<thead>
			<tr>
				<th colspan="8" class="mfgr" id="AMD">AMD</th>
			</tr>
		</thead>
		<thead class="colheader">
	<tr>
		<th>Product Name</th>
		<th>GPU Chip</th>
		<th>Released</th>
		<th>Bus</th>
		<th>Memory</th>
		<th>GPU clock</th>
		<th>Memory clock</th>
		<th>Shaders / TMUs / ROPs</th>
	</tr>
</thead>

										<tbody><tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/playstation-5-gpu.c3480">Playstation 5 GPU</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-oberon.g936">Oberon</a>

			</td>
	<td>Nov 12th, 2020</td>
	<td>IGP</td>
	<td>16 GB, GDDR6, 256 bit</td>
	<td>2233 MHz</td>
	<td>1750 MHz</td>
	<td>2304 / 144 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-graphics-320sp-mobile.c3613">Radeon Graphics 320SP Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-renoir-m.g935">Renoir-M</a>

			</td>
	<td>Jan 6th, 2020</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>400 MHz</td>
	<td>System Shared</td>
	<td>320 / 20 / 8</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-graphics-384sp-mobile.c3511">Radeon Graphics 384SP Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-renoir-m.g935">Renoir-M</a>

			</td>
	<td>Jan 6th, 2020</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>400 MHz</td>
	<td>System Shared</td>
	<td>384 / 24 / 8</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-graphics-448sp.c4024">Radeon Graphics 448SP</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-renoir.g1058">Renoir</a>

			</td>
	<td>Jan 6th, 2020</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>400 MHz</td>
	<td>System Shared</td>
	<td>448 / 28 / 8</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-graphics-448sp-mobile.c3510">Radeon Graphics 448SP Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-renoir-m.g935">Renoir-M</a>

			</td>
	<td>Jan 6th, 2020</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>400 MHz</td>
	<td>System Shared</td>
	<td>448 / 28 / 8</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-graphics-512sp.c4023">Radeon Graphics 512SP</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-renoir.g1058">Renoir</a>

			</td>
	<td>Mar 7th, 2020</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>400 MHz</td>
	<td>System Shared</td>
	<td>512 / 32 / 8</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-graphics-512sp-mobile.c3587">Radeon Graphics 512SP Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-renoir-m.g935">Renoir-M</a>

			</td>
	<td>Mar 7th, 2020</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>400 MHz</td>
	<td>System Shared</td>
	<td>512 / 32 / 8</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-instinct-mi100.c3496">Radeon Instinct MI100</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-arcturus.g927">Arcturus</a>

			</td>
	<td>Nov 16th, 2020</td>
	<td>PCIe 4.0 x16</td>
	<td>32 GB, HBM2, 4096 bit</td>
	<td>1000 MHz</td>
	<td>1200 MHz</td>
	<td>7680 / 480 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-5300.c3665">Radeon Pro 5300</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-14.g919">Navi 14</a>

			</td>
	<td>Aug 4th, 2020</td>
	<td>PCIe 4.0 x8</td>
	<td>4 GB, GDDR6, 128 bit</td>
	<td>1000 MHz</td>
	<td>1750 MHz</td>
	<td>1280 / 80 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-5500-xt.c3664">Radeon Pro 5500 XT</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-14.g919">Navi 14</a>

			</td>
	<td>Aug 4th, 2020</td>
	<td>PCIe 4.0 x8</td>
	<td>8 GB, GDDR6, 128 bit</td>
	<td>1187 MHz</td>
	<td>1750 MHz</td>
	<td>1536 / 96 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-5600m.c3612">Radeon Pro 5600M</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-12.g922">Navi 12</a>

			</td>
	<td>Jun 15th, 2020</td>
	<td>PCIe 4.0 x16</td>
	<td>8 GB, HBM2, 2048 bit</td>
	<td>822 MHz</td>
	<td>770 MHz</td>
	<td>2560 / 160 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-5700.c3663">Radeon Pro 5700</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-10.g861">Navi 10</a>

			</td>
	<td>Aug 4th, 2020</td>
	<td>PCIe 4.0 x16</td>
	<td>8 GB, GDDR6, 256 bit</td>
	<td>1243 MHz</td>
	<td>1500 MHz</td>
	<td>2304 / 144 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-5700-xt.c3662">Radeon Pro 5700 XT</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-10.g861">Navi 10</a>

			</td>
	<td>Aug 4th, 2020</td>
	<td>PCIe 4.0 x16</td>
	<td>16 GB, GDDR6, 256 bit</td>
	<td>1243 MHz</td>
	<td>1500 MHz</td>
	<td>2560 / 160 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-v520.c3755">Radeon Pro V520</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-12.g922">Navi 12</a>

			</td>
	<td>Dec 1st, 2020</td>
	<td>PCIe 4.0 x16</td>
	<td>8 GB, HBM2, 2048 bit</td>
	<td>1000 MHz</td>
	<td>1000 MHz</td>
	<td>2304 / 144 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-v540.c4133">Radeon Pro V540</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-12.g922">Navi 12</a>

			</td>
	<td>Never Released</td>
	<td>PCIe 4.0 x16</td>
	<td>8 GB, HBM2, 2048 bit</td>
	<td>1000 MHz</td>
	<td>1000 MHz</td>
	<td>2304 / 144 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-vii.c3575">Radeon Pro VII</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-vega-20.g848">Vega 20</a>

			</td>
	<td>May 13th, 2020</td>
	<td>PCIe 4.0 x16</td>
	<td>16 GB, HBM2, 4096 bit</td>
	<td>1400 MHz</td>
	<td>1000 MHz</td>
	<td>3840 / 240 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-w5500.c3479">Radeon Pro W5500</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-14.g919">Navi 14</a>

			</td>
	<td>Feb 10th, 2020</td>
	<td>PCIe 4.0 x8</td>
	<td>8 GB, GDDR6, 128 bit</td>
	<td>1744 MHz</td>
	<td>1750 MHz</td>
	<td>1408 / 88 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-w5500m.c3478">Radeon Pro W5500M</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-14.g919">Navi 14</a>

			</td>
	<td>Feb 10th, 2020</td>
	<td>PCIe 4.0 x8</td>
	<td>4 GB, GDDR6, 128 bit</td>
	<td>1448 MHz</td>
	<td>1750 MHz</td>
	<td>1408 / 88 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-5300-oem.c3584">Radeon RX 5300 OEM</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-14.g919">Navi 14</a>

			</td>
	<td>May 28th, 2020</td>
	<td>PCIe 4.0 x8</td>
	<td>3 GB, GDDR6, 96 bit</td>
	<td>1327 MHz</td>
	<td>1750 MHz</td>
	<td>1408 / 88 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-5600-oem.c3475">Radeon RX 5600 OEM</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-10.g861">Navi 10</a>

			</td>
	<td>Jan 21st, 2020</td>
	<td>PCIe 4.0 x16</td>
	<td>6 GB, GDDR6, 192 bit</td>
	<td>1130 MHz</td>
	<td>1500 MHz</td>
	<td>2048 / 128 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-5600-xt.c3474">Radeon RX 5600 XT</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-10.g861">Navi 10</a>

			</td>
	<td>Jan 21st, 2020</td>
	<td>PCIe 4.0 x16</td>
	<td>6 GB, GDDR6, 192 bit</td>
	<td>1130 MHz</td>
	<td>1500 MHz</td>
	<td>2304 / 144 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-5600m.c3492">Radeon RX 5600M</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-10.g861">Navi 10</a>

			</td>
	<td>Jul 7th, 2020</td>
	<td>PCIe 4.0 x16</td>
	<td>6 GB, GDDR6, 192 bit</td>
	<td>1035 MHz</td>
	<td>1500 MHz</td>
	<td>2304 / 144 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-5700m.c3476">Radeon RX 5700M</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-10.g861">Navi 10</a>

			</td>
	<td>Mar 1st, 2020</td>
	<td>PCIe 4.0 x16</td>
	<td>8 GB, GDDR6, 256 bit</td>
	<td>1465 MHz</td>
	<td>1500 MHz</td>
	<td>2304 / 144 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-590-gme.c3505">Radeon RX 590 GME</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-20.g807">Polaris 20</a>

			</td>
	<td>Mar 9th, 2020</td>
	<td>PCIe 3.0 x16</td>
	<td>8 GB, GDDR5, 256 bit</td>
	<td>1257 MHz</td>
	<td>2000 MHz</td>
	<td>2304 / 144 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-640-oem.c4110">Radeon RX 640 OEM</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-23.g920">Polaris 23</a>

			</td>
	<td>Apr 9th, 2020</td>
	<td>PCIe 3.0 x8</td>
	<td>4 GB, GDDR5, 128 bit</td>
	<td>1295 MHz</td>
	<td>1500 MHz</td>
	<td>640 / 40 / 16</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-6800.c3713">Radeon RX 6800</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-21.g923">Navi 21</a>

			</td>
	<td>Oct 28th, 2020</td>
	<td>PCIe 4.0 x16</td>
	<td>16 GB, GDDR6, 256 bit</td>
	<td>1700 MHz</td>
	<td>2000 MHz</td>
	<td>3840 / 240 / 96</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-6800-xt.c3694">Radeon RX 6800 XT</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-21.g923">Navi 21</a>

			</td>
	<td>Oct 28th, 2020</td>
	<td>PCIe 4.0 x16</td>
	<td>16 GB, GDDR6, 256 bit</td>
	<td>1825 MHz</td>
	<td>2000 MHz</td>
	<td>4608 / 288 / 128</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-6900-xt.c3481">Radeon RX 6900 XT</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-21.g923">Navi 21</a>

			</td>
	<td>Oct 28th, 2020</td>
	<td>PCIe 4.0 x16</td>
	<td>16 GB, GDDR6, 256 bit</td>
	<td>1825 MHz</td>
	<td>2000 MHz</td>
	<td>5120 / 320 / 128</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-6900-xtx.c3800">Radeon RX 6900 XTX</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-navi-21.g923">Navi 21</a>

			</td>
	<td>Never Released</td>
	<td>PCIe 4.0 x16</td>
	<td>16 GB, GDDR6, 256 bit</td>
	<td>2075 MHz</td>
	<td>2250 MHz</td>
	<td>5120 / 320 / 128</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-vega-3-mobile.c3592">Radeon Vega 3 Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-picasso-m.g1055">Picasso-M</a>

			</td>
	<td>Jan 6th, 2020</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>192 / 12 / 4</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/xbox-series-s-gpu.c3683">Xbox Series S GPU</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-lockhart.g970">Lockhart</a>

			</td>
	<td>Nov 10th, 2020</td>
	<td>IGP</td>
	<td>8 GB, GDDR6, 128 bit</td>
	<td>1565 MHz</td>
	<td>1750 MHz</td>
	<td>1280 / 80 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/xbox-series-x-gpu.c3482">Xbox Series X GPU</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-scarlett.g924">Scarlett</a>

			</td>
	<td>Nov 10th, 2020</td>
	<td>IGP</td>
	<td>10 GB, GDDR6, 320 bit</td>
	<td>1825 MHz</td>
	<td>1750 MHz</td>
	<td>3328 / 208 / 64</td>
</tr>
		
			</tbody></table>
"""

csv_file_path = 'Gpu\AMD\AMD_2020.csv'
product_urls = extract_gpu_urls(html_content)
with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Product Name', 'Main Specs', 'Additional Specs', 'Derived Models'])
counter = 0
for name, url in product_urls.items():
    result = extract_gpu_details(url)
    if None in result:
        if result[0] is not None:  # 제품명이 None이 아니라면 출력
            print(f"Product Name: {result[0]}")
        continue  # 결과 중 하나라도 None이면 이 URL에 대한 처리를 건너뛰기
    product_name, main_specs, additional_specs, retail_boards_data = result
    with open(csv_file_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([product_name, main_specs, additional_specs, retail_boards_data])
    counter += 1
    print(product_name)
    print(counter)
    if counter % 10 == 0:
        print("Waiting for 30 seconds...")
        sleep(40)  # 10개 처리 후 5초 대기
print(f'Data has been saved to {csv_file_path}')