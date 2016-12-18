__author__ = 'tpaul'

from Tkinter import *
import controller.read_config
import ttk
import os
container_settings = Frame()
container_settings['borderwidth'] = 2

container_settings['relief'] = 'groove'
text_label_local_working_dir = StringVar()
text2_label_local_working_dir = StringVar()
text_label_2G_databases = StringVar()
text2_label_2G_databases = StringVar()
text_label_3G_databases = StringVar()
text2_label_3G_databases = StringVar()
text_label_FTP_HOST = StringVar()
text2_label_FTP_HOST = StringVar()
text_label_FTP_USER = StringVar()
text2_label_FTP_USER = StringVar()
text_label_FTP_PASS = StringVar()
text2_label_FTP_PASS = StringVar()
text_label_FTP_Directory = StringVar()
text2_label_FTP_Directory = StringVar()

text_label_SQL_USER = StringVar()
text2_label_SQL_USER = StringVar()

text_label_SQL_HOST = StringVar()
text2_label_SQL_HOST = StringVar()

text_label_SQL_PASS = StringVar()
text2_label_SQL_PASS = StringVar()


entry_local_working_dir = ttk.Entry(container_settings, width=50)
entry_2g_db_dir = ttk.Entry(container_settings, width=50)
entry_3g_db_dir = ttk.Entry(container_settings, width=50)
entry_ftp_host = ttk.Entry(container_settings, width=50)
entry_ftp_user = ttk.Entry(container_settings, width=50)
entry_ftp_pass = ttk.Entry(container_settings, width=50)
entry_ftp_dir = ttk.Entry(container_settings, width=50)
entry_sql_host = ttk.Entry(container_settings, width=50)
entry_sql_user = ttk.Entry(container_settings, width=50)
entry_sql_pass = ttk.Entry(container_settings, width=50)

def load():
    entry_local_working_dir.delete(0, END)
    entry_2g_db_dir.delete(0, END)
    entry_3g_db_dir.delete(0, END)
    entry_ftp_host.delete(0, END)
    entry_ftp_user.delete(0, END)
    entry_ftp_pass.delete(0, END)
    entry_ftp_dir.delete(0, END)

    config_object = controller.read_config.ReadConfig()
    aconfig = config_object.reader()
    print aconfig
    text_label_local_working_dir.set(aconfig[0][0])
    text2_label_local_working_dir.set(aconfig[1][0])

    text_label_2G_databases.set(aconfig[0][1])
    text2_label_2G_databases.set(aconfig[1][1])

    text_label_3G_databases.set(aconfig[0][2])
    text2_label_3G_databases.set(aconfig[1][2])

    text_label_FTP_HOST.set(aconfig[0][3])
    text2_label_FTP_HOST.set(aconfig[1][3])

    text_label_FTP_USER.set(aconfig[0][4])
    text2_label_FTP_USER.set(aconfig[1][4])

    text_label_FTP_PASS.set(aconfig[0][5])
    text2_label_FTP_PASS.set(aconfig[1][5])

    text_label_FTP_Directory.set(aconfig[0][6])
    text2_label_FTP_Directory.set(aconfig[1][6])

    label_local_working_dir = ttk.Label(container_settings, text=text_label_local_working_dir.get()).grid(row=0, column=0)
    #entry_local_working_dir = ttk.Entry(container_settings, width=50)
    entry_local_working_dir.insert(0, text2_label_local_working_dir.get())
    entry_local_working_dir.grid(row=0, column=1, padx=(10, 10), pady=(5, 5))


    label_2g_db_dir = ttk.Label(container_settings, text=text_label_2G_databases.get()).grid(row=1, column=0)
    #entry_2g_db_dir = ttk.Entry(container_settings, width=50)
    entry_2g_db_dir.insert(0, text2_label_2G_databases.get())
    entry_2g_db_dir.grid(row=1, column=1, padx=(10, 10), pady=(5, 5))

    label_3g_db_dir = ttk.Label(container_settings, text=text_label_3G_databases.get()).grid(row=2, column=0)

    entry_3g_db_dir.insert(0, text2_label_3G_databases.get())
    entry_3g_db_dir.grid(row=2, column=1, padx=(10, 10), pady=(5, 5))


    label_ftp_host = ttk.Label(container_settings, text=text_label_FTP_HOST.get()).grid(row=3, column=0)

    entry_ftp_host.insert(0, text2_label_FTP_HOST.get())
    entry_ftp_host.grid(row=3, column=1, padx=(10, 10), pady=(5, 5))

    label_ftp_user = ttk.Label(container_settings, text=text_label_FTP_USER.get()).grid(row=4, column=0)

    entry_ftp_user.insert(0, text2_label_FTP_USER.get())
    entry_ftp_user.grid(row=4, column=1, padx=(10, 10), pady=(5, 5))

    label_ftp_pass = ttk.Label(container_settings, text=text_label_FTP_PASS.get()).grid(row=5, column=0)

    entry_ftp_pass.insert(0, text2_label_FTP_PASS.get())
    entry_ftp_pass.grid(row=5, column=1, padx=(10, 10), pady=(5, 5))


    label_ftp_dir = ttk.Label(container_settings, text=text_label_FTP_Directory.get()).grid(row=6, column=0)

    entry_ftp_dir.insert(0, text2_label_FTP_Directory.get())
    entry_ftp_dir.grid(row=6, column=1, padx=(10, 10), pady=(5, 5))

load()
def save():
    fp = open(os.getcwd()+'\\resources\\test.conf', 'w+')
    fp.write(text_label_local_working_dir.get()+" = "+entry_local_working_dir.get()+"\n")
    fp.write(text_label_2G_databases.get()+" = "+entry_2g_db_dir.get()+"\n")
    fp.write(text_label_3G_databases.get()+" = "+entry_3g_db_dir.get()+"\n")
    fp.write(text_label_FTP_HOST.get()+" = "+entry_ftp_host.get()+"\n")
    fp.write(text_label_FTP_USER.get()+" = "+entry_ftp_user.get()+"\n")
    fp.write(text_label_FTP_PASS.get()+" = "+entry_ftp_pass.get()+"\n")
    fp.write(text_label_FTP_Directory.get()+" = "+entry_ftp_dir.get()+"\n")
    fp.close()
    load()
    pass
def open_config():
    print os.getcwd()
    os.chdir('../resources/')
    os.startfile(os.getcwd()+"\\resources\\test.conf")

    pass
ttk.Button(container_settings, text="Load", command=lambda: load()).grid(row=7, column=0)
ttk.Button(container_settings, text="Save", command=lambda: save()).grid(row=7, column=1)
ttk.Button(container_settings, text="Open Config", command=lambda: open_config()).grid(row=7, column=2)

container_settings.pack_forget()