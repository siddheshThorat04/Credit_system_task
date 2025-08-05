from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import Customer
from core.serializers import CustomerSerializer

@api_view(["POST"])
def register_customer(request):
    phone_number = request.data.get("phone_number")

    
    if Customer.objects.filter(phone_number=phone_number).exists():
        return Response(
            {"error": "A customer with this phone number already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        monthly_salary = float(request.data.get("monthly_salary", 0))
    except (TypeError, ValueError):
        monthly_salary = 0

    approved_limit = monthly_salary * 36

    
    customer = Customer.objects.create(
        first_name=request.data.get("first_name"),
        last_name=request.data.get("last_name"),
        age=request.data.get("age"),
        phone_number=phone_number,
        monthly_salary=monthly_salary,
        approved_limit=approved_limit,
        current_debt=0
    )

    serializer = CustomerSerializer(customer)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import Customer, Loan
import math
@api_view(["POST"])
def check_eligibility(request):
    try:
        customer_id = request.data.get("customer_id")
        loan_amount = float(request.data.get("loan_amount", 0))
        tenure_months = int(request.data.get("tenure", 0))

        customer = Customer.objects.get(customer_id=customer_id)

        
        if loan_amount > customer.approved_limit:
            return Response({
                "eligible": False,
                "message": "Loan amount exceeds approved limit."
            }, status=status.HTTP_200_OK)

        
        if (customer.current_debt + loan_amount) > customer.approved_limit:
            return Response({
                "eligible": False,
                "message": "Loan would exceed your total borrowing limit."
            }, status=status.HTTP_200_OK)

        
        loans = Loan.objects.filter(customer=customer)
        if loans.exists():
            total_emis = sum(l.tenure for l in loans)  
            emis_on_time = sum(l.emis_paid_on_time for l in loans)
            on_time_percentage = (emis_on_time / total_emis) * 100 if total_emis > 0 else 100
        else:
            on_time_percentage = 100  

        
        if on_time_percentage >= 90:
            interest_rate = 8
        elif on_time_percentage >= 75:
            interest_rate = 10
        elif on_time_percentage >= 60:
            interest_rate = 12
        else:
            interest_rate = 15

        
        monthly_rate = interest_rate / (12 * 100)
        emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
              ((1 + monthly_rate) ** tenure_months - 1)

        return Response({
            "eligible": True,
            "approved_limit": customer.approved_limit,
            "interest_rate": interest_rate,
            "monthly_emi": round(emi, 2),
            "credit_score": round(on_time_percentage, 2),
            "message": "Customer is eligible based on credit history."
        }, status=status.HTTP_200_OK)

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
from django.utils import timezone

@api_view(["POST"])
def create_loan(request):
    try:
        customer_id = request.data.get("customer_id")
        loan_amount = float(request.data.get("loan_amount", 0))
        tenure_months = int(request.data.get("tenure", 0))

        customer = Customer.objects.get(customer_id=customer_id)

        
        if loan_amount > customer.approved_limit:
            return Response({"error": "Loan amount exceeds approved limit."}, status=status.HTTP_400_BAD_REQUEST)
        if (customer.current_debt + loan_amount) > customer.approved_limit:
            return Response({"error": "Loan would exceed your total borrowing limit."}, status=status.HTTP_400_BAD_REQUEST)

        
        loans = Loan.objects.filter(customer=customer)
        if loans.exists():
            total_emis = sum(l.tenure for l in loans)
            emis_on_time = sum(l.emis_paid_on_time for l in loans)
            on_time_percentage = (emis_on_time / total_emis) * 100 if total_emis > 0 else 100
        else:
            on_time_percentage = 100

        if on_time_percentage >= 90:
            interest_rate = 8
        elif on_time_percentage >= 75:
            interest_rate = 10
        elif on_time_percentage >= 60:
            interest_rate = 12
        else:
            interest_rate = 15


        monthly_rate = interest_rate / (12 * 100)
        emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
              ((1 + monthly_rate) ** tenure_months - 1)

        
        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            tenure=tenure_months,
            interest_rate=interest_rate,
            monthly_repayment=emi,
            emis_paid_on_time=0,
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timezone.timedelta(days=tenure_months * 30)).date()
        )

        
        customer.current_debt += loan_amount
        customer.save()

        return Response({
            "loan_id": loan.loan_id,
            "customer_id": customer.customer_id,
            "loan_amount": loan_amount,
            "tenure": tenure_months,
            "interest_rate": interest_rate,
            "monthly_emi": round(emi, 2),
            "start_date": loan.start_date,
            "end_date": loan.end_date
        }, status=status.HTTP_201_CREATED)

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def view_loan(request):
    loan_id = request.query_params.get("loan_id")
    customer_id = request.query_params.get("customer_id")

    
    if loan_id:
        try:
            loan = Loan.objects.get(loan_id=loan_id)
            return Response({
                "loan_id": loan.loan_id,
                "customer_id": loan.customer.customer_id,
                "loan_amount": loan.loan_amount,
                "tenure": loan.tenure,
                "interest_rate": loan.interest_rate,
                "monthly_emi": loan.monthly_repayment,
                "emis_paid_on_time": loan.emis_paid_on_time,
                "start_date": loan.start_date,
                "end_date": loan.end_date
            })
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)

    
    if customer_id:
        loans = Loan.objects.filter(customer__customer_id=customer_id)
        loan_list = [{
            "loan_id": l.loan_id,
            "loan_amount": l.loan_amount,
            "tenure": l.tenure,
            "interest_rate": l.interest_rate,
            "monthly_emi": l.monthly_repayment,
            "emis_paid_on_time": l.emis_paid_on_time,
            "start_date": l.start_date,
            "end_date": l.end_date
        } for l in loans]

        return Response({
            "customer_id": customer_id,
            "loans": loan_list
        })

    return Response({"error": "Please provide either loan_id or customer_id"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(["GET"])
def view_loans_by_customer(request, customer_id):
    try:
        loans = Loan.objects.filter(customer__customer_id=customer_id)
        if not loans.exists():
            return Response({"message": "No loans found for this customer."}, status=status.HTTP_404_NOT_FOUND)

        loan_list = [{
            "loan_id": l.loan_id,
            "loan_amount": l.loan_amount,
            "tenure": l.tenure,
            "interest_rate": l.interest_rate,
            "monthly_emi": l.monthly_repayment,
            "emis_paid_on_time": l.emis_paid_on_time,
            "start_date": l.start_date,
            "end_date": l.end_date
        } for l in loans]

        return Response({
            "customer_id": customer_id,
            "loans": loan_list
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def view_all_loans(request):
    loans = Loan.objects.filter(start_date__isnull=False)
    if not loans.exists():
        return Response({"message": "No loans found in the system."}, status=status.HTTP_404_NOT_FOUND)

    loan_list = [{
        "loan_id": l.loan_id,
        "customer_id": l.customer.customer_id,
        "customer_name": f"{l.customer.first_name} {l.customer.last_name}",
        "loan_amount": l.loan_amount,
        "tenure": l.tenure,
        "interest_rate": l.interest_rate,
        "monthly_emi": l.monthly_repayment,
        "emis_paid_on_time": l.emis_paid_on_time,
        "start_date": l.start_date,
        "end_date": l.end_date
    } for l in loans]

    return Response({"total_loans": loans.count(), "loans": loan_list}, status=status.HTTP_200_OK)
