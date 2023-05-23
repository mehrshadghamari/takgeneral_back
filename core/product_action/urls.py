from django.urls import path
from product_action import views

urlpatterns = [
    path('create-comment/', views.CreateComment.as_view()),
    path('like-disslike-comment/', views.CommentLikeOrDisslike.as_view()),
    path('create-question/', views.ProducrQuestion.as_view()),
    path('question-reply', views.ReplyQuestion.as_view()),

]
