__author__ = 'tpaul'
from lxml import etree as et
import time
from lxml import _elementpath as _dummy
class XmlCreator:
    def __init__(self, dictionary, directory, in_adjtype, in_operation_type):
        self.operation_type = in_operation_type
        self.dictionary = dictionary
        self.directory = directory
        self.adjType = in_adjtype
        self.mccKey, self.mncKey, self.lacKey, self.ciKey = "", "", "", ""
        self.input_count = len(self.dictionary['sourceLac'])
        self.raml = ""
        self.cmData = ""

        self.prepare()
        self.header()
        self.core()
        self.footer()

    def prepare(self):
        self.mccKey = self.adjType[0].upper()+self.adjType[1:].lower()+'MCC'
        self.mncKey = self.adjType[0].upper()+self.adjType[1:].lower()+'MNC'
        self.lacKey = self.adjType[0].upper()+self.adjType[1:].lower()+'LAC'
        self.ciKey = self.adjType[0].upper()+self.adjType[1:].lower()+'CI'



        self.dictionary[self.mccKey] = ["470"]*self.input_count
        self.dictionary[self.mncKey] = ["03"]*self.input_count

        if self.adjType == 'ADJS':
            self.dictionary['HSDPAHopsIdentifier'] = ["2"]*self.input_count
            self.dictionary['RTWithHSDPAHopsIdentifier'] = ["2"]*self.input_count
            self.dictionary['NrtHopsIdentifier'] = ["1"]*self.input_count
            self.dictionary['RtHopsIdentifier'] = ["1"]*self.input_count

        elif self.adjType == 'ADJG':
            self.dictionary['NrtHopgIdentifier'] = ["1"]*self.input_count
            self.dictionary['RtHopgIdentifier'] = ["1"]*self.input_count

    def header(self):

        self.raml = et.Element("raml")
        self.raml.set("version", "1.0")
        self.raml.set("xmlns", "raml20.xsd")
        self.cmData = et.SubElement(self.raml, "cmData")
        self.cmData.set("type", "plan")
        self.cmData.set("name", "NSN_NPO")
        header = et.SubElement(self.cmData, "header")
        log = et.SubElement(header, "log")
        log.set("user", "ab212ba")
        log.set("dateTime", time.ctime()) # Need to change
        log.set("action", "created")
        log.set("appInfo", "NPO_EJ")
        log.text = "No Description"
        pass

    def core(self):
        if self.operation_type == "delete":
            self.core_del()
            return 0
        del self.dictionary['sourceLac']
        del self.dictionary['sourceCI']
        for i in range(self.input_count):
            if self.dictionary['distName'][i].split("-")[-1] == '0':
                    continue
            try:
                mo = et.SubElement(self.cmData, "managedObject")
                mo.set("class", self.adjType)
                mo.set("distName", self.dictionary['distName'][i])
            except IndexError:
                continue
            mo.set("operation", "create")

            for key, value in self.dictionary.iteritems():
                if key != 'distName':
                    p = et.SubElement(mo, "p")
                    p.set("name", key)
                    p.text = str(self.dictionary[key][i])
        pass

    def core_del(self):
        for i in range(self.input_count):
            if self.dictionary['distName'][i].split("-")[-1] == '0':
                    continue
            try:
                mo = et.SubElement(self.cmData, "managedObject")
                mo.set("class", self.adjType)
                mo.set("distName", self.dictionary['distName'][i])
            except IndexError:
                continue
            mo.set("operation", "delete")


    def footer(self):
        filename = self.directory+"/new_"+self.adjType+self.operation_type+".xml"
        tree = et.ElementTree(self.raml)
        x = et.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8", doctype="<!DOCTYPE raml SYSTEM 'raml20.dtd'>")
        fp = open(filename, "w+")
        fp.write(et.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8", doctype="<!DOCTYPE raml SYSTEM 'raml20.dtd'>"))
        fp.close()

        pass