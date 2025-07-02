from django.db import models
from datetime import date

class Department(models.Model):
    name = models.CharField(max_length=100)
    head = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date_of_joining = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    performance_score = models.FloatField()
    promotion_count = models.IntegerField(default=0)
    resignation_date = models.DateField(null=True, blank=True)

    def age(self):
        today = date.today()
        if self.date_of_birth:
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    def tenure(self):
        end_date = self.resignation_date if self.resignation_date else date.today()
        return (end_date - self.date_of_joining).days // 365

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
