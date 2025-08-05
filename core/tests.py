# core/tests.py
from django.test import TestCase
from django.urls import reverse
from core.models import Customer, Loan
from datetime import date

class LoanAPITest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            customer_id=999,
            first_name="Test",
            last_name="User",
            age=25,
            phone_number="9000000000",
            monthly_salary=50000,
            approved_limit=1000000,
            current_debt=0
        )

    def test_create_customer(self):
        response = self.client.post(
            reverse("register_customer"),
            data={
                "first_name": "John",
                "last_name": "Doe",
                "age": 30,
                "phone_number": "9998887777",
                "monthly_salary": 40000
            },
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_create_loan(self):
        response = self.client.post(
            reverse("create_loan"),
            data={
                "customer_id": self.customer.customer_id,
                "loan_amount": 200000,
                "tenure": 12
            },
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        