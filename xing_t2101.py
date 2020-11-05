import win32com.client
import pythoncom

import xing_login
import win32com


class XQuery_t2101:
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
        name  = self.GetFieldData("t2101OutBlock", "hname", 0)
        price = self.GetFieldData("t2101OutBlock", "price", 0)
        change= self.GetFieldData("t2101OutBlock", "change", 0)
        volume= self.GetFieldData("t2101OutBlock", "volume", 0)
        print("종목; {0}".format(name))
        print("현재가; {0}".format(price))
        print("전일대비; {0}".format(change))
        print("누적거래량; {0}".format(volume))

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


if __name__ == "__main__":
    def get_single_data():
        xq_t2101 = XQuery_t2101.get_instance()
        xq_t2101.single_request("101QC000") # 선물20년12월물

        while xq_t2101.is_data_received == False:
            pythoncom.PumpWaitingMessages()


    xsession = xing_login.XSession.get_instance()
    xsession.api_login(id="myid", pwd="pass", cert_pwd="pass2")

    get_single_data()
