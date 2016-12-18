__author__ = 'tpaul'

from Tkinter import *
import ttk

from controller.parameter import Paramchange
from controller.generate_plan import read_input
from gui_interfaces.gui_settings import *
'''
class SimpleTable(Listbox):
    def __init__(self, parent=None, **config):
        # use black background so it "peeks through" to
        # form grid lines
        Listbox.__init__(self, parent, **config)
        self._widgets = []



        for row in range(20):
            current_row = []
            for column in range(40):
                label = Label(self, text="%s/%s" % (row, column), borderwidth=0, width=10)
                label.grid(row=row, column=column, padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(40):
            self.grid_columnconfigure(0, weight=0)


    def seta(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
'''
def askopenfile(var_input_filename):
    from tkFileDialog import askopenfilename
    filename = askopenfilename(initialdir=entry_local_working_dir.get())
    var_input_filename.set(filename)
    #var_input_filename.set('E:\Parameter\parameter.xlsx')

    #d = dict(zip(PC.PARAMNAME, PC.PARAMVALUE))
    '''
    canvas = Canvas(container_parameter, bg='#FFAABB', scrollregion=(0, 0, 1500, 1500))
    table = SimpleTable(canvas)
    #table.seta(0, 0, "Hellow")
    #table.insert(END,"HELLOW WORLD")
    table.pack()
    sb = Scrollbar(container_parameter, orient="horizontal")
    sb.pack(side=BOTTOM, fill=X)

    canvas.config(xscrollcommand=sb.set)
    canvas.pack(side=LEFT, expand=True, fill=BOTH)
    sb.config(command=canvas.xview)
    '''

def make(in_output_type, in_sheet_index):
    if in_output_type== 'MML':

        pc = Paramchange()
        pc.readxl(var_input_filename.get(), in_sheet_index)
        pc.GuiMap()
        pc.IntGuiConv()
        pc.CmdMaker()
        commands = pc.CmdCombiner()
        pc.writer(commands)
    else:

        #top = Tkinter.Tk()
        #managedObject_name = raw_input("Write MO name").upper()
        aReadInput = read_input(var_input_filename.get(), in_sheet_index)
        aReadInput.ReadExcel()

        aReadInput.main()
    pass

container_parameter = Frame()

frame_background = PhotoImage(file=os.getcwd()+'\\resources\\images\\banner.gif')
container_parameter.image = frame_background
frame1 = Frame(container_parameter)
frame1['borderwidth'] = 2
frame1['relief'] = 'groove'

frame1.pack(side=TOP, fill=X, padx=(5, 5), pady=(5, 5))
var_input_filename = StringVar()
var_input_filename.set(entry_local_working_dir.get()+'input_nsn.xlsx')
label_file_choose = ttk.Label(frame1, textvariable=var_input_filename).pack(side=LEFT, anchor=NW, fill=Y)
browse_button = ttk.Button(frame1, text='Browse', command = lambda : askopenfile(var_input_filename))
browse_button.pack(side=TOP, anchor=NE)

make_button = ttk.Button(container_parameter, text="Make MML", command=lambda :make('MML', 2)).pack()
make_button = ttk.Button(container_parameter, text="Make XML", command=lambda :make('XML', 0)).pack()

#make_xml = ttk.Button(container_parameter, text="Make XML for 3G", command=lambda : make('XML', 1)).pack()

