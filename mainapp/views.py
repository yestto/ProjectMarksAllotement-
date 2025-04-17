import os
from tkinter import Image
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from Final import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import BadHeaderError
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from .models import Student,MarkSheet
from django.db import models
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
import random
from io import BytesIO
from django.core.mail import EmailMessage
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter,landscape,A4
from reportlab.pdfgen import canvas
from django.conf import settings
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from .forms import MentorMarksForm, ExaminerMarksForm
from .forms import MentorEndsemMarksForm, ExaminerEndsemMarksForm
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

from .models import Professor, Student

def professor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')  # Get username from form
        password = request.POST.get('password', '')  # Get password from form

        # Authenticate user by username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                # Check if the user is a professor
                professor = Professor.objects.get(user=user)

                # If credentials match professor, show "Generate OTP" button
                if 'generate_otp' in request.POST:  # If OTP generation is requested
                    # Generate and send OTP (same as in the previous code)
                    otp = random.randint(100000, 999999)
                    subject = "Your OTP Code"
                    email_message = f"Your OTP code is: {otp}"
                    send_mail(subject, email_message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

                    request.session['otp'] = otp
                    request.session['username'] = username
                    messages.success(request, "OTP has been sent to your email.")

                    return render(request, 'login.html', {
                        'show_otp': True,
                        'username': username,
                        'password': password
                    })

                elif 'login' in request.POST:
                    entered_otp = request.POST.get('otp')

                    if 'otp' in request.session and str(request.session['otp']) == entered_otp:
                        login(request, user)
                        request.session.pop('otp', None)
                        return redirect('role_selection')
                    else:
                        messages.error(request, "Invalid OTP or credentials.")

                # Render page with "Generate OTP" button
                return render(request, 'login.html', {
                    'show_generate_otp': True,
                    'username': username,
                    'password': password
                })

            except Professor.DoesNotExist:
                # If the user is a student, redirect to student dashboard
                try:
                    student = Student.objects.get(user=user)
                    return redirect('student_dashboard')   # Redirect to student dashboard
                except Student.DoesNotExist:
                    messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")  # Get the email from the form
        associated_users = User.objects.filter(email=email)  # Filter users by email
        
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                otp = random.randint(100000, 999999)  # Generate a random OTP
                
                # Prepare a simple email message
                email_message = f"""
                Hi {user.username},

                You requested a password reset. Here is your OTP: {otp}

                Please use this OTP to verify your request.

                Thank you,
                Your Website Team
                """
                
                try:
                    send_mail(subject, email_message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)  # Send email
                    # Store OTP in session for later verification
                    request.session['otp'] = otp
                    request.session['username'] = user.username  # Save username to verify later
                    
                    messages.success(request, "OTP has been sent to your email.")  # Success message
                    return redirect("otp_verify")  # Redirect to OTP verification page
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                except Exception as e:
                    messages.error(request, f"An error occurred while sending email: {str(e)}")  # Handle any exceptions
        else:
            messages.error(request, "Email not registered.")  # Error if email doesn't exist
    
    return render(request, "forgot_password.html")  # Render the forgot password form

# OTP Verification View
def otp_verify(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        username = request.session.get('username')
        stored_otp = request.session.get('otp')

        if entered_otp == str(stored_otp):
            return redirect('reset_password')  # Redirect to reset password page
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'otp_verify.html')


# Password Reset View
def reset_password(request):
    if request.method == "POST":
        new_password = request.POST.get("new_password")  # Get the new password from the form
        confirm_password = request.POST.get("confirm_password")  # Get the confirmation password
        username = request.session.get('username')  # Get the username from the session

        # Check if the new password and confirmation password match
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again.")
            return render(request, 'reset_password.html')  # Render the form again with error message
        
        try:
            user = User.objects.get(username=username)  # Retrieve the user
            user.set_password(new_password)  # Hash the new password
            user.save()  # Save the user
            messages.success(request, "Password has been reset successfully.")
            return redirect('professor_login')  # Redirect to login page
        except User.DoesNotExist:
            messages.error(request, "User not found.")

    return render(request, 'reset_password.html')  # Render the reset password form


def dashboard(request):
    return render(request, 'dashboard.html')  # Renders a basic dashboard template

def role_selection_view(request):
    if request.method == 'POST':
        selected_role = request.POST.get('role')
        return redirect('student_list', role=selected_role)
    return render(request, 'home.html')

from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from io import BytesIO
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer, HRFlowable

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Image
from django.http import HttpResponse
from django.core.files.base import ContentFile

@login_required
def send_marks_email(request, role):
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids')
        students = Student.objects.filter(id__in=student_ids)

        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=1*inch, leftMargin=1.5*inch, rightMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []

        # Logo and header text layout
        logo_path = find_logo_path()
        if logo_path:
            img = Image(logo_path, width=1.2*inch, height=1.2*inch)
            header_text = Paragraph("National Institute of Technology Surathkal, Karnataka", getSampleStyleSheet()['Title'])
            header = Table([[img, header_text]], colWidths=[1*inch, 8*inch])
            header.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(header)
            elements.append(Spacer(1, 0.5*inch))  # Space after header

            elements.append(Spacer(1, 10))  # Adjust the height as needed

            # Add the new heading for the list of submitted students
            heading_text = Paragraph("List of Submitted Students", getSampleStyleSheet()['Heading2'])
            elements.append(heading_text)
            elements.append(Spacer(1, 0.2*inch))  # Space after heading

        # Table data for marks
        data = [
            ['Name', 'Roll Number', 'Depth of\nUnderstanding', 'Work Done\nResults', 'Exceptional\nWork', 'Viva Voce', 'Presentation', 'Report', 'Attendance', 'Total Marks']
        ]

        for student in students:
            marks = MarkSheet.objects.filter(student=student, user=request.user).first()
            if marks:
                total_marks = sum([
                    int(marks.depth_of_understanding),
                    int(marks.work_done_and_results),
                    int(marks.exceptional_work),
                    int(marks.viva_voce),
                    int(marks.presentation),
                    int(marks.report),
                    int(marks.attendance)
                ])
                data.append([
                    student.name,
                    student.roll_number,
                    str(marks.depth_of_understanding),
                    str(marks.work_done_and_results),
                    str(marks.exceptional_work),
                    str(marks.viva_voce),
                    str(marks.presentation),
                    str(marks.report),
                    str(marks.attendance),
                    str(total_marks)
                ])

        # Table styling and creation
        total_width = landscape(A4)[0] - 2*inch
        column_widths = [total_width/10] * 10
        table = Table(data, colWidths=column_widths)

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('WORDWRAP', (0, 0), (-1, -1), True)
        ]))

        elements.append(table)

        # Build PDF
        doc.build(elements)

        # Send email with PDF
        pdf = buffer.getvalue()
        buffer.close()
        subject = f'Student Marks Report - {role.capitalize()}'
        body = 'Please find attached the marks report for the selected students.'
        email = EmailMessage(subject, body, settings.EMAIL_HOST_USER, [request.user.email])
        email.attach('student_marks_report.pdf', pdf, 'application/pdf')
        email.send(fail_silently=False)

        # Provide the download option
        response = HttpResponse(ContentFile(pdf), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="student_marks_report.pdf"'

        messages.success(request, "Marks report has been generated, and the email sent successfully.")
        return render(request, 'pdf_success.html', {'pdf_data': pdf})  # Pass PDF data to template
        

    return redirect('student_list', role=role)

def pdf_success(request):
    return render(request, 'pdf_success.html')

def find_logo_path():
    possible_paths = [
        os.path.join(settings.BASE_DIR, 'mainapp', 'static', 'logo.jpg'),
        os.path.join(settings.BASE_DIR, 'static', 'logo.jpg'),
        os.path.join(settings.BASE_DIR, 'mainapp', 'static', 'mainapp', 'logo.jpg'),
    ]
    
    if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
        possible_paths.append(os.path.join(settings.STATIC_ROOT, 'mainapp', 'static', 'logo.jpg'))
        possible_paths.append(os.path.join(settings.STATIC_ROOT, 'logo.jpg'))

    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Student, MarkSheet, ExaminerAssignment

@login_required
def student_list_view(request, role):
    user = request.user

    if role == 'mentor':
        students = Student.objects.filter(professor=user)
    elif role == 'examiner':
        examiner_assignments = ExaminerAssignment.objects.filter(examiner=user)
        students = Student.objects.filter(examinerassignment__in=examiner_assignments).exclude(professor=user)

    for student in students:
        if role == 'mentor':
            student.current_user_midsem_marks = student.professor_marks
            student.current_user_endsem_marks = student.professor_endmarks
        elif role == 'examiner':
            examiner_assignment = ExaminerAssignment.objects.filter(student=student, examiner=user).first()
            if examiner_assignment:
                student.current_user_midsem_marks = examiner_assignment.examiner_marks
                student.current_user_endsem_marks = examiner_assignment.examiner_endmarks
            else:
                student.current_user_midsem_marks = 0
                student.current_user_endsem_marks = 0

    context = {
        'students': students,
        'role': role,
    }
    return render(request, 'authentication/student_list.html', context)

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, MarkSheet, ExaminerAssignment
from .forms import MentorMarksForm, ExaminerMarksForm

@login_required
def update_midsem_marks(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = request.user

    # Determine the role of the user
    if user == student.professor:
        role = 'mentor'
        FormClass = MentorMarksForm
    else:
        role = 'examiner'
        FormClass = ExaminerMarksForm
        # Check if the user is an examiner for this student
        examiner_assignment = get_object_or_404(ExaminerAssignment, student=student, examiner=user)

    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            marksheet, created = MarkSheet.objects.get_or_create(student=student, user=user)
            
            # Update MarkSheet
            for field in form.cleaned_data:
                setattr(marksheet, field, form.cleaned_data[field])
            marksheet.save()

            # Calculate total marks
            total_marks = sum(form.cleaned_data[field] for field in form.cleaned_data 
                              if field not in ['guide_name', 'presentation_date', 'start_time', 'end_time', 'project_title'])

            # Update Student or ExaminerAssignment model based on user role
            if role == 'mentor':
                student.professor_marks = total_marks
                student.save()
            else:
                examiner_assignment.examiner_marks = total_marks
                examiner_assignment.submission_status = 'Submitted'  # Update submission status
                examiner_assignment.save()

            student.update_total_marks()
            student.update_submission_status()

            messages.success(request, "Midsem marks updated successfully and email sent.")
            return redirect('student_list', role=role)
    else:
        # Pre-fill the form if marks already exist
        initial_data = {}
        if role == 'mentor':
            initial_data = {field: getattr(student, field) for field in FormClass.base_fields if hasattr(student, field)}
        else:
            initial_data = {'examiner_marks': examiner_assignment.examiner_marks}
        
        form = FormClass(initial=initial_data)

    context = {
        'form': form,
        'student': student,
        'role': role,
        'submission_status': examiner_assignment.submission_status if role == 'examiner' else None,
    }
    return render(request, 'authentication/update_midsem_marks.html', context)

@login_required
def update_endsem_marks(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = request.user

    # Determine the role of the user
    if user == student.professor:
        role = 'mentor'
        FormClass = MentorEndsemMarksForm
    else:
        role = 'examiner'
        FormClass = ExaminerEndsemMarksForm
        # Check if the user is an examiner for this student
        examiner_assignment = get_object_or_404(ExaminerAssignment, student=student, examiner=user)

    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            marksheet, created = MarkSheet.objects.get_or_create(student=student, user=user)
            
            # Update MarkSheet
            for field in form.cleaned_data:
                setattr(marksheet, field, form.cleaned_data[field])
            marksheet.save()

            # Calculate total marks
            total_marks = sum(form.cleaned_data[field] for field in form.cleaned_data 
                              if field not in ['guide_name', 'presentation_date', 'start_time', 'end_time', 'project_title'])

            # Update Student or ExaminerAssignment model based on user role
            if role == 'mentor':
                student.professor_endmarks = total_marks
                student.save()
            else:
                examiner_assignment.examiner_endmarks = total_marks
                examiner_assignment.submission_endstatus = 'Submitted'  # Update submission status
                examiner_assignment.save()

            student.update_total_marks()
            student.update_submission_endstatus()

            messages.success(request, "Endsem marks updated successfully and email sent.")
            return redirect('student_list', role=role)
    else:
        # Pre-fill the form if marks already exist
        initial_data = {}
        if role == 'mentor':
            initial_data = {field: getattr(student, field) for field in FormClass.base_fields if hasattr(student, field)}
        else:
            initial_data = {'examiner_endmarks': examiner_assignment.examiner_endmarks}
        
        form = FormClass(initial=initial_data)

    context = {
        'form': form,
        'student': student,
        'role': role,
        'submission_endstatus': examiner_assignment.submission_endstatus if role == 'examiner' else None,
    }
    return render(request, 'authentication/update_midsem_marks.html', context)


# Create your views here.
def home(request):
    return render(request, "home.html")




def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('role_selection')  # Redirect to role selection
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from .models import Student

# views.py

from django.shortcuts import render



from .models import Student

@login_required
def student_dashboard(request):
    try:
        # Get the student using session data (after successful login)
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        return redirect('error_page')  # Redirect if the student is not found

    context = {
        'student': student,
        'midsem_submitted': student.submission_status == 'green',
        'endsem_submitted': student.submission_endstatus == 'green',
        'mid_marks': student.total_midsem_marks if student.submission_status == 'green' else None,
        'endsem_marks': student.total_endsem_marks if student.submission_endstatus == 'green' else None,
    }

    if context['midsem_submitted'] and context['endsem_submitted']:
        context['total_marks'] = (student.total_midsem_marks * 0.4) + (student.total_endsem_marks * 0.6)
    else:
        context['total_marks'] = None

    return render(request, 'dash.html', context)

def custom_login(request):
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number', '')
        password = request.POST.get('password', '')

        try:
            student = Student.objects.get(roll_number=roll_number)
            if student.password == password:  # Use `check_password()` if passwords are hashed
                request.session['student_id'] = student.id
                return redirect('student_dashboard')
            else:
                messages.error(request, "Invalid roll number or password.")
        except Student.DoesNotExist:
            messages.error(request, "Student not found.")

    return render(request, 'student_login.html')

def professor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if 'generate_otp' in request.POST:
                try:
                    otp = random.randint(100000, 999999)
                    subject = "Your OTP Code"
                    email_message = f"Your OTP code is: {otp}"
                    send_mail(subject, email_message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

                    request.session['otp'] = otp
                    request.session['username'] = username
                    messages.success(request, "OTP has been sent to your email.")
                    
                    return render(request, 'login.html', {
                        'show_otp': True,
                        'username': username,
                        'password': password
                    })
                except Exception as e:
                    messages.error(request, f"An error occurred while sending OTP: {str(e)}")
            elif 'login' in request.POST:
                entered_otp = request.POST.get('otp')
                if 'otp' in request.session and str(request.session['otp']) == entered_otp:
                    login(request, user)
                    request.session.pop('otp', None)
                    return redirect('role_selection')
                else:
                    messages.error(request, "Invalid OTP.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html', {'show_generate_otp': True})

def landing_page(request):
    return render(request, 'landing_page.html')