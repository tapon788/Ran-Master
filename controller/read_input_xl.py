__author__ = 'tpaul'

import xlrd


class ReadInput:

    def __init__(self, input_file, update_flag):
        self.input_file = input_file
        self.update_flag = update_flag
        self.injection_error_flag = 0
        pass

    def read_excel(self, adjType):
        from adjg_input_model import Input
        Input.sourceLac = []
        Input.sourceCI = []
        Input.targetLac = []
        Input.targetCI = []
        Input.injectionParameterName = []
        Input.injectionParameterValue = []

        sh1 = None
        input_dict = {}
        input_dict.clear()
        self.parameterNameArray = []

        lacKey = adjType[0].upper()+adjType[1:].lower()+'LAC'
        ciKey = adjType[0].upper()+adjType[1:].lower()+'CI'
        wb = xlrd.open_workbook(self.input_file)
        print self.input_file, adjType
        sh1 = wb.sheet_by_name(adjType)
        self.basicParameterNameArray = ['sourceLac', 'sourceCI', lacKey, ciKey]

        # Fix or default parameter read
        for rownum in range(2, sh1.nrows):
            Input.sourceLac.append(str(sh1.row_values(rownum)[Input.indexSourceLac]).split(".")[0])
            Input.sourceCI.append(str(sh1.row_values(rownum)[Input.indexSourceCI]).split(".")[0])
            Input.targetLac.append(str(sh1.row_values(rownum)[Input.indexTargetLac]).split(".")[0])
            Input.targetCI.append(str(sh1.row_values(rownum)[Input.indexTargetCI]).split(".")[0])

        # Injection parameter read
        for colnum in range(7, sh1.ncols):
            if sh1.col_values(colnum)[1] == '':
                continue
            else:
                p_name = str(sh1.col_values(colnum)[1].split('(')[0].strip())
                # if adjType+'LAC' is injection parameter, 'NEW' is appended to segregate targetLAC from dictionary
                if p_name == lacKey:
                    Input.injectionParameterName.append(p_name+'NEW')

                else:
                    Input.injectionParameterName.append(p_name)

                try:
                    Input.injectionParameterValue.append(map(int, sh1.col_values(colnum)[2:]))
                except:
                    self.injection_error_flag = 1
                    Input.injectionParameterName.pop()



        input_dict = dict(zip(self.basicParameterNameArray,
                              (Input.sourceLac, Input.sourceCI, Input.targetLac, Input.targetCI,)))

        input_injection_dict = zip(Input.injectionParameterName, Input.injectionParameterValue)
        # Fix or Default parameter dictionary + Injection Parameter dictionary
        input_dict.update(input_injection_dict)

        return input_dict
