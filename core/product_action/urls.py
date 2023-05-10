from django.urls import path
from product_action import views


urlpatterns = [
    path('comment/',views.ProductComment.as_view()),
    path('create-comment/',views.CreateComment.as_view()),
    path('like-disslike-comment/<>',views.CommentLikeOrDisslike.as_view()),

]