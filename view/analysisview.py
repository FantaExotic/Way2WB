import tkinter as tk
from tkinter import ttk
from ttkwidgets import CheckboxTreeview

from tkcalendar import DateEntry

class Analysisview(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=10)  # more weight to row with Listbox
        
        self.symbol_var = tk.StringVar(self)
        self.symbol_entry = tk.Entry(self, textvariable=self.symbol_var)
        self.symbol_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ne")

        self.enterbutton = tk.Button(self, text="Add")
        self.enterbutton.grid(row=0, column=2, padx=5, pady=5, sticky="ne")

        self.button_return = tk.Button(self, text="Return")
        self.button_return.grid(row=0, column=3, padx=5, pady=5, sticky="ne")

        self.button_delete = tk.Button(self, text="Delete")
        self.button_delete.grid(row=3, column=3, padx=5, pady=5, sticky="ne")

        self.listbox = CheckboxTreeview(self)
        self.listbox.grid(row=3, column=0, padx=15, pady=15, sticky="nsew")

        self.methods = []
        self.listbox_methods = tk.Listbox(self)
        self.listbox_methods.grid(row=3, column=1, padx=15, pady=15, sticky="nsew")

        style = ttk.Style(self)
        style.layout('Checkbox.Treeview.Item', 
             [('Treeitem.padding',
               {'sticky': 'nswe',
                'children': [('Treeitem.image', {'side': 'left', 'sticky': ''}),
                             ('Treeitem.focus', {'side': 'left', 'sticky': '',
                                                 'children': [('Treeitem.text', 
                                                               {'side': 'left', 'sticky': ''})]})]})])
        style.configure('Checkbox.Treeview', borderwidth=1, relief='sunken')

    def add_method(self, param):
        temp = f'moving average: {param}'
        self.listbox_methods.insert(tk.END,temp)
        pass

    def remove_ma_entry(self):
        pass

    def add_ma_entry():
        pass

    def remove_ma_entry():
        pass

    def appendWatchlist(self):
        pass

    def deleteMethod(self):
        selected_element = self.listbox_methods.curselection()[0]
        self.listbox_methods.delete(selected_element)
        return selected_element #return index to remove from model.methods