from django.contrib import admin

from .models import Laboratory, Laboratory_Status, Student, EducationalGroup

@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "lecturer", "educational", "created_at")
    list_display_links = ("id", "title")
    empty_value_display = "---"
    search_fields = ("title", "lecturer__user__name", "lecturer__user__surname")

    def get_queryset(self, request):
        return Laboratory.objects.select_related("lecturer", "educational")

@admin.register(Laboratory_Status)
class LaboratoryStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "laboratory", "student",
                    "status", "additional_status",
                    "student_status", "lecturer_comment",
                    "student_comment", "created_at", "updated_at")
    list_display_links = ("id", "laboratory")
    list_editable = ("status", "additional_status",
                     "student_status", "lecturer_comment")
    empty_value_display = "---"
    search_fields = ("laboratory__title", "student__user__name",
                     "student__user__surname", "status", "student_status")
    list_filter = ("laboratory__title", "status", "student_status", "additional_status")

    def get_queryset(self, request):
        return Laboratory_Status.objects.select_related("laboratory", "student")



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "group", "get_user_name", "get_user_surname", "get_user_patronymic", "created_at", "updated_at")
    list_display_links = ("id", "get_user_name", "get_user_surname", "get_user_patronymic")
    list_editable = ("group",)
    empty_value_display = "---"
    search_fields = ("group", "user__name", "user__surname", "user__patronymic")
    list_filter = ("group",)

    def get_queryset(self, request):
        return Student.objects.select_related("group", "user")

    def get_user_name(self, obj):
        return obj.user.name if obj.user else ""
    get_user_name.short_description = "Имя"

    def get_user_surname(self, obj):
        return obj.user.surname if obj.user else ""
    get_user_surname.short_description = "Фамилия"

    def get_user_patronymic(self, obj):
        return obj.user.patronymic if obj.user else ""
    get_user_patronymic.short_description = "Отчество"

@admin.register(EducationalGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "description", "created_at", "updated_at")
    list_display_links = ("id", "number")
    empty_value_display = "---"
    search_fields = ("number",)
    list_filter = ("number",)
