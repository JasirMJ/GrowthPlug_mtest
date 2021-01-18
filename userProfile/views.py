from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields ="__all__"

class FBUserAuth(ListAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self,request):
        is_new_user = False

        try:
            email= self.request.POST.get("email","")
            first_name = self.request.POST.get("first_name","")
            last_name = self.request.POST.get("last_name","")
            username = self.request.POST.get("username","")

            obj_user = User.objects.filter(email= email)

            if obj_user.count() == 0:
                is_new_user = True
                obj_user = User()
                obj_user.first_name = first_name
                obj_user.last_name = last_name
                obj_user.email = email
                obj_user.username = username
                obj_user.password = make_password(str(123123))
                obj_user.save()

                print("user created")

            else:
                obj_user = obj_user.first()

            token, created = Token.objects.get_or_create(user= obj_user)

            return Response({
                "status": True,
                'token': "Token " + token.key,
                'user_id': obj_user.id,
                'is_new_user': is_new_user,
            })

        except Exception as e:
            return Response({
                "status":False,
                "message":str(e)
            })

    def get_queryset(self):
        qs = User.objects.all()
        return qs

    def delete(self,request):
        qs = User.objects.all().delete()
        print(qs)
        return Response({
            "status":True,
            "message":"Deleted all user data",
            "data":str(qs),
        })

    def patch(self,request):
        basic_salary = self.request.POST.get('basic_salary',0)
        increment = self.request.POST.get('increment',0)

        month_list = [
            {"id":1,"name":"JAN","increment":1},
            {"id":1,"name":"FEB","increment":0},
            {"id":1,"name":"MAR","increment":0},
            {"id":1,"name":"APR","increment":1},
            {"id":1,"name":"MAY","increment":0},
            {"id":1,"name":"JUN","increment":0},
            {"id":1,"name":"JUL","increment":1},
            {"id":1,"name":"AUG","increment":0},
            {"id":1,"name":"SEP","increment":0},
            {"id":1,"name":"OCT","increment":1},
            {"id":1,"name":"NOV","increment":0},
            {"id":1,"name":"DEC","increment":0},
        ]

        total = 0
        basic = int(basic_salary)
        salary_sheet = []
        for index,x in enumerate(month_list,1):
            print("Basic",basic)
            if x['increment']==1:
                basic = basic + increment
            salary = f"Salary of month {x['name']} {basic}"
            print(salary)
            salary_sheet.append({
                x['name']:basic
            })

            total = total + basic

        return Response({
            "Initail":basic_salary,
            "Total":total,
            "Salary_sheet":salary_sheet
        })