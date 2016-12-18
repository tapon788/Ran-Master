__author__ = 'tapon'

from lxml import etree as et
from lxml import etree as et2
import time
from gui_interfaces.gui_settings import *


class CreateNodeB:

    def __init__(self, parameter_name, parameter_array, mo_name, template_param_name, template_param_value):

        self.parameter_name = parameter_name
        self.parameter_array = parameter_array
        self.mo_name = mo_name
        self.template_param_name = template_param_name
        self.template_param_value = template_param_value
        self.output_dir = entry_local_working_dir.get()



        print parameter_name
        print parameter_array
        pass


    def create_header(self):



        self.raml = et.Element("raml")
        self.raml.set("version", "1.0")
        self.raml.set("xmlns", "raml20.xsd")
        self.cmData = et.SubElement(self.raml, "cmData")
        self.cmData.set("type", "plan")
        self.cmData.set("name", "OMC_RND")
        header = et.SubElement(self.cmData, "header")
        log = et.SubElement(header, "log")
        log.set("user", "tapon1")
        log.set("dateTime", time.ctime()) # Need to change
        log.set("action", "created")
        log.set("appInfo", "OMCB")
        log.text = "No Description"
        et2 = et
        pass


    def create_ipnb(self):
        self.create_header()
        print "No of IPNB"+str(len(self.parameter_array))

        for i in range((len(self.parameter_array))):
            self.mo = et.SubElement(self.cmData, "managedObject")
            self.mo.set("class", self.mo_name)
            self.mo.set("distName", 'PLMN-PLMN\\RNC-173\\'+self.mo_name+"-"+self.parameter_array[i][0])
            self.mo.set("operation", "create")


            for j in range(len(self.parameter_array[i])):
                p = et.SubElement(self.mo, "p")


                p.set("name", self.parameter_name[j])
                p.text = str(self.parameter_array[i][j])
            self.create_full_nodeB()



        self.footer(self.mo_name, et)




    def create_wcel(self):
        self.create_header()
        print "No of WCEL"+str(len(self.parameter_array))
        for i in range((len(self.parameter_array))):
            self.mo = et.SubElement(self.cmData, "managedObject")
            self.mo.set("class", self.mo_name)
            self.mo.set("distName",
                   'PLMN-PLMN/RNC-'+self.parameter_array[i][0]+'/' +
                   'WBTS-'+self.parameter_array[i][1]+'/' +
                   'WCEL-'+self.parameter_array[i][2])
            self.mo.set("operation", "create")
            for j in range(3, len(self.parameter_array[i])):
                print self.parameter_array[i][j]
                if j == 8:
                    lst = et.SubElement(self.mo, "list")
                    lst.set("name",self.parameter_name[j])
                    p = et.SubElement(lst, "p")
                    p.text = str(self.parameter_array[i][j])
                else:


                    p = et.SubElement(self.mo, "p")
                    p.set("name", self.parameter_name[j])
                    p.text = str(self.parameter_array[i][j])

            for k in range(1,len(self.template_param_name)):

                p = et.SubElement(self.mo, "p")
                p.set("name", self.template_param_name[k])
                p.text = str(self.template_param_value[k])

            self.create_full_nodeB()

        self.footer(self.mo_name, et)

    def create_wbts(self):
        self.create_header()
        print "No of WBTS"+str(len(self.parameter_array))

        for i in range((len(self.parameter_array))):
            self.mo = et.SubElement(self.cmData, "managedObject")
            self.mo.set("class", self.mo_name)
            self.mo.set("distName", 'PLMN-PLMN\\RNC-173\\'+self.mo_name+"-"+self.parameter_array[i][0])
            self.mo.set("operation", "create")
            for j in range(len(self.parameter_array[i])):
                p = et.SubElement(self.mo, "p")
                p.set("name", self.parameter_name[j])
                p.text = str(self.parameter_array[i][j])
            self.create_full_nodeB()
        self.footer(self.mo_name, et)


    def footer(self, mo_name, in_et):
        et = in_et
        filename = self.output_dir+"nodeB_"+mo_name+".xml"
        tree = et.ElementTree(self.raml)
        #x = et.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8", doctype="<!DOCTYPE raml SYSTEM 'raml20.dtd'>")
        fp = open(filename, "w+")
        fp.write(et.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8", doctype="<!DOCTYPE raml SYSTEM 'raml20.dtd'>"))
        fp.close()

        pass

    def create_full_nodeB(self):

        fp = open(self.output_dir+"newNodeB.xml", "a+")
        tree2 = et.ElementTree(self.mo)
        fp.write(et.tostring(tree2, pretty_print=True))
        fp.close()
        pass

    def remove_contents(self):
        fp = open(self.output_dir+"newNodeB.xml", "w+")
        fp.close()


