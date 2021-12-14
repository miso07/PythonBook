import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from selenium import  webdriver
from time import sleep

# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

driver = webdriver.Chrome(executable_path="chromedriver.exe")

driver.get('https://kr.investing.com/crypto/bitcoin/historical-data?')
sleep(1)
content = BeautifulSoup(driver.page_source, 'html.parser')

inputs = content.select('table')

print("=============selenium===============")
table_html = str(inputs)
df = pd.read_html(table_html)
driver.quit()

df_day = df[0]
xs=df_day.index.to_list() #플롯할 데이터 모두 list로 저장

print("df_day:",df_day)

ys_date=df_day['날짜'].apply(lambda x: x[6:]).to_list() #년도는 빼고 보여줌.
ys_open=df_day['오픈'].to_list()
ys_close=df_day['종가'].to_list()

plt.figure(figsize=(10, 8)) #전체 그래프 크기 설정
plt.plot(ys_date, ys_open, 'o-', ms=5, lw=3, label='Open') #xy데이터 플롯-line
plt.plot(ys_date, ys_close, 'o-', ms=5, lw=3, label='Close') #xy데이터 플롯

plt.legend(['Open','Close'], loc='upper left')

plt.xticks(ticks=xs, labels=ys_date) # x축눈금표시
plt.locator_params(axis='x', nbins=len(ys_date)/5) # x축의 눈금 빈도

plt.ylim(30000, 100000) #y축 최대, 최소값
plt.xlabel('Date') #x축 이름
plt.ylabel('Price ($)') #y축 이름 plt.legend()

plt.show()

#스타일 문자열	약자	의미
#color	c	선 색깔
#linewidth	lw	선 굵기
#linestyle	ls	선 스타일
#marker		마커 종류
#markersize	ms	마커 크기
#markeredgecolor	mec	마커 선 색깔
#markeredgewidth	mew	마커 선 굵기
#markerfacecolor	mfc	마커 내부 색깔

#plt.yscale('log') #y축 로그스케일 설정
#plt.rc('xtick', labelsize=10)  # x축 눈금 폰트 크기