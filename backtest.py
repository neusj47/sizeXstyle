from load import *

# 사이즈, 스타일 로테이션 전략
# 0. 대상기간 설정하기(6M)
# 1. [Size] 대형주, 중소형주 Signal 생성하기
# 2. [Size to Style]
  # 2.1 대형주일 경우 : 대형순수성장 vs 대형순수가치
     # 2.1.1. 대형순수성장일 경우 : 대형순수성장 vs 중소형순수가치
       # 2.1.1.1. 대형순수성장일 경우 : 대형순수성장 pick
       # 2.1.1.2. 중소형순수가치일 경우 : ''
     # 2.1.2. 대형순수가치일 경우 : 대형순수가치 vs 중소형순수성장
       # 2.1.2.1. 대형순수가치일 경우 : 대형순수가치 pick
       # 2.1.2.2. 중소형순수성장일 경우 : ''
  # 2.2. 중소형주일 경우 : 중소형순수성장 vs 중소형순수가치
    # 2.2.1. 중소형순수성장일 경우 : 중소형순수성장 vs 대형순수가치
       # 2.2.1.1. 중소형순수성장일 경우 : 중소형순수성장 pick
       # 2.2.1.2. 대형순수가치일 경우 : ''
    # 2.2.2. 중소형순수가치일 경우 : 중소형순수가치 vs 대형순수성장
       # 2.2.2.1. 중소형순수가치일 경우 : 중소형순수가치 pick
       # 2.2.2.2. 대형순수성장일 경우 : ''
# 3. [Style to Size]
  # 3.1 성장주일 경우 : 대형순수성장 vs 중소형순수성장
     # 2.1.1. 대형순수성장일 경우 : 대형순수성장 vs 중소형순수가치
       # 2.1.1.1. 대형순수성장일 경우 : 대형순수성장 pick
       # 2.1.1.2. 중소형순수가치일 경우 : ''
     # 2.1.2. 중소형순수성장일 경우 : 중소형순수성장 vs 대형순수가치
       # 2.1.2.1. 중소형순수성장일 경우 : 중소형순수성장 pick
       # 2.1.2.2. 대형순수가치일 경우 : ''
  # 2.2. 가치주일 경우 : 대형순수가치 vs 중소형순수가치
    # 2.2.1. 대형순수가치일 경우 : 대형순수가치 vs 중소형순수성장
       # 2.2.1.1. 대형순수가치일 경우 : 대형순수가치 pick
       # 2.2.1.2. 중소형순수성장일 경우 : ''
    # 2.2.2. 중소형순수가치일 경우 : 중소형순수가치 vs 대형순수성장
       # 2.2.2.1. 중소형순수가치일 경우 : 중소형순수가치 pick
       # 2.2.2.2. 대형순수성장일 경우 : ''

def get_size_style_signal(start_date, end_date) :
    size_signal = get_signal('대형주', '중소형주', start_date, end_date)[1]
    if size_signal == '대형주' :
        size_style_signal = get_signal('대형순수성장','대형순수가치',start_date,end_date)[1]
        if size_style_signal == '대형순수성장' :
            size_style_test_signal = get_signal('대형순수성장','중소형순수가치',start_date,end_date)[1]
            if size_style_test_signal == '대형순수성장' :
                print('대형순수성장')
                size_to_style = size_style_test_signal
            else :
                print('판단유보')
                size_to_style = ''
        else :
            size_style_test_signal = get_signal('대형순수가치', '중소형순수성장', start_date, end_date)[1]
            if size_style_test_signal == '대형순수가치':
                print('대형순수가치')
                size_to_style = size_style_test_signal
            else:
                print('판단유보')
                size_to_style = ''
    else :
        size_style_signal = get_signal('중소형순수성장', '중소형순수가치', start_date, end_date)[1]
        if size_style_signal == '중소형순수성장' :
            size_style_test_signal = get_signal('중소형순수성장','대형순수가치',start_date,end_date)[1]
            if size_style_test_signal == '중소형순수성장' :
                print('중소형순수성장')
                size_to_style = size_style_test_signal
            else :
                print('판단유보')
                size_to_style = ''
        else :
            size_style_test_signal = get_signal('중소형순수가치', '대형순수성장', start_date, end_date)[1]
            if size_style_test_signal == '중소형순수가치':
                print('중소형순수가치')
                size_to_style = size_style_test_signal
            else:
                print('판단유보')
                size_to_style = ''
    return size_to_style

def get_style_size_signal(start_date, end_date) :
    style_signal = get_signal('성장주', '가치주', start_date, end_date)[1]
    if style_signal == '성장주' :
        style_size_signal = get_signal('대형순수성장','중소형순수성장',start_date,end_date)[1]
        if style_size_signal == '대형순수성장' :
            style_size_test_signal = get_signal('대형순수성장','중소형순수가치',start_date,end_date)[1]
            if style_size_test_signal == '대형순수성장' :
                print('대형순수성장')
                style_to_size = style_size_test_signal
            else :
                print('판단유보')
                style_to_size = ''
        else :
            style_size_test_signal = get_signal('중소형순수성장', '대형순수가치', start_date, end_date)[1]
            if style_size_test_signal == '중소형순수성장':
                print('중소형순수성장')
                style_to_size = style_size_test_signal
            else:
                print('판단유보')
                style_to_size = ''
    else :
        style_size_signal = get_signal('대형순수가치', '중소형순수가치', start_date, end_date)[1]
        if style_size_signal == '대형순수가치' :
            style_size_test_signal = get_signal('대형순수가치','중소형순수성장',start_date,end_date)[1]
            if style_size_test_signal == '대형순수가치' :
                print('대형순수가치')
                style_to_size = style_size_test_signal
            else :
                print('판단유보')
                style_to_size = ''
        else :
            style_size_test_signal = get_signal('중소형순수가치', '대형순수성장', start_date, end_date)[1]
            if style_size_test_signal == '중소형순수가치':
                print('중소형순수가치')
                style_to_size = style_size_test_signal
            else:
                print('판단유보')
                style_to_size = ''
    return style_to_size


end_date = '20220331'
start_date = '20191230'
bdate_m = get_bdate_info(start_date, end_date)
bdate_m = bdate_m[bdate_m['월말']==1].reset_index(drop=True)

df = pd.DataFrame()
for i in range(0,len(bdate_m)) :
    end_date = datetime.strftime(bdate_m.일자[i], "%Y%m%d")
    start_date = stock.get_nearest_business_day_in_a_week(datetime.strftime(datetime.strptime(end_date, "%Y%m%d") - relativedelta(months=3),"%Y%m%d"))
    size_style_signal = get_size_style_signal(start_date, end_date)
    style_size_signal = get_style_size_signal(start_date, end_date)
    df_temp = pd.DataFrame({'StdDate':[end_date], 'size_style':[size_style_signal], 'style_size':[style_size_signal]})
    df = pd.concat([df,df_temp])
    print(end_date, size_style_signal,style_size_signal)

df.to_excel('C:/Users/ysj/Desktop/all.xlsx')
