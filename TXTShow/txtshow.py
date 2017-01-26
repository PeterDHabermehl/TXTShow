#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys, time, os
from TxtStyle import *
from threading import Timer
from auxiliaries import *

local = os.path.dirname(os.path.realpath(__file__)) + "/"
icondir = local + "icons/"
picsdir = local + "pics/"
ovldir = local + "overlay/"
        
class FtcGuiApplication(TxtApplication):
    def __init__(self, args):
        TxtApplication.__init__(self, args)
        
        self.maxpic=0
        self.maxdir=0
        self.currpic=1
        self.currdir=""
        self.autorotate=True
        self.autoscale=True
        self.allowZoom=False
        self.timerdelay=3000
        
        self.window = TxtWindow("TXTShow")
        self.setupLayout()
        
        self.timer =QTimer(self)
        self.timer.timeout.connect(self.on_timer)
        
        self.scan_directories()
        
        # read preferences here
        
        self.scan_images()
        
        self.window.show()
        
        self.timer.start(self.timerdelay)
        self.on_timer() # erstes Bild laden!
         
        self.exec_()        

#
#*****************************
#

    def on_timer(self):
        if not self.layer_picture.isVisible():
            return()
        self.currpic=self.currpic+1
        self.scan_images()
        if self.currpic>=len(self.picstack): self.currpic=0
        self.layer_picture.setAlignment(Qt.AlignCenter)
        
        self.offset_x=0
        self.offset_y=0
        
        self.currpixmap=QPixmap(picsdir+self.currdir+"/"+self.picstack[self.currpic])
        
        if (self.currpixmap.size().width()>self.currpixmap.size().height()) and self.autorotate:
            self.currpixmap = self.currpixmap.transformed(QTransform().rotate(270))
        
        if self.currpixmap.width()>240 or self.currpixmap.height()>320:
            self.allowZoom=True
        else:
            self.allowZoom=False
        
        if self.autoscale or (not self.allowZoom):
            self.layer_picture.setPixmap(self.currpixmap.scaled(QSize(240, 320), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.paint_zoom()        
                
        self.fw_dial.setValue(self.currpic+1)
    
    def paint_zoom(self):
        if not self.allowZoom: return()
        base_x = (self.currpixmap.width()/2)-120
        base_y = (self.currpixmap.height()/2)-160
        target=QPixmap(240,320)
        p = QPainter()
        p.begin(target)
        p.drawPixmap(0,0,240,320,self.currpixmap,base_x+self.offset_x,base_y+self.offset_y,240,320)
        p.end()
        self.layer_picture.setPixmap(target)
    
    def scan_directories(self):
        dirs = os.listdir(picsdir)
        
        self.dirstack=list()
        
        for data in dirs:
            if os.path.isdir(picsdir + data): self.dirstack.append(data)
        
        self.dirstack.sort()
        self.album.clear()
        self.album.addItems(self.dirstack)
        
    def scan_images(self):
        
        self.picstack=list()
        
        if self.currdir in self.dirstack:
            self.picstack=os.listdir(picsdir+self.currdir)
            self.picstack.sort()
        elif len(self.dirstack)>0:
            self.currdir=self.dirstack[0]
            self.picstack=os.listdir(picsdir+self.currdir)
            self.picstack.sort()
  
        if len(self.picstack)==0:
            self.picstack=list()
            if self.currdir != "":
              self.picstack.append("../fail.png")
            else: self.picstack.append("fail.png")
            self.currpic=0
        
        self.fw_dial.setRange(1,len(self.picstack))
       
              
    def switch(self):
        self.fw_dial.setValue(self.currpic+1)
        if self.myStack.currentIndex()==0:
          self.myStack.setCurrentIndex(1)
        elif self.myStack.currentIndex()==1:
          self.myStack.setCurrentIndex(2)
        else:
          self.myStack.setCurrentIndex(0)
    
    def switchback(self):
        self.fw_dial.setValue(self.currpic+1)     
        if self.myStack.currentIndex()==2:
          self.myStack.setCurrentIndex(1)
        elif self.myStack.currentIndex()==1:
          self.myStack.setCurrentIndex(0)
        else:
          self.myStack.setCurrentIndex(2)
    
        
    def setupLayout(self):
        # create the empty main window
        
        self.myStack = QStackedWidget()

        self.myStackLayout1 = QWidget() # Layout 1 -> vor- und zurückblättern
        self.myStackLayout2 = QWidget() # Layout 2 -> Bilder verschieben und löschen
        self.myStackLayout3 = QWidget() # Layout 3 -> Alben(Ordner) verwalten
        
        self.FirstWidget()
        self.SecondWidget()
        self.ThirdWidget()
        
        self.myStack.addWidget(self.myStackLayout1)
        self.myStack.addWidget(self.myStackLayout2)
        self.myStack.addWidget(self.myStackLayout3)
        
        self.myStack.setCurrentIndex(0)
        
        self.window.setCentralWidget(self.myStack)
        
        self.layer_black = QLabel(self.window)
        self.layer_black.setGeometry(0, 0, 240, 320)
        self.layer_black.setPixmap(QPixmap(ovldir+"ovl_black.png"))

        self.layer_picture = QLabel(self.window)
        self.layer_picture.setGeometry(0, 0, 240, 320)
        self.layer_picture.mousePressEvent=self.on_picture_clicked
        
        self.layer_overlay = QLabel(self.window)
        self.layer_overlay.setGeometry(0, 0, 240, 320)
        self.layer_overlay.setPixmap(QPixmap(ovldir+"ovl_pause.png"))
        self.layer_overlay.mousePressEvent=self.on_ovl_clicked

        self.layer_overlay.hide()
        
    def toggle_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            if self.autoscale: self.layer_overlay.setPixmap(QPixmap(ovldir+"ovl_play.png"))
            else: self.layer_overlay.setPixmap(QPixmap(ovldir+"ovl_play_zoom.png"))
        else:
            self.timer.start(self.timerdelay)
            if self.autoscale: self.layer_overlay.setPixmap(QPixmap(ovldir+"ovl_pause.png"))
            else: self.layer_overlay.setPixmap(QPixmap(ovldir+"ovl_pause_zoom.png"))
    
    def toggle_autoscale(self):
        self.autoscale=not self.autoscale
        #if not self.allowZoom: self.autoscale=True
        if self.timer.isActive():
            if self.autoscale: self.layer_overlay.setPixmap(QPixmap(ovldir+"ovl_pause.png"))
            else: self.layer_overlay.setPixmap(QPixmap(ovldir+"ovl_pause_zoom.png"))
        else:
            if self.autoscale: self.layer_overlay.setPixmap(QPixmap(ovldir+"ovl_play.png"))
            else: self.layer_overlay.setPixmap(QPixmap(ovldir+"ovl_play_zoom.png"))
            
    def on_picture_clicked(self,event):
        x = event.pos().x()
        y = event.pos().y()
        
        if x<48: column="left"
        elif x>191: column="right"
        elif x>95 and x<145: column="middle"
        else: column="empty"
        
        if y<48: row="top"
        elif y>272: row="bottom"
        elif y>135 and y<185: row="middle"
        else: row="empty"
        
        if self.autoscale:
            #if row=="top" and column=="right": self.program_exit()
            if row=="middle":
                tx = self.timer.isActive()
                if column=="left":
                    self.timer.stop()
                    self.currpic=self.currpic-2
                    if self.currpic<-1: self.currpic=len(self.picstack)-2
                    self.on_timer()
                    if tx: self.timer.start(self.timerdelay)
                elif column=="right":
                    self.timer.stop()
                    self.on_timer()
                    if tx: self.timer.start(self.timerdelay)
                else: self.layer_overlay.show()
            else: self.layer_overlay.show()
        else: self.layer_overlay.show()
    

    
    def on_ovl_clicked(self,event):
        
        x = event.pos().x()
        y = event.pos().y()
        
        if x<48: column="left"
        elif x>191: column="right"
        elif x>95 and x<145: column="middle"
        else: column="empty"
        
        if y<48: row="top"
        elif y>272: row="bottom"
        elif y>135 and y<185: row="middle"
        else: row="empty"
        
        if self.autoscale:  #bei automatischer größenanpassung
            if row=="top" and column=="right": self.program_exit()
            elif row=="top" and column=="middle": row="empty"
            elif row=="top" and column=="left": self.layer_hide()
            elif row=="bottom" and column=="right": self.toggle_timer()
            elif row=="bottom" and column=="left":
                self.toggle_autoscale()
                self.currpic=self.currpic-1
                self.on_timer()
            elif row=="bottom" and column=="middle": row="empty"
                
            if row=="middle":
                tx = self.timer.isActive()
                if column=="left":
                    self.timer.stop()
                    self.currpic=self.currpic-2
                    if self.currpic<-1: self.currpic=len(self.picstack)-2
                    self.on_timer()
                    if tx: self.timer.start(self.timerdelay)
                elif column=="right":
                    self.timer.stop()
                    self.on_timer()
                    if tx: self.timer.start(self.timerdelay)
                else: column="empty"
        
        else:  # bei 1:1 (zoom) -> anderes overlay
            if row=="bottom" and column=="right": self.toggle_timer()
            elif row=="bottom" and column=="left":
                self.toggle_autoscale()
                self.currpic=self.currpic-1
                self.on_timer()
            elif row=="middle" and column=="middle":
                row="empty"
            elif row=="middle" and column=="left":
                self.offset_x=max(0-(self.currpixmap.width()/2)+120,self.offset_x-64)
                self.paint_zoom()
            elif row=="middle" and column=="right":
                self.offset_x=min((self.currpixmap.width()/2)-120,self.offset_x+64)
                self.paint_zoom()
            elif row=="top" and column=="middle":
                self.offset_y=max(0-(self.currpixmap.height()/2)+160,self.offset_y-64)
                self.paint_zoom()
            elif row=="bottom" and column=="middle":
                self.offset_y=min((self.currpixmap.height()/2)-160,self.offset_y+64)
                self.paint_zoom()
            elif row=="top" and column=="right":
                row="empty"
            elif row=="top" and column=="left":
                row="empty"
                
        if row=="empty" or column=="empty": self.layer_overlay.hide()
        
    
    def layer_hide(self):
        self.scan_directories()
        self.scan_images()
        self.layer_black.hide()
        self.layer_picture.hide()
        self.layer_overlay.hide()
        
    def layer_show(self):
        if self.timer.isActive(): 
            self.timer.stop()
            self.timer.start(self.timerdelay)
        self.layer_black.show()
        self.layer_picture.show()
        self.layer_overlay.hide()
        self.currpic=self.currpic-1
        self.on_timer() # --> load current picture here
    
    def program_exit(self):
        exit()
        
    def FirstWidget(self):
        layout = QVBoxLayout()
        

        self.fw_dial = QDial()
        self.fw_dial.setNotchesVisible(True)
        self.fw_dial.setRange(1,10)        
        self.fw_dial.valueChanged.connect(self.fw_show_value)
        layout.addWidget(self.fw_dial)
        
        midbox = QHBoxLayout()
  
        #midbox.addStretch()
        self.fw_bckbutt = PicButton(QPixmap(icondir+"arrow-left.png"))
        self.fw_bckbutt.setMinimumHeight(50)
        self.fw_bckbutt.clicked.connect(self.fw_bckbutt_clicked)
        midbox.addWidget(self.fw_bckbutt)
        
        midbox.addStretch()
        self.fw_current = QLabel()
        self.fw_current.setAlignment(Qt.AlignCenter)
        midbox.addWidget(self.fw_current)
        midbox.addStretch()
        
        self.fw_fwdbutt = PicButton(QPixmap(icondir+"arrow-right.png"))
        self.fw_fwdbutt.clicked.connect(self.fw_fwdbutt_clicked)
        midbox.addWidget(self.fw_fwdbutt)
                
        layout.addLayout(midbox)
        
        bottbox = QHBoxLayout()
        
        self.fw_pback = PicButton(QPixmap(icondir+"go-previous-disabled.png"))
        
        bottbox.addWidget(self.fw_pback)
        bottbox.addStretch()
        
        
        fw_preturn = PicButton(QPixmap(icondir+"key-enter.png"))
        fw_preturn.clicked.connect(self.layer_show)
        bottbox.addWidget(fw_preturn)
        
        self.fw_camera = PicButton(QPixmap(icondir+"camera-web-disabled.png"))
        self.fw_camera.setEnabled(False)
        self.fw_camera.setDisabled(True)
        bottbox.addWidget(self.fw_camera)
        bottbox.addStretch()
        
        self.fw_pfwd = PicButton(QPixmap(icondir+"go-next.png"))
        bottbox.addWidget(self.fw_pfwd)
        
        layout.addLayout(bottbox)
                
        self.myStackLayout1.setLayout(layout)
        
        self.fw_pfwd.clicked.connect(self.switch)
        
        self.fw_dial.setValue(5)
    
    def fw_bckbutt_clicked(self):
        self.fw_dial.setValue(max(1,self.fw_dial.value()-1))
    
    def fw_fwdbutt_clicked(self):
        self.fw_dial.setValue(min(self.fw_dial.value()+1,self.fw_dial.maximum()))

    def fw_show_value(self):
        self.fw_current.setText(str(self.fw_dial.value()))
        self.currpic=self.fw_dial.value()-1
        
    def SecondWidget(self):
        layout = QVBoxLayout()
        
        self.sw_image=QLabel()
        self.sw_image.setStyleSheet("border: 2px solid; border-style: outset")
        layout.addWidget(self.sw_image)
        
        midbox = QHBoxLayout()
        midbox.addStretch()
        
        self.sw_copy = PicButton(QPixmap(icondir+"edit-copy.png"))
        #self.sw_copy.clicked.connect(self.sw_copy_clicked)
        midbox.addWidget(self.sw_copy)
        
        midbox.addStretch()
        
        self.sw_move = PicButton(QPixmap(icondir+"edit-cut.png"))
        #self.sw_move.clicked.connect(self.sw_move_clicked)
        midbox.addWidget(self.sw_move)
        
        midbox.addStretch()
        
        self.sw_delete = PicButton(QPixmap(icondir+"trash-empty.png"))
        midbox.addWidget(self.sw_delete)
        midbox.addStretch()
        
        layout.addLayout(midbox)
        
        
        bottbox = QHBoxLayout()
        
        self.sw_pback = PicButton(QPixmap(icondir+"go-previous.png"))
        
        bottbox.addWidget(self.sw_pback)
        bottbox.addStretch()
        
        
        sw_preturn = PicButton(QPixmap(icondir+"key-enter.png")) 
        sw_preturn.clicked.connect(self.layer_show)
        bottbox.addWidget(sw_preturn)
        
        self.sw_camera = PicButton(QPixmap(icondir+"camera-web-disabled.png")) 
        self.sw_camera.setEnabled(False)
        self.sw_camera.setDisabled(True)
        bottbox.addWidget(self.sw_camera)
        bottbox.addStretch()
        
        self.sw_pfwd = PicButton(QPixmap(icondir+"go-next.png"))
        bottbox.addWidget(self.sw_pfwd)
        self.sw_pfwd.clicked.connect(self.switch)
        self.sw_pback.clicked.connect(self.switchback)
        
        layout.addLayout(bottbox)
        
        self.myStackLayout2.setLayout(layout)

    def albumlist(self):
        if self.album.currentItem():
          self.currdir=self.album.currentItem().text()
          self.scan_images()
          self.currpic=0
          self.on_timer()
        
    def ThirdWidget(self):
        layout = QVBoxLayout()
     
        self.album = QListWidget()
        self.album.addItems([])
        self.album.currentItemChanged.connect(self.albumlist)
        layout.addWidget(self.album)
        
        bottbox = QHBoxLayout()
        
        self.tw_pback = PicButton(QPixmap(icondir+"go-previous.png"))
        
        midbox=QHBoxLayout()
        
        midbox.addStretch()
        
        tw_addAlbum = PicButton(QPixmap(icondir+"folder-add.png"))
        midbox.addWidget(tw_addAlbum)

        midbox.addStretch()
        
        tw_delAlbum = PicButton(QPixmap(icondir+"folder-del.png"))
        midbox.addWidget(tw_delAlbum)
        
        midbox.addStretch()
        
        tw_renameAlbum = PicButton(QPixmap(icondir+"edit-rename.png"))
        midbox.addWidget(tw_renameAlbum)
        
        midbox.addStretch()
       
        layout.addLayout(midbox)
        layout.addStretch()
        
        bottbox.addWidget(self.tw_pback)
        bottbox.addStretch()
        
        
        tw_preturn = PicButton(QPixmap(icondir+"key-enter.png")) 
        tw_preturn.clicked.connect(self.layer_show)
        bottbox.addWidget(tw_preturn)
        
        self.tw_camera = PicButton(QPixmap(icondir+"camera-web-disabled.png"))
        self.tw_camera.setEnabled(False)
        self.tw_camera.setDisabled(True)
        bottbox.addWidget(self.tw_camera)
        bottbox.addStretch()
        
        self.tw_pfwd = PicButton(QPixmap(icondir+"go-next-disabled.png"))
        bottbox.addWidget(self.tw_pfwd)
        #self.tw_pfwd.clicked.connect(self.switch)
        self.tw_pback.clicked.connect(self.switchback)
        
        layout.addLayout(bottbox)
        
        self.myStackLayout3.setLayout(layout)
   
                             
if __name__ == "__main__":
    FtcGuiApplication(sys.argv)