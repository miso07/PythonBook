import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

import FinanceDataReader as fdr
import matplotlib.pyplot as plt
from datetime import datetime
import urllib.request as req
from bs4 import BeautifulSoup
import json
import threading
import math

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from timer_graph_popup import UI_Qt5_Popup

# 현재시간 가져오기
now = datetime.now()
year = now.strftime('%Y') # 현재연도 가져오기
print(year)

df   = fdr.DataReader('BTC/USD', year)
df_1 = fdr.DataReader('ETH/USD', year)
df_2 = fdr.DataReader('SOL/USD', year)

print(df)

form_class = uic.loadUiType("coinTrader.ui")[0]
class MyWindow(QMainWindow, form_class):
    #팝업으로 데이타 전송하기 위한 파라미터(선택된 콤보박스)
    coin = "비트코인"

    # 프로그램 시작
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 이벤트 로그에 추가
        self.listWidget.addItem('프로그램 start')

        #조회버튼 기능 연결
        self.pushButton.clicked.connect(self.send_search)

        #분봉조회 팝업버튼 기능 연결
        self.pushButton2.clicked.connect(self.openPopup)

        # CheckBox에 기능 연결 - 알람ON(2%차이) 했을경우 이벤트 처리
        self.checkBox1.stateChanged.connect(self.chkFunction1)

        # CheckBox에 기능 연결 - 알람ON(5%차이) 했을경우 이벤트 처리
        self.checkBox2.stateChanged.connect(self.chkFunction2)

        #일별 그래프 추가
        self.fig = plt.figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.fig)
        self.verticalLayout.addWidget(self.canvas)

        #거래소별 가격차이가 발생했을 경우 지능형 알림 발생
        self.fn_runIntelligentAlerting()


    #조회
    def send_search(self):

        #그래프 그리기
        self.drawGraph()

    #분봉조회 팝업 호출
    def openPopup(self) :

        #선택된 콤보박스 내용 가져오기
        self.coin = self.comboBox.currentText()

        #팝업을 호출할 때 부모창의 정보를 self로 넘겨준다.
        self.popup = UI_Qt5_Popup(self)
        self.popup.setGeometry(self.x()+100, self.y()+100, 800, 400)
        self.popup.show()

    #체크박스선택-알람ON(2%차이) 했을경우 이벤트 처리
    def chkFunction1(self):
        if self.checkBox1.isChecked() :
            # 이벤트 로그에 추가
            print("checkBox1 isChecked")
            self.listWidget.insertItem(0, self.fn_now()+' 알람ON(2%차이) 이벤트 추가')

        else:
            print("checkBox1 is not Checked")
            self.listWidget.insertItem(0, self.fn_now()+' 알람ON(2%차이) 이벤트 삭제')

    #체크박스선택-알람ON(5%차이) 했을경우 이벤트 처리
    def chkFunction2(self):
        if self.checkBox2.isChecked() :
            # 이벤트 로그에 추가
            print("checkBox2 isChecked")
            self.listWidget.insertItem(0, self.fn_now()+' 알람ON(5%차이) 이벤트 추가')
        else:
            print("checkBox2 is not Checked")
            self.listWidget.insertItem(0, self.fn_now()+' 알람ON(5%차이) 이벤트 삭제')


    #그래프 그리기
    def drawGraph(self):
        try:
            coin = self.comboBox.currentText()

            # comboBox가 비트코인인 경우
            my_crypto = df
            if(coin=='이더리움'): # comboBox가 이더리움인 경우
                my_crypto = df_1

            if(coin=='솔라나'): # comboBox가 솔라나인 경우
                my_crypto = df_2

            # 이벤트 로그에 추가
            self.listWidget.insertItem(0, self.fn_now()+" "+coin+" 그래프 실행")

            # matplotlib을 이용한 그래프 그리기 
            plt.cla()
            plt.plot(my_crypto['Open'], alpha=0.7, lw=2)
            plt.plot(my_crypto['Close'], alpha=0.7, lw=2)
            plt.title("Cryptocurrencies Graph(Year)")
            plt.xlabel('Months')
            plt.ylabel('Crypto Price USD($)')
            plt.legend(['Open','Close'], loc='upper left')
            self.canvas.draw()

        # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
        except Exception as e:
            print('예외가 발생했습니다.', e)

    #거래소별 가격차이가 발생했을 경우 지능형 알림 발생
    def fn_runIntelligentAlerting(self):

        print(self.fn_now()+" 배치실행(1분)")
        self.timer = threading.Timer(60, self.fn_runIntelligentAlerting)

        arrCoin=['BTC', 'ETH', 'SOL']
        try:
            for i in arrCoin:

                # 데이타 가져옴
                res1 = req.urlopen("https://api.coinone.co.kr/ticker/?currency="+i)
                res2 = req.urlopen("https://api.bithumb.com/public/ticker/"+i)

                #HTML 파싱
                soup1 = BeautifulSoup(res1, "html.parser")
                soup2 = BeautifulSoup(res2, "html.parser")

                #UTF-8로 디코딩
                coin_info1 = soup1.decode('utf-8')
                coin_info2 = soup2.decode('utf-8')

                #JSON으로 로드
                jsonString1 = json.loads(coin_info1)
                jsonString2 = json.loads(coin_info2)
                
                # 코인원과 빗썸에서 가져온 방식이 달라서 가져오는 부분이 다름
                # 코인원에서 가져온 종가 금액에 .0 이 붙는 부분을 삭제
                last1 = jsonString1['last'].replace(".0", "")
                
                # 빗썸에서 가져온 종가 금액을 가져옴
                last2 = jsonString2['data']['closing_price']

                # 숫자 타입으로 변환
                ilast1 = float(last1)
                ilast2 = float(last2)

                d = ilast2 - ilast1 # 두값 차이(빗썸 가격-코인원 가격)

                print( self.fn_now()+" ("+i+") 코인원:"+last1+", 빗썸:"+last2
                       +" 차이:"+ str(self.fn_abs(self.fn_per(ilast1, d))))

                #빗썸과 코인원의 가격이 5%이상 발생했을 경우 이벤트 로그에 추가
                if self.fn_abs(self.fn_per(ilast1, d)) >= 5:
                    if self.checkBox1.isChecked() :
                        self.listWidget.insertItem(0, self.fn_now()+" ("+i+") "
                                    +str(self.fn_abs(self.fn_per(ilast1, d)))
                                    +"% 차이 발생. 코인원:"+last1+", 빗썸:"+last2)
                        print(self.fn_now() + " (" + i + ") 코인원:" + last1 + ", 빗썸:"
                              + last2 + " 차이:" + str(self.fn_abs(self.fn_per(ilast1, d))))

                #빗썸과 코인원의 가격이 5%이상 발생했을 경우 이벤트 로그에 추가
                if self.fn_abs(self.fn_per(ilast1, d)) >= 2:
                    if self.checkBox2.isChecked() :
                        self.listWidget.insertItem(0, self.fn_now()+" ("+i+") "
                                    +str(self.fn_abs(self.fn_per(ilast1, d)))
                                    +"% 차이 발생. 코인원:"+last1+", 빗썸:"+last2)
                        print(self.fn_now() + " (" + i + ") 코인원:" + last1 + ", 빗썸:"
                              + last2 + " 차이:" + str(self.fn_abs(self.fn_per(ilast1, d))))

            self.timer.start()

        # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
        except Exception as e:
            print('예외가 발생했습니다.', e)
            self.timer.start()

    # -값이 있어서 절대값을 만들
    def fn_abs(self, a):
        b = a * a
        return math.sqrt(b)

    # 차이가 몇%인지 확인
    def fn_per(self, a, c):
        return round(self.fn_abs(c / a * 100))

    # 현재시간 가져오기
    def fn_now(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #화면을 닫을경우 배치까지 종료
    def closeEvent(self, event):
        print('closeEvent System exit2')
        self.timer.cancel()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())