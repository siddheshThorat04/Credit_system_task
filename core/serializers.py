from rest_framework import serializers
from core.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "customer_id",
            "first_name",
            "last_name",
            "age",
            "phone_number",
            "monthly_salary",
            "approved_limit",
            "current_debt",
        ]
        read_only_fields = ["customer_id", "approved_limit", "current_debt"]
