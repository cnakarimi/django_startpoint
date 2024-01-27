from django.shortcuts import render, redirect

from django.http import HttpResponse

from .models import Task

from .forms import TaskForm, CreateUserForm, LoginForm


from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout


from django.contrib.auth.decorators import login_required




# Homepage / first page of website
def homepage(request):
    
    return render(request, 'crm/index.html')


# CRUD - Create a task

def create_task(request):
    
    form = TaskForm()
    
    
    if request.method == 'POST':
        
        form = TaskForm(request.POST)
        
        if form.is_valid():
            
            form.save()
            
            return redirect('view-tasks')
            
            
    
    context = {'TaskForm':form}
    
    return render(request,'crm/create-task.html',context)


# CRUD - Read a tasks

def tasks(request):

    queryDataAll = Task.objects.all()
    
    context={'AllTasks':queryDataAll}
    
    return render(request,'crm/view-tasks.html',context)



# CRUD - Update a tasks

def update_task(request, pk):
    
    task = Task.objects.get(id=pk)
    
    form = TaskForm(instance=task)
    
    if request.method == 'POST':
        
        form = TaskForm(request.POST, instance=task)
        
        if form.is_valid():
            
            form.save()
            
            return redirect('view-tasks')
        
    context = {'UpdateTask': form}
    
    return render(request, 'crm/update-task.html', context)



# CRUD - Delete task

def delete_task(request, pk):
    
    task = Task.objects.get(id=pk)
    
    if request.method == 'POST':
        
        task.delete()
        
        return redirect('view-tasks')
    
    return render(request, 'crm/delete-task.html')
    


# Registration webpage

def register(request):
    
    form = CreateUserForm()
    
    if request.method == 'POST':
        
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            
            form.save()
            
            return redirect('my-login')
    
    context = {'RegistrationForm': form}



    return render(request, 'crm/register.html', context)



# Login

def my_login(request):
    
    form = LoginForm()
    if request.method == 'POST':
        
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                
                auth.login(request, user)
                
                return redirect('dashboard')

    context = {'LoginForm': form}
    
    return render(request, 'crm/my-login.html', context)







# Dashboard

@login_required(login_url= 'my-login')
def dashboard(request):
    
    return render(request, 'crm/dashboard.html')



# Logout

def user_logout(requset):
    
    auth.logout(requset)
    
    return redirect('')
