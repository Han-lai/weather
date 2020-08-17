import requests
from bs4 import BeautifulSoup
from urllib import parse
import json
import os
import pandas as pd
import time
# ss = requests.session()

url ='https://e-service.cwb.gov.tw/wdps/obs/state.htm'
headers = {'urgent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
res = requests.get(url=url, headers=headers)
res.encoding = "Big5"
soup = BeautifulSoup(res.text, 'html.parser')
station_list = soup.select('tr')
station_info = enumerate(station_list)
for n, tr in station_info:
    # if n > 1 and n < 610: #>1 <610
    if n > 2 and n < 4:  # >1 <610
        td = tr.select('td')
        td_info = enumerate(td)
    # print(td)
        for m, info in td_info:
            if m == 0:
                station_no = info.select('p.MsoNormal')[0].text
            if m == 1:
                name = info.select('p.MsoNormal')[0].text

                station_name1= parse.quote(name)

                station_name = parse.quote(station_name1)

            # if m == 3:
            #     station_lon = info.select('p.MsoNormal')[0].text
            # if m == 4:
            #     station_lat = info.select('p.MsoNormal')[0].text
            # if m == 5:
            #     station_city = info.select('p.MsoNormal')[0].text


            # try :
                weather_url = 'https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station={}&stname={}&datepicker=2020-06'.format(station_no, station_name)
                # print(weather_url)
                headers = {'urgent':
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
                res = requests.get(url=weather_url, headers=headers)
                # print(res)
                # res.encoding = "gbk"
                soup = BeautifulSoup(res.text, 'html.parser')
                # print(soup)
                each_list = soup.select('tr')
                del each_list[0]
                del each_list[0]
                del each_list[0]
                del each_list[0]
                each_info = enumerate(each_list)
                print(each_list)

                for n, td in each_info:
                    # if n in range(3,34):
                    data = td.select('td')
                    print(data)
                    data_info = enumerate(data)
                    for m, env in data_info:
                        # for m in range(34):
                        ObsTime = env.text
                        print(ObsTime)



            #
            # except IndexError as err:
            #     print(err)

    else:
        continue
# weather_url = 'https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=467571&stname=%E6%96%B0%E7%AB%B9&datepicker=2020-06'
# print(weather_url)
# headers = {'urgent':
#                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
# res = requests.get(url=weather_url, headers=headers)
# # print(res)
# res.encoding = "Big5"
# soup = BeautifulSoup(res.text, 'html.parser')
# print(soup)