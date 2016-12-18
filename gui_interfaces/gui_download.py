__author__ = 'tpaul'
from Tkinter import *
import ttk
import os
from gui_interfaces.gui_settings import *
import datetime,time
def open_files():
    today = str(datetime.date.today())
    today = today.split("-")[2]+today.split("-")[1]+today[2:4]

    if var_db_type.get() == '2G':
        print entry_2g_db_dir.get()
        os.startfile(entry_2g_db_dir.get()[:-1]+"\XML_DATABASE\\"+today+"\\")

    else:
        print entry_3g_db_dir.get()
        os.startfile(entry_3g_db_dir.get()[:-1]+"\XML_DATABASE\\"+today+"\\")

var_db_type = StringVar()
container_download = Frame()
container_download['borderwidth'] = 2

container_download['relief'] = 'groove'
dl_progress = ttk.Progressbar(container_download, orient="horizontal", length=565, mode="determinate")
dl_progress.pack(side=TOP)

dl_label_text = StringVar()
dl_local_count_text = StringVar()
dl_remote_count_text = StringVar()
dl_remaining_count_text = StringVar()
btn_view_files = ttk.Button(container_download, text="View", command=lambda :open_files())
btn_view_files.pack(side=BOTTOM)
label_downloader = Label(container_download, textvariable=dl_label_text)
label_downloader.pack()
Label(container_download, text="Local: ", width=6).pack(side=LEFT)
Label(container_download, textvariable=dl_local_count_text).pack(side=LEFT)
Label(container_download, text="", width=22).pack(side=LEFT)
Label(container_download, text="Remote: ", width=8).pack(side=LEFT)

Label(container_download, textvariable=dl_remote_count_text,).pack(side=LEFT)

Label(container_download, textvariable=dl_remaining_count_text).pack(side=RIGHT)
Label(container_download, text="Remaining: ", width=8).pack(side=RIGHT)


dl_label_text.set('')
dl_local_count_text.set('')
dl_remote_count_text.set('')
container_download.pack_forget()
#end download