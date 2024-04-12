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
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        html_content = driver.page_source
        driver.quit() 
        
        soup = BeautifulSoup(html_content, 'html.parser')

        product_name_tag = soup.find("h1", class_="gpudb-name")
        if not product_name_tag:
            print(f"Product name error {url}")
            return None, None, None, None

        product_name = product_name_tag.text.strip()
        # 메인 스펙 
        main_specs_div = soup.find("dl", class_="gpudb-specs-large")
        main_specs = "\n".join([f"{spec.find('dt').text.strip()}: {spec.find('dd').text.strip()}" for spec in main_specs_div.find_all("div", class_="gpudb-specs-large__entry")])

        # 추가 스펙
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

        retail_boards_section = soup.find("section", class_="details customboards")
        if retail_boards_section is not None:
            retail_boards_rows = retail_boards_section.find("tbody").find_all("tr")
            retail_boards_data = ""
            for row in retail_boards_rows:
                cols = row.find_all("td")
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
        print(f"{url}")
        return None, None, None, None

def extract_gpu_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    table = soup.find('table', class_='processors')

    product_urls = {}

    for tr in table.find_all('tr'):
        td = tr.find('td', class_='vendor-Intel')
        if td:
            a_tag = td.find('a') 
            if a_tag:
                product_name = a_tag.text.strip()  
                product_url = 'https://www.techpowerup.com' + a_tag['href'] 
                product_urls[product_name] = product_url 

    return product_urls


html_content = """
<table class="processors">
				<thead>
			<tr>
				<th colspan="8" class="mfgr" id="Intel">Intel</th>
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
	<td class="vendor-Intel">
		<a href="/gpu-specs/iris-plus-graphics-645-mobile.c3486">Iris Plus Graphics 645 Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-coffee-lake-gt3e.g868">Coffee Lake GT3e</a>

			</td>
	<td>Oct 7th, 2019</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>384 / 48 / 6</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/iris-plus-graphics-g4-48eu-mobile.c3647">Iris Plus Graphics G4 48EU Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-ice-lake-gt1.g896">Ice Lake GT1</a>

			</td>
	<td>May 29th, 2019</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>384 / 24 / 8</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/uhd-graphics-24eu-mobile.c3604">UHD Graphics 24EU Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-amber-lake-gt2.g879">Amber Lake GT2</a>

			</td>
	<td>Aug 21st, 2019</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>192 / 24 / 3</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/uhd-graphics-24eu-mobile.c3644">UHD Graphics 24EU Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-comet-lake-gt1.g950">Comet Lake GT1</a>

			</td>
	<td>Aug 21st, 2019</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>192 / 24 / 3</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/uhd-graphics-24eu-mobile.c3484">UHD Graphics 24EU Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-comet-lake-gt2.g925">Comet Lake GT2</a>

			</td>
	<td>Aug 21st, 2019</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>192 / 24 / 3</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/uhd-graphics-g1-32eu-mobile.c3447">UHD Graphics G1 32EU Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-ice-lake-gt1.g896">Ice Lake GT1</a>

			</td>
	<td>May 29th, 2019</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>256 / 16 / 8</td>
</tr>
		
			</tbody></table>
"""

csv_file_path = 'Gpu\\INTER\\INTER_2019 .csv'

product_urls = extract_gpu_urls(html_content)
with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Product Name', 'Main Specs', 'Additional Specs', 'Derived Models'])
counter = 0
for name, url in product_urls.items():
    result = extract_gpu_details(url)
    if None in result:
        if result[0] is not None:  
            print(f"Product Name: {result[0]}")
        continue  
    product_name, main_specs, additional_specs, retail_boards_data = result
    with open(csv_file_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([product_name, main_specs, additional_specs, retail_boards_data])
    counter += 1
    print(product_name)
    print(counter)
    if counter % 10 == 0:
        print("Waiting")
        sleep(40)  
print(f'Data has been saved to {csv_file_path}')