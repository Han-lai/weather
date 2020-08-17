import requests
from bs4 import BeautifulSoup
from urllib import parse
import datetime
import json
import os
import pandas as pd
import time
# ss = requests.session()
#--------------------------------------------
# resource_path = (r'./weather')
# if not os.path.exists(resource_path):
#     os.mkdir(resource_path)
#--------------------------------------------
all = []
df = pd.DataFrame(columns=['日期', '縣市別', '觀測站編號', '觀測站', '氣溫', '相對溼度', '風速', '降水量', '降水時數', '日照時數', '日照率', '蒸發量'])

url ='https://e-service.cwb.gov.tw/wdps/obs/state.htm'
headers = {'urgent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
res = requests.get(url=url, headers=headers)
res.encoding = "Big5"
soup = BeautifulSoup(res.text, 'html.parser')
#--------------------------------------------
begin_date = datetime.date(2019, 1,1)
end_date = datetime.date(2019, 1,2)
for i in range((end_date - begin_date).days + 1):
    day = begin_date + datetime.timedelta(days=i)
    date = str(day)
    month =date.split('-')[0]+'-'+date.split('-')[1]
# month = '2020-04'
#------------------------------------------------------------

#-----------鎮宏-------------------------
    station_list = soup.select('tr')[2:5]  # 46~c0:(>2,,470)
    # print(station_list)
    station_info = [s.text.split('\n\n') for s in station_list] #先做分隔
    notation = ['\n', '\r', ' '] #有奇怪符號的
    station = []
    for i in station_info[0][:3]:  # [第幾筆資料][第幾欄]
        if len(i) > 1:
            for n in notation:
                i = i.replace(n, '')#把換行符號換掉
            station.append(i)

    # print(station)
    # -----------鎮宏-------------------------
    # print(l)
    # station_info = enumerate(station_list)
    # for n, tr in station_info:
    #     # if n > 1 and n < 610: #>1 <6+10
    #     if n > 1 and n < 4:  # >1 <610   46~c0:(>2,,470)
    #         td = tr.select('td')
    # td_info = [t.select('p.MsoNormal')[0].text for t in td]
    # td_info = enumerate(td)
    # print(td_info)
    #         for m, info in td_info:
    #             if m == 5:
    #                 station_city = info.select('p.MsoNormal')[0].text
    #             if m == 0:
    #                 station_no = info.select('p.MsoNormal')[0].text
    #             if m == 1:
    #                 name = info.select('p.MsoNormal')[0].text
    #                 station_name = parse.quote(parse.quote(name))
    #
    #
    # # ------------------------------------------------------------
    #
    weather_url = 'https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station={}&stname={}&datepicker={}'.format(
        station[0], parse.quote(parse.quote(station[1])), month)
    headers = {'urgent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    res = requests.get(url=weather_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup)

    #     each_list = soup.select('tr')
    #     del each_list[0]
    #     del each_list[0]
    #     del each_list[0]
    #     del each_list[0]
    #     each_info = enumerate(each_list)
    #     # print(each_list)
    #
    #     for n, td in each_info:
    #         print('第%s天資料'.format(date))
    #         if n in range(3,34):
    #             data = td.select('td')
    #             # date = data[0].text
    #             Temperature= data[7].text.strip()
    #             RH= data[13].text.strip()
    #             WS= data[16].text.strip()
    #             Precp= data[21].text.strip()
    #             PrecpHour = data[22].text.strip()
    #             SunShine= data[27].text.strip()
    #             SunShineRate= data[28].text.strip()
    #             EvapA= data[31].text.strip()
    #
    #             ej = []
    #             ej.append(date)
    #             ej.append(station_city)
    #             ej.append(station_no)
    #             ej.append(name)
    #             ej.append(Temperature)
    #             ej.append(RH)
    #             ej.append(WS)
    #             ej.append(Precp)
    #             ej.append(PrecpHour)
    #             ej.append(SunShine)
    #             ej.append(SunShineRate)
    #             ej.append(EvapA)
    #             time.sleep(3)
    #         all.append(ej)
    #                         # print(all)
    #                     #
    #                     # except IndexError as err:
    #                     #     print(err)
    #
    #
    # a_df = df.append(pd.DataFrame(all, columns=['日期','縣市別', '觀測站編號','觀測站', '氣溫', '相對溼度', '風速', '降水量', '降水時數', '日照時數', '日照率', '蒸發量']))
    # # print(a_df)
    # a_df.to_csv(r'./weather/%s/%s.csv' % (station_city, name), index=False, encoding="Big5")
