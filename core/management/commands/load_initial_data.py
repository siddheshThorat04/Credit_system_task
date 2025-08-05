from django.core.management.base import BaseCommand
import pandas as pd
import datetime
from core.models import Customer, Loan
from django.db import transaction
from pathlib import Path


class Command(BaseCommand):
    help = "Load initial customer and loan data from Excel files"

    def handle(self, *args, **kwargs):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        customer_file = base_dir / "customer_data.xlsx"
        loan_file = base_dir / "loan_data.xlsx"

        if not customer_file.exists() or not loan_file.exists():
            self.stdout.write(self.style.ERROR("Excel files not found in project root"))
            return

        self.stdout.write("Loading data...")

        with transaction.atomic():
            # --- Load Customers ---
            customer_df = pd.read_excel(customer_file)
            customer_df.columns = (
                customer_df.columns.str.strip().str.lower().str.replace(" ", "_")
            )

            # Ensure required columns exist
            if "age" not in customer_df.columns:
                customer_df["age"] = None
            if "current_debt" not in customer_df.columns:
                customer_df["current_debt"] = 0

            for _, row in customer_df.iterrows():
                Customer.objects.update_or_create(
                    customer_id=row.get("customer_id"),
                    defaults={
                        "first_name": row.get("first_name"),
                        "last_name": row.get("last_name"),
                        "age": row.get("age"),
                        "phone_number": str(row.get("phone_number")),
                        "monthly_salary": row.get("monthly_salary", 0),
                        "approved_limit": row.get("approved_limit", 0),
                        "current_debt": row.get("current_debt", 0),
                    }
                )

            # --- Load Loans ---
            loan_df = pd.read_excel(loan_file)
            loan_df.columns = (
                loan_df.columns.str.strip().str.lower().str.replace(" ", "_")
            )

            # Ensure required columns exist
            for col in [
                "emis_paid_on_time",
                "monthly_repayment_emi",
                "start_date",
                "end_date"
            ]:
                if col not in loan_df.columns:
                    loan_df[col] = None if col in ["start_date", "end_date"] else 0

            def parse_excel_date(value):
                if pd.isna(value) or value is None:
                    return None
                if isinstance(value, pd.Timestamp):
                    return value.date()
                if isinstance(value, datetime.datetime):
                    return value.date()
                if isinstance(value, datetime.date):
                    return value
                try:
                    return datetime.date.fromisoformat(str(value))
                except Exception:
                    return None

            for _, row in loan_df.iterrows():
                customer = Customer.objects.get(customer_id=row.get("customer_id"))
                Loan.objects.update_or_create(
                    loan_id=row.get("loan_id"),
                    defaults={
                        "customer": customer,
                        "loan_amount": row.get("loan_amount", 0),
                        "tenure": row.get("tenure", 0),
                        "interest_rate": row.get("interest_rate", 0),
                        "monthly_repayment": row.get("monthly_repayment_emi", 0),
                        "emis_paid_on_time": row.get("emis_paid_on_time", 0),
                        "start_date": parse_excel_date(row.get("start_date")),
                        "end_date": parse_excel_date(row.get("end_date")),
                    }
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Data successfully loaded: {Customer.objects.count()} customers, {Loan.objects.count()} loans."
            )
        )
