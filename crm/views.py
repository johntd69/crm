from django.shortcuts import render,redirect
from django.views.generic import View
# Create your views here.
from crm.forms import EmployeeForm,EmployeeModelForm,RegistrationForm,LoginForm
from crm.models import Employees
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


@method_decorator(signin_required,name="dispatch")
class EmployeeCreateView(View):
    def get(self,request,*args,**kwargs):
        form=EmployeeModelForm()
        return render(request,"emp_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=EmployeeModelForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Employee details added successfully")
            print(form.cleaned_data)
            # Employees.objects.create(**form.cleaned_data)
            print("created")
            return render(request,"emp_add.html",{"form":form})
        else:
            messages.error(request,"Fail to add employee")
            return render(request,"emp_add.html",{"form":form})
@method_decorator(signin_required,name="dispatch")
class EmployeeListView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            qs=Employees.objects.all()
            return render(request,"emp_list.html",{"data":qs})
        else:
            messages.error(request,"invalid session")
            return redirect("signin")

    
    def post(self,request,*args,**kwargs):
        name=request.POST.get("box")
        qs=Employees.objects.filter(name__icontains=name)
        return render(request,"emp_list.html",{"data":qs})
@method_decorator(signin_required,name="dispatch")
class EmployeeDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employees.objects.get(id=id)
        return render(request,"emp_detail.html",{"data":qs})
@method_decorator(signin_required,name="dispatch")
class EmployeeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employees.objects.get(id=id).delete()
        messages.success(request,"employee details deleted")
        return redirect("emp-all")
@method_decorator(signin_required,name="dispatch")
class EmployeeUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Employees.objects.get(id=id)
        form=EmployeeModelForm(instance=obj)
        return render(request,"emp_edit.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Employees.objects.get(id=id)

        form=EmployeeModelForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,"employee details updated")
            return redirect("emp-details",pk=id)
        else:
            messages.error(request,"fail to update employee details")
            return render(request,"emp_edit.html",{"form":form})
        
class SignupView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"created successfully :)")
            return render(request,"register.html",{"form":form})
            print("saved")
        else:
            print("failed")
            return render(request,"register.html",{"form":form})
        
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            # print(u_name,password)
            user_obj=authenticate(request,username=u_name,password=password)
            if user_obj:
                print("valid credintial")
                login(request,user_obj)
                return redirect("emp-all")
            
        messages.error(request,"invalid credential")
        return render(request,"login.html",{"form":form})
@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

    
        
   