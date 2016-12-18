__author__ = 'tpaul'
import os


class ReadConfig:

    def __init__(self):
        print "ReadConfig called"
        self.label_name = []
        self.label_value = []
        pass

    def reader(self):
        print os.getcwd()
        fp = open(os.getcwd()+'\\resources\\test.conf')
        for line in fp.readlines():
            self.label_name.append(line.split("=")[0].strip())
            self.label_value.append(line.split("=")[1].strip())
        fp.close()
        return self.label_name, self.label_value