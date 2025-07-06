from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage

from  . import models
from . import emailAPI

import time

def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def service(request):
    return render(request,"service.html")

def register(request):
    if request.method=="GET":
        return render(request,"register.html",{"output":""})
    else:
        #to recieve data from UI 'form'
        name=request.POST.get("name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")

        #to insert record in database using models
        p=models.Register(name=name,email=email,password=password,mobile=mobile,address=address,city=city,gender=gender,status=0,role="user",info=time.asctime())
        p.save()

        #to integrate Email API
        emailAPI.sendemail(email,password)

        return render(request,"register.html",{"output":"User register successfully...."})    


def login(request):
    if request.method=="GET":    
        return render(request,"login.html",{"output":""})
    else:
        #to recieve data from UI 'form'
        email=request.POST.get("email")
        password=request.POST.get("password")

        #to check record in database
        userDetails=models.Register.objects.filter(email=email,password=password,status=1)

        if len(userDetails)>0:

            request.session['sun'] = userDetails[0].email
            request.session['srole'] = userDetails[0].role

            #print(userDetails[0].role) #to get user role
            if userDetails[0].role=="admin":
                return redirect("/myadmin/")
            else:    
                return redirect("/user/")
        else:
            return render(request,"login.html",{"output":"Invalid user or verify your account...."})            


def verify(request):
    vemail=request.GET.get("vemail")
    models.Register.objects.filter(email=vemail).update(status=1)
    return redirect("/user/")


def adminhome(request):
    return render(request,"adminhome.html",{"sun":request.session["sun"]})

def manageusers(request):
    userDetails=models.Register.objects.filter(role="user")
    return render(request,"manageusers.html",{"userDetails":userDetails})    

def manageuserstatus(request):
    #to get data from url
    s=request.GET.get("s")
    regid=int(request.GET.get("regid"))

    if s=="active":
        models.Register.objects.filter(regid=regid).update(status=1)
    elif s=="inactive":
        models.Register.objects.filter(regid=regid).update(status=0)
    else:
        models.Register.objects.filter(regid=regid).delete()
                    

    return redirect("/manageusers/")

def userhome(request):
    return render(request,"userhome.html",{"sun":request.session["sun"]})


def sharenotes(request):
    if request.method=="GET":
        return render(request,"sharenotes.html",{"sun":request.session["sun"],"output":""})
    else:

        #to recieve data from ui
        title=request.POST.get("title")
        category=request.POST.get("category")
        description=request.POST.get("description")

        #to recive file & to push file in media folder
        file=request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(file.name,file)

        p=models.sahrenotes(title=title,category=category,description=description,filename=filename,uid=request.session["sun"],info=time.asctime())
        p.save()

        return render(request,"sharenotes.html",{"sun":request.session["sun"],"output":"Content uploaded successfully....."})   


def viewnotes(request):
    data=models.sahrenotes.objects.all()
    return render(request,"viewnotes.html",{"sun":request.session["sun"],"data":data})             


def funds(request):
    paypalURl ="https://www.sandbox.paypal.com/cgi-bin/webscr"
    paypalID = ""
    amt=100
    return render(request,"funds.html")



def cpadmin(request):
    email=request.session["sun"]
    if request.method == "GET":
        return render(request,"cpadmin.html",{"sun":email,"output":""})
    else:
        opass = request.POST.get("opass")
        npass = request.POST.get("npass")
        cpass = request.POST.get("cpass")

    userDetails = models.Register.objects.filter(email=email,password=opass)

    if len(userDetails)>0:
        if npass==cpass:
            models.Register.objects.filter(email=email).update(password=cpass)
        else:
            msg ="New & Confirm new password is not same"
    return render(request,"cpadmin.html",{"sun":email,"output":msg})

def epadmin (request):
    email = request.session["sun"]
    UserDetails = models.Register.objects.filter(email=email)
    return render(request,"epadmin.html",{"sun":email,"user":UserDetails[0]})