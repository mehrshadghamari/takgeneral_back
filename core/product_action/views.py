from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import CreateCommentSerializer, CommentLikeSerializer
from product_action.models import Comment, CommentLike
from account.models import MyUser


class ProductComment(APIView):
    def get(self, request):
        queryset = Comment.objects.filter(id=1)
        serializer = CreateCommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = CreateCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CommentLikeOrDisslike(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request,):
        # Check if the comment exists
        try:
            comment = Comment.objects.get(pk=request.data['comment'])
        except Comment.DoesNotExist:
            return Response({'error': 'Comment does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already liked or disliked the comment
        user_id = 1
        user = MyUser.objects.get(id=user_id)
        try:
            comment_like = CommentLike.objects.get(comment=comment, user=user)
        except CommentLike.DoesNotExist:
            comment_like = None

        data = request.data.copy()
        data['user']=user_id

        if 'like_vote' in data:
            like_vote = bool(data['like_vote'])
        else:
            like_vote = False

        if 'dislike_vote' in data:
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print(data)
            dislike_vote = bool(data['dislike_vote'])
            print(dislike_vote)
        else:
            dislike_vote = False

        if like_vote and dislike_vote:
            return Response({'error': 'You can only like or dislike the comment, not both.'}, status=status.HTTP_400_BAD_REQUEST)

        # If the user already voted, update their vote
        if comment_like is not None:
            if like_vote:
                comment_like.like_vote = True
                comment_like.dislike_vote = False
            elif dislike_vote:
                comment_like.like_vote = False
                comment_like.dislike_vote = True

            serializer = CommentLikeSerializer(comment_like,data=data)
        # Otherwise, create a new like or dislike for the comment
        else:
            print("************************************")
            data['comment'] = comment.id
            data['user'] = user_id
            if like_vote:
                data['like_vote'] = True
                data['dislike_vote'] = False
            elif dislike_vote:
                data['like_vote'] = False
                data['dislike_vote'] = True
            print(data)
            serializer = CommentLikeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
