from django.http import JsonResponse
from .models import Employee
from sklearn.linear_model import LinearRegression

def predict_salary(request, department_name, experience_years):
    try:
        exp = float(experience_years)
    except ValueError:
        return JsonResponse({"error": "Invalid experience value."}, status=400)

    employees = Employee.objects.filter(
        department__name=department_name,
        resignation_date__isnull=True
    )

    X = []
    y = []
    employee_list = []

    for emp in employees:
        experience = getattr(emp, 'experience', emp.tenure() if hasattr(emp, 'tenure') else None)
        if experience is not None and emp.salary is not None:
            X.append([float(experience)])
            y.append(float(emp.salary))
            employee_list.append({
                "name": emp.first_name,
                "experience": float(experience),
                "salary": float(emp.salary)
            })

    if len(X) < 2:
        return JsonResponse({"error": "Not enough data to make a prediction."}, status=400)

    model = LinearRegression()
    model.fit(X, y)
    predicted_salary = model.predict([[exp]])[0]
    lower = round(predicted_salary * 0.9, 2)
    upper = round(predicted_salary * 1.1, 2)

    # Clean up the output: all numbers as floats, rounded, not strings
    return JsonResponse({
        "department": department_name,
        "experience": round(exp, 2),
        "predicted_salary": round(predicted_salary, 2),
        "predicted_salary_range": {
            "lower": lower,
            "upper": upper
        },
        "employees": employee_list
    })
