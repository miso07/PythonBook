from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime

#업비트 API 정보
import pyupbit

class UI_Qt5_Popup(QMainWindow):

    def __init__(self, parant):
        super().__init__()

        try:
            print("==============popup============")

            #부모창의 정보를 가져온다.
            self.parant = parant
            print(self.parant.coin)

            self.coin_kind='KRW-BTC'
            if(self.parant.coin=='이더리움'):
                self.coin_kind='KRW-ETH'
            if(self.parant.coin=='솔라나'):
                self.coin_kind='KRW-SOL'

            self.main_widget = QWidget()
            self.setCentralWidget(self.main_widget)

            vbox = QVBoxLayout(self.main_widget)

            dynamic_canvas = FigureCanvas(Figure(figsize=(10, 8)))
            vbox.addWidget(dynamic_canvas)

            self.dynamic_ax = dynamic_canvas.figure.subplots()
            
            # 업비트에서 1분데이타 200개 가져옴
            my_crypto = pyupbit.get_ohlcv(self.coin_kind, interval="minute1")

            print(my_crypto)
            self.dynamic_ax.plot(my_crypto['open'], alpha=0.7, lw=2)
            self.dynamic_ax.figure.canvas.draw()

            #20초 마다 그래프를 갱신한다.
            self.timer = dynamic_canvas.new_timer(20000, [(self.update_canvas, (), {})])
            self.timer.start()

            self.setWindowTitle(self.parant.coin+" 분봉 그래프")
            self.show()

        # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
        except Exception as e:
            print('예외가 발생했습니다.', e)

    #20초 마다 업비트에서 데이타를 가져와서 그래프를 갱신한다.
    def update_canvas(self):
        print('update_canvas:'+self.fn_now())
        self.dynamic_ax.clear()
        my_crypto = pyupbit.get_ohlcv(self.coin_kind, interval="minute1")

        self.dynamic_ax.plot(my_crypto['open'], alpha=0.7, lw=2)
        self.dynamic_ax.figure.canvas.draw()

    # 현재시간 가져오기
    def fn_now(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def closeEvent(self, event):
        print('closeEvent myDialog')

