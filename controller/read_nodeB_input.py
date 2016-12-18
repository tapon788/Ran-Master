__author__ = 'tapon'

import xlrd
from create_nodeB import CreateNodeB

class ReadNodeBInput:

    def __init__(self, filename):

        self.filename = filename
        self.wb = None
        self.parameter_set = []
        self.template_parameter_name = []
        self.template_parameter_value = []
        self.template_parameter_set = []
        pass

    def open_file(self):
        self.wb = xlrd.open_workbook(self.filename)
        pass

    def read_ipnb(self):
        sheet_ipnb = self.wb.sheet_by_name("IPNB")

        for rownum in range(sheet_ipnb.nrows):
            #print "\n---------------------\n"
            parameters = []
            for colnum in range(sheet_ipnb.ncols):
                if len(str(sheet_ipnb.col_values(colnum)[rownum]).split(".")) == 2:
                    parameters.append(str(sheet_ipnb.col_values(colnum)[rownum]).split(".")[0])
                else:
                    parameters.append(str(sheet_ipnb.col_values(colnum)[rownum]))
                pass
            self.parameter_set.append(parameters)

        parameter_name = self.parameter_set[0]
        parameter_value = self.parameter_set[1:]
        print "\n\nIPNB\n"
        print parameter_name
        print parameter_value

        aNodeB = CreateNodeB(parameter_name, parameter_value, "IPNB", self.template_parameter_name, self.template_parameter_value)
        aNodeB.remove_contents()  # Clear nodeB_ALL file
        aNodeB.create_ipnb()



    def read_wbts(self):

        self.parameter_set = []
        sheet_wbts = self.wb.sheet_by_name("WBTS")
        print sheet_wbts
        for rownum in range(sheet_wbts.nrows):
            #print "\n---------------------\n"
            parameters = []
            for colnum in range(sheet_wbts.ncols):
                parameters.append(str(sheet_wbts.col_values(colnum)[rownum]).split(".")[0])
                #print str(sheet_wcel.col_values(colnum)[rownum]).split(".")[0]
            self.parameter_set.append(parameters)

        parameter_name = self.parameter_set[0]
        parameter_value = self.parameter_set[1:]
        print "\n\nWBTS\n"
        print parameter_name
        print parameter_value
        aNodeB = CreateNodeB(parameter_name, parameter_value, "WBTS", self.template_parameter_name,self.template_parameter_value)
        aNodeB.create_wbts()
        pass

    def read_wcel(self):

        self.parameter_set = []
        sheet_wcel = self.wb.sheet_by_name("WCEL")


        '''

        for colnum in range(sheet_wcel.ncols):
            print "\n---------------------\n"
            for rownum in range(sheet_wcel.nrows):
                parameters.append(str(sheet_wcel.row_values(rownum)[colnum]).split(".")[0])
            self.parameter_set.append(parameters)
        print self.parameter_set
        '''


        for rownum in range(sheet_wcel.nrows):
            #print "\n---------------------\n"
            parameters = []
            for colnum in range(sheet_wcel.ncols):
                parameters.append(str(sheet_wcel.col_values(colnum)[rownum]).split(".")[0])
                #print str(sheet_wcel.col_values(colnum)[rownum]).split(".")[0]
            self.parameter_set.append(parameters)

        #print self.parameter_set

        parameter_name = self.parameter_set[0]
        parameter_value = self.parameter_set[1:]
        print "\n\nWCEL\n"
        print parameter_name
        print parameter_value

        aNodeB = CreateNodeB(parameter_name, parameter_value, "WCEL", self.template_parameter_name,self.template_parameter_value)
        aNodeB.create_wcel()
        pass


    def read_template(self):

        sheet_wcel = self.wb.sheet_by_name("WCEL_TEMPLATE")
        for rownum in range(sheet_wcel.nrows):
            self.template_parameter_name.append(str(sheet_wcel.row_values(rownum)[0]).split(".")[0])
            self.template_parameter_value.append(str(sheet_wcel.row_values(rownum)[1]).split(".")[0])

        #print self.template_parameter_name, self.template_parameter_value
        pass




'''
if __name__ == '__main__':
    aInput = ReadNodeBInput('D:\NodeBCrTemp.xlsx')
    aInput.open_file()
     #aInput.read_ipnb()
    aInput.read_template()
    aInput.read_wcel()
'''