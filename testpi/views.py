# Written By - Ankesh

import os 
from django.shortcuts import render
from datetime import datetime as dt
from django.http import HttpResponse

# To write commands typed in text box in an file.
def likho_file_mai(cmd):
    f = open("testpi/script","a")
    if(cmd == "history"):
        f.write("cat {0}\n".format(cmd))
    else:
        f.write("{0}\n".format(cmd))
    f.close()
    os.system("chmod +x testpi/script")
    return True

# To run command on device
def run_command(cmd):
    dir = os.getcwd()
    if(cmd == "clear"):
        os.system("echo 'No History' > testpi/history")
        return {'pwd':dir,'output': ""}
    else:
        if(likho_file_mai(cmd)):
            dircontent =  os.listdir()
            os.system("cd testpi && ./script>output")
            # Preparing content to represent 
            f = open("{0}/testpi/output".format(dir),'r')
            content = ""
            for x in f:
             content+='<p style="margin-right:3px;">{0}</p>'.format(x)
            f.close()
            with open("testpi/history", 'a') as h:
                with open("testpi/output", 'r') as o:
                    h.write(o.read())
            os.system("cd testpi && rm script && rm output")
            return {'pwd':dir,'output': content}

# To get the output of command after running on device with parameters
def getOutput(cmd):
    output = run_command(cmd)
    params = {'locationName':'Zara','User':'Web Team', 'cmd':cmd ,'output':output}
    return params

# To get command typed in input box
def getCmd(request):
    cmd = request.GET.get('cmdInput',"")
    return getOutput(cmd)

# It will reneder index.html page
def index(request):
    params = {'device1':{'name': 'Zara','href':'Zara/'},'device2':{'name': 'Levis','href':'Levis/'}}
    return render(request, 'index.html', params)

# It will render devices.html with Zara spacific data
def Zara(request):
    params = getCmd(request)
    return render(request, 'devices.html', params)

# It will render devices.html with Levis spacific data
def Levis(request):
    params = getCmd(request)
    params['User'] = 'IOT Team'
    return render(request, 'devices.html', params)

