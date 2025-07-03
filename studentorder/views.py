from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import StudentOrder
from .Serializers import StudentOrderSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

class UserStudentOrderView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        orders=StudentOrder.objects.filter(user=request.user).select_related('student').order_by('order')
        serializer=StudentOrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    
class ReorderStudentsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        StudentOrder.objects.filter(user=request.user).delete()

        for index,item in enumerate(request.data):
            StudentOrder.objects.create(
                user=request.user,
                student_id=item['student_id'],
                order=index
            )
        return Response({"message": "Students reordered successfully."})

# from django.contrib.auth.models import User
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import StudentOrder

# class ReorderStudentsView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         try:
#             dummy_user = User.objects.last()
#             if not dummy_user:
#                 return Response({"error": "No users found in DB."}, status=500)

#             StudentOrder.objects.filter(user=dummy_user).delete()

#             for index, item in enumerate(request.data):
#                 StudentOrder.objects.create(
#                     user=dummy_user,
#                     student_id=item['student_id'],
#                     order=index
#                 )

#             return Response({"message": "Students reordered successfully."})
#         except Exception as e:
#             return Response({"error": str(e)}, status=500)
