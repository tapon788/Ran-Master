__author__ = 'tpaul'

import time,datetime,os,ftplib
import threading
class Downloader(threading.Thread):
    def __init__(self, localdir_root, ftphost, ftpuser, ftppass, ftpdir, progress, in_dl_label_text,
                 in_dl_local_count_text, in_dl_remote_count_text, in_dl_remaining_count_text, in_dbtype):
        threading.Thread.__init__(self)
        print ftphost
        self.dbtype = in_dbtype
        self.progress = progress

        self.local_count_text = in_dl_local_count_text
        self.remote_count_text = in_dl_remote_count_text
        self.remaining_count_text = in_dl_remaining_count_text
        self.counter = 0
        self.backcounter = 0
        self.dl_label_text = in_dl_label_text
        self.localdir_root = localdir_root
        self.local_full_path = ""
        self.ftphost = ftphost
        self.ftpuser = ftpuser
        self.ftppass = ftppass
        self.ftpdir = ftpdir

        self.files_in_local = []
        self.files_size_in_local = []
        self.local_match = []
        self.files_in_remote = []
        self.files_size_in_remote = []
        self.remote_match = []
        self.remote_file_count = 0
        today = str(datetime.date.today())
        self.today = today.split("-")[2]+today.split("-")[1]+today[2:4]




    def create_local_dir(self):

        self.local_full_path = self.localdir_root+"\\"+self.today

        try:
            os.makedirs(self.local_full_path)
        except WindowsError, e:
            pass


    def get_local_file_attr(self):
        os.chdir(self.local_full_path)
        self.files_in_local = os.listdir(self.local_full_path)

        for filename in self.files_in_local:
            self.files_size_in_local.append(str(os.path.getsize(filename)))
            self.local_match.append(filename+"__"+str(os.path.getsize(filename)))
        self.counter = len(self.local_match)
        self.local_count_text.set(str(self.counter))


    def get_remote_file_attr(self):
        ftp = ftplib.FTP(self.ftphost, self.ftpuser, self.ftppass)

        ftp.cwd(self.ftpdir+self.today)
        log = []
        ftp.retrlines('LIST', callback = log.append)
        files = (line.rsplit(None, 1)[1] for line in log)
        files_list = list(files)

        for f in files_list:
            if self.dbtype == '2G':
                if f.find("xml") >= 0:
                    if f.find("BS") >= 0:
                        self.remote_file_count += 1
                        self.files_size_in_remote.append(str(ftp.size(f)))
                        self.remote_match.append(f+"__"+str(ftp.size(f)))
            else:
                if f.find("xml") >= 0:
                    if f.find("RN") >= 0:
                        self.remote_file_count += 1
                        self.files_size_in_remote.append(str(ftp.size(f)))
                        self.remote_match.append(f+"__"+str(ftp.size(f)))

        ftp.close()


    def get_delta_files(self):
        for f in self.remote_match:
            if f not in self.local_match:
                self.files_in_remote.append(f.split("__")[0])
        self.backcounter = len(self.files_in_remote)
        self.remote_count_text.set(str(self.backcounter))
        self.remaining_count_text.set(str(self.backcounter))

    def run(self):

        self.create_local_dir()
        self.get_local_file_attr()
        self.get_remote_file_attr()
        self.get_delta_files()

        if len(self.files_in_remote) == 0:
            self.dl_label_text.set("Nothing to download")
            return

        self.progress['value'] = 0
        self.progress['maximum'] = len(self.files_in_remote)
        print self.files_in_remote
        self.files_in_remote = self.files_in_remote
        ftp = ftplib.FTP(self.ftphost, self.ftpuser, self.ftppass)
        ftp.cwd(self.ftpdir+self.today)

        for f in self.files_in_remote:

            self.dl_label_text.set('Downloading to '+self.local_full_path)
            #print "Downloading "+f
            self.file = open(f, 'wb')
            try:
                self.counter += 1
                ftp.retrbinary('RETR ' + f, self.handleDownload)
                time.sleep(1)
                self.progress['value'] += 1
                self.backcounter -= 1
                self.local_count_text.set(str(self.counter))
                self.remaining_count_text.set(str(self.backcounter))

            except ftplib.error_perm, resp:
                raise
            self.file.close()


        self.dl_label_text.set('Done')
        ftp.close()
        pass

    def handleDownload(self, block):
        self.file.write(block)



'''
if __name__ == '__main__':
    dl = Downloader("E:\\ftptest", '10.10.10.113', 'jamil_rc', 'rc@jamil', '/DATABASE/FLEXI/')
    dl.start()
'''