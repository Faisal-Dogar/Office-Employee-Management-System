from django.shortcuts import render,redirect,HttpResponse
from .models import Employee,Role,Department
from django.utils import timezone

def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'all_emp.html', context)

def add_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept_id = int(request.POST['dept'])
        role_id = int(request.POST['role'])

        department = Department.objects.get(id=dept_id)
        role = Role.objects.get(id=role_id)

        new_emp = Employee(
            name=name, 
            salary=salary, 
            bonus=bonus, 
            phone=phone, 
            dept=department, 
            role=role, 
            hire_date=timezone.now()
        )
        new_emp.save()
        return render(request, 'add_emp.html', {
            'departments': Department.objects.all(),
            'roles': Role.objects.all(),
            'success_message': 'Employee added successfully!'
        })

    elif request.method == 'GET':
        departments = Department.objects.all()
        roles = Role.objects.all()
        return render(request, 'add_emp.html', {'departments': departments, 'roles': roles})

    else:
        return HttpResponse("Invalid request method.")
    

# def remove_emp(request, emp_id = 0):
#     if emp_id:
#         try:
#             emp_to_be_removed = Employee.objects.get(id=emp_id)
#             emp_to_be_removed.delete()
#             return HttpResponse("Employee Removed Successfully")
#         except:
#             return HttpResponse("Please Enter A Valid EMP ID")
#     emps = Employee.objects.all()
#     context = {
#         'emps': emps
#     }
#     return render(request, 'remove_emp.html',context)

def remove_emp(request, emp_id=0):
    if request.method == 'POST':
        emp_id = int(request.POST.get('emp_id', emp_id))
        emp_to_be_removed = Employee.objects.filter(id=emp_id).first()
        if emp_to_be_removed:
            emp_to_be_removed.delete()
            return redirect('remove_emp')
        else:
            return HttpResponse("Please Enter A Valid EMP ID")

    elif emp_id:
        emp_to_be_removed = Employee.objects.filter(id=emp_id).first()
        if emp_to_be_removed:
            emp_to_be_removed.delete()
            return redirect('remove_emp')
        else:
            return HttpResponse("Please Enter A Valid EMP ID")

    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', context)




def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(name__icontains = name) 
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        if role:
            emps = emps.filter(role__name__icontains = role)

        context = {
            'emps': emps
        }
        return render(request, 'all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An Exception Occurred')