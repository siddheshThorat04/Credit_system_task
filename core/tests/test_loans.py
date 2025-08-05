from django.test import TestCase
from django.urls import reverse
from core.models import Customer, Loan
from datetime import date

class LoanAPITest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            customer_id=500,
            first_name="Test",
            last_name="User",
            age=30,
            phone_number="9999999999",
            monthly_salary=50000,
            approved_limit=1800000,
            current_debt=0
        )

    def test_register_customer(self):
        url = reverse('register-customer')
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "phone_number": "8888888888",
            "monthly_salary": 50000
        }
        res = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn("customer_id", res.json())

    def test_check_eligibility(self):
        url = reverse('check-loan-eligibility')
        payload = {
            "customer_id": self.customer.customer_id,
            "loan_amount": 200000,
            "tenure": 12
        }
        res = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertIn("eligible", res.json())

    def test_create_loan(self):
        url = reverse('create-loan')
        payload = {
            "customer_id": self.customer.customer_id,
            "loan_amount": 200000,
            "tenure": 12
        }
        res = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn("loan_id", res.json())

    def test_view_loans_by_customer(self):
        Loan.objects.create(
            loan_id=9999,
            customer=self.customer,
            loan_amount=100000,
            tenure=12,
            interest_rate=10,
            monthly_emi=8500,
            emis_paid_on_time=0,
            start_date=date.today(),
            end_date=date(2026, 1, 1)
        )
        url = reverse('view-loans-by-customer', args=[self.customer.customer_id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("loans", res.json())