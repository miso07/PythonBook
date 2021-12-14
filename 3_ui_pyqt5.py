import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

import FinanceDataReader as fdr
import matplotlib.pyplot as plt
from datetime import datetime

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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

        #일별 그래프 추가
        self.fig = plt.figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.fig)
        self.verticalLayout.addWidget(self.canvas)

    #조회
    def send_search(self):

        #그래프 그리기
        self.drawGraph()

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

    # 현재시간 가져오기
    def fn_now(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #화면을 닫을경우 배치까지 종료
    def closeEvent(self, event):
        print('closeEvent System exit')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())