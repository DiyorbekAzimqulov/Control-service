from django.db.models import fields
from rest_framework import serializers
from .models import Employee, Organization, User, ComeOut, ComeIn, DaySummary
import uuid


def generate_unique_image_name(image_name, unique_id):
    """generates unique image name which corresponds database record"""
    image_ext = image_name.split('.')[-1]
    ready_image_name = str(unique_id) + "." + image_ext
    return ready_image_name


class UserSerializer(serializers.ModelSerializer):
    """Serializer class for user object"""
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for Organization model class"""

    class Meta:
        model = Organization
        fields = ['name', 'description']

class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee object"""

    class Meta:
        model = Employee
        fields = ['first_name', 'middle_name', 'last_name', 'photo', 'organization']
    
    def create(self, validated_employee):
        """save an object with new uuid."""
        unique_id = uuid.uuid4()
        validated_employee.get('photo').name = generate_unique_image_name(image_name=validated_employee.get('photo').name,
                                                                            unique_id=unique_id
                                                                           )
        employee = Employee.objects.create(**validated_employee)        
        employee.unique_id = unique_id
        employee.save()
        return employee

class ComeInSerializer(serializers.ModelSerializer):
    """Serializer for ComeIn object"""
    class Meta:
        model = ComeIn
        fields = ['employee', 'date']


class DaySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DaySummary
        fields = ['employee', 'come_in', 'come_out', 'total_work_hours']

    def create(self, validated_summary):
        """
            save an object and set the total working hours
        """
        summary = DaySummary.objects.create(**validated_summary)
        total_hours = summary.come_out - summary.come_in
        summary.total_work_hours = total_hours
        summary.save()
        return summary
