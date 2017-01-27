#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys, time, os
from TouchStyle import *
from threading import Timer

try:
    if TouchStyle_version<1.2:
        print("aux: TouchStyle >= v1.2 not found!")        
except:
    print("aux: TouchStyle_version not found!")
    TouchStyle_version=0


class TouchAuxListRequester(TouchDialog):
    def __init__(self,title:str,message:str,items,inititem,button:str,parent=None):
        TouchDialog.__init__(self,title,parent)  
                
        self.result=""
        self.button=button
        self.confbutclicked=False
        self.inititem=inititem
        
        self.layout=QVBoxLayout()
        
        # the message
        if message:
            mh=QHBoxLayout()
            msg=QLabel(message)
            msg.setObjectName("smalllabel")
            msg.setWordWrap(True)
            msg.setAlignment(Qt.AlignCenter)
            mh.addWidget(msg)
            self.layout.addLayout(mh)
            
        # the list
        self.itemlist = QListWidget()
        self.itemlist.setObjectName("smalllabel")
        self.itemlist.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.itemlist.addItems(items)
        self.itemlist.currentItemChanged.connect(self.on_itemchanged)

        self.layout.addWidget(self.itemlist)
               
        # the label
        midbox = QHBoxLayout()
  
        self.actitem = QLineEdit()
        self.actitem.setReadOnly(True)
        self.actitem.setObjectName("smalllabel")
        self.actitem.setStyleSheet("color: #fcce04")
        self.actitem.setAlignment(Qt.AlignLeft)

        midbox.addWidget(self.actitem)
             
        self.layout.addLayout(midbox)
        self.itemlist.setCurrentRow(items.index(inititem))
        
        # confirm button
        
        #self.layout.addWidget(self.dial)
        #self.layout.addStretch()
        
        # the button
        but_okay = QPushButton(button)
        but_okay.setObjectName("smalllabel")
        but_okay.clicked.connect(self.on_select)
        
        if TouchStyle_version >=1.4:
            self.addConfirm()
            self.setCancelButton()
        else:    
            self.layout.addWidget(but_okay)
        
        self.centralWidget.setLayout(self.layout)    
        
        
    def on_itemchanged(self):
        self.actitem.setText(self.itemlist.currentItem().text())
                
    def on_select(self):
        self.result = self.sender().text()
        self.close()
     
    def exec_(self):
        TouchDialog.exec_(self)
        
        if self.confbutclicked==True: return True, self.itemlist.currentItem().text()
        if self.result==self.button: return True, self.itemlist.currentItem().text()
        return False, self.inititem
      

class TouchAuxRequestInteger(TouchDialog):
    def __init__(self,title:str,message:str,initvalue:int,minval,maxval,button:str,parent=None):
        TouchDialog.__init__(self,title,parent)  
        
        
        self.result=""
        self.button=button
        self.confbutclicked=False
        self.initvalue=initvalue
        
        self.layout=QVBoxLayout()
        
        # the message
        if message:
            mh=QHBoxLayout()
            msg=QLabel(message)
            msg.setObjectName("smalllabel")
            msg.setWordWrap(True)
            msg.setAlignment(Qt.AlignCenter)
            mh.addWidget(msg)
            self.layout.addLayout(mh)
            
        # the dial 
        #db=QVBoxLayout()
        self.dial=QDial()
        self.dial.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.dial.setNotchesVisible(True)
        self.dial.setRange(minval,maxval)
        self.dial.setValue(initvalue)
        self.dial.valueChanged.connect(self.show_value)
        #db.addWidget(self.dial)
        self.layout.addWidget(self.dial)
        
        #self.layout.addStretch()
        
        
        # buttons and label
        midbox = QHBoxLayout()
  
        #midbox.addStretch()
        self.bckbutt = QPushButton(" < ")
        self.bckbutt.clicked.connect(self.bckbutt_clicked)
        midbox.addWidget(self.bckbutt)
        
        midbox.addStretch()
        self.actval = QLabel()
        self.actval.setAlignment(Qt.AlignCenter)
        self.actval.setText(str(self.dial.value()))
        midbox.addWidget(self.actval)
        midbox.addStretch()
        
        self.fwdbutt = QPushButton(" > ")
        self.fwdbutt.clicked.connect(self.fwdbutt_clicked)
        midbox.addWidget(self.fwdbutt)
                
        self.layout.addLayout(midbox)
        
        # confirm button
        
        #self.layout.addWidget(self.dial)
        #self.layout.addStretch()
        
        # the button
        but_okay = QPushButton(button)
        but_okay.setObjectName("smalllabel")
        but_okay.clicked.connect(self.on_select)
        
        if TouchStyle_version >=1.4:
            self.addConfirm()
            self.setCancelButton()
        else:    
            self.layout.addWidget(but_okay)
        
        self.centralWidget.setLayout(self.layout)    
        
        
    def bckbutt_clicked(self):
        self.dial.setValue(max(self.dial.minimum(),self.dial.value()-1))
    
    def fwdbutt_clicked(self):
        self.dial.setValue(min(self.dial.value()+1,self.dial.maximum()))

    def show_value(self):
        self.actval.setText(str(self.dial.value()))
                
    def on_select(self):
        self.result = self.sender().text()
        self.close()
     
    def exec_(self):
        TouchDialog.exec_(self)
        
        if self.confbutclicked==True: return True, self.dial.value()
        if self.result==self.button: return True, self.dial.value()
        return False, self.initvalue
      
      

class TouchAuxRequestText(TouchDialog):

    def __init__(self,title:str,message:str,inittext:str,button:str,parent=None):
        TouchDialog.__init__(self,title,parent)  
        
        
        self.result=""
        self.button=button
        self.confbutclicked=False
        self.inittext=inittext
        
        self.layout=QVBoxLayout()
        self.layout.addStretch()
        
        # the message
        msg=QLabel(message)
        msg.setObjectName("smalllabel")
        msg.setWordWrap(True)
        msg.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(msg)
        self.layout.addStretch()
        
        # the text line
        self.txline=QLineEdit()
        self.txline.setText(inittext)
        
        self.layout.addWidget(self.txline)
        self.layout.addStretch()
        
        # the button
        but_okay = QPushButton(button)
        but_okay.setObjectName("smalllabel")
        but_okay.clicked.connect(self.on_select)
        
        if TouchStyle_version >=1.3:
            self.addConfirm()
            self.setCancelButton()
        else:    
            self.layout.addWidget(but_okay)
        
        self.centralWidget.setLayout(self.layout)    
        
    def on_select(self):
        self.result = self.sender().text()
        self.close()
     
    def exec_(self):
        TouchDialog.exec_(self)
        
        if self.confbutclicked==True: return True, self.txline.text()
        if self.result==self.button: return True, self.txline.text()
        return False, self.inittext

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
          
class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

class TouchAuxMessageBox(TouchDialog):
    """ Versatile MessageBox for TouchUI
        
        msg = TouchMessageBox(title, parent)
        
        Methods:
        
        msg.addConfirm() adds confirm button at the left of the title
        msg.setCancelButton() changes style of the close icon to cancel icon
        
        msg.addPixmap(QPixmap) adds a QPixmap to be shown on top of the message text
        msg.setPixmapBelow() places the pixmap below the text (inbetween text and buttons), defalt is above the text
        
        msg.setText(text) sets message text, default ist empty string
        msg.setPosButton(pos_button_text) sets text for positive button, default is None (no button)
        msg.setNegButton(neg_button_text) sets text for negative button, default is None (no button)
        
        msg.setTextSize(size) set 4- big 3 - normal (default); 2 - smaller; 1 - smallest
        msg.setBtnTextSize(size)
        
        msg.alignTop() aligns message text to top of the window
        msg.alignCenter() centers text in window (default)
        msg.alignBottom() aligns message text to bottom of the window
    
        msg.buttonsVertical(bool=True) arrange buttons on top of each other (True, default) or side-by-side (False)
        msg.buttonsHorizontal(bool=True) see above...
        
        Return values:
        
        (success, text) = msg.exec_()
        success == True if one of the buttons or the confirm button was used
        success == False if MessageBox was closed by its close icon (top right)
        
        text == None if MessageBox was closed by its close icon
        text == pos_button_text | neg_button_text depending on which button was clicked
    """
    
    
    def __init__(self,title,parent):
        TouchDialog.__init__(self,title,parent)
        
        self.buttVert=True
        self.align=2
        self.textSize=3
        self.btnTextSize=3
        self.pixmap=None
        self.pmapalign=1
        self.text=""
        self.text_okay=None
        self.text_deny=None
        self.parent=parent
        
        self.result = ""
        self.confbutclicked=False
        
    def addPixmap(self, pmap: QPixmap):
        self.pixmap=pmap
    
    def setPixmapBelow(self):
        self.pmapalign=2
    
    def buttonsVertical(self,flag=True):
        self.buttVert=flag
    
    def buttonsHorizontal(self, flag=True):
        self.buttVert=not flag
        
    def setText(self,text):
        self.text=text
    
    def setPosButton(self,text):
        self.text_okay=text
    
    def setNegButton(self,text):
        self.text_deny=text
    
    def setTextSize(self,size):
        if (size>0 and size<5): self.textSize=size
        else: self.textSize=3
    
    def setBtnTextSize(self,size):
        if (size>0 and size<5): self.btnTextSize=size
        else: self.btnTextSize=3
    
    def alignTop(self):
        self.align=1
    def alignCenter(self):
        self.align=2
    def alignBottom(self):
        self.align=3
        
    def on_select(self):
        self.result = self.sender().text()
        self.close()
     
    def exec_(self):
        self.result = ""
        
        self.layout = QVBoxLayout()
        
        # the pixmap ist (in case of pmapalign=1
        
        if self.pixmap and self.pmapalign==1:
            ph = QHBoxLayout()
            ph.addStretch()
            p = QLabel()
            p.setPixmap(self.pixmap)
            ph.addWidget(p)
            ph.addStretch()
            self.layout.addLayout(ph)
            
        # text horiontal alignment in vbox
        
        if self.align>1: self.layout.addStretch()
        
        # the message is:
        
        textfield = QTextEdit(self.text)#QLabel(self.text)
        
        if self.textSize==4:
            textfield.setObjectName("biglabel")
        elif self.textSize==3:
            textfield.setObjectName("smalllabel")
        elif self.textSize==2:
            textfield.setObjectName("smallerlabel")
        elif self.textSize==1:
            textfield.setObjectName("tinylabel")

        textfield.setAlignment(Qt.AlignCenter)
        textfield.setReadOnly(True)
        self.layout.addWidget(textfield)
        
        # the pixmap ist (in case of pmapalign=1
        
        if self.pixmap and self.pmapalign==2:
            ph = QHBoxLayout()
            ph.addStretch()
            p = QLabel()
            p.setPixmap(self.pixmap)
            ph.addWidget(p)
            ph.addStretch()
            self.layout.addLayout(ph)
        
        
        # the buttons are:
        
        if not (self.text_okay==None and self.text_deny==None):
            butbox =QWidget()       
            if self.buttVert: blayou = QVBoxLayout()
            else: blayou = QHBoxLayout()
            
            butbox.setLayout(blayou)
            
            if self.buttVert: blayou.addStretch()
        
        if not self.text_okay==None:
            but_okay = QPushButton(self.text_okay)
            
            if self.btnTextSize==4:
                but_okay.setObjectName("biglabel")
            elif self.btnTextSize==3:
                but_okay.setObjectName("smalllabel")
            elif self.btnTextSize==2:
                but_okay.setObjectName("smallerlabel")
            elif self.btnTextSize==1:
                but_okay.setObjectName("tinylabel")
            
            but_okay.clicked.connect(self.on_select)
        
            blayou.addWidget(but_okay)
        
        if not self.text_deny==None:
            but_deny = QPushButton(self.text_deny)
            
            if self.btnTextSize==4:
                but_deny.setObjectName("biglabel")
            elif self.btnTextSize==3:
                but_deny.setObjectName("smalllabel")
            elif self.btnTextSize==2:
                but_deny.setObjectName("smallerlabel")
            elif self.btnTextSize==1:
                but_deny.setObjectName("tinylabel")
            
            but_deny.clicked.connect(self.on_select)
        
            blayou.addWidget(but_deny)
        
        # finalize layout
        
        if self.align<3: self.layout.addStretch()
        
        if not (self.text_okay==None and self.text_deny==None):
            self.layout.addWidget(butbox)
        
        self.centralWidget.setLayout(self.layout)
        
        # and run...
        
        TouchDialog.exec_(self)
        if self.confbutclicked==True: return True, None
        if self.text_okay==None and self.text_deny==None: return None,None
        elif self.result=="": return False,None
        else: return True,self.result

if __name__ == "__main__":
    print("This is a python3 module containing stuff for ft TXT programming\n")
    print("Current contents:")
    print("def run_program(rcmd):              runs a shell command")
    print("class PicButton(QAbstractButton):   provides a grapical QPushButton")
