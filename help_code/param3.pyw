#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      tapon
#
# Created:     12/02/2014
# Copyright:   (c) tapon 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import xlrd
import sys
import os
import MySQLdb
import Tkinter
from tkMessageBox import *
class Paramchange:
    def __init__(self,filename,mapfile):
        self.filename = filename
        self.mapfile = mapfile
        self.BSC = []
        self.BCF = []
        self.BTS = []
        self.TRX = []
        self.ADJLAC = []
        self.ADJCI = []
        self.PARAMNAME = []
        self.PARAMVALUE = []
        self.BSCINDEX = 0
        self.BCFINDEX = 1
        self.BTSINDEX = 2
        self.TRXINDEX = 3
        self.ADJLACINDEX = 4
        self.ADJCIINDEX = 5
        self.PARAMSTARTINDEX = 6
        self.CMD = []

    def get_SEGID(self,in_cmd):
        cmd = in_cmd
        bsc = cmd.split("@")[1]
        bts = cmd.split(":")[1]
        db = MySQLdb.connect('localhost','root','','myflexml')
        cursor = db.cursor()

        cursor.execute("SELECT bsc,bcf,bts,segmentid FROM bts where bsc="+bsc+" and "+bts+";")
        data = cursor.fetchall()
        cursor.close()
        db.commit()
        print data[0][3]
        return data[0][3]




    def writer(self,commands):
        cmd = commands
        fp = open("E:\\Parameter\\out.txt","w+")
        for c in cmd:
            fp.writelines(c+"\n")
        fp.close()
        os.startfile("E:\\Parameter\\out.txt")

    def readxl(self):
        wb = xlrd.open_workbook(self.filename)
        sh1 = wb.sheet_by_index(0)

        for rownum in range(sh1.nrows):
            self.BSC.append(str(sh1.row_values(rownum)[self.BSCINDEX]).split(".")[0])
            self.BCF.append(str(sh1.row_values(rownum)[self.BCFINDEX]).split(".")[0])
            self.BTS.append(str(sh1.row_values(rownum)[self.BTSINDEX]).split(".")[0])
            self.TRX.append(str(sh1.row_values(rownum)[self.TRXINDEX]).split(".")[0])
            self.ADJLAC.append(str(sh1.row_values(rownum)[self.ADJLACINDEX]).split(".")[0])
            self.ADJCI.append(str(sh1.row_values(rownum)[self.ADJCIINDEX]).split(".")[0])

        for colnum in range(sh1.ncols):
            if sh1.col_values(colnum)[1]=='':
                continue
            else:
                self.PARAMNAME.append(str(sh1.col_values(colnum)[1].split('(')[0].strip()))
                self.PARAMVALUE.append(sh1.col_values(colnum)[2:])

        self.BSC = self.BSC[2:]
        self.BCF = self.BCF[2:]
        self.BTS = self.BTS[2:]
        self.TRX = self.TRX[2:]
        self.ADJLAC = self.ADJLAC[2:]
        self.ADJCI = self.ADJCI[2:]

        print "\nPrint form readxl()\nBSC,BCF,BTS,TRX,ADJLAC,ADJCI,PARAMNAME,PARAMVALUE from INPUT: "
        print self.BSC,self.BCF,self.BTS,self.TRX,self.ADJLAC,self.ADJCI,self.PARAMNAME,self.PARAMVALUE


    def GuiMap(self):
        self.INTERNALNAME = []
        self.GUINAME = []
        self.CONVERSION = []
        self.MML = []
        self.PLEVEL = []
        self.MODIFICATION = []
        ALLPARAM = []
        wb2 = xlrd.open_workbook(self.mapfile)
        sh1 = wb2.sheet_by_index(0)

        for param in self.PARAMNAME:
            for rownum in range(sh1.nrows):
                if str(sh1.row_values(rownum)[0]) not in ALLPARAM:
                    ALLPARAM.append(str(sh1.row_values(rownum)[0]))
                if param in sh1.row_values(rownum):
                    self.GUINAME.append(str(sh1.row_values(rownum)[1]))
                    self.CONVERSION.append(str(sh1.row_values(rownum)[2]))
                    self.MML.append(str(sh1.row_values(rownum)[3]))
                    self.MODIFICATION.append(str(sh1.row_values(rownum)[5]))
                    if str(sh1.row_values(rownum)[4])=='HOC' or str(sh1.row_values(rownum)[4])=='POC':
                        self.PLEVEL.append('SEG')
                    else:
                        self.PLEVEL.append(str(sh1.row_values(rownum)[4]))

        print "\nPrint from GuiMap()\nALLPARAM,GUINAME,CONVERSION,MML,MODIFICATION"
        print ALLPARAM,self.GUINAME,self.CONVERSION,self.MML,self.MODIFICATION
        print "\n-----^-------------------------------"
        for p in self.PARAMNAME:
            if p not in ALLPARAM:

                a = showinfo( "Alert!","["+p+"]  Not found in MAP file\n Please update MAP.xlsx!")
                self.PARAMNAME.pop(self.PARAMNAME.index(p))
                if a=="ok":
                    os.startfile("E:\\Parameter\\MAP.xlsx")
                    print "Good Bye!!!"
                    sys.exit()
        print "-----^-------------------------------\n"
        info = ""

        for pn in self.PARAMNAME:
            info = info+pn+" works on "+self.PLEVEL[self.PARAMNAME.index(pn)]+"\n"
        if 'GL' in self.MODIFICATION:
            info = info + "\n  [GPRS will be disabled]  "
        if 'L' in self.MODIFICATION:
            info = info + "\n  [BTS will be locked]  "
        if 'TL' in self.MODIFICATION:
            info = info + "\n  [BTS/TRX will be locked]  "
        showinfo("Have a look!",info)

    def IntGuiConv(self):
        cnt  = -1
        self.newPARAMVALUE = []
        for c in self.CONVERSION:
            paramArray = []
            cnt +=1
            multiplier = 1
            adder = 0
            if c.split("/")[0].find('EXP')>=0:
                    for val in self.PARAMVALUE[cnt]:
                        for x in c.split("/"):
                            if x.split("-")[0]== str(int(val)):
                                paramArray.append(x.split("-")[1])

            else:
                multiplier = c.split("/")[0].split("_")[1]
                adder =c.split("/")[1].split("_")[1]
                if  c.split("/")[1].split("_")[0]=='S':
                    adder = int(adder)*(-1)
                print self.PARAMVALUE
                for val in self.PARAMVALUE[cnt]:
                    paramArray.append(int(multiplier)*int(val)+int(adder))
            self.newPARAMVALUE.append(paramArray)
        print "\nPrint from IntGuiConv()\nnewPARAMVALUE"
        print self.newPARAMVALUE


    def CmdMaker(self):
        cnt =-1
        for val_array in self.newPARAMVALUE:
            cnt  +=1
            cnt_p = -1
            for paramval in val_array:
                cnt_p+=1
                if self.PLEVEL[cnt]=="BCF":
                    self.CMD.append(str(self.MML[cnt]+":"+self.BCF[cnt_p]+":"+self.GUINAME[cnt]+"="+str(paramval)+";@"+self.BSC[cnt_p]+"@")+"--"+self.MODIFICATION[cnt])
                elif self.PLEVEL[cnt]=="ADCE":
                    self.CMD.append(str(self.MML[cnt]+":SEG="+self.BTS[cnt_p]+"::MCC=470,MNC=03,LAC="+self.ADJLAC[cnt_p]+",CI="+self.ADJCI[cnt_p]+":"+self.GUINAME[cnt]+"="+str(paramval)+";@"+self.BSC[cnt_p]+"@")+"--"+self.MODIFICATION[cnt])
                elif self.PLEVEL[cnt]=="TRX":
                    self.CMD.append(str(self.MML[cnt]+":BTS="+self.BTS[cnt_p]+",TRX="+self.TRX[cnt_p]+":"+self.GUINAME[cnt]+"="+str(paramval)+";@"+self.BSC[cnt_p]+"@")+"--"+self.MODIFICATION[cnt])

                else:
                    self.CMD.append(str(self.MML[cnt]+":"+str(self.PLEVEL[cnt])+"="+self.BTS[cnt_p]+":"+self.GUINAME[cnt]+"="+str(paramval)+";@"+self.BSC[cnt_p]+"@")+"--"+self.MODIFICATION[cnt])

        print "\nPrint from CmdMaker()\nCMD"
        for c in self.CMD:
            print c


    def CmdCombiner(self):
        combined_cmd = []
        cmd_pattern = []
        newCMD = []
        finalCMD = []
        new_cmd = ""
        cnt3 = -1
        #print self.CMD
        for cmd in self.CMD:
            new_cmd = ""
            c = ""

            cmd_pattern.append(len(cmd.split(":")))

            if cmd.split(":")[0]=="ZEAM":
                if cmd.split(":")[0]+cmd.split(":")[1]+cmd.split(":")[3] not in combined_cmd:
                    combined_cmd.append(cmd.split(":")[0]+cmd.split(":")[1]+cmd.split(":")[3])
                    newCMD.append(cmd)

                else:

                    if len(cmd.split(":"))==len((newCMD[combined_cmd.index(cmd.split(":")[0]+cmd.split(":")[1]+cmd.split(":")[3])]).split(":")):
                        if cmd.split("--")[1] == newCMD[combined_cmd.index(cmd.split(":")[0]+cmd.split(":")[1]+cmd.split(":")[3])].split("--")[1]:

                            if cmd.split(":")[-1].split(";")[0]==newCMD[combined_cmd.index(cmd.split(":")[0]+cmd.split(":")[1]+cmd.split(":")[3])].split(";")[0].split(":")[-1]:
                             print"continued"
                             continue
                            else:
                                newCMD[combined_cmd.index(cmd.split(":")[0]+cmd.split(":")[1]+cmd.split(":")[3])] = newCMD[combined_cmd.index(cmd.split(":")[0]+cmd.split(":")[1]+cmd.split(":")[3])].split(";")[0]+","+cmd.split(":")[-1]
                        else:
                            newCMD.append(cmd)
                    else:
                        newCMD.append(cmd)

                    pass

            else:

                if  cmd.split(":")[0]+cmd.split(":")[1]+cmd.split("@")[1] not in combined_cmd:
                    combined_cmd.append(cmd.split(":")[0]+cmd.split(":")[1]+cmd.split("@")[1])
                    newCMD.append(cmd)
                else:

                    if len(cmd.split(":"))==len((newCMD[combined_cmd.index(cmd.split(":")[0]+cmd.split(":")[1]+cmd.split("@")[1])]).split(":")):
                        if cmd.split("--")[1] == newCMD[combined_cmd.index(cmd.split(":")[0]+cmd.split(":")[1]+cmd.split("@")[1])].split("--")[1]:

                            if cmd.split(":")[-1].split(";")[0]==newCMD[combined_cmd.index(cmd.split(":")[0]+cmd.split(":")[1]+cmd.split("@")[1])].split(";")[0].split(":")[-1]:
                                continue
                            else:
                                newCMD[combined_cmd.index(cmd.split(":")[0]+cmd.split(":")[1]+cmd.split("@")[1])] = newCMD[combined_cmd.index(cmd.split(":")[0]+cmd.split(":")[1]+cmd.split("@")[1])].split(";")[0]+","+cmd.split(":")[-1]
                        else:
                            newCMD.append(cmd)
                    else:
                        newCMD.append(cmd)

                    pass

        print "\nnewCMD"
        for nc in newCMD:
            print nc
        for x in newCMD:
            if x.split(":")[0]=="ZERM":
                #print "ZEQS:"+x.split(":")[1].split(",")[0]+":L;"
                finalCMD.append("ZEQS:"+x.split(":")[1].split(",")[0]+":L;@"+x.split("@")[1]+"@")

            if x.split("--")[1]=='TL':
                #print "ZERS:"+x.split(":")[1]+":L;"
                finalCMD.append("ZERS:"+x.split(":")[1]+":L;@"+x.split("@")[1]+"@")
                #print x.split("--")[0]
                finalCMD.append(x.split("--")[0])
                #print "ZERS:"+x.split(":")[1]+":U;"
                finalCMD.append("ZERS:"+x.split(":")[1]+":U;@"+x.split("@")[1]+"@")

            if x.split("--")[1]=='L':
                #print "ZEQS:"+x.split(":")[1]+":L;"
                finalCMD.append("ZEQS:"+x.split(":")[1]+":L;@"+x.split("@")[1]+"@")
                #print x.split("--")[0]
                finalCMD.append(x.split("--")[0])
                #print "ZEQS:"+x.split(":")[1]+":U;"
                finalCMD.append("ZEQS:"+x.split(":")[1]+":U;@"+x.split("@")[1]+"@")
            if x.split(":")[0]=="ZERM":
                #print "ZEQS:"+x.split(":")[1].split(",")[0]+":U;"
                finalCMD.append("ZEQS:"+x.split(":")[1].split(",")[0]+":U;@"+x.split("@")[1]+"@")

            elif x.split("--")[1]=='GL':
                SEGID = self.get_SEGID(x.split("--")[0])
                #print "ZEQV:SEG="+str(SEGID)+":GENA=N;"
                finalCMD.append("ZEQV:SEG="+str(SEGID)+":GENA=N;@"+x.split("@")[1]+"@")
                #print x.split("--")[0]
                finalCMD.append(x.split("--")[0])
                #print "ZEQV:SEG="+str(SEGID)+":GENA=Y;"
                finalCMD.append("ZEQV:SEG="+str(SEGID)+":GENA=Y;@"+x.split("@")[1]+"@")

            else:
                finalCMD.append(x.split("--")[0])

        duplicate = []
        duplicate_index = []
        cnt  = -1
        #print finalCMD
        for c in finalCMD:
            cnt +=1
            if c.split(":")[1]+c.split(":")[2] not in duplicate:
                if c.split(":")[2]=='GENA=N;' or c.split(":")[2]=="L;@"+x.split("@")[1]+"@":
                    duplicate.append(c.split(":")[1]+c.split(":")[2])
            else:
                duplicate_index.append(cnt)
        pop_cnt = -1
        for d in duplicate_index:
            pop_cnt+=1
            finalCMD.pop(d-pop_cnt)
            pop_cnt+=1
            finalCMD.pop(d-pop_cnt)
        return finalCMD


if __name__ == '__main__':
    top = Tkinter.Tk()
    top.withdraw()
    PC = Paramchange('E:\Parameter\parameter.xlsx','E:\Parameter\Map.xlsx')
    PC.readxl()
    PC.GuiMap()
    PC.IntGuiConv()
    PC.CmdMaker()
    commands = PC.CmdCombiner()
    PC.writer(commands)

