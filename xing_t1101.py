import win32com.client
import pythoncom

import xing_login
import win32com


class XQuery_t1101:
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
        name = self.GetFieldData("t1101OutBlock", "hname", 0)
        price = self.GetFieldData("t1101OutBlock", "price", 0)
        volume = self.GetFieldData("t1101OutBlock", "volume", 0)
        print("종목; {0}".format(name))
        print("현재가; {0}".format(price))
        print("누적거래량; {0}".format(volume))

        print("tr code ==> {0}".format(tr_code))

    def single_request(self, stockcode):
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t1101.res"  # RES 파일 등록
        self.SetFieldData("t1101InBlock", "shcode", 0, stockcode)  # 종목코드 설정
        err_code = self.Request(False)  # data 요청하기 --  연속조회인경우만 True

        if err_code < 0:
            print("error... {0}".format(err_code))

    @classmethod
    def get_instance(cls):
        # DispatchWithEvents로 instance 생성하기
        xq_t1101 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", cls)
        return xq_t1101


if __name__ == "__main__":
    def get_single_data():
        xq_t1101 = XQuery_t1101.get_instance()
        xq_t1101.single_request("005930") # 삼성전자.

        while xq_t1101.is_data_received == False:
            pythoncom.PumpWaitingMessages()


    xsession = xing_login.XSession.get_instance()
    xsession.api_login()

    get_single_data()
