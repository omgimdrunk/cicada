"""

    borderwidth − Width of the border which gives a three-dimensional look to the widget.

    highlightthickness − Width of the highlight rectangle when the widget has focus.

    padX padY − Extra space the widget requests from its layout manager beyond the minimum the
        widget needs to display its contents in the x and y directions.

    selectborderwidth − Width of the three-dimentional border around selected items of the widget.

    wraplength − Maximum line length for widgets that perform word wrapping.

    height − Desired height of the widget; must be greater than or equal to 1.

    underline − Index of the character to underline in the widget's text (0 is the first character,
        1 the second one, and so on).

    width − Desired width of the widget.


    import threading
import os

"""

import sys
import tkinter as tk
from tkinter import Text, Entry
from tkinter.font import Font
from loguru import logger
from cicada import sockio

#logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
FILL = tk.N + tk.S + tk.W + tk.E


@logger.catch
class AttribsOBJ(dict):
    def __init__(self):

        super().__init__()

        self['borderwidth'] = 0
        self['highlightthickness'] = 0
        self.fontface = "DejaVuSansMono"
        self.fontsize = 9
        self['font'] = Font(family=self.fontface, size=self.fontsize)


@logger.catch
class TextOBJ(Text):
    def __init__(self, master=None, onkey=None):
        super().__init__(master=master)

        self.master = master
        self.linecolor = '#393D46'
        self.key_binds = dict()
        self.curline = 1
        self.onkey = onkey
        self.bind('<Key>', self.is_bound)
        self.bind('<KeyRelease>', self.setline)
        self.bind('<Motion>', self.mpos)
        self.configure(bg='#222331', fg='#FFFFFF', insertbackground='#00FF00',
                       selectbackground='#330033')
        self.tag_config('curline', background=self.linecolor)
        self.return_count = 5

    def mpos(self, event):
        print(self.winfo_pointerxy())

    def _make_local(self, line: str):   
        return '_{}'.format(line.lower())
        
    def is_bound(self, event):
        self.update()
        if event.keysym == 'Up' and self.curline > 1:
            self.clear_select(self.curline)
            self.line_select(self.curline - 1)



    def setline(self, event):
        if event.keysym == 'Return':
            self.clear_select(self.curline)
        self.curline = int(self.index(tk.INSERT).split('.')[0])

    def clear_select(self, curline):
        self.tag_remove('curline', '{}.0'.format(curline), '{}.end+1c'.format(curline))
        self.update()

    def line_select(self, new_line):
        self.tag_add('curline', '{}.0'.format(new_line), '{}.end+1c'.format(new_line))
        self.update()


class EntryOBJ(Entry):
    def __init__(self, master=None, row=0, column=0, sticky=FILL, on_return=None):

        super().__init__(master=master)
        self.prompt = 0

        self.on_return = on_return
        self.bind('<Return>', self.do_return)
        self.input_anchor(None)
        self.configure(bg='#222331', fg='#FFFFFF', insertbackground='#00FF00')
        self.configure(font=AttribsOBJ()['font'], borderwidth=1, highlightthickness=0)

        self.grid(row=row, column=column, sticky=sticky)

    def input_anchor(self, event):
        self.delete(0, tk.END)
        self.insert(0, 'strix:$ ')
        self.prompt = self.index(tk.INSERT)
        print(self.prompt, event)

    def do_return(self, event):
        buff = self.get()[self.prompt:]
        self.input_anchor(event)
        self.on_return(buff)


class _hndlTE(tk.Tk):
    def __init__(self, on_key=None):
        super().__init__()

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=1)
        self.configure(bg='#DEDEDE', padx=1, pady=0)
        self.main_edit = TextOBJ(master=self, onkey=on_key)
        self.main_edit.grid(row=0, column=0, sticky=FILL)
        self.user_input = EntryOBJ(master=self, row=1, column=0, sticky=FILL)

    def add_data(self, data):
        self.main_edit.configure(state=tk.NORMAL)
        self.main_edit.insert(tk.END, data.replace('\r', ''))
        self.main_edit.configure(state=tk.DISABLED)
        self.main_edit.see(tk.END)

    def newtitle(self, event):
        print(event)
        self.main_edit.configure(state=tk.NORMAL)

    @logger.catch
    def cmd_ctrl(self, data):

        cmd, *args = data.strip().split(' ')
        _runit = getattr(self.main_edit, cmd)
        _runit(*args)



# TEXT_EDIT = _hndlTE()
# TEXT_EDIT.geometry('700x500+2000+100')
#
# TEXT_EDIT.mainloop()
