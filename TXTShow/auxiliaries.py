#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys, time, os
from TxtStyle import *
from threading import Timer

def run_program(rcmd):
    """
    Runs a program, and it's paramters (e.g. rcmd="ls -lh /var/www")
    Returns output if successful, or None and logs error if not.
    """

    cmd = shlex.split(rcmd)
    executable = cmd[0]
    executable_options=cmd[1:]    

    try:
        proc  = Popen(([executable] + executable_options), stdout=PIPE, stderr=PIPE)
        response = proc.communicate()
        response_stdout, response_stderr = response[0].decode('UTF-8'), response[1].decode('UTF-8')
    except OSError as e:
        if e.errno == errno.ENOENT:
            print( "Unable to locate '%s' program. Is it in your path?" % executable )
        else:
            print( "O/S error occured when trying to run '%s': \"%s\"" % (executable, str(e)) )
    except ValueError as e:
        print( "Value error occured. Check your parameters." )
    else:
        if proc.wait() != 0:
            print( "Executable '%s' returned with the error: \"%s\"" %(executable,response_stderr) )
            return response
        else:
            #print( "Executable '%s' returned successfully." %(executable) )
            #print( " First line of response was \"%s\"" %(response_stdout.split('\n')[0] ))
            return response_stdout
          
class TouchRequester(TouchDialog):
    
    def __init__(self,title,text,text_okay=None,text_deny=None,parent=None):
        TouchDialog.__init__(self,title,parent)
        
        self.doNotCenter=False
        self.text=text
        self.text_okay=text_okay
        self.text_deny=text_deny
        self.parent=parent
        
    def alignTop(self):
        self.doNotCenter=True
       
    def on_select(self):
        self.result = self.sender().text()
        self.close()
        
    def exec_(self):
        self.result = ""
        
        self.layout = QVBoxLayout()
        
        if not self.doNotCenter: self.layout.addStretch()
        
        # the message is:
        
        label = QLabel(self.text)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        
        self.layout.addWidget(label)
        
        # the buttons are:
        
        if not (self.text_okay==None and self.text_deny==None):
            butbox =QWidget()       
            blayou = QVBoxLayout()
            butbox.setLayout(blayou)
            blayou.addStretch()
        
        if not self.text_okay==None:
            but_okay = QPushButton(self.text_okay)
            but_okay.clicked.connect(self.on_select)
        
            blayou.addWidget(but_okay)
        
        if not self.text_deny==None:
            but_deny = QPushButton(self.text_deny)
            but_deny.clicked.connect(self.on_select)
        
            blayou.addWidget(but_deny)
        
        # finalize layout
        
        self.layout.addStretch()
        if not (self.text_okay==None and self.text_deny==None):
            self.layout.addWidget(butbox)
        self.centralWidget.setLayout(self.layout)
        
        # and run...
        
        TouchDialog.exec_(self)
        if self.result=="": return False,None
        else: return True,self.result    



class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

if __name__ == "__main__":
    print("This is a python3 module containing stuff for ft TXT programming\n")
    print("Current contents:")
    print("def run_program(rcmd):              runs a shell command")
    print("class TouchRequester(TouchDialog):  provides a requester model")
    print("class PicButton(QAbstractButton):   provides a grapical QPushButton")
