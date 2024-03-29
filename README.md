# CBNU Raspberry Pi Group Repository

> **&laquo;본인 행적 좀 적어주새오...&raquo;**


## Socket Project (2020/12~)

### 최근 추가
  * 최지문
    * 2021.01.25: Command.py 추가
    * 2021.01.28: 최지문 왔다감
    * 2021.02.05: 벌써 2
    * 2021.02.06: Test_Client 추가
    * 2021.02.09: Test_Client psuh 기능추가 (테스트 안함)
    * 2021.02.11: Test_Client GUi 버전 추가 (기능 구현중)
    * 2021.02.16: work.py에서 list_f가 확장자끼리 묶지않고 그냥 나오게 변경
    * 2021.02.18: log_Text_Client 추가 로그인 부분 추가한 버전
    * 2021.02.21: Recv.py  ,Commmand.py 파일을 보내거나 받을때 마지막 상대의 디렉토리현황을 확일할수 있게함
    * 2021.02.21: clientgui 최신 업데이트
    * 2021.02.21: client.py 최신 업데이트 
                * infinite_loof_sever.py 무한으로 안돌던 오류수정
                * commmand.py , send.py 변경된 서버에 맞게 구문수정
    * 2021.02.26: Clientgui_Manual 추가 
  * 이정호
    * 2021.01.25: Send.py 추가
    * 2021.01.25: 폴더 정리
    * 2021.02.05: Identification.py 추가
    * 2021.02.16: C++버전 클라이언트 수정, Txt 받기 성공
    * 2021.02.17: C++ 클라이언트 이미지 받기 작업중
    * 2021.02.18: Identification.py 수정
    * 2021.02.23: Logging.py 파일 추가, 서버로깅 기능 
  * 황지현
    * 2021.02.15: client register.py add
    * 2021.02.16: client register.py 
    * 2021.02.19: client infinit roof of login and registor add
    * 2021.02.19: server infinit roof of login and registor (with 2.5)
    * 2021.02.20: infinite_loof_server.py revise
    * 2021.02.20: infinite infinite_registor_and_login_with_client.py revise
  * 고민성
    * 2021.02.05: Recv.py 수정
    * 2021.02.09: 고민성 왔다감, recv.py 수정
    * 2021.02.15: recv.py 이미지 수신부분 수정
    * 2021.02.18: recv.py 텍스트 부분(null문자 encode수정), 수신하는데 걸리는 시간 및 데이터 용량 표시
    * 2021.02.21: recv.py와 work 모듈 합치는 과정 속 오류 수정, recv.py 데이터 용량 표기 오류 수정
    * 2021.02.23: recv.py와 send.py에 바이너리파일(mp3,mp4,avi) 송수신 가능 추가
      work.py,commmand.py,client.py에서 바이너리파일 인식하게 수정(클라이언트 gui 버전 수정해야합니다)
      recv.py 주석 추가
    * 2021.02.28  commmand.py, send.py recv.py 변경된 클라이언트에 맞게 수정
    * 2021.03.01 commmand.py, send.py recv.py,client.py 이미지 송수신 부분 바이너리 송수신부분으로 대체가능하고 전송속도 및 통일성을 위해 주석처리    
   
      
### 진행상황
  * 2021.02.18: 
    * 클라이언트와 서버가 서로 이미지, 텍스트 파일 주고받기 성공
    * 서버,클라이언트 로그인 기능 구현중 (서로 통신되는것 확인) 
  * 2021.02.21:
    * clientgui 최초버전 완성
     * 로그인기능 구현
     * 파일 업로드 ,다운로드 가능
     * 클라이언트 gui화 완료
     * 서버무한가동 구현
  * 2021.02.24:
     * 서버무한가동중 작동중지하는 오류 수정
     * pull ,push 과정에서 이미 존재하는 파일이있으면 서버가 정지하는 현상 수정    

### 필요모듈
  *  PIL
  *  PyQt5
  *  Cryptography
  

### 작업환경
  * Window
  * Python3.7+
  * vscode

### 추가예정 기능
  * 서버로깅
  * 서버무한가동 (완료) 
  * 로그인 기능 (완료) 
  * 클라이언트 gui화 (완료)
 
