import pandas as pd

# 날씨 데이터
## 데이터 불러오기
wth = pd.read_csv('C:\\dd\\my2.csv', encoding='cp949')

wth_y = pd.read_csv('C:\\dd\\ygj2.csv', encoding='cp949')

## 열 이름 설정
wth.columns = ['code', 'name', 'date', 'C', 'humid', 'rain', 'cloud', 'solar']
wth2 = wth[wth['name'] != '문경'].copy()

wth_y.columns = ['code', 'name', 'date', 'C', 'humid', 'rain', 'cloud', 'solar']


## datetime으로 통일
wth2['date'] = wth2['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m'))

wth_y['date'] = wth_y['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m'))

## 탑선-광주 분리
wth3 = wth2[wth2['name'] == '광주']

## 영흥-인천 분리
wth4 = wth2[wth2['name'] == '인천']

## 경상대, 삼천포, 삼천포#5-진주 분리
wth_yj = wth_y[wth_y['name'] == '진주']

## 여수-여수 분리
wth_yy = wth_y[wth_y['name'] == '여수']

## 강릉-영동 분리
wth_yg = wth_y[wth_y['name'] == '강릉']



# 발전량 데이터
## 데이터 불러오기
df = pd.read_excel('C:\\dd\\한국남동발전_발전실적 (1).xls')
df.columns = ['loc', 'plant', 'date', 'storage', 'EG', 'ther', 'userate', 'generator']
df2 = df[df['generator'] == '태양력'].copy()

## datetime으로 통일
df2['date'] = df2['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m'))
df2 = df2.sort_values('date')

## 예천태양광, 영흥태양광5, 광양항세방태양광, 두산태양광, 구미태양광 삭제
dlt = df2['loc'] != ('예천태양광' and '영흥태양광#5' and '광양항세방태양광' and '두산태양광' and '구미태양광' and '삼천포태양광#6')
df3 = df2[dlt]

# 날씨 추가
## 탑선태양광에 날씨 추가
df4 = df3[df3['loc'] == '탑선태양광']
tmp = pd.merge(df4, wth3, on='date', how='left')

## 영흥태양광에 날씨 추가
df5 = df3[df3['loc'] == '영흥태양광']
tmp1 = pd.merge(df5, wth4, on='date', how='left')

df6 = df3[df3['loc'] == '영흥태양광 #3']
tmp2 = pd.merge(df6, wth4, on='date', how='left')

## 경상대태양광에 날씨 추가
df7 = df3[df3['loc'] == '경상대태양광']
tmp3 = pd.merge(df7, wth_yj, on='date', how='left')

## 삼천포태양광에 날씨 추가
df8 = df3[df3['loc'] == '삼천포태양광']
tmp4 = pd.merge(df8, wth_yj, on='date', how='left')

df9 = df3[df3['loc'] == '삼천포태양광#5']
tmp5 = pd.merge(df9, wth_yj, on='date', how='left')

## 여수태양광에 날씨 추가
df10 = df3[df3['loc'] == '여수태양광']
tmp6 = pd.merge(df10, wth_yy, on='date', how='left')

## 영동태양광에 날씨 추가
df11 = df3[df3['loc'] == '영동태양광']
tmp7 = pd.merge(df11, wth_yg, on='date', how='left')


## 탑선 + 영흥 + 삼천포 + 여수 + 영동 + 경동
temp = tmp.append([tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7])

## 완성
ee = pd.merge(df3, temp, how='left')

ee.to_excel('C:\\dd\\main.xlsx')
