# -*- coding: UTF-8 -*-
#-*-author by Zhoumb 2018-----------------------

from xyftsub import SaveDatatoMysql
from xyftsub import GetLastIDFromTable
from xyftsub import GetIDAccordingCurentTime
from xyftsub import rdUpdate
from xyftsub import piUpdate
from xyftsub import GetWaitingTime
from xyftsub import piLatestDataDisp #zhoumb180723
from xyftsub import ContinueCheck # added by zhoumb 20200201

import threading
import time


def sing(num):
    for i in range(num):
        print("sing%d" % i)
        time.sleep(0.5)


def dance(num):
    for i in range(num):
        print("dancing%d" % i)
        time.sleep(0.5)


def main():
    """创建启动线程"""
    t_sing = threading.Thread(target=sing, args=(5,))
    t_dance = threading.Thread(target=dance, args=(6, ))
    t_sing.start()
    t_dance.start()


if __name__ == '__main__':
    main()


if __name__ == "__main__":

    while True:
            
            lastballnum = GetLastIDFromTable('xyft')
            ballnum,daynum,today_num = GetIDAccordingCurentTime()

            #print(ballnum,lastballnum)
            
            
            if(ballnum > lastballnum):
                SaveDatatoMysql(ballnum,daynum,today_num,lastballnum)
                numberdiff = ballnum - lastballnum
                if(numberdiff > 3):
                    ContinueCheck(lastballnum,ballnum,"xyft") # added by zhoumb 2020020
            else:
                firstID = GetLastIDFromTable('xyftrd')
                if(ballnum >firstID):
                    rdUpdate(firstID,ballnum)

                firstID = GetLastIDFromTable('xyftpi')
                piUpdate(firstID,ballnum)

                waitingtime = GetWaitingTime()
                print('%d seconds waiting for new data....' %waitingtime)
                time.sleep(waitingtime)     