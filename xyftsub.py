# -*- coding: UTF-8 -*--------------------------
#-*-author by Zhoumb 2018-----------------------

import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import urllib
import time
import datetime
import string
import xlrd #读写EXCEL2003
import xlwt
from xlutils.copy import copy
import os
import random

import pymysql #操作mysql数据库


def GetLastIDFromTable(tableName):  #获得最后一天记录 zhoumb2018061      

        # 打开数据库连接
        db = pymysql.connect("localhost","root","zhoumb1202","luckyairship" )
 
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        try :  
            
            sql = "SELECT ID FROM %s order by ID desc limit 1 "  
            cursor.execute(sql %tableName)  
            result = cursor.fetchall()
            for row in result:
                    lastID = row[0]
            #print(lastID)
    
        except Exception as err:  
            print("DBERR数据库查询单条记录失败03： \n[%s]" % (err))  
            exit()

        db.close

        print("获取最后一个ID成功", tableName)
        return(lastID)

 
def GetNextDayballnum(ballnum):
        year = ballnum//10000000
        month = ballnum%10000000
        month  = month//100000
        day = ballnum%100000
        day = day//1000

        date = datetime.date(year, month, day)
        date = date + datetime.timedelta(1)

        ballnum  = date.year*10000000 + date.month*100000 + date.day*1000 + 1

        return (ballnum)

def GetIDAccordingCurentTime(): #从当前时间获取xyft当前期数 zhoumb201800809

        timedelta_temp = datetime.timedelta(seconds=0, minutes=4, hours=13) #以下一段程序，根据当前时间获取当前期号
        now = datetime.datetime.now()
        time_delta = now - timedelta_temp
        minutediff = time_delta.hour * 60 + time_delta.minute
        ballnum = minutediff//5
        #print("minutediff,ballnum",minutediff,ballnum)
        #print("time_delta",time_delta)

        today_num = ballnum
        if ballnum ==0:
            today_num = 180
            time_delta -= datetime.timedelta(1)
            ballnum  = time_delta.year*10000000 + time_delta.month*100000 + time_delta.day*1000 + 180 # set last number
        else:
            if ballnum > 180:
                today_num = 180
                ballnum  = time_delta.year*10000000 + time_delta.month*100000 + time_delta.day*1000 + 180 # set last number
            else:
                ballnum  = time_delta.year*10000000 + time_delta.month*100000 + time_delta.day*1000 + ballnum

        daynum = time_delta.year*10000 + time_delta.month*100 + time_delta.day   #当前期年月日
        if(today_num > 131):                                                     #>131在下一天数据中
            daynum = GetNextDaynum(daynum)

        #print(ballnum,daynum,today_num)

        return(ballnum,daynum,today_num)

def GetNextDaynum(daynum):              #zhoumb20180809
    year = daynum//10000
    month = daynum%10000
    month = month//100
    day = daynum%100
    date = datetime.date(year, month, day)
    date = date + datetime.timedelta(1)

    daynum = date.year*10000 + date.month*100 + date.day

    return(daynum)

def GetPriDaynum(daynum):              #zhoumb20181012
    year = daynum//10000
    month = daynum%10000
    month = month//100
    day = daynum%100
    date = datetime.date(year, month, day)
    date = date - datetime.timedelta(1)

    daynum = date.year*10000 + date.month*100 + date.day

    return(daynum)

def DatatoMysqlExe(checkball,daynum,numbers): #add check ball by zhoumb20181022
    
        #url = 'http://api.caipiaokong.cn/lottery/?name=xyft&format=json&uid=698146&token=1b9699513be7adfd28cc6e6d9a78ed9f87eb95b6' #test

        daystr = '&date='+str(daynum)
        url = 'http://api.caipiaokong.cn/lottery/?name=xyft&format=json'
        url += daystr
        url += '&uid=698146&token=1b9699513be7adfd28cc6e6d9a78ed9f87eb95b6'
        #print(url)

        trytimes = 10
        for i in range(trytimes):
                try:
                        header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
                        html=requests.get(url,headers = header)  
                        html.raise_for_status()
                except requests.RequestException as e:#处理异常
                        print(e)
                        print('等1秒')
                        time.sleep(1)
                                
                else:
                        soup = BeautifulSoup(html.text,'html.parser')
                        soup = str(soup) #将网页文本转换成字符串
                        wn_pk10 = re.compile(r'"(.*?)"')
                        names = re.findall(wn_pk10,soup)
                        wn_one_str = ','.join(names)
                firstwn = wn_one_str[0:11]
                if(firstwn == str(checkball)):
                        print('Get Data success')
                        break;
                else:
                        print('Get Data failed, wating 20 seconds')
                        time.sleep(20)
                

            
        # 打开数据库连接
        db = pymysql.connect("localhost","root","zhoumb1202","luckyairship" )
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
    
        offset = 0
        for i in range(numbers):
            offset = i*78
                    
            cwn_num = int(wn_one_str[offset+0:offset+11])
            cfirst  = int(wn_one_str[offset+19:offset+21])
            csecond = int(wn_one_str[offset+22:offset+24])
            cthird = int(wn_one_str[offset+25:offset+27])
            cfourth = int(wn_one_str[offset+28:offset+30])
            cfifth = int(wn_one_str[offset+31:offset+33])
            csixth = int(wn_one_str[offset+34:offset+36])
            cseventh = int(wn_one_str[offset+37:offset+39])
            ceighth = int(wn_one_str[offset+40:offset+42])
            cnineth = int(wn_one_str[offset+43:offset+45])
            ctenth = int(wn_one_str[offset+46:offset+48])
            ccdate = wn_one_str[offset+58:offset+68]
            cctime = wn_one_str[offset+69:offset+77]

            print(cwn_num,cfirst,csecond,cthird,cfourth,cfifth,csixth,cseventh,ceighth,cnineth,ctenth,ccdate,cctime)        
            # SQL 插入语句
            insert_data = ("INSERT INTO xyft(ID,F1,S2,T3,F4,F5,S6,S7,E8,N9,T10)"
                       "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            pk10_data = (cwn_num,cfirst,csecond,cthird,cfourth,cfifth,csixth,cseventh,ceighth,cnineth,ctenth)
            try:
                   # 执行sql语句
                   cursor.execute(insert_data,pk10_data)
                   # 提交到数据库执行
                   db.commit()
            except:
                   # 如果发生错误则回滚
                   db.rollback()
                   print('数据库更新失败')        

        db.close
def SaveDatatoMysql(ballnum,daynum,today_num,lastballnum):

        lastdaynum = lastballnum//1000 #最后一期年月日
        last_num = lastballnum%1000
        daysrange = 365
        lastID = GetLastIDFromTable('xyft')
        
        for i in range(daysrange):
            
            timedelta_temp = datetime.timedelta(seconds=0, minutes=0, hours=0,days=i)
            now = datetime.datetime.now()
            time_delta = now - timedelta_temp        
            #print(time_delta)
            daynum = time_delta.year*10000 + time_delta.month*100 + time_delta.day

            daystr = '&date='+str(daynum)
            url = 'http://api.caipiaokong.cn/lottery/?name=xyft&format=json'
            url += daystr
            url += '&uid=698146&token=1b9699513be7adfd28cc6e6d9a78ed9f87eb95b6'

            print(url)

            GetAndSave(url,lastID)

            if daynum == lastdaynum:
                break;
            time.sleep(6)

 
def GetAndSave(url,lastID):
        
        trytimes = 3
        for i in range(trytimes):
                try:
                        header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
                        html=requests.get(url,headers = header)  
                        html.raise_for_status()
                except requests.RequestException as e:#处理异常
                        print(e)
                        print('等3秒')
                        time.sleep(3)
                                
                else:
                        soup = BeautifulSoup(html.text,'html.parser')
                        soup = str(soup) #将网页文本转换成字符串
                        wn_pk10 = re.compile(r'"(.*?)"')
                        names = re.findall(wn_pk10,soup)
                        wn_one_str = ','.join(names)


                if len(wn_one_str) > 0:
                        #print(wn_one_str)
                        print('Get Data success')
                        wn_one_str_lenth = len(wn_one_str) + 1
                        readnums = wn_one_str_lenth//78
                        print(readnums)
                        if readnums == 0:
                            print('Get blank data')
                            print('等30秒')
                            time.sleep(30)
                        
                        break;
                else:
                        print('Get Data failed')
                        print('等5秒')
                        time.sleep(6)


        # 打开数据库连接
        db = pymysql.connect("localhost","root","zhoumb1202","luckyairship" )
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
    
        offset = 0
        for i in range(readnums):
            offset = i*78
                    
            cwn_num = int(wn_one_str[offset+0:offset+11])
            cfirst  = int(wn_one_str[offset+19:offset+21])
            csecond = int(wn_one_str[offset+22:offset+24])
            cthird = int(wn_one_str[offset+25:offset+27])
            cfourth = int(wn_one_str[offset+28:offset+30])
            cfifth = int(wn_one_str[offset+31:offset+33])
            csixth = int(wn_one_str[offset+34:offset+36])
            cseventh = int(wn_one_str[offset+37:offset+39])
            ceighth = int(wn_one_str[offset+40:offset+42])
            cnineth = int(wn_one_str[offset+43:offset+45])
            ctenth = int(wn_one_str[offset+46:offset+48])
            ccdate = wn_one_str[offset+58:offset+68]
            cctime = wn_one_str[offset+69:offset+77]

            print(cwn_num,cfirst,csecond,cthird,cfourth,cfifth,csixth,cseventh,ceighth,cnineth,ctenth,ccdate,cctime)        
            if cwn_num == lastID or cwn_num < lastID:
                print("数据库更新完成") 
                break;
            # SQL 插入语句
            insert_data = ("INSERT INTO xyft(ID,F1,S2,T3,F4,F5,S6,S7,E8,N9,T10)"
                       "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            pk10_data = (cwn_num,cfirst,csecond,cthird,cfourth,cfifth,csixth,cseventh,ceighth,cnineth,ctenth)
            try:
                   # 执行sql语句
                   cursor.execute(insert_data,pk10_data)
                   # 提交到数据库执行
                   db.commit()
            except:
                   # 如果发生错误则回滚
                   db.rollback()
                   print('数据库更新失败')        

        db.close

        return(1)
        #print("从网上获取一天数据写入xyft表成功")

def ContinueCheck(firstID,lastID,tableName):  #连续性检查 zhoumb20200131      

        continueflag = 1

        # 打开数据库连接
        db = pymysql.connect("localhost","root","zhoumb1202","luckyairship" )
 
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        currentID = firstID
        trytimes = lastID - firstID

        for i in range(trytimes):
            
            #sql = "SELECT ID FROM %s order by ID desc limit 1 "  
            sql = "select * from %s where id > %d order by id asc limit 1"
            cursor.execute(sql %(tableName,currentID))  
            result = cursor.fetchall()
            for row in result:
                    nextID = row[0]
            
            if(nextID == lastID): #最后一个ID检查完成，终止循环 zhoumb20200210
                    db.close
                    print("Continue checked",firstID,lastID,tableName)
                    break

            nextcheckID = currentID + 1
            temp = nextcheckID%1000
            if temp > 180: 
                nextcheckID = GetNextDayballnum(currentID)  
            
            if(nextID == nextcheckID):
                continueflag = 1
            else:
                continueflag = 0
                cwn_num = nextcheckID
                nextID = cwn_num
                cfirst  = 2
                csecond = 3
                cthird = 4
                cfourth = 5
                cfifth = 6
                csixth = 7
                cseventh = 8
                ceighth = 9
                cnineth = 10
                ctenth = 1
                insert_data = ("INSERT INTO xyft(ID,F1,S2,T3,F4,F5,S6,S7,E8,N9,T10)"
                               "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                pk10_data = (cwn_num,cfirst,csecond,cthird,cfourth,cfifth,csixth,cseventh,ceighth,cnineth,ctenth)
                try:
                    # 执行sql语句
                    cursor.execute(insert_data,pk10_data)
                    # 提交到数据库执行
                    db.commit()
                    print("add a lost record", nextID)
                except:
                    # 如果发生错误则回滚
                    db.rollback()
                    print('数据库更新失败')   
            print(nextID,continueflag)

            currentID = nextID

        db.close

        return(1)
        
def SaveDatatoMysqlbak20191210(ballnum,daynum,today_num,lastballnum):

        lastdaynum = lastballnum//1000 #最后一期年月日
        last_num = lastballnum%1000
        if(last_num>130):
            lastdaynum = GetNextDaynum(lastdaynum)

        print(last_num,lastdaynum,ballnum,daynum,today_num)

        checkball = ballnum #add check ball by zhoumb20181022

        if(daynum > lastdaynum): # read many days by zhoumb20181012
                numbers = today_num - 131
                if numbers < 0:
                        numbers += 180
                DatatoMysqlExe(checkball,daynum,numbers) #add check ball by zhoumb20181022
                print('5 seconds waiting for new data....')
                time.sleep(5)

                loop = True
                while loop:
                        daynum = GetPriDaynum(daynum)
                        checkball = daynum*1000 + 131 #add check ball by zhoumb20181022
                        if(daynum > lastdaynum):
                                numbers = 180
                                DatatoMysqlExe(checkball,daynum,numbers) #add check ball by zhoumb20181022
                                print('5 seconds waiting for new data....')
                                time.sleep(5)
                        else:
                                loop = False
                                numbers = 131 - last_num
                                if numbers < 0:
                                        numbers += 180
                                DatatoMysqlExe(checkball,daynum,numbers) #add check ball by zhoumb20181022
                                break
                                        
                
        else: #read today(one day) by zhoumb20181012
                numbers = today_num - last_num
                if numbers < 0:
                        numbers  += 180
                        
                print(daynum,numbers)
                DatatoMysqlExe(checkball,daynum,numbers) #add check ball by zhoumb20181022

 
#-------------------------end of SaveDatatoMysql-------------------zhoumb20180618


def BigJudge(number,refnum,big):
    if (number > refnum):
        if big > 0: big = big+1
        else: big = 1
    else:
        if big > 0: big = -1
        else: big = big-1
    return big    

def EvenJudge(number,even):
    if number%2 > 0:
        if even > 0: even = even+1
        else: even = 1
    else:
        if even > 0: even = -1
        else: even = even-1
    return even        

def DTJudge(num1,num2,numDT):
    if (num1>num2):
        if numDT > 0: numDT = numDT+1
        else: numDT = 1
    else:
        if numDT > 0: numDT = -1
        else: numDT = numDT-1
    return numDT

def GetDateFromID(ID):
        
        temp = ID//10000000
        year = temp

        temp = ID%10000000
        temp = temp//100000
        month =  temp

        temp = ID%100000
        day = temp//1000

        number = ID%1000

        date = datetime.date(year, month, day)
        if number > 131:
                date = date + datetime.timedelta(1)                


        return(date)
    
def GetTimeFromID(ID):
        hour = 13      #初始化时间
        mininute = 4
        second = 0

        temp = ID%1000
        temp = temp*5 + 4

        hour = hour + temp//60
        if hour > 23:
                hour = hour -24
                
        minute = temp%60
        ctime = datetime.time(hour,minute,second)

        return(ctime)

def CalulateFirstIDForxyftrd(firstnumber):
# 打开数据库连接
        db = pymysql.connect("localhost","root","zhoumb1202","luckyairship" )
 
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        #获取原始数据指定行数据
        try :  
            tableName = 'xyft'            
            sql = "SELECT * FROM %s WHERE ID = %d LIMIT 1"  
            cursor.execute(sql %(tableName,int(firstnumber)))  
            result = cursor.fetchall()            
            for row in result:
                num = row[0]
                F1 = row[1]
                S2 = row[2]
                T3 = row[3]
                F4 = row[4]
                F5 = row[5]
                S6 = row[6]
                S7 = row[7]
                E8 = row[8]
                N9 = row[9]
                T10 = row[10]

                print(num,F1,S2,T3,F4,F5,S6,S7,E8,N9,T10)         
        except Exception as err:  
            print("DBERR数据库查询单条记录失败01： \n[%s]" % (err))  
            exit()

        
        ID = firstnumber

        CSSUM = F1+S2
        CSBIG = BigJudge(CSSUM,11,0)
        CSEVEN = EvenJudge(CSSUM,0)

        F1BIG = BigJudge(F1,5,0)
        F1EVEN = EvenJudge(F1,0)
        F1DT = DTJudge(F1,T10,0)

        S2BIG = BigJudge(S2,5,0)
        S2EVEN = EvenJudge(S2,0)
        S2DT = DTJudge(S2,N9,0)

        T3BIG = BigJudge(T3,5,0)
        T3EVEN = EvenJudge(T3,0)
        T3DT = DTJudge(T3,E8,0)

        F4BIG = BigJudge(F4,5,0)
        F4EVEN = EvenJudge(F4,0)
        F4DT = DTJudge(F4,S7,0)

        F5BIG = BigJudge(F5,5,0)
        F5EVEN = EvenJudge(F5,0)
        F5DT = DTJudge(F5,S6,0)

        S6BIG = BigJudge(S6,5,0)
        S6EVEN = EvenJudge(S6,0)
        S7BIG = BigJudge(S7,5,0)
        S7EVEN = EvenJudge(S7,0)
        E8BIG = BigJudge(E8,5,0)
        E8EVEN = EvenJudge(E8,0)
        N9BIG = BigJudge(N9,5,0)
        N9EVEN = EvenJudge(N9,0)
        T10BIG = BigJudge(T10,5,0)
        T10EVEN = EvenJudge(T10,0)
        CDATE = GetDateFromID(ID)
        CTIME = GetTimeFromID(ID)


        ORFLAG = max(abs(CSBIG),abs(CSEVEN),abs(F1BIG),abs(F1EVEN),abs(F1DT),abs(S2BIG),abs(S2EVEN),abs(S2DT),abs(T3BIG),abs(T3EVEN),abs(T3DT),abs(F4BIG),abs(F4EVEN),abs(F4DT),abs(F5BIG),abs(F5EVEN),abs(F5DT),
                      abs(S6BIG),abs(S6EVEN),abs(S7BIG),abs(S7EVEN),abs(E8BIG),abs(E8EVEN),abs(N9BIG),abs(N9EVEN),abs(T10BIG),abs(T10EVEN))
        print(ID,CSSUM,CSBIG,CSEVEN,F1BIG,F1EVEN,F1DT,S2BIG,S2EVEN,S2DT,T3BIG,T3EVEN,T3DT,F4BIG,F4EVEN,F4DT,F5BIG,F5EVEN,F5DT,
                      S6BIG,S6EVEN,S7BIG,S7EVEN,E8BIG,E8EVEN,N9BIG,N9EVEN,T10BIG,T10EVEN,ORFLAG,CDATE,CTIME)  




 

        # SQL 插入语句
        insert_data = ("INSERT INTO xyftrd(ID,CSS,CSB,CSE,F1B,F1E,F1DT,S2B,S2E,S2DT,T3B,T3E,T3DT,F4B,F4E,F4DT,F5B,F5E,F5DT,S6B,S6E,S7B,S7E,E8B,E8E,N9B,N9E,T10B,T10E,ORF,CDATE,CTIME)"
                       "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        pk10_data = (ID,CSSUM,CSBIG,CSEVEN,F1BIG,F1EVEN,F1DT,S2BIG,S2EVEN,S2DT,T3BIG,T3EVEN,T3DT,F4BIG,F4EVEN,F4DT,F5BIG,F5EVEN,F5DT,
                      S6BIG,S6EVEN,S7BIG,S7EVEN,E8BIG,E8EVEN,N9BIG,N9EVEN,T10BIG,T10EVEN,ORFLAG,CDATE,CTIME)
        try:
           cursor.execute(insert_data,pk10_data) # 执行sql语句

           db.commit() # 提交到数据库执行
        except:
          db.rollback()  # 如果发生错误则回滚
            
  
        db.close        

        print("xyft表第一条记录成功")


def rdUpdate(firstID,lastID):

    number = firstID


    # 打开数据库连接
    db = pymysql.connect("localhost","root","zhoumb1202","luckyairship" )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 更新xyftrd start----------------------
    
    while True:
        prenumber = number

        if number > lastID:
            print('数据库最新，不需要更新')
            break;
        
    
        #获取原始数据指定行数据
        try :  
            tableName = 'xyft'            
            sql = "SELECT * FROM %s WHERE ID > %d LIMIT 1"  
            cursor.execute(sql %(tableName,int(number)))  
            result = cursor.fetchall()            
            for row in result:
                num = row[0]
                F1 = row[1]
                S2 = row[2]
                T3 = row[3]
                F4 = row[4]
                F5 = row[5]
                S6 = row[6]
                S7 = row[7]
                E8 = row[8]
                N9 = row[9]
                T10 = row[10]

                number = num
                print(num,F1,S2,T3,F4,F5,S6,S7,E8,N9,T10)         
        except Exception as err:  
            print("DBERR数据库查询单条记录失败01： \n[%s]" % (err))  
            exit()

        #获取计算结果前一行数据
        try :  
            tableName = 'xyftrd'            
            sql = "SELECT * FROM %s WHERE ID = %d LIMIT 1"  
            cursor.execute(sql %(tableName,int(prenumber)))  
            result = cursor.fetchall()            
            for row in result:
                ID = row[0]
                CSSUM = row[1]
                CSBIG = row[2]
                CSEVEN = row[3]
                F1BIG = row[4]
                F1EVEN = row[5]
                F1DT = row[6]
                S2BIG = row[7]
                S2EVEN = row[8]
                S2DT = row[9]
                T3BIG = row[10]
                T3EVEN = row[11]
                T3DT = row[12]
                F4BIG = row[13]
                F4EVEN = row[14]
                F4DT = row[15]
                F5BIG = row[16]
                F5EVEN = row[17]
                F5DT = row[18]

                S6BIG = row[19]
                S6EVEN = row[20]
                S7BIG = row[21]
                S7EVEN = row[22]
                E8BIG = row[23]
                E8EVEN = row[24]
                N9BIG = row[25]
                N9EVEN = row[26]
                T10BIG = row[27]
                T10EVEN = row[28]

                ORFLAG = row[29]
                
                
                #print(ID,CSSUM,CSBIG,CSEVEN,F1BIG,F1EVEN,F1DT,S2BIG,S2EVEN,S2DT,T3BIG,T3EVEN,T3DT,F4BIG,F4EVEN,F4DT,F5BIG,F5EVEN,F5DT,
                #      S6BIG,S6EVEN,S7BIG,S7EVEN,E8BIG,E8EVEN,N9BIG,N9EVEN,T10BIG,T10EVEN,ORFLAG)         
        except Exception as err:  
            print("DBERR数据库查询单条记录失败02： \n[%s]" % (err))  
            exit()



        ID = number

        CSSUM = F1+S2
        CSBIG = BigJudge(CSSUM,11,CSBIG)
        CSEVEN = EvenJudge(CSSUM,CSEVEN)

        F1BIG = BigJudge(F1,5,F1BIG)
        F1EVEN = EvenJudge(F1,F1EVEN)
        F1DT = DTJudge(F1,T10,F1DT)

        S2BIG = BigJudge(S2,5,S2BIG)
        S2EVEN = EvenJudge(S2,S2EVEN)
        S2DT = DTJudge(S2,N9,S2DT)

        T3BIG = BigJudge(T3,5,T3BIG)
        T3EVEN = EvenJudge(T3,T3EVEN)
        T3DT = DTJudge(T3,E8,T3DT)

        F4BIG = BigJudge(F4,5,F4BIG)
        F4EVEN = EvenJudge(F4,F4EVEN)
        F4DT = DTJudge(F4,S7,F4DT)

        F5BIG = BigJudge(F5,5,F5BIG)
        F5EVEN = EvenJudge(F5,F5EVEN)
        F5DT = DTJudge(F5,S6,F5DT)

        S6BIG = BigJudge(S6,5,S6BIG)
        S6EVEN = EvenJudge(S6,S6EVEN)
        S7BIG = BigJudge(S7,5,S7BIG)
        S7EVEN = EvenJudge(S7,S7EVEN)
        E8BIG = BigJudge(E8,5,E8BIG)
        E8EVEN = EvenJudge(E8,E8EVEN)
        N9BIG = BigJudge(N9,5,N9BIG)
        N9EVEN = EvenJudge(N9,N9EVEN)
        T10BIG = BigJudge(T10,5,T10BIG)
        T10EVEN = EvenJudge(T10,T10EVEN)
        CDATE = GetDateFromID(ID)
        CTIME = GetTimeFromID(ID)


        ORFLAG = max(abs(CSBIG),abs(CSEVEN),abs(F1BIG),abs(F1EVEN),abs(F1DT),abs(S2BIG),abs(S2EVEN),abs(S2DT),abs(T3BIG),abs(T3EVEN),abs(T3DT),abs(F4BIG),abs(F4EVEN),abs(F4DT),abs(F5BIG),abs(F5EVEN),abs(F5DT),
                      abs(S6BIG),abs(S6EVEN),abs(S7BIG),abs(S7EVEN),abs(E8BIG),abs(E8EVEN),abs(N9BIG),abs(N9EVEN),abs(T10BIG),abs(T10EVEN))
        #print(ID,CSSUM,CSBIG,CSEVEN,F1BIG,F1EVEN,F1DT,S2BIG,S2EVEN,S2DT,T3BIG,T3EVEN,T3DT,F4BIG,F4EVEN,F4DT,F5BIG,F5EVEN,F5DT,
        #              S6BIG,S6EVEN,S7BIG,S7EVEN,E8BIG,E8EVEN,N9BIG,N9EVEN,T10BIG,T10EVEN,ORFLAG,CDATE,CTIME)  




 

        # SQL 插入语句
        insert_data = ("INSERT INTO xyftrd(ID,CSS,CSB,CSE,F1B,F1E,F1DT,S2B,S2E,S2DT,T3B,T3E,T3DT,F4B,F4E,F4DT,F5B,F5E,F5DT,S6B,S6E,S7B,S7E,E8B,E8E,N9B,N9E,T10B,T10E,ORF,CDATE,CTIME)"
                       "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        pk10_data = (ID,CSSUM,CSBIG,CSEVEN,F1BIG,F1EVEN,F1DT,S2BIG,S2EVEN,S2DT,T3BIG,T3EVEN,T3DT,F4BIG,F4EVEN,F4DT,F5BIG,F5EVEN,F5DT,
                      S6BIG,S6EVEN,S7BIG,S7EVEN,E8BIG,E8EVEN,N9BIG,N9EVEN,T10BIG,T10EVEN,ORFLAG,CDATE,CTIME)
        try:
           cursor.execute(insert_data,pk10_data) # 执行sql语句

           db.commit() # 提交到数据库执行
        except:
          db.rollback()  # 如果发生错误则回滚
            
        #print(number)
        if(number == lastID):
            print('rd记录追加完成',lastID)
            break;
        
        
        #print("pk10rd数据库追加记录成功")          

    db.close            
    # 更新xyftrd end----------------------

def DispORFLAG(number): #显示最近100列ORFLAG数据
        # 打开数据库连接
        db = pymysql.connect("localhost","root","zhoumb1202","luckyairship" )
 
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        #获取原始数据指定行数据
        try :  
            tableName = 'pk10rd'
            number  = number -100 #显示100个数据
            sql = "SELECT ORF FROM %s WHERE ID > %d "  
            cursor.execute(sql %(tableName,number))  
            result = cursor.fetchall()
            print(result)
    
        except Exception as err:  
            print("DBERR数据库查询单条记录失败03： \n[%s]" % (err))  
            exit()

        db.close
        print("显示pk10rd最近100个ORFLAG成功")

def GetORF(number):
        # 打开数据库连接
        db = pymysql.connect("localhost","root","zhoumb1202","luckyairship" )
 
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()        #获取计算结果指定行数据
        try :  
            tableName = 'xyftrd'            
            sql = "SELECT * FROM %s WHERE ID = %d LIMIT 1"  
            cursor.execute(sql %(tableName,int(number)))  
            result = cursor.fetchall()
            for row in result:
                ORF = row[29]
        except Exception as err:  
            print("DBERR数据库查询单条记录失败： \n[%s]" % (err))  
            exit()


        return(ORF)

def SaveDataToxyftpi(prenumberID,ORFpri,STEP):
        # 打开数据库连接
        db = pymysql.connect("localhost","root","zhoumb1202","luckyairship" )
 
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        CDATE = GetDateFromID(prenumberID)
        CTIME = GetTimeFromID(prenumberID)

  
        # SQL 插入语句
        insert_data = ("INSERT INTO xyftpi(ID,NC,ORF,NORF,STEP,CDATE,CTIME)"
                       "VALUES(%s,%s,%s,%s,%s,%s,%s)")
        pk10_data = (prenumberID,0,ORFpri,0,STEP,CDATE,CTIME)
        try:
           cursor.execute(insert_data,pk10_data) # 执行sql语句

           db.commit() # 提交到数据库执行
        except:
          db.rollback()  # 如果发生错误则回滚
            
  
        db.close        

        #print(prenumberID,0,ORFpri,0,STEP,CDATE,CTIME)

def GetDeltaID(ID,Delta):
        temp = ID%1000
        if temp > Delta:
                ID = ID -Delta
        else:
                temp = temp + 180 - Delta
                year = ID//10000000
                month = ID%10000000
                month  = month//100000
                day = ID%100000
                day = day//1000

                date = datetime.date(year, month, day)
                date = date - datetime.timedelta(1)

                year = date.year
                month = date.month
                day = date.day
                ID = year*10000000 + month*100000 + day*1000 + temp
        return(ID)
def GetMaxValueStr(ID):

        
        # 打开数据库连接
        db = pymysql.connect("localhost","root","zhoumb1202","luckyairship" )
 
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        try :  
            tableName = 'xyftrd'
            sql = "SELECT * FROM %s where ID = %d"  
            cursor.execute(sql %(tableName,ID))  
            result = cursor.fetchall()
            for row in result:
                #ID = row[0]
                CSSUM = row[1]
                CSBIG = row[2]
                CSEVEN = row[3]
                F1BIG = row[4]
                F1EVEN = row[5]
                F1DT = row[6]
                S2BIG = row[7]
                S2EVEN = row[8]
                S2DT = row[9]
                T3BIG = row[10]
                T3EVEN = row[11]
                T3DT = row[12]
                F4BIG = row[13]
                F4EVEN = row[14]
                F4DT = row[15]
                F5BIG = row[16]
                F5EVEN = row[17]
                F5DT = row[18]

                S6BIG = row[19]
                S6EVEN = row[20]
                S7BIG = row[21]
                S7EVEN = row[22]
                E8BIG = row[23]
                E8EVEN = row[24]
                N9BIG = row[25]
                N9EVEN = row[26]
                T10BIG = row[27]
                T10EVEN = row[28]

                ORFLAG = row[29]          
    
        except Exception as err:  
            print("DBERR数据库查询单条记录失败03： \n[%s]" % (err))  
            exit()

        db.close

        MaxValueStr = []

        if (abs(CSBIG) == ORFLAG):
                if CSBIG > 0:
                        MaxValueStr.append('冠亚大')
                else:
                        MaxValueStr.append('冠亚小')
                        
        if (abs(CSEVEN) == ORFLAG):
                if CSEVEN > 0:
                        MaxValueStr.append('冠亚单')
                else:
                        MaxValueStr.append('冠亚双')
                
        if (abs(F1BIG) == ORFLAG):
                if F1BIG > 0:
                        MaxValueStr.append('冠大')
                else:
                        MaxValueStr.append('冠小')
                
        if (abs(F1EVEN) == ORFLAG):
                if F1EVEN > 0:
                        MaxValueStr.append('冠单')
                else:
                        MaxValueStr.append('冠双')

        if (abs(F1DT) == ORFLAG):
                if F1DT > 0:
                        MaxValueStr.append('冠龙')
                else:
                        MaxValueStr.append('冠虎')
       
        if (abs(S2BIG) == ORFLAG):
                if S2BIG > 0:
                        MaxValueStr.append('亚大')
                else:
                        MaxValueStr.append('亚小')

        if (abs(S2EVEN) == ORFLAG):
                if S2EVEN > 0:
                        MaxValueStr.append('亚单')
                else:
                        MaxValueStr.append('亚双')
       
        if (abs(S2DT) == ORFLAG):
                if S2DT > 0:
                        MaxValueStr.append('亚龙')
                else:
                        MaxValueStr.append('亚虎')

        if (abs(T3BIG) == ORFLAG):
                if T3BIG > 0:
                        MaxValueStr.append('三大')
                else:
                        MaxValueStr.append('三小')

        if (abs(T3EVEN) == ORFLAG):
                if T3EVEN > 0:
                        MaxValueStr.append('三单')
                else:
                        MaxValueStr.append('三双')
       
        if (abs(T3DT) == ORFLAG):
                if T3DT > 0:
                        MaxValueStr.append('三龙')
                else:
                        MaxValueStr.append('三虎')

        if (abs(F4BIG) == ORFLAG):
                if F4BIG > 0:
                        MaxValueStr.append('四大')
                else:
                        MaxValueStr.append('四小')

        if (abs(F4EVEN) == ORFLAG):
                if F4EVEN > 0:
                        MaxValueStr.append('四单')
                else:
                        MaxValueStr.append('四双')
       
        if (abs(F4DT) == ORFLAG):
                if F4DT > 0:
                        MaxValueStr.append('四龙')
                else:
                        MaxValueStr.append('四虎')
        if (abs(F5BIG) == ORFLAG):
                if F5BIG > 0:
                        MaxValueStr.append('五大')
                else:
                        MaxValueStr.append('五小')

        if (abs(F5EVEN) == ORFLAG):
                if F5EVEN > 0:
                        MaxValueStr.append('五单')
                else:
                        MaxValueStr.append('五双')
       
        if (abs(F5DT) == ORFLAG):
                if F5DT > 0:
                        MaxValueStr.append('五龙')
                else:
                        MaxValueStr.append('五虎')

        if (abs(S6BIG) == ORFLAG):
                if S6BIG > 0:
                        MaxValueStr.append('六大')
                else:
                        MaxValueStr.append('六小')

        if (abs(S6EVEN) == ORFLAG):
                if S6EVEN > 0:
                        MaxValueStr.append('六单')
                else:
                        MaxValueStr.append('六双')

        if (abs(S7BIG) == ORFLAG):
                if S7BIG > 0:
                        MaxValueStr.append('七大')
                else:
                        MaxValueStr.append('七小')

        if (abs(S7EVEN) == ORFLAG):
                if S7EVEN > 0:
                        MaxValueStr.append('七单')
                else:
                        MaxValueStr.append('七双')

        if (abs(E8BIG) == ORFLAG):
                if E8BIG > 0:
                        MaxValueStr.append('八大')
                else:
                        MaxValueStr.append('八小')

        if (abs(E8EVEN) == ORFLAG):
                if E8EVEN > 0:
                        MaxValueStr.append('八单')
                else:
                        MaxValueStr.append('八双')

        if (abs(N9BIG) == ORFLAG):
                if N9BIG > 0:
                        MaxValueStr.append('九大')
                else:
                        MaxValueStr.append('九小')

        if (abs(N9EVEN) == ORFLAG):
                if N9EVEN > 0:
                        MaxValueStr.append('九单')
                else:
                        MaxValueStr.append('九双')

        if (abs(T10BIG) == ORFLAG):
                if T10BIG > 0:
                        MaxValueStr.append('十大')
                else:
                        MaxValueStr.append('十小')

        if (abs(T10EVEN) == ORFLAG):
                if T10EVEN > 0:
                        MaxValueStr.append('十单')
                else:
                        MaxValueStr.append('十双')
        return(MaxValueStr)

def piLatestDataDisp(numbers):


        lastID = GetLastIDFromTable('xyftpi')
        ID = GetDeltaID(lastID,numbers)
        
        # 打开数据库连接
        db = pymysql.connect("localhost","root","zhoumb1202","luckyairship" )
 
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        for i in range(numbers):
                try :
                        tableName = 'xyftpi'
                        sql = "SELECT * FROM %s where ID > %d limit 1"  
                        cursor.execute(sql %(tableName,ID))  
                        result = cursor.fetchall()
                                               
                        for row in result:
                                ID = row[0]
                                NC = row[1]
                                ORF = row[2]
                                NORF = row[3]
                                STEP = row[4]
                                CDATE = row[5]
                                CTIME = row[6]

                        MaxValueStr = []
                        if (STEP >2):
                                MaxValueStr = GetMaxValueStr(ID)
                                print('%-14s%-4s%-4s%-8s' %(ID,ORF,STEP,CTIME),MaxValueStr)
                        else:
                                print('%-14s%-4s%-4s%-8s' %(ID,ORF,STEP,CTIME))
                                

                except Exception as err:
                        print("DBERR数据库查询单条记录失败03： \n[%s]" % (err))  
                        exit()

                if (ID == lastID):
                                break;

        db.close 
# 更新xyftpi start----------------------

def piUpdate(firstID,lastID):

    ORFstart = GetORF(firstID)
    ORFpri = ORFstart
    STEP = 0

    prenumberID = firstID
    numberID = firstID + 1

    temp  = numberID%1000
    #print(numberID)
    #print(temp)
    if temp > 180: 
             numberID = GetNextDayballnum(numberID)    

    while True:

        
        #print("failed debug 1007",numberID,firstID,lastID)
        ORF = GetORF(numberID)
        
        flag = ORF - ORFpri

        if(flag < 0):
           step = ORFpri - ORFstart
           
           SaveDataToxyftpi(prenumberID,ORFpri,step)
           

           ORFstart = ORF
           ORFpri = ORF
        
        elif(flag == 0):
            step = ORFpri - ORFstart
            
            SaveDataToxyftpi(prenumberID,ORFpri,step)

            ORFstart = ORF
            ORFpri = ORF
        
        elif(flag>0):
            ORFpri = ORF

        prenumberID = numberID

        numberID = numberID + 1
        temp  = numberID%1000
        if temp > 180: 
                 numberID = GetNextDayballnum(numberID)    

        if numberID>lastID:
                piLatestDataDisp(350)
                print('--------------------------------')
                step = ORF - ORFstart
                print(lastID,'STEP',step)
                bpratio()
                MaxValueDisplay() 
                print('--------------------------------')
                if step > 3:
                        DispStepMoreThanSeries(step-1,30,lastID)                
                #print('pi数据更新完成')
                break
# --更新xyftpi end----------------------

def DispStepMoreThanSeries(step_level,numbers,ID):
        # 打开数据库连接
        db = pymysql.connect("localhost","root","zhoumb1202","luckyairship" )
 
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        for i in range(numbers):
                try :
                        tableName = 'xyftpi'
                        sql = "SELECT * FROM %s where step > %d && ID < %d order by ID desc limit 1"  
                        cursor.execute(sql %(tableName,step_level,ID))  
                        result = cursor.fetchall()
                                               
                        for row in result:
                                 ID = row[0]
                                 NC = row[1]
                                 ORF = row[2]
                                 NORF = row[3]
                                 STEP = row[4]
                                 CDATE = row[5]
                                 CTIME = row[6]
                        print('%-14s%-4s%-4s%-12s%-8s' %(ID,ORF,STEP,CDATE,CTIME))

                except Exception as err:
                        print("DBERR数据库查询单条记录失败03： \n[%s]" % (err))  
                        exit()
        db.close

def bpratio():
        

        ballnum,daynum,today_num = GetIDAccordingCurentTime()
        currentID = ballnum
        
        picount = GetPK10piCount(currentID)

        currentID = currentID%1000


        if currentID >0:
                bpratio = round(picount/currentID,3)
        else:
                bpratio = 0

        print('当前BP比值',bpratio)
        
def GetPK10piCount(currentID):

        startID = currentID//1000
        startID = startID*1000 + 1
        
        # 打开数据库连接
        db = pymysql.connect("localhost","root","zhoumb1202","luckyairship" )
 
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        today = datetime.date.today()

        #获取开始行数据
        try :  
            #tableName = 'pk10pi'
            
            sql = "select count(*) from xyftpi where ID > %d"  
            cursor.execute(sql %(startID))  
            result = cursor.fetchall()
            for row in result:
                countpi = row[0]
            #print(countpi)
                
                    
        except Exception as err:  
            print("DBERR数据库查询第一行记录失败： \n[%s]" % (err))  
            exit()

        db.close
       
        return(countpi)
def GetWaitingTime(): #by zhoumb 2018-06-01
    now = datetime.datetime.now()
    currenthour = now.hour
    currentmin = now.minute
    currentsec = now.second
    currentmin = currentmin%10
    #print(currentmin)
    if (currentmin == 3 or currentmin == 8):
        waitingtime = 150 - currentsec
    if (currentmin == 4 or currentmin == 9):
        waitingtime = 90 - currentsec
    if (currentmin == 5 or currentmin == 0):
        waitingtime = 330 - currentsec
    if (currentmin == 6 or currentmin == 1):
        waitingtime = 270 - currentsec
    if (currentmin == 7 or currentmin == 2):
        waitingtime = 210 - currentsec

    if(currenthour>4 and currenthour<13):
            waitingtime = 500
            
    
    return(waitingtime)

def SeqValueDisp(ID,position,numbers):
        # 打开数据库连接
        db = pymysql.connect("localhost","root","zhoumb1202","luckyairship" )
 
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        numberlist = []
        for i in range(numbers):
                try :
                        tableName = 'xyft'
                        sql = "SELECT * FROM %s where ID = %d "  
                        cursor.execute(sql %(tableName,ID))  
                        result = cursor.fetchall()
                        ID = GetDeltaID(ID,1)
                        
                        for row in result:
                                numberlist.append(row[position])
         
    
                except Exception as err:
                        print("DBERR数据库查询单条记录失败03： \n[%s]" % (err))  
                        exit()

        print(numberlist)
        db.close
        
def MaxValueDisplay():
        
        # 打开数据库连接
        db = pymysql.connect("localhost","root","zhoumb1202","luckyairship" )
 
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        try :  
            tableName = 'xyftrd'
            sql = "SELECT * FROM %s order by ID desc limit 1 "  
            cursor.execute(sql %tableName)  
            result = cursor.fetchall()
            for row in result:
                ID = row[0]
                CSSUM = row[1]
                CSBIG = row[2]
                CSEVEN = row[3]
                F1BIG = row[4]
                F1EVEN = row[5]
                F1DT = row[6]
                S2BIG = row[7]
                S2EVEN = row[8]
                S2DT = row[9]
                T3BIG = row[10]
                T3EVEN = row[11]
                T3DT = row[12]
                F4BIG = row[13]
                F4EVEN = row[14]
                F4DT = row[15]
                F5BIG = row[16]
                F5EVEN = row[17]
                F5DT = row[18]

                S6BIG = row[19]
                S6EVEN = row[20]
                S7BIG = row[21]
                S7EVEN = row[22]
                E8BIG = row[23]
                E8EVEN = row[24]
                N9BIG = row[25]
                N9EVEN = row[26]
                T10BIG = row[27]
                T10EVEN = row[28]

                ORFLAG = row[29]          
    
        except Exception as err:  
            print("DBERR数据库查询单条记录失败03： \n[%s]" % (err))  
            exit()

        db.close

        if (abs(CSBIG) == ORFLAG):
                if CSBIG > 0:
                        print('冠亚大',ORFLAG)
                else:
                        print('冠亚小',ORFLAG)
                SeqValueDisp(ID,1,ORFLAG)
                SeqValueDisp(ID,2,ORFLAG)
                        
        if (abs(CSEVEN) == ORFLAG):
                if CSEVEN > 0:
                        print('冠亚单',ORFLAG)
                else:
                        print('冠亚双',ORFLAG)
                SeqValueDisp(ID,1,ORFLAG)
                SeqValueDisp(ID,2,ORFLAG)
                
        if (abs(F1BIG) == ORFLAG):
                if F1BIG > 0:
                        print('冠大',ORFLAG)
                else:
                        print('冠小',ORFLAG)        
                SeqValueDisp(ID,1,ORFLAG)
                
        if (abs(F1EVEN) == ORFLAG):
                if F1EVEN > 0:
                        print('冠单',ORFLAG)
                else:
                        print('冠双',ORFLAG)      
                SeqValueDisp(ID,1,ORFLAG)

        if (abs(F1DT) == ORFLAG):
                if F1DT > 0:
                        print('冠龙',ORFLAG)
                else:
                        print('冠虎',ORFLAG)    
                SeqValueDisp(ID,1,ORFLAG)
                SeqValueDisp(ID,10,ORFLAG)
       
        if (abs(S2BIG) == ORFLAG):
                if S2BIG > 0:
                        print('亚大',ORFLAG)
                else:
                        print('亚小',ORFLAG)        
                SeqValueDisp(ID,2,ORFLAG)

        if (abs(S2EVEN) == ORFLAG):
                if S2EVEN > 0:
                        print('亚单',ORFLAG)
                else:
                        print('亚双',ORFLAG)      
                SeqValueDisp(ID,2,ORFLAG)
       
        if (abs(S2DT) == ORFLAG):
                if S2DT > 0:
                        print('亚龙',ORFLAG)
                else:
                        print('亚虎',ORFLAG)       
                SeqValueDisp(ID,2,ORFLAG)
                SeqValueDisp(ID,9,ORFLAG)

        if (abs(T3BIG) == ORFLAG):
                if T3BIG > 0:
                        print('三大',ORFLAG)
                else:
                        print('三小',ORFLAG)        
                SeqValueDisp(ID,3,ORFLAG)

        if (abs(T3EVEN) == ORFLAG):
                if T3EVEN > 0:
                        print('三单',ORFLAG)
                else:
                        print('三双',ORFLAG)      
                SeqValueDisp(ID,3,ORFLAG)
       
        if (abs(T3DT) == ORFLAG):
                if T3DT > 0:
                        print('三龙',ORFLAG)
                else:
                        print('三虎',ORFLAG)
                SeqValueDisp(ID,3,ORFLAG)
                SeqValueDisp(ID,8,ORFLAG)

        if (abs(F4BIG) == ORFLAG):
                if F4BIG > 0:
                        print('四大',ORFLAG)
                else:
                        print('四小',ORFLAG)        
                SeqValueDisp(ID,4,ORFLAG)

        if (abs(F4EVEN) == ORFLAG):
                if F4EVEN > 0:
                        print('四单',ORFLAG)
                else:
                        print('四双',ORFLAG)      
                SeqValueDisp(ID,4,ORFLAG)
       
        if (abs(F4DT) == ORFLAG):
                if F4DT > 0:
                        print('四龙',ORFLAG)
                else:
                        print('四虎',ORFLAG)                          
                SeqValueDisp(ID,4,ORFLAG)
                SeqValueDisp(ID,7,ORFLAG)
        if (abs(F5BIG) == ORFLAG):
                if F5BIG > 0:
                        print('五大',ORFLAG)
                else:
                        print('五小',ORFLAG)        
                SeqValueDisp(ID,5,ORFLAG)

        if (abs(F5EVEN) == ORFLAG):
                if F5EVEN > 0:
                        print('五单',ORFLAG)
                else:
                        print('五双',ORFLAG)      
                SeqValueDisp(ID,5,ORFLAG)
       
        if (abs(F5DT) == ORFLAG):
                if F5DT > 0:
                        print('五龙',ORFLAG)
                else:
                        print('五虎',ORFLAG)  

                SeqValueDisp(ID,5,ORFLAG)
                SeqValueDisp(ID,6,ORFLAG)

        if (abs(S6BIG) == ORFLAG):
                if S6BIG > 0:
                        print('六大',ORFLAG)
                else:
                        print('六小',ORFLAG)        
                SeqValueDisp(ID,6,ORFLAG)

        if (abs(S6EVEN) == ORFLAG):
                if S6EVEN > 0:
                        print('六单',ORFLAG)
                else:
                        print('六双',ORFLAG)      
                SeqValueDisp(ID,6,ORFLAG)

        if (abs(S7BIG) == ORFLAG):
                if S7BIG > 0:
                        print('七大',ORFLAG)
                else:
                        print('七小',ORFLAG)        
                SeqValueDisp(ID,7,ORFLAG)

        if (abs(S7EVEN) == ORFLAG):
                if S7EVEN > 0:
                        print('七单',ORFLAG)
                else:
                        print('七双',ORFLAG)    
                SeqValueDisp(ID,7,ORFLAG)

        if (abs(E8BIG) == ORFLAG):
                if E8BIG > 0:
                        print('八大',ORFLAG)
                else:
                        print('八小',ORFLAG)        
                SeqValueDisp(ID,8,ORFLAG)

        if (abs(E8EVEN) == ORFLAG):
                if E8EVEN > 0:
                        print('八单',ORFLAG)
                else:
                        print('八双',ORFLAG)    
                SeqValueDisp(ID,8,ORFLAG)

        if (abs(N9BIG) == ORFLAG):
                if N9BIG > 0:
                        print('九大',ORFLAG)
                else:
                        print('九小',ORFLAG)        
                SeqValueDisp(ID,9,ORFLAG)

        if (abs(N9EVEN) == ORFLAG):
                if N9EVEN > 0:
                        print('九单',ORFLAG)
                else:
                        print('九双',ORFLAG)    
                SeqValueDisp(ID,9,ORFLAG)

        if (abs(T10BIG) == ORFLAG):
                if T10BIG > 0:
                        print('十大',ORFLAG)
                else:
                        print('十小',ORFLAG)        
                SeqValueDisp(ID,10,ORFLAG)

        if (abs(T10EVEN) == ORFLAG):
                if T10EVEN > 0:
                        print('十单',ORFLAG)
                else:
                        print('十双',ORFLAG)    
                SeqValueDisp(ID,10,ORFLAG)

    

