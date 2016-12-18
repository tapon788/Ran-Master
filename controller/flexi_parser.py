__author__ = 'tpaul'
import sys
import os
from xml.sax.handler import ContentHandler
from xml.sax import parse
import MySQLdb
import warnings
from colorama import init
from termcolor import colored, cprint

import pickle
import datetime
import threading
from gui_interfaces.gui_settings import *
class ManagedObjectHandler(ContentHandler, threading.Thread):
    in_headline = False
    def __init__(self, headlines, in_parse_progress, in_parse_label_text, in_total_count, in_completed_count, in_remaining_count):
        ContentHandler.__init__(self)
        threading.Thread.__init__(self)
        self.parse_progress = in_parse_progress
        self.parse_label_text = in_parse_label_text
        self.total_count = in_total_count
        self.remaining_count = in_remaining_count
        self.completed_count = in_completed_count
        self.isdata = ""
        self.param_value = []
        self.param_list = []
        self.headlines = headlines
        self.BSC = []
        self.BCF=[]
        self.BTS=[]
        self.TRX=[]
        self.LAPD=[]
        self.ADCE=[]
        self.ADJW=[]
        self.HOC=[]
        self.POC=[]
        self.DAP=[]
        self.CSDAP = []
        self.ALL=[self.BSC,self.BCF,self.BTS,self.TRX,self.LAPD,self.ADCE,self.ADJW,self.HOC,self.POC,self.DAP,self.CSDAP]


        self.ADCE_ADDR=[]
        self.grep = ["BSC", "BCF", "BTS", "TRX", "LAPD", "ADCE", "ADJW", "HOC", "POC", "DAP", "CSDAP"]
        self.sql_user="root"
        self.sql_pass=""
        self.sql_host="localhost"
        self.sql_db = "myflexml"

    def startElement(self, name, Attributes):
        self.param_name=Attributes.values()
        if name == 'managedObject':
            self.param_name = []
            self.isdata = ""
            self.param_value=[]
            self.param_list=[]
            self.class_address=[]
            self.class_name = Attributes.values()[(Attributes.keys().index('class'))]
            if self.class_name in self.grep:
                self.in_headline = True
            self.class_address = Attributes.values()[(Attributes.keys().index('distName'))]

    def characters(self, string):
        if self.in_headline:
            string = string.rstrip()
            if(len(string)>0):
                self.isdata = self.isdata+string
            else:
                self.isdata = "";

    def endElement(self, name):

        self.param_list.append(self.param_name)
        self.param_value.append(self.isdata)

        if name == 'managedObject':
            if self.in_headline:
                self.in_headline = False
                self.array_maker()
        if name =='raml':
            self.file_writer()

    def array_maker(self):

        if self.class_name in self.grep:
            #a =self.class_address+self.param_list+self.param_value
            #print a
            '''
            self.ADCE.append(self.param_list)
            self.ADCE_VAL.append(self.param_value)
            self.ADCE_ADDR.append(self.class_address)
            '''
            line=""
            for paramName,paramVal in map(None,self.param_list,self.param_value):
                #fpp.writelines(str(paramName)+"->"+str(paramVal)+"\n")
                if (paramName==[] or paramVal==""):
                    continue
                line =line+str(paramName)[3:-2]+"->"+str(paramVal)+","
                #print line

            def adce():
                #print "ALL_ARRAY "+self.class_name
                self.ADCE.append(str(self.class_address)+","+line)
                #print self.ADCE
            def bts():
                #print "ALL_ARRAY "+self.class_name
                self.BTS.append(str(self.class_address)+","+line)
                #fpp.writelines(line+"\n")
                #print self.BTS

            def bsc():
                #print line
                #print "ALL_ARRAY "+self.class_name
                self.BSC.append(str(self.class_address)+","+line)
                #print self.BSC
            def bcf():
                #print "ALL_ARRAY "+self.class_name
                self.BCF.append(str(self.class_address)+","+line)
                #print self.BCF
            def trx():
                #print "ALL_ARRAY "+self.class_name
                self.TRX.append(str(self.class_address)+","+line)
                #print self.TRX
            def lapd():
                #print "ALL_ARRAY "+self.class_name
                self.LAPD.append(str(self.class_address)+","+line)
                #print self.LAPD

            def adjw():
                #print "ALL_ARRAY "+self.class_name
                self.ADJW.append(str(self.class_address)+","+line)
                #print self.ADJW
            def hoc():
                #print "ALL_ARRAY "+self.class_name
                self.HOC.append(str(self.class_address)+","+line)
                #print self.HOC

            def poc():
                #print "ALL_ARRAY "+self.class_name
                self.POC.append(str(self.class_address)+","+line)
                #print self.POC

            def dap():
                #print "ALL_ARRAY "+self.class_name
                self.DAP.append(str(self.class_address)+","+line)
                #print self.DAP
            def csdap():
                #print "ALL_ARRAY "+self.class_name
                self.CSDAP.append(str(self.class_address)+","+line)
                #print self.CSDAP

            options={"BSC":bsc,
                     "BCF":bcf,
                     "BTS":bts,
                     "TRX":trx,
                     "LAPD":lapd,
                     "ADCE":adce,
                     "ADJW":adjw,
                     "HOC":hoc,
                     "POC":poc,
                     "DAP":dap,
                     "CSDAP":csdap
                     }
            options[self.class_name]()




    def file_writer(self):

        for fname in self.grep:

            file_name =PARSED_DB_DIR+fname
            fp = open (file_name,"a+")
            for data in self.ALL[self.grep.index(fname)]:
                fp.writelines(data)
                fp.writelines('\n')
            fp.close()

        '''
        SQL operations

        '''
    def Dbdelcreate(self):
        db = MySQLdb.connect(self.sql_host, self.sql_user, self.sql_pass)
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS myflexml;")
        cursor.close()
        db.commit()

        db = MySQLdb.connect(self.sql_host,self.sql_user,self.sql_pass,self.sql_db)
        cursor = db.cursor()
        cursor.execute("DROP DATABASE IF EXISTS myflexml; CREATE DATABASE myflexml;")
        cursor.close()
        db.commit()

    def Createtable(self):
        db = MySQLdb.connect(self.sql_host,self.sql_user,self.sql_pass,self.sql_db)
        self.table_name = os.listdir(PARSED_DB_DIR)
        self.parse_progress['value'] = 0
        self.parse_progress['maximum'] = len(os.listdir(PARSED_DB_DIR))
        for table in self.table_name:
            self.parse_label_text.set("Creating "+table+" table")
            self.parameter = []
            fp = open(PARSED_DB_DIR+table,"r")

            for line in fp.readlines():
                plmn = line.split(",")[0]
                for p in plmn.split("/")[1:]:
                    if p.split("-")[0] not in self.parameter:
                        self.parameter.append(p.split("-")[0])

                for csv in line.split(",")[1:]:
                    if csv.split("->")[0] not in self.parameter:
                        self.parameter.append(csv.split("->")[0])
            fp.close()

            query_1 = "CREATE TABLE IF NOT EXISTS "+table+" (PLMN VARCHAR(70),"
            query_2=""

            self.parameter[:]=(value for value in self.parameter if value != '\n')

            if (len(self.parameter)==0):
                continue
            for p in self.parameter:
                query_2+=p+"  VARCHAR(60),"
            query = query_1+query_2[:-1]+");"
            cursor=db.cursor()
            self.parse_progress['value'] += 1

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                x = "["+table+"]"
                sys.stdout.write("Creating table ")
                cprint("%5s"%table,'blue','on_white',attrs=['bold'])
                cursor.execute(query)
            cursor.close()
        db.commit()

    '''

    Update Table based on PARSED_DATABASE file

    '''
    def Updatetable(self):
        db = MySQLdb.connect(self.sql_host,self.sql_user,self.sql_pass,self.sql_db)
        cursor = db.cursor()
        #fptest =open("C:\\qry.txt",'w+')
        self.parse_progress['value'] = 0
        self.parse_progress['maximum'] = len(self.table_name)
        for table in self.table_name:
            self.parse_label_text.set("Updating "+table+" table")
            fp = open(PARSED_DB_DIR+table,"r")
            data =[]
            param=[]
            plmn = []
            for line in fp.readlines():
                data =[line.split(",")[0]]          #['PLMN-PLMN/BSC-372586/BCF-9/BTS-99/TRX-9']

                param=['PLMN']
                plmn = line.split(",")[0]           # PLMN-PLMN/BSC-372586/BCF-9/BTS-99/TRX-9

                for p in plmn.split("/")[1:]:       # ['BSC-372586', 'BCF-9', 'BTS-99', 'TRX-9']
                    #print p
                    data.append(p.split("-")[1])    # 372586
                    param.append(p.split("-")[0])   # BSC
                #if table=="BTS":
                    #fptest.writelines(line)
                for csv in line.split(",")[1:-1]:
                    if csv.split("->")[0] not in param:
                        #print csv.split("->")[1]

                        data.append(csv.split("->")[1])
                        param.append(csv.split("->")[0])
                if len(param)<2:
                    continue
                data = str(data).replace("[","(")
                param = str(param).replace("[","(").replace("'","")
                query =  "INSERT INTO "+table+" "+param.replace("]",")")+" VALUES"+data.replace("]",")")+";"
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")

                    cursor.execute(query)
            sys.stdout.write("Data inserted to ")
            cprint("%5s"%table,'blue','on_cyan')
            self.parse_progress['value'] += 1
            #fptest.writelines("\n")

        cursor.close()
        db.commit()
        #fptest.close()
        fp.close()
        self.parse_label_text.set("Database(myflexml) is up to date")

    def modifyTable(self):
        db = MySQLdb.connect(self.sql_host,self.sql_user,self.sql_pass,self.sql_db)
        cursor = db.cursor()
        cursor.execute("ALTER TABLE bts ADD lacCI VARCHAR(60) AFTER bts;")
        cursor.execute("UPDATE bts SET lacCI = concat(bts.locationareaidlac,bts.cellid);")

        cursor.execute("ALTER TABLE trx ADD match_plmn VARCHAR(60) AFTER plmn;")

        cursor.execute("UPDATE trx SET match_plmn = SUBSTRING_INDEX(trx.plmn,'/', 4);")
        cursor.execute("alter table adce ADD tgtBTS varchar(60) after BTS, ADD tgtBSC varchar(60) after BTS;")

        cursor.execute("UPDATE adce SET tgtBTS = SUBSTRING_INDEX(targetCellDN,'/', -3);")
        cursor.execute("UPDATE adce SET tgtBSC = SUBSTRING_INDEX(tgtBTS,'/', 1);")
        cursor.execute("UPDATE adce SET tgtBSC = SUBSTRING_INDEX(tgtBSC,'-', -1);")

        cursor.execute("UPDATE adce SET tgtBTS = SUBSTRING_INDEX(tgtBTS,'/', -1);")
        cursor.execute("UPDATE adce SET tgtBTS = SUBSTRING_INDEX(tgtBTS,'-', -1);")

        #cursor.execute("ALTER TABLE adce ADD match_plmn VARCHAR(60) AFTER plmn;")
        #cursor.execute("UPDATE adce SET match_plmn = SUBSTRING_INDEX(adce.plmn,'/', 4);")
        #cursor.execute("ALTER TABLE adce ADD tgtLacCI VARCHAR(60) AFTER bts, ADD srcLacCI VARCHAR(60) after bts;")
        #cursor.execute("update adce t1 inner join bts t2 on t1.match_plmn = t2.plmn set t1.srcLacCI = t2.lacci,tgtLacCI=concat(adjacentcellidlac,adjacentcellidci);")
        cursor.close()
        db.commit()

    def Drawline(self):

        cprint("\n----------------x----------------\n",attrs=['bold'])
        return 0

    def run(self):
        self.Dbdelcreate()
        obj = datetime.date.today()
        d = str(obj)
        mod_date = d.split("-")[2]+d.split("-")[1]+d[2:4]

        #XML_DB_DIR = config.XML_DB_DIR+mod_date+"\\"
        XML_DB_DIR = entry_2g_db_dir.get()+"XML_DATABASE\\"+mod_date+"\\"

        print XML_DB_DIR
        for xml_db in os.listdir(XML_DB_DIR):

            for f in os.listdir(PARSED_DB_DIR):
                os.remove(PARSED_DB_DIR+f)
            try:
                fp = open(XML_DB_DIR+xml_db,"r")
                fp2 = open(XML_DB_DIR+"_temp"+xml_db,"w+")
            except:
                cprint("Abnormal quit previously, Run again to fix it!","white","on_red",attrs=['bold'])
                sys.exit()
            for line in fp:
                if (line.find("DOCTYPE")<0):
                    fp2.write(line)
            fp.close()
            fp2.close()
            os.remove(XML_DB_DIR+xml_db)
        self.total_count.set(len(os.listdir(XML_DB_DIR)))
        self.parse_progress['value'] = 0
        self.parse_progress['maximum'] = self.total_count.get()
        for xml_db in os.listdir(XML_DB_DIR):
            os.rename(XML_DB_DIR+xml_db,XML_DB_DIR+xml_db.replace("_temp",""))

        #Mysignature()

        self.Drawline()
        #---------------------------------------------------------------------------


        cprint("Parsing Started",'green',attrs=['bold'])

        self.Drawline()
        headlines=[]
        #fpp = open("C:\\check.txt","a+")
        #----------------------------FILE PARSING-----------------------------------
        for xml_db in os.listdir(XML_DB_DIR):
            cprint("Parsing "+xml_db, 'white', 'on_blue')
            parse(XML_DB_DIR+xml_db, ManagedObjectHandler(headlines, self.parse_progress, self.parse_label_text,
                                                          self.total_count,self.completed_count,
                                                          self.remaining_count))
            self.parse_label_text.set("Parsing "+xml_db)
            self.parse_progress['value'] += 1
            self.completed_count.set(self.parse_progress['value'])
            remaining = int(self.total_count.get()) - int(self.completed_count.get())
            self.remaining_count.set(str(remaining))
        self.Drawline()

        cprint("MySQL in action", 'cyan', attrs=['bold'])

        self.Drawline()

        self.Createtable()

        self.Drawline()

        cprint("Table creation completed",'magenta',attrs=['bold'])

        self.Drawline()

        self.Updatetable()

        self.Drawline()

        cprint("Table update completed",'blue',attrs=['bold'])

        self.Drawline()

        #sql.modifyTable()

        cprint(" **** XML File parsing done ****\n",'green',attrs=['bold'])

PARSED_DB_DIR = entry_2g_db_dir.get()+"PARSED_DATABASE\\"