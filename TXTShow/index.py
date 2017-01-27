#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import cgi
import sys, os, shlex, time, json
#from TxtStyle import *
from PyQt4 import QtGui, QtCore
from subprocess import Popen, call, PIPE

local = os.path.dirname(os.path.realpath(__file__)) + "/"
local = ""
picsdir = local + "pics/"

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

def scan_for_images():
    global picstack, maxpic
    
    picstack = run_program("ls " + picsdir).split()
    maxpic = len(picstack)

def save_uploaded_file():
    form = cgi.FieldStorage()
    if "datei" not in form:
        return False,"No appfile"

    fileitem = form["datei"]
    if not fileitem.file or not fileitem.filename:
        return False,"No valid file"

    filename = fileitem.filename
    
    print("Writing file to " + filename + "<br/>")
    open(localdir+filename, 'wb').write(fileitem.file.read())

    return True,filename

def create_html_output():
    global picstack, maxpic, picsdir
    
    print('Content-Type: text/html')
    print('')
    print('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
    print('<html xmlns="http://www.w3.org/1999/xhtml">')
    print('<head>')
    print('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
    print('<meta http-equiv="cache-control" content="max-age=0" />')
    print('<meta http-equiv="cache-control" content="no-cache" />')
    print('<meta http-equiv="expires" content="0" />')
    print('<meta http-equiv="expires" content="Tue, 01 Jan 1980 1:00:00 GMT" />')
    print('<meta http-equiv="pragma" content="no-cache" />')
    print('<title>TXTShow</title>')
    print('<link rel="stylesheet" href="/txt.css" />')
    print('<link rel="icon" href="/favicon.ico" type="image/x-icon" />')
    print('</head>')
    
    print('<body>')
       
    print('<center>')

    print('<h1><div class="outline"><font color="red">fischer</font><font color="#046ab4">technik</font>&nbsp;<font color="#fcce04">TXT</font></div></h1>')
    
    print('<p/><h1>TXTShow</h1><p/>Present your images on the TXT<br>')

    print('<div style="width:90%; height:296px; line-height:3em;overflow:scroll;padding:5px;background-color:#549adc;color:#0c6acc;border:4px solid #0c6acc;border-style: outset;">')
    
    for pic in picstack:
      print('<div title="'+pic+'"; style="width:80; height:124px; float: left; padding: 2px; margin: 4px; border:1px #0c6acc solid; border-style: inset;"><a href="'+picsdir+pic+'">')
      print('<img style="border:1px #0c6acc solid; border-style: outset" src="'+picsdir+pic+'" height="96"></a><br>')
      print('<center><a href="index.py?r='+pic+'" onclick="return confirm('+"'"+'Really delete image '+pic+'?'+"'"+')"><img src="remove.png"></a></center>')
      print('</div>')


    print('</div><br>')
    
    print('Click on the picture itself to view. Right-click to download.<br>Click <img src="remove.png"> to remove picture from TXT <b>permanently.</b><br><br>')
    print('Pictures should be 240px wide and 320px high to be shown correctly.<br>')
    print('<form action="index.py" method="post" enctype="multipart/form-data">')
    print('<label>Select a picture to add (*.png, *.jpg):')
    print('<input name="datei" type="file" size="50" accept="image/*"> </label>')
    print('<button type="submit">Add</button></form>')
    print('<br><br><a href="/"> TXT Home </a>')
    
    print('</body></html>')

def upload():    
    
    print('Content-Type: text/html')
    print('')
    print('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
    print('<html xmlns="http://www.w3.org/1999/xhtml">')
    print('<head>')
    print('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
    print('<meta http-equiv="cache-control" content="max-age=0" />')
    print('<meta http-equiv="cache-control" content="no-cache" />')
    print('<meta http-equiv="expires" content="0" />')
    print('<meta http-equiv="expires" content="Tue, 01 Jan 1980 1:00:00 GMT" />')
    print('<meta http-equiv="pragma" content="no-cache" />')
    print('<title>TXTShow</title>')
    print('<link rel="stylesheet" href="/txt.css" />')
    print('<link rel="icon" href="/favicon.ico" type="image/x-icon" />')
    print('</head>')
    
    print('<body>')
       
    print('<center>')

    print('<h1><div class="outline"><font color="red">fischer</font><font color="#046ab4">technik</font>&nbsp;<font color="#fcce04">TXT</font></div></h1>')
    
    print('<p/><h1>TXTShow</h1><p/>Uploading, please wait...<br>')
    print('</body></html>')

def parse_args():
   #dummy
   print("Baeh")

def save_uploaded_file(tdir):
    global form
    if "datei" not in form:
        return False,"No file"

    fileitem = form["datei"]
    if not fileitem.file or not fileitem.filename:
        return False,"No valid file"

    filename = fileitem.filename
    
    #print("Writing file to " + filename + "<br/>")
    open(tdir+filename, 'wb').write(fileitem.file.read())

    return True,filename


form = cgi.FieldStorage()

if "r" in form:
    #dummy = run_program("mv pics/" + form["r"].value+" pics/."+form["r"].value)
    dummy = run_program("rm pics/" + form["r"].value)
elif "datei" in form:
    upload()
    save_uploaded_file("pics/")
    
scan_for_images()
create_html_output()