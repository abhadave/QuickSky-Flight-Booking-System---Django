from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def login_(request):
    if request.method == 'POST':
        username_data=request.POST['username']
        password_data=request.POST['password']
        u=authenticate(username=username_data,password=password_data)
        print(u)
        if u is not None:
            login(request,u)
            return redirect('home')
        else:
            return render(request,'login.html',{'wrong_credentials':True})

    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        firstname_data=request.POST['firstname']
        lastname_data=request.POST['lastname']
        email_data=request.POST['email']
        username_data=request.POST['username']
        password_data=request.POST['password']
        print(firstname_data,lastname_data,email_data,username_data,password_data)

        try:
            u=User.objects.get(username=username_data)
            return render(request,'register.html',{'username_exist':True})
        
        except:
            u= User.objects.create(
                first_name=firstname_data,
                last_name=lastname_data,
                email=email_data,
                username=username_data,
        
        )
        u.set_password(password_data)
        u.save()
        return redirect('login')


    return render(request,'register.html')

def logout_(request):
    logout(request)
    return redirect('login')

def profile(request):
    return render(request,'profile.html')

def update_profile(request):
    user= User.objects.get(username=request.user.username)
    if request.method == 'POST':
        firstname_data=request.POST['firstname']
        lastname_data=request.POST['lastname']
        email_data=request.POST['email']
        username_data=request.POST['username']
        
        user.first_name=firstname_data
        user.last_name=lastname_data
        user.email=email_data
        user.username=username_data

        user.save()
        return redirect('profile')

    return render(request,'update_profile.html')

def reset_pass(request):
    if request.method == 'POST':
        try:
            oldpass_data=request.POST['oldpassword']
            user_data=User.objects.get(username=request.user.username)
            u=authenticate(username=user_data,password=oldpass_data)
            if u:
                return render(request,'reset_pass.html',{'old_pass_matched':True})
            else:
                return render(request,'reset_pass.html',{'old_pass_notmatched':True})
            
        except:
            newpass_data=request.POST['newpassword']
            confirm_pass_data=request.POST['confirmpassword']

            if newpass_data == confirm_pass_data:
                user= User.objects.get(username=request.user.username)
                user.set_password(newpass_data)
                user.save()
                return redirect('login')
            else:
                return render(request,'reset_pass.html',{'confirm_notmatched':True})

    return render(request,'reset_pass.html')