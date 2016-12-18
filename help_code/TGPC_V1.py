# Author:      tapon
# Created:     12/03/2015
# Copyright:   (c) tapon 2015

import xlrd
import MySQLdb
from lxml import etree as ET
import sys,time
from tkMessageBox import *
import Tkinter

class read_input:
    def __init__(self,in_sheet_index):
        self.filename = "E:\\3gext\TGPC\input_TGPC.xlsx"
        self.RNC = []
        self.WBTS = []
        self.WCEL = []
        self.TRX = []

        self.RNCINDEX = 0
        self.WBTSINDEX = 1
        self.WCELINDEX = 2
        self.TRXINDEX = 3

        self.PARAMNAME = []
        self.PARAMVALUE = []
        self.sheet_index = in_sheet_index
        all_parameter = []
        'Reading input'
        pass
    def ReadExcel(self):
        wb = xlrd.open_workbook(self.filename)
        sh1 = wb.sheet_by_index(self.sheet_index)
        for rownum in range(sh1.nrows):
            self.RNC.append(str(sh1.row_values(rownum)[self.RNCINDEX]).split(".")[0])
            self.WBTS.append(str(sh1.row_values(rownum)[self.WBTSINDEX]).split(".")[0])
            self.WCEL.append(str(sh1.row_values(rownum)[self.WCELINDEX]).split(".")[0])
            self.TRX.append(str(sh1.row_values(rownum)[self.TRXINDEX]).split(".")[0])

        for colnum in range(sh1.ncols):
            if sh1.col_values(colnum)[1]=='':
                continue
            else:
                self.PARAMNAME.append(str(sh1.col_values(colnum)[1].split('(')[0].strip()))
                self.PARAMVALUE.append(sh1.col_values(colnum)[2:])

        self.RNC = self.RNC[2:]
        self.WBTS = self.WBTS[2:]
        self.WCEL = self.WCEL[2:]
        self.TRX = self.TRX[2:]
        self.MO = self.PARAMNAME[:4]
        self.PARAMNAME = self.PARAMNAME[4:]
        self.PARAMVALUE =  self.PARAMVALUE[4:]
        print self.PARAMVALUE
        print self.PARAMNAME
        print self.MO

        self.PARAMVALUE = zip(*self.PARAMVALUE)
        pass
    def main(self):
            raml = ET.Element("raml")
            raml.set("version","1.0")
            raml.set("xmlns","raml20.xsd")
            cmData = ET.SubElement(raml,"cmData")
            cmData.set("type","plan")
            cmData.set("name","OMC_RND")
            header = ET.SubElement(cmData,"header")
            log = ET.SubElement(header,"log")
            log.set("user","Tapon")
            log.set("dateTime",time.ctime()) # Need to change
            log.set("action","created")
            log.set("appInfo","Python_Generated")
            log.text = "No Description"
            index = -1



            for parameter in self.PARAMVALUE:
                index += 1
                print index
                distname = "PLMN-PLMN/"+self.MO[0]+"-" + self.RNC[index]+ "/"+self.MO[1]+"-"+self.WBTS[index]+\
                            "/" + self.MO[2]+"-"+self.WCEL[index]+"/" + self.MO[3]+"-"+self.TRX[index]

                if self.WBTS[0] == '':
                    distname = '/'.join(distname.split('/')[:2])


                elif self.WCEL[0] == '':
                    distname = '/'.join(distname.split('/')[:3])

                elif self.TRX[0] == '':
                    distname = '/'.join(distname.split('/')[:4])

                print distname

                mo = ET.SubElement(cmData,"managedObject")
                mo.set("class", "com.omc.mcrnc:"+managedObject_name)
                mo.set("distName", distname)
                mo.set("operation", "update")
                param_index= -1
                for aParameter in parameter:

                    param_index+=1
                    p = ET.SubElement(mo, "p")
                    p.set("name", self.PARAMNAME[param_index])
                    try:
                        p.text = str(int(aParameter))
                    except ValueError:
                        pass

            tree = ET.ElementTree(raml)
            x = ET.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8",doctype="<!DOCTYPE raml SYSTEM 'raml20.dtd'>")
            fp = open("E:\\3gext\TGPC\parameter.xml","w+")
            fp.write(ET.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8",doctype="<!DOCTYPE raml SYSTEM 'raml20.dtd'>"))
            fp.close()


            pass

if __name__ == '__main__':
    top = Tkinter.Tk()
    managedObject_name = raw_input("Write MO name").upper()
    aReadInput = read_input(1)
    aReadInput.ReadExcel()

    aReadInput.main()