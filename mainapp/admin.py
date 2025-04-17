from django.contrib import admin
from django.forms import inlineformset_factory
from .models import Student, MarkSheet, Professor, ExaminerAssignment

class ExaminerAssignmentInline(admin.TabularInline):
    model = ExaminerAssignment
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'email', 'project_title', 'total_marks', 'submission_status','submission_endstatus')
    readonly_fields = ('professor_marks','professor_endmarks', 'total_marks', 'total_midsem_marks', 'total_endsem_marks', 'submission_status','submission_endstatus')
    inlines = [ExaminerAssignmentInline]
    
    change_form_template = 'student_change_form.html'

    def get_fields(self, request, obj=None):
        fields = ['name', 'roll_number', 'email', 'project_title', 'presentation_date', 'presentation_from_time', 'presentation_to_time', 'professor']
        if obj and request.GET.get('show_details', 'false') == 'true':
            fields += ['professor_marks','professor_endmarks', 'total_marks', 'total_midsem_marks', 'total_endsem_marks', 'submission_status','submission_endstatus']
        return fields

admin.site.register(Student, StudentAdmin)
admin.site.register(Professor)
admin.site.register(MarkSheet)