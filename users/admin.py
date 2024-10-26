from django.contrib import admin

from users.models import User, Group, Teacher, Student


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['number', 'specialization', 'department']
    search_fields = ['number', 'specialization']
    list_filter = ['number', 'department']


admin.site.register(Student)
admin.site.register(Teacher)


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'student information'


class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'teacher information'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = []

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj)
        if obj:
            if obj.is_student:
                inlines.append(StudentInline(self.model, self.admin_site))
            elif obj.is_teacher:
                inlines.append(TeacherInline(self.model, self.admin_site))
        return inlines
