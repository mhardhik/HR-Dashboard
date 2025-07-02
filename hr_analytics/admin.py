from django.contrib import admin
from django.db.models import Avg, Count, Sum
from .models import Employee, Department
from datetime import date
from django.db.models import Sum
from django.contrib.admin.views.main import ChangeList

@admin.register(Department)
class Department(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name','age' ,'department', 'salary', 'performance_score', 'promotion_count')
    list_filter = ('department', 'gender')

    def changelist_view(self, request, extra_context=None):
        total_employees = Employee.objects.count()
        average_salary = Employee.objects.aggregate(Avg('salary'))['salary__avg'] or 0
        total_salary = Employee.objects.aggregate(Sum('salary'))['salary__sum'] or 0
        average_performance = Employee.objects.aggregate(Avg('performance_score'))['performance_score__avg'] or 0
        gender_count = Employee.objects.values('gender').annotate(count=Count('gender'))

        total_resigned = Employee.objects.filter(resignation_date__isnull=False).count()
        turnover_rate = (total_resigned / total_employees) * 100 if total_employees else 0

        average_promotions = Employee.objects.aggregate(Avg('promotion_count'))['promotion_count__avg'] or 0
        gender_count = Employee.objects.values('gender').annotate(count=Count('gender'))
        # Calculate average tenure manually
        tenures = [emp.tenure() for emp in Employee.objects.all()]
        average_tenure = sum(tenures) / len(tenures) if tenures else 0

        # 🔥 NEW: Add salary-by-department data
        salary_by_dept = (
        Employee.objects.values("department__name")
        .annotate(total_salary=Sum("salary"))
        .order_by("department__name")
    )

        extra_context = {
            'total_employees': total_employees,
            'average_salary': average_salary,
            'total_salary': total_salary,
            'average_performance': average_performance,
            'gender_count': list(gender_count),
            'turnover_rate': turnover_rate,
            'average_promotions': average_promotions,
            'average_tenure': average_tenure,
            'salary_by_dept': list(salary_by_dept),
        }
        return super().changelist_view(request, extra_context=extra_context)
