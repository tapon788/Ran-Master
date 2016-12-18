__author__ = 'tpaul'

from Tkinter import *
import ttk
#parser

container_parse = Frame()
container_parse['borderwidth'] = 2

container_parse['relief'] = 'groove'
parse_progress = ttk.Progressbar(container_parse, orient="horizontal", length=200, mode="determinate")
parse_progress.config(length=280)
parse_progress.pack(side=TOP)

parse_label_text = StringVar()
parse_total_count_text = StringVar()
parse_completed_count_text = StringVar()
parse_remaining_count_text = StringVar()

label_parser = Label(container_parse, textvariable=parse_label_text)
label_parser.pack()
parse_label_text.set('Parsing is started')
Label(container_parse, text="Total: ").pack(side=LEFT)
Label(container_parse, textvariable=parse_total_count_text, width=5).pack(side=LEFT)
Label(container_parse, text="Done: ").pack(side=LEFT)
Label(container_parse, textvariable=parse_completed_count_text, width=5).pack(side=LEFT)
Label(container_parse, textvariable=parse_remaining_count_text).pack(side=RIGHT)
Label(container_parse, text="Remaining: ").pack(side=RIGHT)
container_parse.pack_forget()
# end Parser
