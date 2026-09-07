from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from .models import Student
from .forms import StudentForm

@require_GET
def student_list(request):
    students = Student.objects.all()

    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student_list.html', {'page_obj': page_obj})

@require_http_methods(['GET', 'POST'])
def student_add(request):

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Student save successfully.')
            return redirect('student_list')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = StudentForm()

    return render(request, 'student_add.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def student_edit(request, student_uuid):

    student = get_object_or_404(Student, uuid=student_uuid)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            messages.success(request, 'Student details edit successfully.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = StudentForm(instance=student)

    return render(request, 'student_edit.html', {'form':form, 'student':student})


def student_delete(request, student_uuid):

    student = get_object_or_404(Student, uuid=student_uuid)
    student_name = student.student_name
    student.delete()

    messages.success(request, f'Student {student_name} deleted successfully.')
    return redirect('student_list')
