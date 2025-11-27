from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project, Education, ContactInfo, Skill

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'tech_stack', 'live_url', 'repo_url')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_year', 'end_year')

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'order')
    list_editable = ('level', 'order')
    ordering = ('order', 'name')
