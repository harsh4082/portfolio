from django.db import models

# Create your models here.
from django.db import models

class Education(models.Model):
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    start_year = models.CharField(max_length=10, blank=True)
    end_year = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.degree} — {self.institution}"

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=300, blank=True)
    live_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)  # Pillow required to use ImageField

    def __str__(self):
        return self.title

class ContactInfo(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=200, blank=True)
    short_bio = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50, blank=True, help_text="e.g. Beginner / Intermediate / Expert")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first")

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name