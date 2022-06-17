import requests
import pandas as pd
from datetime import datetime
from pykrx import stock
import numpy as np
from dateutil.relativedelta import relativedelta
import math
import warnings
warnings.filterwarnings('ignore')

def get_bdate_info(start_date, end_date) :
    end_date = stock.get_nearest_business_day_in_a_week(datetime.strftime(datetime.strptime(end_date, "%Y%m%d") + relativedelta(days=1),"%Y%m%d"))
    date = pd.DataFrame(stock.get_previous_business_days(fromdate=start_date, todate=end_date)).rename(columns={0: '일자'})
    prevbdate = date.shift(1).rename(columns={'일자': '전영업일자'})
    date = pd.concat([date, prevbdate], axis=1).fillna(
        datetime.strftime(datetime.strptime(stock.get_nearest_business_day_in_a_week(datetime.strftime(datetime.strptime(start_date, "%Y%m%d") - relativedelta(days=1), "%Y%m%d")), "%Y%m%d"),"%Y-%m-%d %H:%M:%S"))
    date['주말'] = ''
    for i in range(0, len(date) - 1):
        if abs(datetime.strptime(datetime.strftime(date.iloc[i + 1].일자, "%Y%m%d"), "%Y%m%d") - datetime.strptime(datetime.strftime(date.iloc[i].일자, "%Y%m%d"), "%Y%m%d")).days > 1:
            date['주말'].iloc[i] = 1
        else:
            date['주말'].iloc[i] = 0
    month_list = date.일자.map(lambda x: datetime.strftime(x, '%Y-%m')).unique()
    monthly = pd.DataFrame()
    for m in month_list:
        try:
            monthly = monthly.append(date[date.일자.map(lambda x: datetime.strftime(x, '%Y-%m')) == m].iloc[-1])
        except Exception as e:
            print("Error : ", str(e))
        pass
    date['월말'] = np.where(date['일자'].isin(monthly.일자.tolist()), 1, 0)
    return date

def get_idx_value(start_date, end_date) :
    bdate = get_bdate_info(start_date, end_date)['일자'].sort_values(ascending=False)
    start_date = datetime.strftime(bdate.iloc[len(bdate) - 1], "%Y-%m-%d")
    end_date = datetime.strftime(bdate.iloc[0], "%Y-%m-%d")
    idx = {'I510T': '대형주',
           'I540T': '중소형주',
           'S10T': '가치주',
           'S20T': '성장주',
           'S31T': '대형순수가치',
           'S41T': '대형순수성장',
           'S44T': '중소형순수성장',
           'S34T': '중소형순수가치'}
    df = pd.DataFrame(columns=['stddate', 'idx', 'idx_value', 'mkt_cap'])
    for keys, values in enumerate(idx.items()) :
        response = requests.get('https://www.wiseindex.com/DataCenter/GridData?currentPage=1&endDT='+ end_date +'&fromDT='+start_date+'&index_ids=WM'+str(values[0])+'&isEnd=1&itemType=1&perPage=600&term=1')
        if (response.status_code == 200):
            json_list = response.json()
            for i in json_list :
                stddate = datetime.strftime(bdate.iloc[i['ROW_IDX']-1], "%Y-%m-%d")
                idx_value = i['IDX1_VAL1']
                mkt_cap = i['IDX1_VAL2'] * 1/1000000
                df = df.append(
                    {'stddate': stddate, 'idx':values[1], 'idx_value': idx_value, 'mkt_cap': mkt_cap}, ignore_index=True)
    return df

def get_signal(tgt1,tgt2,start_date,end_date) :
    df = get_idx_value(start_date, end_date)
    df_1 = df[df.idx == tgt1]
    df_2 = df[df.idx == tgt2]
    df_target = pd.merge(df_1[['stddate','idx_value']], df_2[['stddate','idx_value']], on = 'stddate', how = 'inner')
    df_target.columns = ['stddate',tgt1,tgt2]
    df_target['Ln1'] = df_target[tgt1].apply(lambda x: math.log(float(x)))
    df_target['Ln2'] = df_target[tgt2].apply(lambda x: math.log(float(x)))
    df_target['Sprd'] = df_target['Ln1'] - df_target['Ln2']
    df_target['Mean'] = df_target['Sprd'].mean()
    df_target['Stdev'] = df_target['Sprd'].std()
    df_target['Diff'] = df_target['Sprd'] - df_target['Mean']
    df_target['Signal'] = np.where(df_target['Diff']>df_target['Stdev']*0.5,tgt1,np.where(df_target['Diff']<-df_target['Stdev']*0.5,tgt2,''))
    df_target = df_target.sort_values('stddate').reset_index(drop=True)
    signal = df_target.iloc[len(df_target)-1]['Signal']
    return df_target, signal

def get_constituents(stddate):
    sector = {'WMS41': '대형순수성장',
              'WMS31': '대형순수가치',
              'WMS44': '중소형순수성장',
              'WMS34': '중소형순수가치'}
    df = pd.DataFrame(columns=['지수코드','지수명', '티커', '종목명', '섹터'])
    for i, sec_code in enumerate(sector.keys()):
        response = requests.get('https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=' + stddate + '&sec_cd=' + str(sec_code))
        if (response.status_code == 200):
            json_list = response.json()
            for json in json_list['list'] :
                지수코드 = str(sec_code)
                지수명 = json['IDX_NM_KOR'][7:]
                티커 = "A" + json['CMP_CD']
                종목명 = json['CMP_KOR']
                섹터 = json['SEC_NM_KOR']
                df = df.append(
                    {'지수코드' : 지수코드, '지수명': 지수명, '티커': 티커, '종목명': 종목명, '섹터': 섹터}, ignore_index=True)
    return df
