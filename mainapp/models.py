from django.db import models
from django.contrib.auth.models import User

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

class Student(models.Model):
    ROLE_CHOICES = [
        ('mentor', 'Mentor'),
        ('examiner', 'Examiner'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='mentor')
    name = models.CharField(max_length=100, null=True)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(null=True)
    project_title = models.CharField(max_length=255, default='N/A')
    presentation_date = models.DateField(null=True)
    presentation_from_time = models.CharField(max_length=100, default='N/A')
    presentation_to_time = models.CharField(max_length=100, default='N/A')
    
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentored_students')
    examiners = models.ManyToManyField(User, related_name='examined_students', through='ExaminerAssignment')
    
    submission_status = models.CharField(
        max_length=10,
        choices=[('green', 'Submitted'), ('red', 'Not Submitted')],
        default='red'
    )
    submission_endstatus = models.CharField(
        max_length=10,
        choices=[('green', 'Submitted'), ('red', 'Not Submitted')],
        default='red'
    )
    midsem_marks = models.IntegerField(default=0)
    total_midsem_marks = models.IntegerField(default=0)
    endsem_marks = models.IntegerField(default=0)
    total_endsem_marks = models.IntegerField(default=0)

    password = models.CharField(max_length=128, default='nopw123@')
    professor_marks = models.IntegerField(default=0)
    professor_endmarks = models.IntegerField(default=0)

    def update_total_marks(self):
        
        num_examiners = self.examinerassignment_set.count()
        print(f"Number of Examiners: {num_examiners}")
        if num_examiners > 0:
        
            self.total_midsem_marks = self.professor_marks + (sum(assignment.examiner_marks for assignment in self.examinerassignment_set.all()) / num_examiners)
            self.total_endsem_marks = self.professor_endmarks + (sum(assignment.examiner_endmarks for assignment in self.examinerassignment_set.all()) / num_examiners)
        else:
        
            self.total_midsem_marks = self.professor_marks
            self.total_endsem_marks = self.professor_endmarks

        self.save()

    def check_all_marks_submitted(self):
        return self.professor_marks > 0 and all(assignment.examiner_marks > 0 for assignment in self.examinerassignment_set.all())

    def update_submission_status(self):
        self.submission_status = 'green' if self.check_all_marks_submitted() else 'red'
        self.save()

    def check_all_endmarks_submitted(self):
        return self.professor_endmarks > 0 and all(assignment.examiner_endmarks > 0 for assignment in self.examinerassignment_set.all())

    def update_submission_endstatus(self):
        self.submission_endstatus = 'green' if self.check_all_endmarks_submitted() else 'red'
        self.save()
    
    def __str__(self):
        return f"{self.name} ({self.roll_number})"

    @property
    def total_marks(self):
        return (self.total_midsem_marks)*0.4 + (self.total_endsem_marks)*0.6

class ExaminerAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    examiner = models.ForeignKey(User, on_delete=models.CASCADE)
    examiner_marks = models.IntegerField(default=0)
    examiner_endmarks = models.IntegerField(default=0)
    submission_status = models.CharField(max_length=20, default='Not Submitted', choices=[
        ('Not Submitted', 'Not Submitted'),
        ('Submitted', 'Submitted')
    ])
    submission_endstatus = models.CharField(max_length=20, default='Not Submitted', choices=[
        ('Not Submitted', 'Not Submitted'),
        ('Submitted', 'Submitted')
    ])

    class Meta:
        unique_together = ('student', 'examiner')

class MarkSheet(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    guide_name = models.CharField(max_length=100)
    presentation_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    project_title = models.CharField(max_length=200)
    
    depth_of_understanding = models.IntegerField(null=True)
    work_done_and_results = models.IntegerField(null=True)
    exceptional_work = models.IntegerField(null=True)
    viva_voce = models.IntegerField(null=True)
    presentation = models.IntegerField(null=True)
    report = models.IntegerField(null=True)
    attendance = models.IntegerField(null=True, default=0)

    submitted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.name}'s Marksheet - {self.project_title}"

    @property
    def total_marks(self):
        return sum(getattr(self, field, 0) or 0 for field in [
            'depth_of_understanding', 'work_done_and_results', 'exceptional_work',
            'viva_voce', 'presentation', 'report', 'attendance'
        ])