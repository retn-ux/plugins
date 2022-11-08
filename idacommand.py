from distutils.cmd import Command
import sys
import idaapi
import idc
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt 

import retsync.rsconfig as rsconfig
from retsync.rsconfig import rs_log

PYTHON_PATH = rsconfig.get_python_interpreter()
os.environ['PYTHON_PATH'] = PYTHON_PATH

class IDACommandWidget(idaapi.PluginForm):
    def OnCreate(self, form):
        parent = self.FormToPyQtWidget(form)
        

        label=QtWidgets.QLabel("Command: ")
        label.setAlignment(Qt.AlignCenter)

        self.lineEdit=QtWidgets.QLineEdit()

        

        button=QtWidgets.QPushButton("run")
        button.clicked.connect(self.OnRunBtnClicked)

        layout=QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.lineEdit)
        layout.addWidget(button)

        parent.setLayout(layout)

    def Show(self):
        return idaapi.PluginForm.Show(self, "IDACommand", options=idaapi.PluginForm.WOPN_PERSIST)

    def Close(self, options):
        return idaapi.PluginForm.Close(options)

    def OnRunBtnClicked(self):
        plugin_path=idc.idadir()+"/plugins"
        command=self.lineEdit.text()
        command_list=command.split(" ")
        command_list[0]=plugin_path+"/"+command_list[0]
        with open(command_list[0],'r') as file:
            old_argv=sys.argv
            sys.argv=command_list
            exec(file.read())
            sys.argv=old_argv



class IDACommandPlugin(idaapi.plugin_t):
    flags = idaapi.PLUGIN_PROC
    comment = "IDA's tool IDACommand."
    help = "Launcher for IDA's python command line script."
    wanted_name = 'IDACommand'
    wanted_hotkey = 'Alt-Shift-A'
    global idaCommandWidget
    idaCommandWidget = None

    def init(self):
        return idaapi.PLUGIN_KEEP

    def term(self):
        pass

    def run(self, arg):
        global idaCommandWidget
        if not idaCommandWidget:
            idaCommandWidget = IDACommandWidget()
            idaCommandWidget.Show()
            rs_log("[IDACommand] plugin loaded")


def PLUGIN_ENTRY():
    return IDACommandPlugin()

