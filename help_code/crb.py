#!/usr/bin/python
import commands,time,datetime,sys,os

class crb:
    def __init__(self):
        self.script_dir = ""
        self.resource_dir = ""
        self.backup_dir = ""
        self.remote_host = ""
        self.remote_user = ""
        self.remote_pass = ""
        self.remote_backup_dir = ""
        self.cmd_array=[]
        self.cmd_array.append("/root/backup_cmd")
        self.date = str(datetime.date.today()).replace("-","")
        pass

    def readConfigFile(self):
        fp = open("/sbin/RNC_BACKUP_RESOURCE/rnc_backup_config.txt","r")
        info  =  fp.readlines()
        self.script_dir = info[0].split("=")[1].strip()
        self.resource_dir = info[1].split("=")[1].strip()
        self.backup_dir = info[2].split("=")[1].strip()
        self.remote_host =info[3].split("=")[1].strip()
        self.remote_user =info[4].split("=")[1].strip()
        self.remote_pass =info[5].split("=")[1].strip()
        self.remote_backup_dir =info[6].split("=")[1].strip()

        fp.close()

    def getActiveCFPU(self):
        print "######################################################################"
	print time.ctime()
	print "######################################################################"
        cmd1 = "show has state managed-object /CFPU-1/FSClusterStateServer"
        if commands.getstatusoutput('/opt/Nokia_BP/bin/fsclish -c \"'+cmd1+'\"')[1].split(" ")[-14]=="HOTSTANDBY":
                CFPU=0
        else:
                CFPU=1
        print "ACTIVE CFPU IS CFPU-"+str(CFPU)
        cmd_mod='/opt/Nokia_BP/bin/fsclish -f \"'+self.resource_dir+'backup_cmd\"'
        print "Creating .iso file, Please wait"
        #backup_image_file = self.backup_dir+'RNC-173_partial_backup_20150320_0500.iso' #LOCAL
        print "######################################################################"
	for output in commands.getstatusoutput(cmd_mod):
		print output
	print "######################################################################"
        commands.getstatusoutput("ls "+self.backup_dir+"*"+self.date+"*")[1].split("\n")
        backup_image_file =  commands.getstatusoutput("ls "+self.backup_dir+"*"+self.date+"*")[1].split("\n")[0]
        backup_image_file.split('/')[-1]
        md5_file_name = '_'.join(backup_image_file.split(".")[0].split("_")[2:])+".md5"
        
        cmd_make_md5 = "md5sum "+backup_image_file+" > "+self.backup_dir+md5_file_name
        
        print "Generating "+md5_file_name
        print time.ctime()
        for output in commands.getstatusoutput(cmd_make_md5):
		print output
	print "md5sum generated"
        print time.ctime()
        print "Transfering "+md5_file_name+" file to "+self.remote_host+" This may take upto 30 mins"
        print time.ctime()
        transfer_cmd_iso = self.resource_dir+"sshbackup "+backup_image_file.split('/')[-1]
        transfer_cmd_md5 = self.resource_dir+"sshbackup "+md5_file_name
        commands.getstatusoutput(transfer_cmd_md5)
        print md5_file_name+" Transferred"
	print time.ctime()
	print "Transfering "+backup_image_file+" file to "+self.remote_host+" This may take upto 30 mins"
        commands.getstatusoutput(transfer_cmd_iso)
        print backup_image_file+" Transferred"

	print time.ctime()

    def cleanBackup(self):
	print "Cleaning old backup files"
	for f in commands.getstatusoutput('ls /mnt/backup/backup/*')[1].split('\n')[:-2]:
		print "Deleting "+f
		commands.getstatusoutput('rm '+f )
		

if __name__ == '__main__':

    obj_crb = crb()
    obj_crb.cleanBackup()
    obj_crb.readConfigFile()
    obj_crb.getActiveCFPU()

