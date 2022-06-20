from load import *

def get_size_style_signal(start_date, end_date) :
    size_signal = get_signal('대형주', '소형주', start_date, end_date)[1]
    if size_signal == '대형주' :
        size_style_signal = get_signal('대형순수성장','대형순수가치',start_date,end_date)[1]
        if size_style_signal == '대형순수성장' :
            size_style_test_signal = get_signal('대형순수성장','소형순수가치',start_date,end_date)[1]
            if size_style_test_signal == '대형순수성장' :
                print('대형순수성장')
                size_to_style = size_style_test_signal
            else :
                print('판단유보')
                size_to_style = ''
        else :
            size_style_test_signal = get_signal('대형순수가치', '소형순수성장', start_date, end_date)[1]
            if size_style_test_signal == '대형순수가치':
                print('대형순수가치')
                size_to_style = size_style_test_signal
            else:
                print('판단유보')
                size_to_style = ''
    else :
        size_style_signal = get_signal('소형순수성장', '소형순수가치', start_date, end_date)[1]
        if size_style_signal == '소형순수성장' :
            size_style_test_signal = get_signal('소형순수성장','대형순수가치',start_date,end_date)[1]
            if size_style_test_signal == '소형순수성장' :
                print('소형순수성장')
                size_to_style = size_style_test_signal
            else :
                print('판단유보')
                size_to_style = ''
        else :
            size_style_test_signal = get_signal('소형순수가치', '대형순수성장', start_date, end_date)[1]
            if size_style_test_signal == '소형순수가치':
                print('소형순수가치')
                size_to_style = size_style_test_signal
            else:
                print('판단유보')
                size_to_style = ''
    return size_to_style

def get_style_size_signal(start_date, end_date) :
    style_signal = get_signal('성장주', '가치주', start_date, end_date)[1]
    if style_signal == '성장주' :
        style_size_signal = get_signal('대형순수성장','소형순수성장',start_date,end_date)[1]
        if style_size_signal == '대형순수성장' :
            style_size_test_signal = get_signal('대형순수성장','소형순수가치',start_date,end_date)[1]
            if style_size_test_signal == '대형순수성장' :
                print('대형순수성장')
                style_to_size = style_size_test_signal
            else :
                print('판단유보')
                style_to_size = ''
        else :
            style_size_test_signal = get_signal('소형순수성장', '대형순수가치', start_date, end_date)[1]
            if style_size_test_signal == '소형순수성장':
                print('소형순수성장')
                style_to_size = style_size_test_signal
            else:
                print('판단유보')
                style_to_size = ''
    else :
        style_size_signal = get_signal('대형순수가치', '소형순수가치', start_date, end_date)[1]
        if style_size_signal == '대형순수가치' :
            style_size_test_signal = get_signal('대형순수가치','소형순수성장',start_date,end_date)[1]
            if style_size_test_signal == '대형순수가치' :
                print('대형순수가치')
                style_to_size = style_size_test_signal
            else :
                print('판단유보')
                style_to_size = ''
        else :
            style_size_test_signal = get_signal('소형순수가치', '대형순수성장', start_date, end_date)[1]
            if style_size_test_signal == '소형순수가치':
                print('소형순수가치')
                style_to_size = style_size_test_signal
            else:
                print('판단유보')
                style_to_size = ''
    return style_to_size

end_date = '20220531'
start_date = '20170101'
bdate_m = get_bdate_info(start_date, end_date)
bdate_m = bdate_m[bdate_m['월말']==1].reset_index(drop=True)

def get_monthly_signal(bdate_m):
    df = pd.DataFrame()
    for i in range(0,len(bdate_m)) :
        end_date = datetime.strftime(bdate_m.일자[i], "%Y%m%d")
        start_date = stock.get_nearest_business_day_in_a_week(datetime.strftime(datetime.strptime(end_date, "%Y%m%d") - relativedelta(months=3),"%Y%m%d"))
        size_style_signal = get_size_style_signal(start_date, end_date)
        style_size_signal = get_style_size_signal(start_date, end_date)
        df_temp = pd.DataFrame({'StdDate':[datetime.strftime(datetime.strptime(end_date, "%Y%m%d"),"%Y-%m-%d")], 'size_style':[size_style_signal], 'style_size':[style_size_signal]})
        df = pd.concat([df,df_temp])
        # print(end_date, size_style_signal,style_size_signal)
    return df

df =  get_monthly_signal(bdate_m)
df = df.reset_index(drop=True)

def get_pf_universe(df) :
    df_pf_univ = pd.DataFrame()
    for i in range(0,len(df)) :
        rebal_date = df.StdDate.unique().tolist()
        univ_all = get_constituents(datetime.strftime(datetime.strptime(rebal_date[i], "%Y-%m-%d"),"%Y%m%d"))
        if df.iloc[i]['size_style'] == '중소형순수성장' :
            df_pf_temp = univ_all[univ_all['지수코드'].isin(['WMS44'])]
        elif df.iloc[i]['size_style'] == '중소형순수가치' :
            df_pf_temp = univ_all[univ_all['지수코드'].isin(['WMS34'])]
        elif df.iloc[i]['size_style'] == '대형순수성장' :
            df_pf_temp = univ_all[univ_all['지수코드'].isin(['WMS41'])]
        elif df.iloc[i]['size_style'] == '대형순수가치':
            df_pf_temp = univ_all[univ_all['지수코드'].isin(['WMS31'])]
        elif df.iloc[i]['size_style'] == '소형순수성장':
            df_pf_temp = univ_all[univ_all['지수코드'].isin(['WMS43'])]
        elif df.iloc[i]['size_style'] == '소형순수가치':
            df_pf_temp = univ_all[univ_all['지수코드'].isin(['WMS33'])]
        elif df.iloc[i]['size_style'] == '' :
            df_pf_temp = pd.DataFrame({'지수코드':['KOSPI'],'지수명':['코스피'],'티커': ['A069500'],'종목명':['코스피'],'섹터': ['코스피']})
        df_pf_temp['StdDate'] = datetime.strftime(datetime.strptime(stock.get_nearest_business_day_in_a_week(datetime.strftime(datetime.strptime(rebal_date[i], "%Y-%m-%d") + relativedelta(days=1) ,"%Y%m%d")),"%Y%m%d"),"%Y-%m-%d")
        df_pf_univ = pd.concat([df_pf_temp, df_pf_univ]).sort_values('StdDate', ascending = True)
    return df_pf_univ
df_pf_univ = get_pf_universe(df)
