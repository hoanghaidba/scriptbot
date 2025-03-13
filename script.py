import requests, json, re
from bs4 import BeautifulSoup

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7,fr-FR;q=0.6,fr;q=0.5',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.accuweather.com/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

params = {
    'city': 'hoi an',
}
with requests.Session() as session:
    response = session.get(
    'https://www.accuweather.com/en/vn/hoi-an/355711/weather-forecast/355711',
    params=params,
    headers=headers,
)
soup = BeautifulSoup(response.text, 'html.parser')
for script in soup.find_all('script'):
    if 'recentLocations' in script.get_text():
        match = re.search(r'var recentLocations = (\[.*?\]);', script.get_text(), re.DOTALL)
        if match:
            recent_locations_json = match.group(1)
            recent_locations = json.loads(recent_locations_json)
            location_name = recent_locations[0]['localizedName']
            temp = recent_locations[0]['temp']
            celsius_temp = (int(temp.replace('°', '')) - 32) * 5/9
            realFeel = recent_locations[0]['realFeel']
            celsius_reelFell = (int(realFeel.replace('°', '')) - 32) * 5/9
            print(f'{location_name}|{str(celsius_temp)}|{str(celsius_reelFell)}')
            nd = f'''%f0%9f%8c%8f Địa điểm: {location_name}
%f0%9f%8c%a1 Nhiệt độ hiện tại: {str(celsius_temp)}°
%f0%9f%8c%a4 Cảm giác như: {str(celsius_reelFell)}°'''
with open('bottele1.txt', 'r', encoding='utf-8') as file:
    while True:
        url = file.readline().strip()
        if url == '':
            break
        headers_tele = {
            'authority': 'api.telegram.org',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7,fr-FR;q=0.6,fr;q=0.5',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

        with requests.Session() as session_tele:
            r_tele = session_tele.get(
                f'{url}&text={nd}',
                headers=headers_tele,
            )
