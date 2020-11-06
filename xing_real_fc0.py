import win32com.client
import pythoncom
import time
import xing_login
import win32com


class XQuery_t2101:
    """
    classmethod get_instance() 를 사용하여, instance 를 만들어야함.
    """
    def __init__(self):
        super().__init__()
        self.is_data_received = False

    def OnReceiveData(self, tr_code):  # event handler
        """
        이베스트 서버에서 ReceiveData 이벤트 받으면 실행되는 event handler
        """
        self.is_data_received = True
        hname = self.GetFieldData("t2101OutBlock", "hname", 0)
        price = self.GetFieldData("t2101OutBlock", "price", 0)
        change= self.GetFieldData("t2101OutBlock", "change", 0)
        volume= self.GetFieldData("t2101OutBlock", "volume", 0)
        print("종목: {0}, 현재가: {1}, 전일대비: {2}, 누적거래량: {3}".format(hname, price, change, volume))              

        print("tr code ==> {0}".format(tr_code))

    def single_request(self, focode):
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t2101.res"  # RES 파일 등록
        self.SetFieldData("t2101InBlock", "focode", 0, focode)  # 종목코드 설정
        err_code = self.Request(False)  # data 요청하기 --  연속조회인경우만 True

        if err_code < 0:
            print("error... {0}".format(err_code))

    @classmethod
    def get_instance(cls):
        # DispatchWithEvents로 instance 생성하기
        xq_t2101 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", cls)
        return xq_t2101

class XReal_FC0_:
    def __init__(self):
        super().__init__()
        self.count = 0

    def OnReceiveRealData(self, tr_code):  # event handler
        """
        이베스트 서버에서 ReceiveRealData 이벤트 받으면 실행되는 event handler
        """
        self.count += 1
        price  = self.GetFieldData("OutBlock", "price")  # 현재가
        change = self.GetFieldData("OutBlock", "change") # 등락율        
        drate  = self.GetFieldData("OutBlock", "drate")  # 전일대비
        volume = self.GetFieldData("OutBlock", "volume") # 누적거래량

        print(self.count, price, change, drate, volume)
        print(".... 실시간 TR code => {0}".format(tr_code))

    def start(self, futcode):
        """
        이베스트 서버에 실시간 data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\FC0.res"  # RES 파일 등록
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
        xq_t2101 = XQuery_t2101.get_instance()
        xq_t2101.single_request("101QC000") # 선물20년12월물

        while xq_t2101.is_data_received == False:
            pythoncom.PumpWaitingMessages()

    def get_real_data():
        xreal = XReal_FC0_.get_instance()
        xreal.start("101QC000")

        while xreal.count < 100:
            pythoncom.PumpWaitingMessages()            

            if xreal.count == 30:
                xreal.end()  # 실시간 조회 중단.
                time.sleep(10)
                print("---- end -----")
                break

    xsession = xing_login.XSession.get_instance()
    xsession.api_login(id="myid", pwd="pass", cert_pwd="pass2")

    get_single_data()
    get_real_data()
