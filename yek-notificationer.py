import requests.api
import pandas as pd
import datetime as dt
import calendar
import ctypes
import locale
import time
import getkey


locale.setlocale(locale.LC_ALL, 'tr_TR')
today_date=dt.datetime.now()


yil=str(today_date.year)
ay=str(today_date.month-1) if len(str(today_date.month-1))==2 else '0'+str(today_date.month-1)
son_gun=str(calendar.monthrange(today_date.year, today_date.month-1)[1])


TGT=getkey.get_TGT()

apiheader= {
    "TGT":          TGT,
    "Content-Type": "application/json"
}

api_url = "https://seffaflik.epias.com.tr/electricity-service/v1/renewables/data/unit-cost"

payload = {
    "endDate": yil+"-"+ay+"-"+son_gun+"T23:59:59+03:00",
    "startDate": yil+"-"+ay+"-"+"01T00:00:00+03:00"
}

starttime = time.monotonic()
while True:
    response = requests.post(api_url, json=payload, headers=apiheader)
    bulk_data = response.json()

    df=pd.json_normalize(bulk_data, 'items')

    if len(df.index)==1:
        break
    
    time.sleep(60.0 - ((time.monotonic() - starttime) % 60.0))
    print("tick")

ctypes.windll.user32.MessageBoxW(0, calendar.month_name[int(ay)]+" Ayı YEK Birim Bedeli Açıklandı!", "YEK ALERT!", 0)
df.to_excel("~/Desktop/"+calendar.month_name[int(ay)]+"AYI-YEK-BEDELİ.xlsx")