from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer
from django.shortcuts import get_object_or_404
from attendance.models import Attendance
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.db import connection
from django.http import HttpResponse
import logging
from students.tasks import send_welcome_email ,send_welcome
from students.tasks import task_a, task_b, task_c
from celery import chain
from math import ceil
from django.core.cache import cache
import json
# from django.core.paginator import Paginator
logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({"detail": "CSRF cookie set"})


class ReorderStudentsView(APIView):
    def post(self, request):
        try:
            for dataa in request.data:
                student_id = dataa.get('student_id')
                new_order = dataa.get('order')

                if student_id is not None and new_order is not None:
                    Student.objects.filter(student_id=student_id).update(order=new_order)

            return Response({"message": "Student order updated!"}, status=200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=400)

#Queries
# Select s.student_id,s.email,s.name FROM student AS s WHERE s.email IN ('xyz@gmail.com','abcd@gmail.com');
# Select 
#     s.student_id
#     ,s.email,
#     s.name 
#     FROM student AS s 
#     where s.email IN ('xyz@gmail.com','abcd@gmail.com');
#Select id,student_id,date,status FROM attendance where student_id IN (Select student_id FROM student WHERE email IN ('xyz@gmail.com','abcd@gmail.com'));
# class StudentByEmailView(APIView):
#     def get(self, request):
#         emails = request.GET.get('emails')
#         if not emails:
#             return Response({"error": "No emails provided"}, status=status.HTTP_400_BAD_REQUEST)

#         email_list=emails.split(',')

#         emails_in_query = ','.join(['%s'] * len(email_list))


#         raw_query = f"""
#               SELECT 
#                   s.student_id, 
#                   s.name, 
#         s.email, 
#         a.id AS attendance_id,
#         a.date, 
#         a.status
#     FROM student AS s
#     LEFT JOIN attendance AS a 
#         ON s.student_id = a.student_id
#     WHERE s.email IN ({emails_in_query});
# """

#         with connection.cursor() as cursor:
#             cursor.execute(raw_query, email_list)
#             rows = cursor.fetchall()

#         data = []
#         for row in rows:
#             data.append({
#                 "student_id": row[0],
#                 "name": row[1],
#                 "email": row[2],
#                 "attendance_id": row[3],
#                 "date": row[4],
#                 "status": row[5],
#             })

#         return Response(data, status=status.HTTP_200_OK)
    

class StudentByEmailView(APIView):
   def get(self,request):
      emails=request.GET.get('emails')
      if not emails:
         logger.error("Error . No emails provided")
         return Response({"error": "No emails provided"}, status=status.HTTP_400_BAD_REQUEST)
      
      email_list=emails.split(',')
      attendance_records=Attendance.objects.select_related('student').filter(student__email__in=email_list).values(
         'id','student_id','date','status','student__name','student__email'
      )
      data=[]
      for record in attendance_records:
         data.append({
            'attendance_id':record['id'],
            "student_id": record['student_id'],
            "date": record["date"],
            "status": record["status"],
            "name": record["student__name"],
            "email": record["student__email"]
         })
      logger.info("Students have been gotten by emails")
      return Response(data, status=status.HTTP_200_OK)
        
   


# class StudentByEmailView(APIView):
#     def get(self, request):
#         emails = request.GET.get('emails')
#         if not emails:
#             return Response({"No emails provided"}, status=status.HTTP_400_BAD_REQUEST)

#         email_list = emails.split(",")
#         students = Student.objects.filter(email__in=email_list).prefetch_related(
#             Prefetch('attendance_set', queryset=Attendance.objects.all())
#         )
        
#         if not students.exists():
#             return Response({"No students with provided emails"}, status=status.HTTP_404_NOT_FOUND)

#         data = []
#         for student in students:
#             student_data = StudentSerializer(student).data
#             attendance_records=student.attendance_set.all() 
#             attendance_serializer=AttendanceSerializer(attendance_records,many=True)
#             data.append({
#                 "student": student_data,
#                 "attendance": attendance_serializer.data
#             })
#         return Response(data, status=status.HTTP_200_OK)
    
class StudentDeleteView(APIView):
  def delete(self,request,id):
    user=get_object_or_404(Student, id=id)
    if user is not None:
      user.delete()
    return Response({"message": "Deleted successfully"}, status=204)
      


class StudentCreateandListView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        print(serializer.data)
        return Response(serializer.data) 
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)    

def show_student_names(request):
    count = 0
    with connection.cursor() as cursor:
        while True:
            cursor.execute("SELECT studentname FROM attendance_attendance")
            row = cursor.fetchone()
            print(row)
            count += 1
            if count >= 5:
                break

    return HttpResponse("Executed 5 queries")


# class RegisterView(APIView):
#   def post(self, request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     email= request.data.get('email')
#     if not username or not password or not email:
#       logger.error("Check credentials.")
#       return Response({"error": "Username,email and password are required."}, status=400)
#     if len(password) < 8:
#       return Response({"error": "Password must be at least 8 characters long."}, status=400)
    
#     if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
#       logger.error("User Already Exists.Use unique username and email")
#       return Response("Error : username or email already exists",status=400)
    
#     user=User.objects.create_user(username=username,password=password,email=email)
#     send_welcome_email.delay("Amaz Ahmed", "amaz@gmail.com")
#     login(request,user)
#     logger.info(f"User {user} Registered successfully.")
#     return Response("Congrats, you are registered and logged in.",status=200)

def test_celery(request):
    send_welcome_email.delay("Amaz Ahmed", "amaz@gmail.com")
    send_welcome.delay("fahad","abcd@gmail.com")
    return JsonResponse({"message": "Task triggered!"})


def test_chain(request):
    result = chain(
        task_a.s(5),     
        task_b.s(),      
        task_c.s()       
    )()
    return Response("reponse is ",result)

class BulkCreateUsers(APIView):
    def post(self, request):
        try:
          users = [
            User(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='password123'
            )
            for i in range(1, 1001)
          ]
          User.objects.bulk_create(users)
          
          return Response({"message": "1000 users created successfully!"})
        except:
           return Response("Error in creating 1000 users.")
        
    def get(self,request):
        try:
          page_no=int(request.GET.get('page',1))
          page_size=int(request.GET.get('page_size',5))
          search=request.GET.get('search','').strip()
          orderby=request.GET.get('order','username')

          raw_key = f"{page_no}-{page_size}-{search}-{orderby}"
          cache_key = f"users_list:{raw_key}"
          cached_data=cache.get(cache_key)

          if cached_data:
             print("cache hit")
             return Response(json.loads(cached_data), status=200)
          
          print("cache miss")

          offset=(page_no - 1) * page_size
          limit=offset+page_size
          all_users=User.objects.order_by(orderby)
          
          if search:
             all_users=all_users.filter(username__icontains=search)
             
          total_users=all_users.count()
          total_pages=ceil(total_users/page_size)
          all_users=all_users[offset:limit]

          
          # paginator=Paginator(all_users,page_size)
          # page_obj=paginator.get_page(page_no)

          users_data=[
             {
                'username':user.username,
                'email':user.email
             }for user in all_users
          ]
          cache.set(cache_key, json.dumps(users_data), timeout=300)
          return Response({
             "message":"Pagination done successfully",
             "Total Users":total_users,
             "Total Pages":total_pages,
             "Current Page":page_no,
             "Users":users_data
          },status=200)
        except Exception as e:
           return Response({"Error":str(e)},status=400)

 
        
# @csrf_exempt
# class LoginView(APIView):
#   def post(self,request):
#     username=request.data.get("username")
#     password=request.data.get("password")
#    #  email=request.data.get("email")
#     user=authenticate(request,username=username,password=password)
#     if user is None:
#       logger.error("User not authenticated. Check credentials.")
#       return Response("User not authenticated, please check credentials",status=400)
#     login(request,user)
#    #  send_welcome_email.delay("Amaz Ahmed", "amaz@gmail.com")
#     logger.info(f"User {user} logged in successfully.")
#     return Response("Congrats, you logged in.",status=200)
  

class User_update_and_delete_view(APIView):
  def delete(self,request,username):
      try:
        user=User.objects.get(username=username)
        user.delete()    
        cache.delete(f"user_{username}")
        cache.delete_pattern("users_list*")
        return Response({"message" : "User deleted successfullt."},status=200)
      except User.DoesNotExist:
         return Response({"error": "User not found."}, status=404)
      except Exception as e:
         return Response({"error":str(e)},status=400)
      
  def put(self,request,username):
     try:
        user=User.objects.get(username=username)
        new_username=request.data.get('username',user.username)
        new_email=request.data.get('email',user.email)
        user.username=new_username
        user.email=new_email
        user.save()

        cache.delete(f"user_{username}")
        cache.delete(f"user_{new_username}")
        cache.delete_pattern("users_list*")

        return Response({
           "message":"User updated successfully",
           "user":{
              "username":new_username,
              "Email":new_email
           }
        },status=200)
     except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)
     except Exception as e:
         return Response({"error":str(e)},status=400)
     


  def get(self,request,username):
      try:
        cache_key=f"user_{username}"
        cached_data=cache.get(cache_key)

        if cached_data:
           print("Cache hit for GET user")
           return Response(json.loads(cached_data), status=200)
      
        user=User.objects.get(username=username)
        user_data={
           "username": user.username,
           "email": user.email,
        }
        cache.set(cache_key, json.dumps(user_data), timeout=300)
        print("Cache miss for GET usre")
        return Response(user_data, status=200)
      except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)
      except Exception as e:
         return Response({"error":str(e)},status=400)