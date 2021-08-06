from django.conf import settings
from django.db.models import manager
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.views import APIView
from .models import Employee, Organization, ComeIn, ComeOut, User, DaySummary
from .serializers import ComeInSerializer, DaySummarySerializer, EmployeeSerializer, OrganizationSerializer, UserSerializer
import os
import shutil
import face_recognition


class CreateUserView(APIView):
    """Manages user object in our system"""
    def get(self, request, format=None):
        """Return all existing users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """Creates and saves a new user in our system"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class OrganizationView(APIView):
    """Manages organization object """

    def get(self, request, format=None):
        """
            returns all organizations within our database
        """
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
            creates and saves a new organization
        """
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeView(APIView):
    """Manages Employees within the system"""

    def get(self, request, format=None):
        """
            returns all employees to corresponding organization
        """
        organization = request.query_params.get('organization', None)
        if organization:
            employees = Employee.objects.filter(organization__name=organization)
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'You need to specify which employees of organization you are looking for'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=None):
        """
            creates and saves a new employees with unique id
        """
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComeIn(APIView):
    """Manages the time when employee comes into office."""

    def get(self, request, format=None):
        """return all employees who come or exit to office."""
        try:
            come_in = bool(int(request.query_params.get('come', None)))
            come_out = bool(int(request.query_params.get('go', None)))
        except:
            return Response({'error': 'Make sure you are using params as expected!'})
        if come_in:
            come_ins = ComeIn.objects.all()
            serializer = ComeInSerializer(come_ins)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif come_out:
            come_outs = ComeOut.objects.all()
            serializer = ComeInSerializer(come_outs)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
            accepts an image, compares all Employees in db and if it finds, sets come-in or come-ot time for that eployee 
        """
        # handle incoming image

        photo = request.FILES['photo']
        path = default_storage.save(f'attendance/come/{photo.name}', ContentFile(photo.read()))
        os.path.join(settings.MEDIA_ROOT, path)
        
        incoming_image = face_recognition.load_image_file(f'media/attendance/come/{photo.name}')
        # encode incoming image
        incoming_image_encoding = face_recognition.face_encodings(incoming_image)[0]

        # compare incoming image with existings
        employees_image = [employee.photo.name for employee in Employee.objects.all()]
        for employee_image in employees_image:
            # encode employee image
            loaded_employee_image = face_recognition.load_image_file(f"media/{employee_image}")
            encoded_eployee_image = face_recognition.face_encodings(loaded_employee_image)[0]
            results = face_recognition.compare_faces([encoded_eployee_image], incoming_image_encoding)
            # after done, remove come-in images from storage
            shutil.rmtree('media/attendance/come')
            
            if True in results:
                employee = Employee.objects.filter(photo=employee_image)[0]
                try:
                    come_in = bool(int(request.query_params.get('come', None)))
                    come_out = bool(int(request.query_params.get('go', None)))
                except:
                    return Response({'error': 'Make sure you are using params as expected!'})
                if come_in:
                    # set come-in time to this employee
                    come_in_obj = ComeIn.objects.create(employee=employee) 
                    come_in_obj.save()
                
                elif come_out:
                    # set come-out time to this employee
                    come_out_obj = ComeOut.objects.create(employee=employee) 
                    come_out_obj.save()
                
                # return appropriate response
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'this photo is not recognised!'})


class DaySummaryView(APIView):
    """Manages total hours of work for each employee"""
    def get(self, request, format=None):
        """
            returns total number of hours each worker worked in company.
        """
        summaries = DaySummary.objects.all()
        serializer = DaySummarySerializer(summaries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = DaySummarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

