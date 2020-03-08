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


def GetDataSavetoMysql(statusflag):
    while True:
            
            lastballnum = GetLastIDFromTable('xyft')
            ballnum,daynum,today_num = GetIDAccordingCurentTime()

            #print(ballnum,lastballnum)
                        
            if(ballnum > lastballnum):
                SaveDatatoMysql(ballnum,daynum,today_num,lastballnum)
                numberdiff = ballnum - lastballnum
                if(numberdiff > 3):
                    ContinueCheck(lastballnum,ballnum,"xyft") # added by zhoumb 2020020


            waitingtime = GetWaitingTime()
            print('%d seconds waiting for new data....' %waitingtime)
            time.sleep(waitingtime) 


def UpdateSeriesDisplay(statusflag):
    while True:
            ballnum = GetLastIDFromTable('xyft')
            firstID = GetLastIDFromTable('xyftrd')
            updateflag = 0
            if(ballnum >firstID):
                rdUpdate(firstID,ballnum)
                firstID = GetLastIDFromTable('xyftpi')
                piUpdate(firstID,ballnum)
                updateflag = 1
            
            if(updateflag == 1):
                waitingtime = GetWaitingTime()
                print('%d seconds waiting for series update....v20200308' %waitingtime)
            else:
                waitingtime = 30
                print('Data not update, %d seconds waiting')
            time.sleep(waitingtime) 


def main():
    """创建启动线程"""
    t_get_save = threading.Thread(target=GetDataSavetoMysql, args=(1,))
    t_update = threading.Thread(target=UpdateSeriesDisplay, args=(1, ))
    t_get_save.start()
    t_update.start()


if __name__ == '__main__':
    main()
