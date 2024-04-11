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
		<a href="/gpu-specs/radeon-550x-mobile.c3207">Radeon 550X Mobile</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-23.g920">Polaris 23</a>

			</td>
	<td>Apr 11th, 2018</td>
	<td>PCIe 3.0 x8</td>
	<td>2 GB, GDDR5, 64 bit</td>
	<td>1082 MHz</td>
	<td>1000 MHz</td>
	<td>640 / 40 / 16</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-instinct-mi50.c3335">Radeon Instinct MI50</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-vega-20.g848">Vega 20</a>

			</td>
	<td>Nov 18th, 2018</td>
	<td>PCIe 4.0 x16</td>
	<td>16 GB, HBM2, 4096 bit</td>
	<td>1200 MHz</td>
	<td>1000 MHz</td>
	<td>3840 / 240 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-instinct-mi60.c3233">Radeon Instinct MI60</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-vega-20.g848">Vega 20</a>

			</td>
	<td>Nov 18th, 2018</td>
	<td>PCIe 4.0 x16</td>
	<td>32 GB, HBM2, 4096 bit</td>
	<td>1200 MHz</td>
	<td>1000 MHz</td>
	<td>4096 / 256 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-555x.c3283">Radeon Pro 555X</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-21.g812">Polaris 21</a>

			</td>
	<td>Jul 16th, 2018</td>
	<td>PCIe 3.0 x8</td>
	<td>4 GB, GDDR5, 128 bit</td>
	<td>907 MHz</td>
	<td>1470 MHz</td>
	<td>768 / 48 / 16</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-560x.c3282">Radeon Pro 560X</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-21.g812">Polaris 21</a>

			</td>
	<td>Jul 16th, 2018</td>
	<td>PCIe 3.0 x8</td>
	<td>4 GB, GDDR5, 128 bit</td>
	<td>1004 MHz</td>
	<td>1470 MHz</td>
	<td>1024 / 64 / 16</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-v340-16-gb.c3267">Radeon Pro V340 16 GB</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-vega-10.g800">Vega 10</a>

			</td>
	<td>Aug 26th, 2018</td>
	<td>PCIe 3.0 x16</td>
	<td>16 GB, HBM2, 2048 bit</td>
	<td>852 MHz</td>
	<td>945 MHz</td>
	<td>3584 / 224 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-v340-8-gb.c3977">Radeon Pro V340 8 GB</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-vega-10.g800">Vega 10</a>

			</td>
	<td>Aug 26th, 2018</td>
	<td>PCIe 3.0 x16</td>
	<td>8 GB, HBM2, 2048 bit</td>
	<td>852 MHz</td>
	<td>945 MHz</td>
	<td>3584 / 224 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-v420.c3955">Radeon Pro V420</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-vega-20.g848">Vega 20</a>

			</td>
	<td>Never Released</td>
	<td>PCIe 4.0 x16</td>
	<td>32 GB, HBM2, 4096 bit</td>
	<td>800 MHz</td>
	<td>800 MHz</td>
	<td>4096 / 256 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-vega-16.c3331">Radeon Pro Vega 16</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-vega-12.g859">Vega 12</a>

			</td>
	<td>Nov 14th, 2018</td>
	<td>PCIe 3.0 x16</td>
	<td>4 GB, HBM2, 1024 bit</td>
	<td>815 MHz</td>
	<td>1200 MHz</td>
	<td>1024 / 64 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-vega-20.c3263">Radeon Pro Vega 20</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-vega-12.g859">Vega 12</a>

			</td>
	<td>Nov 14th, 2018</td>
	<td>PCIe 3.0 x16</td>
	<td>4 GB, HBM2, 1024 bit</td>
	<td>815 MHz</td>
	<td>740 MHz</td>
	<td>1280 / 80 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-wx-8200.c3303">Radeon Pro WX 8200</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-vega-10.g800">Vega 10</a>

			</td>
	<td>Aug 13th, 2018</td>
	<td>PCIe 3.0 x16</td>
	<td>8 GB, HBM2, 2048 bit</td>
	<td>1200 MHz</td>
	<td>1000 MHz</td>
	<td>3584 / 224 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-pro-wx-vega-m-gl.c3352">Radeon Pro WX Vega M GL</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-22.g821">Polaris 22</a>

			</td>
	<td>Apr 24th, 2018</td>
	<td>IGP</td>
	<td>4 GB, HBM2, 1024 bit</td>
	<td>931 MHz</td>
	<td>700 MHz</td>
	<td>1280 / 80 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-540x-mobile.c3204">Radeon RX 540X Mobile</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-23.g920">Polaris 23</a>

			</td>
	<td>Apr 11th, 2018</td>
	<td>PCIe 3.0 x8</td>
	<td>2 GB, GDDR5, 128 bit</td>
	<td>1124 MHz</td>
	<td>1500 MHz</td>
	<td>512 / 32 / 16</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-550x-640sp.c3203">Radeon RX 550X 640SP</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-baffin.g796">Baffin</a>

			</td>
	<td>Apr 11th, 2018</td>
	<td>PCIe 3.0 x8</td>
	<td>2 GB, GDDR5, 128 bit</td>
	<td>1019 MHz</td>
	<td>1500 MHz</td>
	<td>640 / 40 / 16</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-550x-mobile.c3205">Radeon RX 550X Mobile</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-23.g920">Polaris 23</a>

			</td>
	<td>Apr 11th, 2018</td>
	<td>PCIe 3.0 x8</td>
	<td>2 GB, GDDR5, 64 bit</td>
	<td>1100 MHz</td>
	<td>1500 MHz</td>
	<td>640 / 40 / 16</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-560dx.c3198">Radeon RX 560DX</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-21.g812">Polaris 21</a>

			</td>
	<td>Apr 11th, 2018</td>
	<td>PCIe 3.0 x8</td>
	<td>4 GB, GDDR5, 128 bit</td>
	<td>1090 MHz</td>
	<td>1500 MHz</td>
	<td>896 / 56 / 16</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-560x.c3193">Radeon RX 560X</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-21.g812">Polaris 21</a>

			</td>
	<td>Apr 11th, 2018</td>
	<td>PCIe 3.0 x8</td>
	<td>4 GB, GDDR5, 128 bit</td>
	<td>1175 MHz</td>
	<td>1750 MHz</td>
	<td>1024 / 64 / 16</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-560x-mobile.c3197">Radeon RX 560X Mobile</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-21.g812">Polaris 21</a>

			</td>
	<td>Apr 11th, 2018</td>
	<td>MXM-B (3.0)</td>
	<td>2 GB, GDDR5, 128 bit</td>
	<td>1175 MHz</td>
	<td>1500 MHz</td>
	<td>1024 / 64 / 16</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-560x-mobile.c3632">Radeon RX 560X Mobile</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-21.g812">Polaris 21</a>

			</td>
	<td>Apr 11th, 2018</td>
	<td>MXM-B (3.0)</td>
	<td>4 GB, GDDR5, 128 bit</td>
	<td>1275 MHz</td>
	<td>1750 MHz</td>
	<td>1024 / 64 / 16</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-560x-mobile.c3631">Radeon RX 560X Mobile</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-21.g812">Polaris 21</a>

			</td>
	<td>Apr 11th, 2018</td>
	<td>MXM-B (3.0)</td>
	<td>4 GB, GDDR5, 128 bit</td>
	<td>1275 MHz</td>
	<td>1450 MHz</td>
	<td>1024 / 64 / 16</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-570x.c3192">Radeon RX 570X</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-20.g807">Polaris 20</a>

			</td>
	<td>Apr 11th, 2018</td>
	<td>PCIe 3.0 x16</td>
	<td>8 GB, GDDR5, 256 bit</td>
	<td>1168 MHz</td>
	<td>1750 MHz</td>
	<td>2048 / 128 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-580-2048sp.c3321">Radeon RX 580 2048SP</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-20.g807">Polaris 20</a>

			</td>
	<td>Oct 15th, 2018</td>
	<td>PCIe 3.0 x16</td>
	<td>4 GB, GDDR5, 256 bit</td>
	<td>1168 MHz</td>
	<td>1750 MHz</td>
	<td>2048 / 128 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-580g.c3323">Radeon RX 580G</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-20.g807">Polaris 20</a>

			</td>
	<td>Oct 15th, 2018</td>
	<td>PCIe 3.0 x16</td>
	<td>8 GB, GDDR5, 256 bit</td>
	<td>1257 MHz</td>
	<td>2000 MHz</td>
	<td>2304 / 144 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-580x.c3190">Radeon RX 580X</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-20.g807">Polaris 20</a>

			</td>
	<td>Apr 11th, 2018</td>
	<td>PCIe 3.0 x16</td>
	<td>8 GB, GDDR5, 256 bit</td>
	<td>1257 MHz</td>
	<td>2000 MHz</td>
	<td>2304 / 144 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-580x-mobile.c3235">Radeon RX 580X Mobile</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-20.g807">Polaris 20</a>

			</td>
	<td>Apr 11th, 2018</td>
	<td>MXM-B (3.0)</td>
	<td>8 GB, GDDR5, 256 bit</td>
	<td>1266 MHz</td>
	<td>2000 MHz</td>
	<td>2304 / 144 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-590.c3322">Radeon RX 590</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-30.g877">Polaris 30</a>

			</td>
	<td>Nov 15th, 2018</td>
	<td>PCIe 3.0 x16</td>
	<td>8 GB, GDDR5, 256 bit</td>
	<td>1469 MHz</td>
	<td>2000 MHz</td>
	<td>2304 / 144 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-vega-11.c3300">Radeon RX Vega 11</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-raven.g816">Raven</a>

			</td>
	<td>May 10th, 2018</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>704 / 44 / 8</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-vega-11.c3054">Radeon RX Vega 11</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-raven.g816">Raven</a>

			</td>
	<td>Feb 12th, 2018</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>704 / 44 / 8</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-vega-11-embedded.c3222">Radeon RX Vega 11 Embedded</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-raven.g816">Raven</a>

			</td>
	<td>Apr 19th, 2018</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>704 / 44 / 8</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-vega-56-mobile.c3333">Radeon RX Vega 56 Mobile</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-vega-10.g800">Vega 10</a>

			</td>
	<td>Jun 1st, 2018</td>
	<td>PCIe 3.0 x16</td>
	<td>8 GB, HBM2, 2048 bit</td>
	<td>1138 MHz</td>
	<td>800 MHz</td>
	<td>3584 / 224 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-vega-m-gh.c3056">Radeon RX Vega M GH</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-22.g821">Polaris 22</a>

			</td>
	<td>Feb 1st, 2018</td>
	<td>IGP</td>
	<td>4 GB, HBM2, 1024 bit</td>
	<td>1063 MHz</td>
	<td>800 MHz</td>
	<td>1536 / 96 / 64</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-rx-vega-m-gl.c3061">Radeon RX Vega M GL</a>

			</td>
	<td>
		<a href="/gpu-specs/amd-polaris-22.g821">Polaris 22</a>

			</td>
	<td>Feb 1st, 2018</td>
	<td>IGP</td>
	<td>4 GB, HBM2, 1024 bit</td>
	<td>931 MHz</td>
	<td>700 MHz</td>
	<td>1280 / 80 / 32</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-vega-11-embedded.c3213">Radeon Vega 11 Embedded</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-raven.g816">Raven</a>

			</td>
	<td>Feb 13th, 2018</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>704 / 44 / 8</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-vega-3-embedded.c3656">Radeon Vega 3 Embedded</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-raven.g816">Raven</a>

			</td>
	<td>Jul 16th, 2018</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>192 / 12 / 4</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-vega-3-embedded.c3290">Radeon Vega 3 Embedded</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-raven.g816">Raven</a>

			</td>
	<td>Sep 6th, 2018</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>192 / 12 / 4</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-vega-3-embedded.c3214">Radeon Vega 3 Embedded</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-raven.g816">Raven</a>

			</td>
	<td>Feb 13th, 2018</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>192 / 12 / 4</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-vega-3-mobile.c3078">Radeon Vega 3 Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-raven-m.g1056">Raven-M</a>

			</td>
	<td>Jan 8th, 2018</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>192 / 12 / 4</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-vega-6-embedded.c3291">Radeon Vega 6 Embedded</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-raven.g816">Raven</a>

			</td>
	<td>May 10th, 2018</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>384 / 24 / 8</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-vega-6-mobile.c3079">Radeon Vega 6 Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-raven-m.g1056">Raven-M</a>

			</td>
	<td>Jan 8th, 2018</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>384 / 24 / 8</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-vega-8.c3042">Radeon Vega 8</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-raven.g816">Raven</a>

			</td>
	<td>Feb 12th, 2018</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>512 / 32 / 8</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-vega-8-embedded.c3212">Radeon Vega 8 Embedded</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-raven.g816">Raven</a>

			</td>
	<td>Feb 13th, 2018</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>512 / 32 / 8</td>
</tr>
								<tr>
	<td class="vendor-AMD">
		<a href="/gpu-specs/radeon-vega-8-embedded.c3223">Radeon Vega 8 Embedded</a>
			</td>
	<td>
		<a href="/gpu-specs/amd-raven.g816">Raven</a>

			</td>
	<td>Apr 19th, 2018</td>
	<td>IGP</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>512 / 32 / 8</td>
</tr>
		
			</tbody></table>
"""
product_urls = extract_gpu_urls(html_content)
for name, url in product_urls.items():
    print(f"{name}: {url}")