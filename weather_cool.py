import requests
from bs4 import BeautifulSoup
from urllib import parse
import datetime
import os
import pandas as pd
import time
import csv

df = pd.DataFrame(columns=['日期', '縣市別', '觀測站編號', '觀測站', '氣溫', '相對溼度', '風速', '降水量', '降水時數', '日照時數', '日照率', '蒸發量'])
resource_path = (r'./weather')
if not os.path.exists(resource_path):
    os.mkdir(resource_path)
#-----------------------------------------------------------
url = 'https://e-service.cwb.gov.tw/wdps/obs/state.htm'
headers = {'Cookie': '_ga=GA1.3.1023143537.1591705251; TS012b38c7=0107dddfef409bb047eb475f7845714ad4a008a40cf724bc4503f8d6b648287c46133674cc',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
res = requests.get(url=url, headers=headers)
res.encoding = "Big5"
soup = BeautifulSoup(res.text, 'html.parser')
#-----------------------------------------------------------
tr = soup.select('tr')[2:470] #測站數量
allst=[]
#-----------------------------------------------------------
begin_date = datetime.date(2019, 1,1)
end_date = datetime.date(2020,5,31)

for i in range((end_date - begin_date).days + 1):
    day = begin_date + datetime.timedelta(days=i)
    date = str(day)
    month =date.split('-')[0]+'-'+date.split('-')[1]
    # -----------------------------------------------------------
    for td in tr:
        list=[]
        td = td.select('td')
        no = td[0].text.replace("\n", "").replace("\r", "")
        st = td[1].text.replace("\n", "").replace("\r", "")
        city = td[5].text.replace("\n", "").replace("\r", "")
        list.append(no)
        list.append(st)
        list.append(city)
        weather_url = 'https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station={}&stname={}&datepicker={}'.format(
            list[0], parse.quote(parse.quote(list[1])), month)
        headers = {'urgent':
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        res = requests.get(url=weather_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        tr = soup.select('tr')[4:35] #日別
        # print(tr)
    #
        for td in tr:
            td = td.select('td')
            # print(td)
            ej = []
            Temperature = td[7].text.strip()
            RH = td[13].text.strip()
            WS = td[16].text.strip()
            Precp = td[21].text.strip()
            PrecpHour = td[22].text.strip()
            SunShine = td[27].text.strip()
            SunShineRate = td[28].text.strip()
            EvapA = td[31].text.strip()

            ej.append(date)
            ej.append(city)
            ej.append(no)
            ej.append(st)
            ej.append(Temperature)
            ej.append(RH)
            ej.append(WS)
            ej.append(Precp)
            ej.append(PrecpHour)
            ej.append(SunShine)
            ej.append(SunShineRate)
            ej.append(EvapA)
            time.sleep(3)
            if len(ej) != 0:
                allst.append(ej)
            else:
               break
        # print(allst)
    #
            city_path = (r'./weather/%s' % (city))
            if not os.path.exists(city_path):
                os.mkdir(city_path)


            a_df = df.append(pd.DataFrame(allst,
                                          columns=['日期', '縣市別', '觀測站編號', '觀測站', '氣溫', '相對溼度', '風速', '降水量', '降水時數',
                                                   '日照時數', '日照率', '蒸發量']))

            a_df.to_csv(str(city_path)+'/%s.csv' % (st), mode='a', header=False, index=False, encoding="utf-8-sig")


