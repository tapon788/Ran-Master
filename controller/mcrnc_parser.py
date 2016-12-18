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

    def __init__(self, headlines, in_parse_progress, in_parse_label_text, in_total_count,
                 in_completed_count, in_remaining_count):
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

        self.RNC = []
        self.WBTS = []
        self.WCEL = []
        self.FMCS = []
        self.FMCG = []
        self.FMCI = []
        self.IPBR = []
        self.IPNB = []
        self.IPQM = []
        self.IUCS = []
        self.IUCSIP = []
        self.IUPS = []
        self.IUPSIP = []
        self.RNAC = []
        self.RNFC = []
        self.RNHSPA = []
        self.RNMOBI = []
        self.RNPS = []
        self.RNRLC = []
        self.RNTRM = []
        self.WAC = []
        self.ADJG = []
        self.ADJS = []

        # **************************POINT2*****************************

        self.ALL = [
            self.RNC,
            self.WBTS,
            self.WCEL,
            self.FMCS,
            self.FMCG,
            self.FMCI,
            self.IPBR,
            self.IPNB,
            self.IPQM,
            self.IUCS,
            self.IUCSIP,
            self.IUPS,
            self.IUPSIP,
            self.RNAC,
            self.RNFC,
            self.RNHSPA,
            self.RNMOBI,
            self.RNPS,
            self.RNRLC,
            self.RNTRM,
            self.WAC,
            self.ADJG,
            self.ADJS
        ]

        # **************************POINT3*****************************

        self.grep = [
            "RNC",
            "WBTS",
            "WCEL",
            "FMCS",
            "FMCG",
            "FMCI",
            "IPBR",
            "IPNB",
            "IPQM",
            "IUCS",
            "IUCSIP",
            "IUPS",
            "IUPSIP",
            "RNAC",
            "RNFC",
            "RNHSPA",
            "RNMOBI",
            "RNPS",
            "RNRLC",
            "RNTRM",
            "WAC",
            "ADJG",
            "ADJS"
        ]
        self.sql_user = "root"
        self.sql_pass = ""
        self.sql_host = "localhost"
        self.sql_db = "myrncml"

    def startElement(self, name, Attributes):
        self.param_name = Attributes.values()

        if name == 'managedObject':
            self.param_name = []
            self.isdata = ""
            self.param_value = []
            self.param_list = []
            self.class_name = Attributes.values()[(Attributes.keys().index('class'))]

            if self.class_name in self.grep:
                self.in_headline = True
            self.class_address = Attributes.values()[(Attributes.keys().index('distName'))]

    def characters(self, string):
        if self.in_headline:
            string = string.rstrip()
            if len(string) > 0:
                self.isdata = string
            else:
                self.isdata = "No_Data"

    def endElement(self, name):

        self.param_list.append(self.param_name)
        self.param_value.append(self.isdata)

        if name == 'managedObject':
            if self.in_headline:
                #print "\n\nParameter list for "+self.class_name+": "
                self.in_headline = False
                self.array_maker()

        if name =='raml':

            self.file_writer()

    def array_maker(self):
        if self.class_name in self.grep:

            line=""
            for paramName,paramVal in map(None,self.param_list,self.param_value):
                if (paramName==[] or paramVal=="No_Data"):
                    continue
                line =line+str(paramName)[3:-2]+"->"+str(paramVal)+","

            #**************************POINT4*****************************

            def rnc():
                self.RNC.append(str(self.class_address)+","+line)

            def wbts():
                self.WBTS.append(str(self.class_address)+","+line)

            def wcel():
                self.WCEL.append(str(self.class_address)+","+line)

            def fmcs():
                self.FMCS.append(str(self.class_address)+","+line)

            def fmcg():
                self.FMCG.append(str(self.class_address)+","+line)

            def fmci():
                self.FMCI.append(str(self.class_address)+","+line)

            def ipbr():
                self.IPBR.append(str(self.class_address)+","+line)

            def ipnb():
                self.IPNB.append(str(self.class_address)+","+line)

            def ipqm():
                self.IPQM.append(str(self.class_address)+","+line)

            def iucs():
                self.IUCS.append(str(self.class_address)+","+line)

            def iucsip():
                self.IUCSIP.append(str(self.class_address)+","+line)

            def iups():
                self.IUPS.append(str(self.class_address)+","+line)

            def iupsip():
                self.IUPSIP.append(str(self.class_address)+","+line)

            def rnac():
                self.RNAC.append(str(self.class_address)+","+line)

            def rnfc():
                self.RNFC.append(str(self.class_address)+","+line)

            def rnhspa():
                self.RNHSPA.append(str(self.class_address)+","+line)

            def rnmobi():
                self.RNMOBI.append(str(self.class_address)+","+line)

            def rnps():
                self.RNPS.append(str(self.class_address)+","+line)

            def rnrlc():
                self.RNRLC.append(str(self.class_address)+","+line)

            def rntrm():
                self.RNTRM.append(str(self.class_address)+","+line)

            def wac():
                self.WAC.append(str(self.class_address)+","+line)

            def adjg():
                self.ADJG.append(str(self.class_address)+","+line)

            def adjs():
                self.ADJS.append(str(self.class_address)+","+line)





            #**************************POINT5*****************************

            options={
            "RNC":rnc,
            "WBTS":wbts,
            "WCEL":wcel,
            "FMCS":fmcs,
            "FMCG":fmcg,
            "FMCI":fmci,
            "IPBR":ipbr,
            "IPNB":ipnb,
            "IPQM":ipqm,
            "IUCS":iucs,
            "IUCSIP":iucsip,
            "IUPS":iups,
            "IUPSIP":iupsip,
            "RNAC":rnac,
            "RNFC":rnfc,
            "RNHSPA":rnhspa,
            "RNMOBI":rnmobi,
            "RNPS":rnps,
            "RNRLC":rnrlc,
            "RNTRM":rntrm,
            "WAC":wac,
            "ADJG":adjg,
            "ADJS":adjs
            }
            options[self.class_name]()



    def file_writer(self):
        #print self.ALL
        #print self.grep
        print "Writing parsed DB"
        for fname in self.grep:
            print fname

            file_name = PARSED_DB_DIR+fname

            fp = open(file_name, "a+")
            for data in self.ALL[self.grep.index(fname)]:
                fp.writelines(data)
                print data
                fp.writelines('\n')
            fp.close()

        '''
        SQL operations

        '''
    def Dbdelcreate(self):
        db = MySQLdb.connect(self.sql_host, self.sql_user, self.sql_pass)
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS myrncml;")
        cursor.close()
        db.commit()

        db = MySQLdb.connect(self.sql_host,self.sql_user,self.sql_pass,self.sql_db)
        cursor = db.cursor()
        cursor.execute("DROP DATABASE IF EXISTS myrncml; CREATE DATABASE myrncml;")
        cursor.close()
        db.commit()

    def Createtable(self):
        db = MySQLdb.connect(self.sql_host, self.sql_user, self.sql_pass, self.sql_db)
        self.table_name = os.listdir(PARSED_DB_DIR)
        self.parse_progress['value'] = 0
        self.parse_progress['maximum'] = len(os.listdir(PARSED_DB_DIR))

        print self.table_name

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

            query_1 = "CREATE TABLE IF NOT EXISTS "+table+" (PLMN VARCHAR(60),"
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
        self.parse_progress['value'] = 0
        self.parse_progress['maximum'] = len(os.listdir(PARSED_DB_DIR))

        for table in self.table_name:
            self.parse_label_text.set("Updating "+table+" table")
            print table
            fp = open(PARSED_DB_DIR+table,"r")
            data =[]
            param=[]
            plmn = []
            for line in fp.readlines():
                data =[line.split(",")[0]]
                param=['PLMN']
                plmn = line.split(",")[0]
                for p in plmn.split("/")[1:]:
                    data.append(p.split("-")[1])
                    param.append(p.split("-")[0])
                for csv in line.split(",")[1:-1]:
                    if csv.split("->")[0] not in param:
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

        cursor.close()
        db.commit()
        fp.close()
        self.parse_label_text.set("Database(myrncml) is up to date")

    def Drawline(self):

        cprint("\n----------------x----------------\n",attrs=['bold'])
        return 0
    def run(self):

        self.Dbdelcreate()

        obj = datetime.date.today()
        d = str(obj)
        mod_date = d.split("-")[2]+d.split("-")[1]+d[2:4]

        #XML_DB_DIR = config1.XML_DB_DIR+mod_date+"\\"
        #print XML_DB_DIR


        XML_DB_DIR = entry_3g_db_dir.get()+"XML_DATABASE\\"+mod_date+"\\"

        print "XML_DB_DIR: "+XML_DB_DIR
        print "PARSED_DB_DIR: "+PARSED_DB_DIR
        for xml_db in os.listdir(XML_DB_DIR):

            for f in os.listdir(PARSED_DB_DIR):
                os.remove(PARSED_DB_DIR+f)
            try:
                fp = open(XML_DB_DIR+xml_db,"r")
                fp2 = open(XML_DB_DIR+"_temp"+xml_db,"w+")
                print "Creating temporary files"
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

        cprint("Parsing Started",'green',attrs=['bold'])

        self.Drawline()
        headlines=[]
        for xml_db in os.listdir(XML_DB_DIR):
            cprint("Parsing "+xml_db,'white','on_blue')
            parse(XML_DB_DIR+xml_db, ManagedObjectHandler(headlines, self.parse_progress, self.parse_label_text,
                                                          self.total_count,
                                                          self.completed_count, self.remaining_count))
            self.parse_label_text.set("Parsing "+xml_db)

            self.parse_progress['value'] += 1
            self.completed_count.set(self.parse_progress['value'])
            remaining = int(self.total_count.get()) - int(self.completed_count.get())
            self.remaining_count.set(str(remaining))

        self.Drawline()

        cprint("MySQL in action",'cyan',attrs=['bold'])

        self.Drawline()

        self.Createtable()

        self.Drawline()

        cprint("Table creation completed",'magenta',attrs=['bold'])

        self.Drawline()

        self.Updatetable()

        self.Drawline()

        cprint("Table update completed",'blue',attrs=['bold'])

        self.Drawline()

        cprint(" **** XML File parsing done ****\n",'green',attrs=['bold'])

PARSED_DB_DIR = entry_3g_db_dir.get()+"PARSED_DATABASE\\"