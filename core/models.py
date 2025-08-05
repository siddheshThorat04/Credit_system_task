from django.db import models


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    monthly_salary = models.FloatField()
    approved_limit = models.FloatField()
    current_debt = models.FloatField(default=0)
  
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="loans")
    loan_amount = models.FloatField()
    tenure = models.IntegerField(help_text="Loan tenure in months")
    interest_rate = models.FloatField()
    monthly_repayment = models.FloatField()
    emis_paid_on_time = models.IntegerField()
    
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)



    def __str__(self):
        return f"Loan {self.loan_id} - {self.customer.first_name}"
