__author__ = 'tpaul'
from Tkinter import *


def downloader(in_dbtype, in_local_dir):
    var_db_type.set(in_dbtype)
    fp_troubleshoot_adj = open('C:\Python27\Adjacency\\troubleshoot.txt', 'a')
    fp_troubleshoot_adj.writelines('\n\n\t\t\t\t*********** gui_download **********\n')
    fp_troubleshoot_adj.close()


    container_parse.pack_forget()
    container_adj.pack_forget()
    container_parameter.pack_forget()
    container_settings.pack_forget()
    container_parameter_3g.pack_forget()
    container_parameter.pack_forget()
    container_node_b_create.pack_forget()
    container_download.pack(side=TOP, fill=X, padx=(5, 5), pady=(5, 5))
    from controller import download

    dl = download.Downloader(in_local_dir, ftp_host, ftp_user, ftp_pass, ftp_dir,
                             dl_progress, dl_label_text, dl_local_count_text, dl_remote_count_text,
                             dl_remaining_count_text, in_dbtype)
    fp_troubleshoot = open('C:\Python27\Adjacency\\troubleshoot.txt', 'a')
    fp_troubleshoot.write(time.ctime()+':'+'gui_download:Task:'+in_dbtype+' databases download requested\n')
    fp_troubleshoot.close()
    dl.start()
    pass


def parser(in_parsetype):
    container_adj.pack_forget()
    container_download.pack_forget()
    container_parameter.pack_forget()
    container_settings.pack_forget()
    container_parameter_3g.pack_forget()
    container_parameter.pack_forget()
    container_node_b_create.pack_forget()
    container_parse.pack(side=TOP, fill=X, padx=(5, 5), pady=(5, 5))

    if in_parsetype == '2G':
        from controller import flexi_parser

        parse = flexi_parser.ManagedObjectHandler([], parse_progress, parse_label_text,
                parse_total_count_text, parse_completed_count_text, parse_remaining_count_text)
    else:
        from controller import mcrnc_parser

        parse = mcrnc_parser.ManagedObjectHandler([], parse_progress, parse_label_text,
                parse_total_count_text, parse_completed_count_text, parse_remaining_count_text)
    parse.start()
    pass

def parameter(in_parametertype):
    container_adj.pack_forget()
    container_download.pack_forget()
    container_parse.pack_forget()
    container_settings.pack_forget()
    container_node_b_create.pack_forget()
    if in_parametertype=='2G':
        container_parameter.pack(fill=BOTH)
        container_parameter_3g.pack_forget()
    else:
        container_parameter_3g.pack(fill=BOTH)
        container_parameter.pack_forget()
    pass


def adjacent():

    fp_troubleshoot_adj = open('C:\Python27\Adjacency\\troubleshoot.txt', 'a')
    fp_troubleshoot_adj.writelines('\n\n\t\t\t\t*********** gui_adjacency **********\n')
    fp_troubleshoot_adj.close()
    print "adjacency"
    container_parameter.pack_forget()
    container_download.pack_forget()
    container_parse.pack_forget()
    container_settings.pack_forget()
    container_parameter_3g.pack_forget()
    container_parameter.pack_forget()
    container_node_b_create.pack_forget()
    container_adj.pack(fill=BOTH)
    pass
def settings():
    container_parameter.pack_forget()
    container_download.pack_forget()
    container_parse.pack_forget()
    container_adj.pack_forget()
    container_parameter_3g.pack_forget()
    container_parameter.pack_forget()
    container_node_b_create.pack_forget()
    container_settings.pack(fill=BOTH)

def node_b_create():
    container_parameter.pack_forget()
    container_download.pack_forget()
    container_parse.pack_forget()
    container_adj.pack_forget()
    container_parameter_3g.pack_forget()
    container_parameter.pack_forget()
    container_settings.pack_forget()
    container_node_b_create.pack(fill=BOTH)



def yet_to_implement():
    showerror('Not Implemented', 'Feature is not currently available ')

if __name__ == '__main__':
    fp_troubleshoot_main = open('troubleshoot.txt', 'w+')
    fp_troubleshoot_main.close()
    filename = ''
    root = Tk()
    root.title('RAN Master')#u'\u09B2\u099C\u09BF\u0995\u09C7\u09B0 \u0995\u09BE\u09B0\u09BF\u0997\u09B0'

    #fp_troubleshoot.write('Creating menu\n')
    menu = Menu(root)

    from gui_interfaces.gui_download import *
    from gui_interfaces.gui_parse import *
    from gui_interfaces.gui_adjacency import *
    from gui_interfaces.gui_parameter_3g import *
    from gui_interfaces.gui_parameter import *
    from gui_interfaces.gui_settings import *
    from gui_interfaces.gui_node_b_creation import *


    ftp_host = entry_ftp_host.get()
    ftp_user = entry_ftp_user.get()
    ftp_pass = entry_ftp_pass.get()
    ftp_dir = entry_ftp_dir.get()
    local_dir_2g = entry_2g_db_dir.get()+"XML_DATABASE\\"
    local_dir_3g = entry_3g_db_dir.get()+"XML_DATABASE\\"
    print ftp_user, ftp_pass, ftp_host, ftp_dir

    download_menu = Menu(menu, tearoff=0, background="#AAFFAA")
    download_menu.add_command(label="2G DB", command=lambda: downloader('2G', local_dir_2g))
    download_menu.add_command(label="3G DB", command=lambda: downloader('3G', local_dir_3g))
    menu.add_cascade(label='Download', menu=download_menu)  # download u'\u09A1\u09BE\u0989\u09A8\u09B2\u09CB\u09A1'
    #fp_troubleshoot.write('Download menu created\n')

    parse_menu = Menu(menu, tearoff=0, background="#FFAAAA")
    parse_menu.add_command(label="Flexi DB", command=lambda: parser('2G'))
    parse_menu.add_command(label="MCRNC DB", command=lambda: parser('3G'))
    menu.add_cascade(label="Parser", menu=parse_menu)
    #fp_troubleshoot.write('Parser menu created\n')

    parameter_menu = Menu(menu, tearoff=0, background="#AADFFF")
    parameter_menu.add_command(label="GSM Tuner", command=lambda: parameter('2G'))
    parameter_menu.add_command(label="WCDMA Tuner", command=lambda: parameter('3G'))
    menu.add_cascade(label="Parameter", menu=parameter_menu)
    #fp_troubleshoot.write('Parameter menu created\n')

    plan_menu = Menu(menu, tearoff=0, background="#FFDFAF")
    plan_menu.add_command(label="Adjacency from RNC", command=lambda : adjacent())
    plan_menu.add_command(label="Adjacency from BSC", command=lambda : yet_to_implement())
    plan_menu.add_separator()
    plan_menu.add_command(label="Exit", command=root.quit)
    menu.add_cascade(label="Adjacency", menu=plan_menu)
    #fp_troubleshoot.write('Adjacency menu created\n')

    misc_menu = Menu(menu, tearoff=0, background="#FFDFAF")
    misc_menu.add_command(label="Search NE", command=lambda: yet_to_implement())
    misc_menu.add_separator()
    misc_menu.add_command(label="BTS create", command=lambda: yet_to_implement())
    misc_menu.add_command(label="BTS delete", command=lambda: yet_to_implement())
    misc_menu.add_separator()
    misc_menu.add_command(label="NodeB create", command=lambda: node_b_create())
    misc_menu.add_command(label="NodeB delete", command=lambda: yet_to_implement())

    misc_menu.add_separator()
    misc_menu.add_command(label="Exit", command=root.quit)
    menu.add_cascade(label="Miscellaneous", menu=misc_menu)



    setting_menu = Menu(menu, tearoff=0, background="#DFDFAF")
    setting_menu.add_command(label="Show Settings", command=lambda: settings())
    menu.add_cascade(label="Settings", menu=setting_menu)
    #fp_troubleshoot.write('Settings menu created\n')
    #fp_troubleshoot.close()

    root.config(menu=menu)
    canvas = Canvas(root)   # 0,0 is top left corner
    canvas.config(width=640, height=200)
    canvas.pack(side=TOP)
    photo = PhotoImage(file=os.getcwd() + '\\resources\\images\\banner.gif')
    canvas.create_image(0, 0, image=photo, anchor=NW)


    root.geometry('580x500')
    root.iconbitmap(default=os.getcwd()+'\\gui_interfaces\\resources\\images\\ranmaster.ico')
    #root.iconbitmap(default=os.getcwd()+'\\resources\\images\\ranmaster.ico')


    root.configure()
    root.resizable(width=FALSE, height=FALSE)
    root.mainloop()