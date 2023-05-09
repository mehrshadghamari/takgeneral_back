from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CommentSerializer
from product_action.models import Comment



class ProductComment(APIView):
    def get(self, request,id):
        queryset = Comment.objects.filter(id=id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        user=request.user.id
        print(request.data)
        print({**request.data,'user':1})
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        serializer = CommentSerializer(data={**request.data,'user':1})
        print(serializer)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

    
        

class CommentDetail(APIView):
    def get(self,request,id):
        queryset = Comment.objects.filter(id=id)
        serializer = CommentSerializer(queryset)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        user_id=request.user.id
        # product_id=id
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user_id)