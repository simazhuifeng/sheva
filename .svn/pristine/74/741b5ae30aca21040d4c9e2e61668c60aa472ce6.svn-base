# coding: utf8
'''
Created on 2014-5-25

@author: sheva.wen
'''
import unittest
import re
import datetime


class Test(unittest.TestCase):
    

    def testName(self):
        source = u'车辆所有人、驾驶人:号牌号码为蒙AAR757的小型汽车于2014年05月14日在内蒙古自治区包头市固阳县X1081(包固一级公路）11公里 100米，实施了驾驶中型以上载客载货汽车、校车、危险物品运输车辆以外的其他机动车行驶超过规定时速20%以上未达到50%的的违法行为，违反了《中华人民共和国道路交通安全法》第四十二条、《中华人民共和国道路交通安全法实施条例》第四十五条、第四十六条，《中华人民共和国道路交通安全法》第九十条,《内蒙古自治区实施<中华人民共和国道路交通安全法>办法》第六十六条之规定，拟处以200元罚款，记6分。如有异议，可申请复核。呼和浩特市公安局交通管理支队<br>2、车辆所有人、驾驶人:号牌号码为蒙AAR757的小型汽车于2014年05月03日在内蒙古自治区呼和浩特市大学东街与丰州路，实施了机动车通过有灯控路口时，不按所需行进方向驶入导向车道的 的违法行为，违反了《中华人民共和国道路交通安全法实施条例》第五十一条第一项，《中华人民共和国道路交通安全法》第九十条，《内蒙古自治区实施<中华人民共和国道路交通安全法>办法》第五十九条第一项之规定，拟处以100元罚款，记2分。如有异议，可申请复核。呼和浩特市公安局交通管理支队'.encode('utf8')
        regex = ur"\d+年\d+月\d+日".encode('utf8')
        p = re.compile(regex)
        m = p.search(source)
        print m.group(0)
        print str(datetime.datetime.strptime(m.group(0), u"%Y年%m月%d日"))
        self.assertEqual("", "", "msg")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()