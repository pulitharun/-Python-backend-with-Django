#views.py

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

# View for handling customer-related operations
class CustomerView(APIView):
    def get(self, request, id=None): 
        
        # Retrieve customer information by ID or all customers if ID is not provided
        if id:
            customer = get_object_or_404(Customer, id=id)
            serializer = CustomerSerializer(customer)
        else:
            customers = Customer.objects.all()
            serializer = CustomerSerializer(customers, many=True)
        return Response({'status': 'success', 'customers': serializer.data})

     # Register a new customer
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Customer registered successfully!", 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'Customer not registered', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# View for handling user login
class LoginView(APIView):
    def post(self, request):  # Authenticate user credentials
        username = request.data.get("username")
        password = request.data.get("password")
        try:
            customer = Customer.objects.get(username=username)
            if customer.password == password:
                return Response({"message": "Login successful!", "username" : username,"password":password})
            return Response({"message": "Invalid credentials!"})
        except Customer.DoesNotExist:
            return Response({"message": "No user exists!"})

class GetidfromusernameView(APIView):
    def get(self,request,*args,**kwargs):
        try:
            username=kwargs.get("username")
            id= Customer.objects.get(username=username).id
            address=Customer.objects.get(username=username).address
            firstname=Customer.objects.get(username=username).first_name
            lastname=Customer.objects.get(username=username).last_name
            email=Customer.objects.get(username=username).email
            datalist={
                "id":id,
                "address":address,
                "firstname":firstname,
                "lastname":lastname,
                "email":email

            }
            return Response({"data":datalist})
        except:
            return Response({"message":"error"})

# View for handling category-related operations
class CategoriesView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request): # Create a new category
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'data': "Please enter data"}, status=status.HTTP_400_BAD_REQUEST)

# View for retrieving category information
class GetCategoryView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if id:
            try:
                result = Category.objects.get(id=id)
                serializer = CategorySerializer(result)
                return Response({'categories': serializer.data}, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({'status': 'error', 'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            result = Category.objects.all()
            serializer = CategorySerializer(result, many=True)
            return Response({'categories': serializer.data}, status=status.HTTP_200_OK)

# View for creating a new product
class AddProductView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product created successfully!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetProductsByID(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"message": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
 # View for retrieving products based on category    
class GetProductsByCategoryView(APIView):
    def get(self, request, *args, **kwargs):
        categoryname = kwargs.get("category")
        try:
            id = Category.objects.get(category_type=categoryname).id
            products = Product.objects.filter(category=id) # filter the products based on category id
            serializer = ProductSerializer(products, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'message': 'error', 'data': "category does not exist"}, status=status.HTTP_400_BAD_REQUEST)  

# View for creating a new invoice    
class CreateInvoiceView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for retrieving invoices based on status
class GetInvoiceBasedOnStatus(APIView):
    def get(self, request,* args, **kwargs):
        try:
            orderstatus = kwargs.get("status")
            if orderstatus:
                getinvoices = Invoice.objects.filter(status=orderstatus)
                serializer = InvoiceSerializer(getinvoices, many=True)
                return Response({'data':serializer.data})
            else:
                result = Invoice.objects.all()
                serializer = InvoiceSerializer(result,many=True)
                return Response({'data':serializer.data})
        except Invoice.DoesNotExist:
            return Response({'message':'No invoices with found.'}, status=status.HTTP_400_BAD_REQUEST)