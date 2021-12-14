# PythonBook
PythonBook example

## 실시간 가상자산 트레이딩 만들기

이번 장에서는, 네트워크를 통해 데이터를 수집하고 이를 화면에 visualization 하는 예를 소개하고자 한다. 한 가지 예로, 가상화폐 중에서 BTC (비트코인), ETH (이더리움), SOL (솔라나)의 가격을 수집하고, 이를 화면에 보여주고, 때에 따라 정해놓은 조건이 성립하는 경우 자동 알람 기능을 구현하는 예를 보인다.

참고로 본 소스에서 사용하는  파이썬 Library는 pip를 이용하여 설치한다. pip는 파이썬(python)으로 작성된 패키지 소프트웨어를 설치, 관리하는 패키지 관리 시스템이다. pip로 설치하는 전체 스크립트는 다음과 같다.


```c
pip install requests
pip install selenium
pip install -U finance-datareader
pip install pandas
pip install pyupbit
```

***

## 1. 문제설명: 실시간 가상자산 트레이딩 만들기
## 2. 1단계 1: 스크래핑으로 화면 웹 데이터 가져오기 
## 3. 단계 2: 스크래핑으로 수집한 (historic data)의 그래프 그리기
## 4. 단계 3: PyQt5를 이용한 화면 UI 구성 
## 5. 단계 4: Timer를 이용한 실시간 그래프 작성  
## 6. 단계 5: 거래소별 가격차이가 발생했을 경우 지능형 알림 발생


***


* 단계1에서는 웹스크래핑과 Rest API를 이용한 예제를 보여준다. (1-1_scraping_simple.py, 1-2_api_simple.py)

<img src="/img/ex1-1.jpg" width="70%" height="70%" title="단계1 스크래핑으로 화면 웹 데이터 가져오기 예제" alt="ex1-1"></img>


* 단계2에서는 스크래핑 (historic data)으로 가져온 데이터를 이용하여 파이썬에서 제공하는 데이터 시각화를 위한 라이브러리 중 matplotlib를 이용하여 그래프 그리기 예제를 보여준다. (2-1_scraping_graph.py, 2-2_api_graph.py)

<img src="/img/ex1-2.jpg" width="70%" height="70%" title="단계2 스크래핑으로 모은 (historic data)의 그래프 그리기 예제" alt="ex1-2"></img>


* 단계3에서는 파이썬에서 제공하는 GUI 프로그래밍 패키지인 PyQt5를 이용하여 화면 UI를 구성하는 예제를 보여준다. (3_ui_pyqt5.py)  

<img src="/img/ex1-3.jpg" width="70%" height="70%" title="단계3 PyQt5를 이용한 화면 UI 구성 예제" alt="ex1-3"></img>


* 단계4에서는 Timer를 이용하여 현재 거래소에서 제공하는 API를 이용하여 실시간 그래프 를 작성하는 예제를 보여준다. (4_timer_graph.py, timer_graph_popup.py)   

<img src="/img/ex1-4.jpg" width="70%" height="70%" title="단계4 Timer를 이용한 실시간 그래프 작성 예제" alt="ex1-4"></img>


* 단계5에서는 가상화폐 중에서 BTC (비트코인), ETH (이더리움), SOL (솔라나)의 가격을 거래소별로 수집에서 가격차이가 발생했을 경우 지능형 알림을 발생하는 프로그램을 작성하는 예제를 보여준다. (5_intelligent_alert.py) 

<img src="/img/ex1-5.jpg" width="70%" height="70%" title="단계5 거래소별 가격차이가 발생했을 경우 지능형 알림 발생 예제" alt="ex1-5"></img>

***

해당 소스는 아래 사이트를 참조

[소스주소(github): 실시간 가상자산 트레이딩 만들기](https://github.com/miso07/PythonBook)
