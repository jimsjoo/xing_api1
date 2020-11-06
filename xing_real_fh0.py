# 호가조회 및 GASP 실시간 계산
import win32com.client
import pythoncom
import time
import xing_login
import win32com
import gasp

class XQuery_t2105:
    """
    classmethod get_instance() 를 사용하여, instance 를 만들어야함.
    """
    def __init__(self):
        self.is_data_received = False

    def OnReceiveData(self, tr_code):  # event handler
        """
        이베스트 서버에서 ReceiveData 이벤트 받으면 실행되는 event handler
        """
        self.is_data_received = True
        ttime = self.GetFieldData("t2105OutBlock", "time", 0)
        hname = self.GetFieldData("t2105OutBlock", "hname", 0)
        scode = self.GetFieldData("t2105OutBlock", "shcode", 0)
        price = self.GetFieldData("t2105OutBlock", "price", 0)
        change= self.GetFieldData("t2105OutBlock", "change", 0)
        diff  = self.GetFieldData("t2105OutBlock", "diff", 0)
        volume= self.GetFieldData("t2105OutBlock", "volume", 0)
        print("시간: {0}, 종목: {1}({2}), 현재가: {3}, 전일대비: {4}, 등락율: {5}, 누적거래량: {6}".format(ttime, hname, scode, price, change, diff, volume))      
        for i in range(1, 6):  # 1~5
            offerho = self.GetFieldData("t2105OutBlock", "offerho"+str(i), 0)
            bidho   = self.GetFieldData("t2105OutBlock", "bidho"+str(i), 0)
            offerem = self.GetFieldData("t2105OutBlock", "offerrem"+str(i), 0)
            bidrem  = self.GetFieldData("t2105OutBlock", "bidrem"+str(i), 0)
            dcnt    = self.GetFieldData("t2105OutBlock", "dcnt"+str(i), 0)
            scnt    = self.GetFieldData("t2105OutBlock", "scnt"+str(i), 0)
            print("호가#{0}, 매도: {1}, 매수: {2}, 매수잔량: {3}, 매도잔량: {4}, 매수건수: {5}, 매도건수: {6}".format(i, offerho, bidho, offerem, bidrem, dcnt, scnt))      

        dvol = self.GetFieldData("t2105OutBlock", "dvol", 0)
        svol = self.GetFieldData("t2105OutBlock", "svol", 0)   
        toffernum = self.GetFieldData("t2105OutBlock", "toffernum", 0)   
        tbidnum = self.GetFieldData("t2105OutBlock", "tbidnum", 0)   
        print("매도총수량: {0}, 매수총수량: {1},  매도건수합: {2}, 매수건수합: {3}".format(dvol, svol, toffernum, tbidnum))      
        print("tr code ==> {0}".format(tr_code))

    def single_request(self, shcode):
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t2105.res"  # RES 파일 등록
        self.SetFieldData("t2105InBlock", "shcode", 0, shcode)  # 종목코드 설정
        err_code = self.Request(False)  # data 요청하기 --  연속조회인경우만 True

        if err_code < 0:
            print("error... {0}".format(err_code))

    @classmethod
    def get_instance(cls):
        # DispatchWithEvents로 instance 생성하기
        xq_t2105 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", cls)
        return xq_t2105

class XReal_FH0_:
    def __init__(self):
        super().__init__()
        self.count = 0

    def OnReceiveRealData(self, tr_code):  # event handler
        """
        이베스트 서버에서 ReceiveRealData 이벤트 받으면 실행되는 event handler
          order_book = {
            'bids': [
                [97, 0.1],
                [96, 0.2],
                [95, 6]
            ],
            'asks': [
                [98, 4],
                [99, 4.6],
                [100, 4.8],
            ]
          }
        """        
        self.count += 1
        hotime = self.GetFieldData("OutBlock", "hotime")
        bids=[]
        asks=[]
        for i in range(1, 6):  # 1~5
            offerho = float(self.GetFieldData("OutBlock", "offerho"+str(i)))
            bidho   = float(self.GetFieldData("OutBlock", "bidho"+str(i)))
            offerem = float(self.GetFieldData("OutBlock", "offerrem"+str(i)))
            bidrem  = float(self.GetFieldData("OutBlock", "bidrem"+str(i)))      
            bids.append([bidho, bidrem])
            asks.append([offerho, offerem])                        
            # print(i, '[', bidho,  ',', bidrem, '] [', offerho, ',', offerem,']')
            # print("시간#{0}, 매도: {1}, 매수: {2}, 매도잔량: {3}, 매수잔량: {4}".format(hotime, offerho, bidho, offerem, bidrem))      
        order_book ={'bids':bids,'asks':asks}
        gasp_value = gasp.calculate_gasp(order_book)
        # totofferrem = self.GetFieldData("OutBlock", "totofferrem")
        # totbidrem   = self.GetFieldData("OutBlock", "totbidrem")
        # print("매도총수량: {0}, 매수총수량: {1}".format(totofferrem, totbidrem))      
        print('시간#{0}, GASP: {1}', hotime, gasp_value)
        print(".... 실시간 TR code => {0}".format(tr_code))

    def start(self, futcode):
        """
        이베스트 서버에 실시간 data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\FH0.res"  # RES 파일 등록
        self.SetFieldData("InBlock", "futcode", futcode)
        self.AdviseRealData()   # 실시간데이터 요청


    def add_item(self, futcode):
        # 실시간데이터 요청 종목 추가
        self.SetFieldData("InBlock", "futcode", futcode)
        self.AdviseRealData()

    def remove_item(self, futcode):
        # futcode 종목만 실시간데이터 요청 취소
        self.UnadviseRealDataWithKey(futcode)

    def end(self):
        self.UnadviseRealData()  # 실시간데이터 요청 모두 취소

    @classmethod
    def get_instance(cls):
        xreal = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", cls)        
        return xreal

if __name__ == "__main__":
    def get_single_data():
        xq_t2105 = XQuery_t2105.get_instance()
        xq_t2105.single_request("101QC000") # 선물20년12월물

        while xq_t2105.is_data_received == False:
            pythoncom.PumpWaitingMessages()

    def get_real_data():
        xreal = XReal_FH0_.get_instance()
        xreal.start("101QC000")
        
        while xreal.count < 100:
          pythoncom.PumpWaitingMessages()            
          if xreal.count == 5:
              xreal.end()  # 실시간 조회 중단.
              time.sleep(5)
              print("---- end -----")
              break

    xsession = xing_login.XSession.get_instance()
    xsession.api_login(id="myid", pwd="pass", cert_pwd="pass2")
    get_single_data()
    get_real_data()