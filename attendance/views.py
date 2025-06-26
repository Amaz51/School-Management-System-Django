from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Attendance
from .serializers import AttendanceSerializer
from django.shortcuts import get_object_or_404
from students.models import Student
from django.http import HttpResponse
from django.http import JsonResponse
import pandas as pd
from .models import Attendance
import logging
logger = logging.getLogger(__name__)
import logging
class List_and_Create_View(APIView) :
  def get(self,request):
    records = Attendance.objects.all()
    serializer = AttendanceSerializer(records, many=True)
    return Response(serializer.data)
  
  def post(self,request):
    serializer = AttendanceSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

class update_and_delete_view(APIView):
  def get_object(self, id):
    return get_object_or_404(Attendance, id=id)
  
  def get(self,request,id):
    user=self.get_object(id)
    serializer = AttendanceSerializer(user)
    return Response(serializer.data)
  
  def put(self,request,id):
    user=self.get_object(id)
    serializer = AttendanceSerializer(instance=user,data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(
          {
              "message": "updated successfully",
              "data": serializer.data
          },
          status=204)
    else:
      return Response(serializer.errors, status=400)

  def delete(self,request,id):
    user=self.get_object(id)
    if user is not None:
      user.delete()
    return Response({"message": "Deleted successfully"}, status=204)
    
class BulkCreateView(APIView):
  def post(self,request):
    data=request.data
    serializer= AttendanceSerializer(data=data, many=True)
    if serializer.is_valid():
      records=[Attendance(**item) for item in data]
      Attendance.objects.bulk_create(records)
      logger.info(f"Bulk Create Successful")
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    logger.info(f"Bulk Create Unsuccessful")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BulkUpdateView(APIView):
  def put(self, request):
        data = request.data  
        ids = [item['id'] for item in data]
        attendance_map = {a.id: a for a in Attendance.objects.filter(id__in=ids)}
        
        for i in data:
            record = attendance_map.get(i['id'])
            if record:
                record.student_id = i.get('student_id', record.student_id)
                record.date = i.get('date', record.date)
                record.status = i.get('status', record.status)
        
        Attendance.objects.bulk_update(attendance_map.values(), ['student_id', 'date', 'status'])
        logger.info("Bulk Update Successful")
        return Response({"message": "Bulk update successful."})
    
# class Attendance_by_username(APIView):
#    def get(self, request, username):
#       student=Student.objects.filter(user__username=username).first()
#       if not student:
#           return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
#       records = Attendance.objects.filter(student=student)
#       serializer = AttendanceSerializer(records, many=True)
#       return Response(serializer.data, status=status.HTTP_200_OK)


def download_attendance_by_email(request):
    email = request.GET.get('email')

    if not email:
        return JsonResponse({'error': 'Email not provided'}, status=400)

    try:
        student = Student.objects.get(email=email)
        attendance_records = Attendance.objects.filter(student=student).values()
        if not attendance_records:
            return JsonResponse({'error': 'No attendance records found'}, status=404)

        df = pd.DataFrame(attendance_records)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={email}_attendance.xlsx'

        df.to_excel(response, index=False)
        return response

    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student with this email does not exist'}, status=404)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)