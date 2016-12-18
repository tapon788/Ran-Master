__author__ = 'tpaul'
from Tkinter import *
import ttk
from tkMessageBox import showerror
import _mysql_exceptions
import time

from controller.create_xml import XmlCreator
from controller.read_input_xl import ReadInput
from controller.create_adjacency import CreateAdjacency
from gui_interfaces.gui_settings import *


class Demo(Frame):
    def __init__(self, parent=None, **args):
        Frame.__init__(self, parent, args)
        self.config()
        self.pack()
        self.var_db_update = IntVar()
        self.var_adj_type = StringVar()
        self.title = ["ADJG Create  (3g-2g) ", "ADJG Update (3g-2g)", "ADJS Create   (3g-3g)", "ADJS Update  (3g-3g)", "ADJS Ext  (3g-3g)", "ADJG Ext  (3g-2g)"]
        self.option_array = ['adjg', 'u_adjg', 'adjs', 'u_adjs', 'e_adjs', 'e_adjg']
        self.var_adj_type.set('ADJG Create')
        for title, option in zip(self.title, self.option_array):

            x = ttk.Radiobutton(self,
                        text=title,
                        variable=self.var_adj_type,
                        value = option
                        )
            x.pack(side=TOP, anchor=NW, pady=(2, 0))

        y = ttk.Checkbutton(self,
                        text= "Update DB",
                        variable = self.var_db_update,
                        )
        y.pack(side=BOTTOM, anchor=NE)


def play(play_button, progress, label_count, label_total, part, var_input_filename, var_label_total, var_label_count,
         open_error_log_button):

    fp_troubleshoot = open('C:\Python27\Adjacency\\troubleshoot.txt', 'a')
    var_label_total.set('')
    var_label_count.set('')
    play_button.config(state=DISABLED)
    progress.pack(side=LEFT, padx=(20, 20))
    label_count.pack(side=LEFT, anchor=NE)
    label_total.pack(side=LEFT, anchor=NE)
    open_error_log_button.pack_forget()
    adjtype = part.var_adj_type.get().upper()
    db_update_chk = part.var_db_update.get()
    input_file = var_input_filename.get()
    fp_troubleshoot.write('\n'+time.ctime()+':gui_adjacency: Task:'+adjtype+' requested\n')
    while True:
        if len(input_file.split('/')) <= 1 or input_file.split('/')[-1] != 'input_nsn.xlsx':
            showerror('Error', 'Browse a valid input')
            play_button.config(state=ACTIVE)
            fp_troubleshoot.write(time.ctime()+' gui_adjacency: Task:'+adjtype+" not completed due to\n")
            fp_troubleshoot.write(input_file+' is an invalid input'+'\n')
            fp_troubleshoot.write('\n\t\t\t\t---------------X---------------\n')
            fp_troubleshoot.close()
            return 0
        else:
            break

    input_dir = '/'.join(input_file.split('/')[:-1])
    update_flag = ""
    error_button_flag = StringVar()
    try:
        update_flag = adjtype.split("_")[0]
        adjtype = adjtype.split('_')[1]
    except IndexError:
        adjtype = adjtype

    inputreader = ReadInput(input_file, update_flag)
    xl_input = inputreader.read_excel(adjtype)
    fp_troubleshoot.write('DIC:'+time.ctime()+":gui_adjacency: [RAW] xl_input:\n")
    for key, val in xl_input.iteritems():
        fp_troubleshoot.write('\t'+key+str(val)+"\n")

    _input_count_ = len(xl_input[adjtype[0]+adjtype[1:].lower()+'LAC'])
    var_label_total.set(str(_input_count_))
    adjacency_object = CreateAdjacency(input_dir, _input_count_, update_flag,
                                       db_update_chk, adjtype)
    fp_troubleshoot.close()
    if update_flag == 'E':
        xl_input = adjacency_object.get_source_adj(xl_input, adjtype)
        fp_troubleshoot = open('C:\Python27\Adjacency\\troubleshoot.txt', 'a')
        fp_troubleshoot.write('DIC:'+time.ctime()+":gui_adjacency: [MOD] xl_input:\n")
        for key, val in xl_input.iteritems():
            fp_troubleshoot.write('\t'+key+str(val)+"\n")

        if len(xl_input) == 0:
            var_label_total.set('')
            showerror('Not found', 'No such relation found')
            progress.pack_forget()
            label_total.pack_forget()
            label_count.pack_forget()
            play_button.config(state=ACTIVE)
            fp_troubleshoot.write(time.ctime()+'gui_adjacency: Task:'+adjtype+" not completed due to\n")
            fp_troubleshoot.write("No relation found for " + adjtype + '\n')
            fp_troubleshoot.write('\n\t\t\t\t---------------X---------------\n')
            fp_troubleshoot.close()
            return 0

    adjacency_dictionary = adjacency_object.get_adj_from_sql(xl_input, progress,
                                                                 var_label_count, error_button_flag)

    if len(adjacency_dictionary) == 1:
        progress.pack_forget()
        label_count.pack_forget()
        label_total.pack_forget()
        play_button.config(state=ACTIVE)
        fp_troubleshoot = open('C:\Python27\Adjacency\\troubleshoot.txt', 'a')
        fp_troubleshoot.write(time.ctime()+'gui_adjacency: Task:'+adjtype+" not completed due to\n")
        fp_troubleshoot.write(adjacency_dictionary['error']+'\n')
        fp_troubleshoot.write('\n\t\t\t\t---------------X---------------!!\n')
        fp_troubleshoot.close()
        showerror("Error", adjacency_dictionary['error'])
        return 0

    fp_troubleshoot = open('C:\Python27\Adjacency\\troubleshoot.txt', 'a')
    fp_troubleshoot.write('DIC:'+time.ctime()+":gui_adjacency: adjacency_dictionary:\n")
    for key, val in adjacency_dictionary.iteritems():
        fp_troubleshoot.write('\t'+key+str(val)+'\n')

    XmlCreator(adjacency_dictionary, input_dir, adjtype, "delete")
    XmlCreator(adjacency_dictionary, input_dir, adjtype, "create")
    adjacency_object.delete_adj_sql()
    if error_button_flag.get() == '1':
        open_error_log_button.pack(anchor=S)
    else:
        open_error_log_button.pack_forget()

    progress.pack_forget()
    label_count.pack_forget()
    label_total.pack_forget()
    play_button.config(state=ACTIVE)
    fp_troubleshoot.write(time.ctime()+' gui_adjacency: Task:'+adjtype+" completed\n")
    fp_troubleshoot.write('\n\t\t\t\t---------------X---------------\n')

    fp_troubleshoot.close()

def askopenfile(var_input_filename):
    from tkFileDialog import askopenfilename
    filename = askopenfilename(initialdir='E:\\Parameter')
    var_input_filename.set(filename)

def openerrorlog(var_input_filename):

    input_dir = '\\'.join(var_input_filename.get().split('\\')[:-1])
    os.startfile(input_dir + '\\warning.log')




container_adj= Frame()
frameP = Frame(container_adj)
progress = ttk.Progressbar(frameP, orient="horizontal", length=475, mode="determinate")
progress.pack_forget()
var_label_total = StringVar()
var_label_total.set('')
label_total = Label(frameP, textvariable=var_label_total, )
label_total.pack_forget()
var_label_count = StringVar()
var_label_count.set('')
label_count = Label(frameP, textvariable=var_label_count, )
label_count.pack_forget()
frameP.pack(side=TOP, fill=X, padx=(2, 2), pady=(2, 2))
# Frame1 = Label + a Button
frame1 = ttk.Frame(container_adj)
frame1['borderwidth'] = 2
frame1['relief'] = 'groove'
frame1.pack(side=TOP, fill=X, padx=(5, 5), pady=(5, 5))
var_input_filename = StringVar()
var_input_filename.set(entry_local_working_dir.get()+'input_nsn.xlsx')
label_file_choose = ttk.Label(frame1, textvariable=var_input_filename).pack(side=LEFT, anchor=NW, fill=Y)
browse_button = ttk.Button(frame1, text='Browse', command = lambda : askopenfile(var_input_filename))
browse_button.pack(side=TOP, anchor=NE)


# Frame2 = Radiobutton groups + a Checkbutton
frame2 = ttk.Frame(container_adj)
frame2['borderwidth'] = 2
frame2['relief'] = 'groove'
part = Demo(frame2)
part.pack(fill=X)
part.var_adj_type.set('adjg')
frame2.pack(side=TOP, fill=X, padx=(5, 5), pady=(5, 5))


# Frame3 contains start button
frame3 = Frame(container_adj, bg="#FFAAFF")

open_error_log_button = ttk.Button(frame3, text="Warning!", command=lambda : openerrorlog(var_input_filename))
open_error_log_button.pack_forget()

play_button = ttk.Button(frame3, text='Start', command=lambda: play(play_button, progress, label_count,
                                                                    label_total, part, var_input_filename,
                                                                    var_label_total, var_label_count,
                                                                    open_error_log_button))
play_button.pack()
frame3.pack(side=TOP, fill=X)
# end Adjacent
