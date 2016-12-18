#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      tapon
#
# Created:     15/09/2014
# Copyright:   (c) tapon 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import MySQLdb
from lxml import etree as ET
import sys,time
class managedObject:
    def __init__(self):
        self.paramName = ["name","AdjgMCC","AdjgMNC","AdjgLAC","AdjgCI","AdjgNCC","AdjgBCC","AdjgBCCH","AdjgBandIndicator","AdjgSIB","AdjgTxPwrMaxRACH","AdjgTxPwrMaxTCH","NrtHopgIdentifier","RtHopgIdentifier"]

    def mo_handler_createNew(self,name,AdjgLAC,AdjgCI,AdjgNCC,AdjgBCC,AdjgBCCH,AdjgNband):

        array_length = len(name)
        array_length = len(name)
        AdjgMCC = ["470"]*array_length
        AdjgMNC = ["03"]*array_length
        AdjgBandIndicator = ["0"]*array_length
        AdjgSIB = ["1"]*array_length
        NrtHopgIdentifier=["1"]*array_length
        RtHopgIdentifier=["1"]*array_length
        var_par =self.bandBasedParam(AdjgNband)
        #print var_par
        AdjgTxPwrMaxRACH=var_par[0]
        AdjgTxPwrMaxTCH = var_par[1]

        data_array = (adjgname,AdjgMCC,AdjgMNC,AdjgLAC,AdjgCI,AdjgNCC,AdjgBCC,AdjgBCCH,AdjgBandIndicator,AdjgSIB,AdjgTxPwrMaxRACH,AdjgTxPwrMaxTCH,NrtHopgIdentifier,RtHopgIdentifier,new_ADJG_ID)
        raml = ET.Element("raml")
        raml.set("version","1.0")
        raml.set("xmlns","raml20.xsd")
        cmData = ET.SubElement(raml,"cmData")
        cmData.set("type","plan")
        cmData.set("name","NSN_NPO")
        header = ET.SubElement(cmData,"header")
        log = ET.SubElement(header,"log")
        log.set("user","ab212ba")
        log.set("dateTime",time.ctime()) # Need to change
        log.set("action","created")
        log.set("appInfo","NPO_EJ")
        log.text = "No Description"
        for i in range(0,len(AdjgNCC)):
            index = -1

            mo = ET.SubElement(cmData,"managedObject")
            mo.set("class","ADJG")
            mo.set("distName",plmnID[i])
            mo.set("operation","create")
            for parameter in self.paramName:
                index+=1
                p = ET.SubElement(mo, "p")
                p.set("name", self.paramName[index])
                p.text =data_array[index][i]


        tree = ET.ElementTree(raml)
        x = ET.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8",doctype="<!DOCTYPE raml SYSTEM 'raml20.dtd'>")
        fp = open("E:\\3gext\NewADJG_create.xml","w+")
        fp.write(ET.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8",doctype="<!DOCTYPE raml SYSTEM 'raml20.dtd'>"))
        fp.close()
        pass


    def bandBasedParam(self,in_AdjgNband):
        rach = []
        tch = []
        for i in in_AdjgNband:
            if int(i)==900:
                rach.append('33')
                tch.append('33')
            else:
                rach.append('30')
                tch.append('30')
        return (rach,tch)




    def mo_handler_create(self,in_data,in_presentCI,in_tgtLAC,in_tgtNCC,in_tgtBCC,in_tgtBCCH):
        raml = ET.Element("raml")
        raml.set("version","1.0")
        raml.set("xmlns","raml20.xsd")
        cmData = ET.SubElement(raml,"cmData")
        cmData.set("type","plan")
        cmData.set("name","NSN_NPO")
        header = ET.SubElement(cmData,"header")
        log = ET.SubElement(header,"log")
        log.set("user","ab212ba")
        log.set("dateTime",time.ctime()) # Need to change
        log.set("action","created")
        log.set("appInfo","NPO_EJ")
        log.text = "No Description"
        cnt1 = -1
        for row in in_data:
            cnt1+=1
            indx_adjgbcch = in_presentCI.index(row[5])
            mo = ET.SubElement(cmData,"managedObject")
            mo.set("class","ADJG")
            mo.set("distName",row[0])
            mo.set("operation","create")
            sys.stdout.write("HO found [SOURCE] %-42.42s and [TARGET] %s\n"%(row[0],row[1]))
            cnt = -1
            for item in row[1:]:
                cnt+=1
                p = ET.SubElement(mo, "p")
                p.set("name", self.paramName[cnt])
                if self.paramName[cnt]=="AdjgLAC":
                    p.text =in_tgtLAC[indx_adjgbcch]

                elif self.paramName[cnt]=="AdjgNCC":
                    p.text =in_tgtNCC[indx_adjgbcch]

                elif self.paramName[cnt]=="AdjgBCC":
                    p.text =in_tgtBCC[indx_adjgbcch]

                elif self.paramName[cnt]=="AdjgBCCH":
                    p.text =in_tgtBCCH[indx_adjgbcch]
                else:
                    p.text =item
        tree = ET.ElementTree(raml)

        fp = open("E:\\3gext\ADJG_create.xml","w+")
        fp.write(ET.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8",doctype="<!DOCTYPE raml SYSTEM 'raml20.dtd'>"))
        fp.close()
        print "\n********************\nNumber of input "+str(len(tgtLAC))
        print "Number of relation found "+str(len(in_data))+"\n******************** "
        pass


    def mo_handler_delete(self,in_data):
        raml = ET.Element("raml")
        raml.set("version","2.0")
        raml.set("xmlns","raml20.xsd")
        cmData = ET.SubElement(raml,"cmData")
        cmData.set("type","plan")
        cmData.set("name","NSN_NPO")
        header = ET.SubElement(cmData,"header")
        log = ET.SubElement(header,"log")
        log.set("user","ab212ba")
        log.set("dateTime",time.ctime()) # Need to change
        log.set("action","created")
        log.set("appInfo","NPO_EJ")
        log.text = "No Description"

        cnt=-1
        for row in in_data:
            cnt+=1
            mo = ET.SubElement(cmData,"managedObject")
            mo.set("class","ADJG")
            mo.set("distName",row[0])
            mo.set("operation","delete")
            cnt = -1
            for item in row[1:6]:
                cnt+=1
                p = ET.SubElement(mo, "p")
                p.set("name", self.paramName[cnt])
                p.text =item
        tree = ET.ElementTree(raml)
        fp = open("E:\\3gext\ADJG_delete.xml","w+")
        fp.write(ET.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8",doctype="<!DOCTYPE raml SYSTEM 'raml20.dtd'>"))
        fp.close()

    #NAC menas New ADJG Create

    def readinput_NAC(self):
        raw_NAC_input = []
        fp = open("E:\\3gext\inputADJG1.csv")

        for line in fp.readlines():
            raw_NAC_input.append(line)
        fp.close()
        return raw_NAC_input
        pass
    def paramArray_NAC(self,in_raw_NAC_input):
        name=[]
        #adjgname = []
        AdjgLAC = []
        AdjgCI = []
        AdjgNCC=[]
        AdjgBCC=[]
        AdjgBCCH=[]
        AdjgNband=[]
        for i in in_raw_NAC_input[1:]:
            #print i.split(",")

            name.append(i.split(",")[0])

            adjgname.append(i.split(",")[8])
            AdjgLAC.append(i.split(",")[10])
            AdjgCI.append(i.split(",")[11])
            AdjgNCC.append(i.split(",")[13].split("-")[0])
            AdjgBCC.append(i.split(",")[13].split("-")[1])
            AdjgBCCH.append(i.split(",")[12])
            AdjgNband.append(i.split(",")[9])
        return(name,AdjgLAC,AdjgCI,AdjgNCC,AdjgBCC,AdjgBCCH,AdjgNband)
        pass


class sql_handler:
    def __init__(self):
        pass
    def sqldata(self,sql_cmd):
        cmd = sql_cmd
        db = MySQLdb.connect('localhost','root','','myrncml')
        cursor = db.cursor()

        cursor.execute(cmd)
        data = cursor.fetchall()
        cursor.close()
        return data


    def query_filter(self):
        present_LAC = []
        present_CI = []
        target_LAC = []
        target_BCC =[]
        target_NCC = []
        target_BCCH = []
        fp = open("E:\\3gext\input.csv","r")
        for line in fp.readlines()[1:]:
            present_LAC.append(line.split(",")[0])
            present_CI.append(line.split(",")[1])
            target_LAC.append(line.split(",")[2])
            target_NCC.append(line.split(",")[3])
            target_BCC.append(line.split(",")[4])
            target_BCCH.append(line.split(",")[5].replace("\n",""))

        query_filter_string = ""
        for i in range(len(present_CI)):
             if i==len(present_CI)-1:
                query_filter_string = query_filter_string + "adjgLAC= "+present_LAC[i]+" and adjgCI= "+present_CI[i]
             else:

                query_filter_string = query_filter_string + "adjgLAC= "+present_LAC[i]+" and adjgCI= "+present_CI[i]+" or "

        sql_cmd_fixed = "select plmn,name,AdjgMCC,AdjgMNC,AdjgLAC,AdjgCI,AdjgNCC,AdjgBCC,AdjgBCCH,AdjgBandIndicator,AdjgSIB,AdjgTxPwrMaxRACH,AdjgTxPwrMaxTCH,NrtHopgIdentifier,RtHopgIdentifier from adjg where "
        sql_cmd  = sql_cmd_fixed+query_filter_string+";"
        data_array = self.sqldata(sql_cmd)
        fp.close()
        return data_array,present_CI,target_LAC,target_NCC,target_BCC,target_BCCH

    def setAdjgID(self,in_name):
        dump=[]
        dump = range(1,32)
        query_sub_string=" name like \"%"+in_name+"%\""
        db = MySQLdb.connect('localhost','root','','myrncml')
        cursor = db.cursor()
        cmd = "select plmn from wcel where "+query_sub_string+";"
        #print cmd
        cursor.execute(cmd)
        data = cursor.fetchall()

        plmn =  data[0][0]
        print "Associated PLMN "+plmn
        query_sub_string ="\"%"+plmn+"%\""

        cmd = "select adjg from adjg where plmn like "+query_sub_string+";"
        #print cmd
        cursor.execute(cmd)
        data = cursor.fetchall()
        cursor.close()
        adjgid = []
        for row in data:
            adjgid.append(int(row[0]))

        adjgid.sort()

        print "Printing adjgid"
        print adjgid
        if plmn not in wcel:

            wcel.append(plmn)
            del offset[:]
            print "Printing Offset"
            print offset
            d =  list((set(dump) - set(adjgid))-set(offset))
            print "Printing d"
            print d
            print "Chosen d[0]: "+str(d[0])
            plmnID.append(plmn+"/ADJG-"+str((d[0])))

            offset.append(d[0])
        else:
            print "Printing Offset"
            print offset
            d = list((set(dump) - set(adjgid))-set(offset))
            plmnID.append(plmn+"/ADJG-"+str((d[0])))
            print "Printing d"
            print d
            print "Chosen d[0]: "+str(d[0])
            offset.append(d[0])


        return (d[0])


    '''
        offsetaary.append(offset)

        db = MySQLdb.connect('localhost','root','','myrncml')
        cursor = db.cursor()
        id = str(d[0])
        pl =plmn+"/ADJG-"+str((d[0]))
        cmd ='Insert into ADJG(PLMN,ADJG) VALUES(\"'+pl+'\",\"'+id+'\");'
        cursor.execute(cmd)


        cursor.close()
        db.commit()
    '''




if __name__ == '__main__':
    wcel=[]
    offset = []
    offsetaary=[]
    plmnID = []
    adjgname = []


    print "\n\t\t\tTime is : " +time.ctime()+"\n"

    operation_type = raw_input("write 'EXT' for Extrenal update and 'NEW' for new ADJG creation ")
    MO_OBJ = managedObject()
    SQL_OBJ = sql_handler()
    data = SQL_OBJ.query_filter()[0]

    if operation_type=="EXT":
        #SQL_OBJ = sql_handler()
        #data = SQL_OBJ.query_filter()[0]
        presentCI = SQL_OBJ.query_filter()[1]
        tgtLAC = SQL_OBJ.query_filter()[2]
        tgtNCC = SQL_OBJ.query_filter()[3]
        tgtBCC = SQL_OBJ.query_filter()[4]
        tgtBCCH = SQL_OBJ.query_filter()[5]
        #print len(tgtLAC),len(tgtBCC)
        print data
        print presentCI
        MO_OBJ.mo_handler_create(data,presentCI,tgtLAC,tgtNCC,tgtBCC,tgtBCCH)
        MO_OBJ.mo_handler_delete(data)
        print "Need to update external"
    elif operation_type == "NEW":
        rw_inp_NAC = MO_OBJ.readinput_NAC()
        prm_ary_NAC = MO_OBJ.paramArray_NAC(rw_inp_NAC)
        print prm_ary_NAC
        new_ADJG_ID = []
        for i in prm_ary_NAC[0]:
            print "cell name sent "+i
            new_Adjg_id = SQL_OBJ.setAdjgID(i)
            new_ADJG_ID.append(new_Adjg_id)
        #print new_ADJG_ID

        MO_OBJ.mo_handler_createNew(prm_ary_NAC[0],prm_ary_NAC[1],prm_ary_NAC[2],prm_ary_NAC[3],prm_ary_NAC[4],prm_ary_NAC[5],prm_ary_NAC[6])

        #print prm_ary_NAC[2]
    else:
        print "Please type correctly 'EXT' or 'NEW'"


