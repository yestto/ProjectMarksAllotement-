from django import forms
from .models import Student, MarkSheet

class UpdateMarksForm(forms.ModelForm):
    marks = forms.IntegerField(min_value=0, max_value=100, label="Marks")

    class Meta:
        model = Student
        fields = ['marks']


class MidsemMarksForm(forms.ModelForm):
    guide_name = forms.CharField(max_length=100, label="Guide Name")
    presentation_date = forms.DateField(widget=forms.SelectDateWidget, label="Presentation Date")
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label="Start Time")
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label="End Time")
    project_title = forms.CharField(max_length=200, label="Project Title")

    # Marks fields
    depth_of_understanding = forms.IntegerField(min_value=0, max_value=100, label="Depth of Understanding(12)")
    work_done_results = forms.IntegerField(min_value=0, max_value=100, label="Work Done Results(18)")
    exceptional_work = forms.IntegerField(min_value=0, max_value=100, label="Exceptional Work(6)")
    viva_voce = forms.IntegerField(min_value=0, max_value=100, label="Viva Voce(12)")
    presentation = forms.IntegerField(min_value=0, max_value=100, label="Presentation(6)")
    report = forms.IntegerField(min_value=0, max_value=100, label="Report(3)")
    attendance = forms.IntegerField(min_value=0, max_value=100, label="Attendance(3)")

    class Meta:
        model = MarkSheet  # Ensure the form is linked to the MarkSheet model
        fields = [
            'guide_name', 'presentation_date', 'start_time', 'end_time', 
            'project_title', 'depth_of_understanding', 'work_done_results', 
            'exceptional_work', 'viva_voce', 'presentation', 
            'report', 'attendance'
        ]


class EndsemMarksForm(forms.ModelForm):
    guide_name = forms.CharField(max_length=100, label="Guide Name")
    presentation_date = forms.DateField(widget=forms.SelectDateWidget, label="Presentation Date")
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label="Start Time")
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label="End Time")
    project_title = forms.CharField(max_length=200, label="Project Title")

    # Marks fields
    depth_of_understanding = forms.IntegerField(min_value=0, max_value=100, label="Depth of Understanding(12)")
    work_done_results = forms.IntegerField(min_value=0, max_value=100, label="Work Done Results(18)")
    exceptional_work = forms.IntegerField(min_value=0, max_value=100, label="Exceptional Work(6)")
    viva_voce = forms.IntegerField(min_value=0, max_value=100, label="Viva Voce(12)")
    presentation = forms.IntegerField(min_value=0, max_value=100, label="Presentation(6)")
    report = forms.IntegerField(min_value=0, max_value=100, label="Report(3)")
    attendance = forms.IntegerField(min_value=0, max_value=100, label="Attendance(3)")

    class Meta:
        model = MarkSheet  # Ensure the form is linked to the MarkSheet model
        fields = [
            'guide_name', 'presentation_date', 'start_time', 'end_time', 
            'project_title', 'depth_of_understanding', 'work_done_and_results', 
            'exceptional_work', 'viva_voce', 'presentation', 
            'report', 'attendance'
        ]
class MentorMarksForm(forms.ModelForm):
    guide_name = forms.CharField(max_length=100, label="Guide Name")
    presentation_date = forms.DateField(widget=forms.SelectDateWidget, label="Presentation Date")
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label="Start Time")
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label="End Time")
    project_title = forms.CharField(max_length=200, label="Project Title")

    # Marks fields
    depth_of_understanding = forms.IntegerField(min_value=0, max_value=12, label="Depth of Understanding(12)")
    work_done_and_results = forms.IntegerField(min_value=0, max_value=18, label="Work Done Results(18)")
    exceptional_work = forms.IntegerField(min_value=0, max_value=6, label="Exceptional Work(6)")
    viva_voce = forms.IntegerField(min_value=0, max_value=12, label="Viva Voce(12)")
    presentation = forms.IntegerField(min_value=0, max_value=6, label="Presentation(6)")
    report = forms.IntegerField(min_value=0, max_value=3, label="Report(3)")
    attendance = forms.IntegerField(min_value=0, max_value=3, label="Attendance(3)")

    class Meta:
        model = MarkSheet
        fields = [
            'guide_name', 'presentation_date', 'start_time', 'end_time', 
            'project_title', 'depth_of_understanding', 'work_done_and_results', 
            'exceptional_work', 'viva_voce', 'presentation', 
            'report', 'attendance'
        ]

class ExaminerMarksForm(forms.ModelForm):
    guide_name = forms.CharField(max_length=100, label="Guide Name")
    presentation_date = forms.DateField(widget=forms.SelectDateWidget, label="Presentation Date")
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label="Start Time")
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label="End Time")
    project_title = forms.CharField(max_length=200, label="Project Title")

    # Marks fields
    depth_of_understanding = forms.IntegerField(min_value=0, max_value=8, label="Depth of Understanding(8)")
    work_done_and_results = forms.IntegerField(min_value=0, max_value=12, label="Work Done Results(12)")
    exceptional_work = forms.IntegerField(min_value=0, max_value=6, label="Exceptional Work(6)")
    viva_voce = forms.IntegerField(min_value=0, max_value=8, label="Viva Voce(8)")
    presentation = forms.IntegerField(min_value=0, max_value=4, label="Presentation(4)")
    report = forms.IntegerField(min_value=0, max_value=2, label="Report(2)")
    class Meta:
        model = MarkSheet
        fields = [
            'guide_name', 'presentation_date', 'start_time', 'end_time', 
            'project_title', 'depth_of_understanding', 'work_done_and_results', 
            'exceptional_work', 'viva_voce', 'presentation', 
            'report'
        ]

class MentorEndsemMarksForm(forms.Form):
    guide_name = forms.CharField(max_length=100, label="Guide Name")
    presentation_date = forms.DateField(widget=forms.SelectDateWidget, label="Presentation Date")
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label="Start Time")
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label="End Time")
    project_title = forms.CharField(max_length=200, label="Project Title")

    # Marks fields
    depth_of_understanding = forms.IntegerField(min_value=0, max_value=12, label="Depth of Understanding(12)")
    work_done_and_results = forms.IntegerField(min_value=0, max_value=18, label="Work Done Results(18)")
    exceptional_work = forms.IntegerField(min_value=0, max_value=6, label="Exceptional Work(6)")
    viva_voce = forms.IntegerField(min_value=0, max_value=12, label="Viva Voce(12)")
    presentation = forms.IntegerField(min_value=0, max_value=6, label="Presentation(6)")
    report = forms.IntegerField(min_value=0, max_value=3, label="Report(3)")
    attendance = forms.IntegerField(min_value=0, max_value=3, label="Attendance(3)")

    class Meta:
        model = MarkSheet
        fields = [
            'guide_name', 'presentation_date', 'start_time', 'end_time', 
            'project_title', 'depth_of_understanding', 'work_done_and_results', 
            'exceptional_work', 'viva_voce', 'presentation', 
            'report', 'attendance'
        ]

class ExaminerEndsemMarksForm(forms.Form):
    guide_name = forms.CharField(max_length=100, label="Guide Name")
    presentation_date = forms.DateField(widget=forms.SelectDateWidget, label="Presentation Date")
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label="Start Time")
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label="End Time")
    project_title = forms.CharField(max_length=200, label="Project Title")

    # Marks fields
    depth_of_understanding = forms.IntegerField(min_value=0, max_value=8, label="Depth of Understanding(8)")
    work_done_and_results = forms.IntegerField(min_value=0, max_value=12, label="Work Done Results(12)")
    exceptional_work = forms.IntegerField(min_value=0, max_value=6, label="Exceptional Work(6)")
    viva_voce = forms.IntegerField(min_value=0, max_value=8, label="Viva Voce(8)")
    presentation = forms.IntegerField(min_value=0, max_value=4, label="Presentation(4)")
    report = forms.IntegerField(min_value=0, max_value=2, label="Report(2)")

    class Meta:
        model = MarkSheet
        fields = [
            'guide_name', 'presentation_date', 'start_time', 'end_time', 
            'project_title', 'depth_of_understanding', 'work_done_and_results', 
            'exceptional_work', 'viva_voce', 'presentation', 
            'report'
        ]