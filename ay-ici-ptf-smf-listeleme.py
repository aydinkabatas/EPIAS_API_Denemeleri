import requests
import pandas as pd
import datetime as dt
import calendar
import getkey

today_date=dt.datetime.now()

TGT=getkey.get_TGT()

apiheader= {
    "TGT":          TGT,
    "Content-Type": "application/json"
}
yil=str(today_date.year)
ay=str(today_date.month) if len(str(today_date.month))==2 else '0'+str(today_date.month)
son_gun=str(calendar.monthrange(today_date.year, today_date.month)[1])

api_url = "https://seffaflik.epias.com.tr/reporting-service/v1/data/ptf-smf-sdf"

payload = {
    "endDate":      yil+"-"+ay+"-"+son_gun+"T23:59:59+03:00",
    "startDate":    yil+"-"+ay+"-"+"01T00:00:00+03:00"
}

response = requests.post(api_url, json=payload, headers=apiheader)
bulk_data = response.json()

df=pd.json_normalize(bulk_data, 'items')

df.to_excel("~/Desktop/"+yil+"-"+ay+"_PTF-SMF-SDF.xlsx")
print(df)
