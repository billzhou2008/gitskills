8# -*- coding: UTF-8 -*-
#-*-author by Zhoumb 2018-----------------------

from xyftsub import SaveDatatoMysql
from xyftsub import GetLastIDFromTable
from xyftsub import GetIDAccordingCurentTime
from xyftsub import rdUpdate
from xyftsub import piUpdate
from xyftsub import GetWaitingTime
from xyftsub import piLatestDataDisp #zhoumb180723
from xyftsub import ContinueCheck # added by zhoumb 20200201

import time


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
 

