from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST, require_http_methods 

from .models import Employee
from .forms import EmployeeForm

@require_GET
def employee_list(request):
    employees = Employee.objects.all()

    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'list.html', {
        'page_obj': page_obj
    })

# --------------------------------------------------
# Add Employee
# --------------------------------------------------   

@require_http_methods(["GET", "POST"])
def employee_create(request):

    if request.method == 'POST':
        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Employee create successfully.')
            return redirect('employee_list')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = EmployeeForm()

    return render(request, 'add.html', {'form':form})  

@require_http_methods(["GET", "POST"])
def employee_edit(request, emp_uuid):

    employee = get_object_or_404(Employee, uuid=emp_uuid)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)

        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employee_list')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'edit.html', {'form': form, 'employee':employee})

@require_POST
def employee_delete(request, emp_uuid):

    employee = get_object_or_404(Employee, uuid=emp_uuid)
    employee_name = employee.emp_name
    employee.delete()

    messages.success(request, f'Employee "{employee_name}" deleted successfully.')
    return redirect('employee_list')