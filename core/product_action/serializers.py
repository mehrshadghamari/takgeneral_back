from rest_framework import serializers
from .models import Comment,CommentLike


class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['user_alias_name','product', 'user','title','content', 'suggest_me','kefiyat_rate','arzesh_rate',]
        read_only_fields = ['id', 'created_at']





class CommentLikeSerializer(serializers.ModelSerializer):
    like_vote = serializers.BooleanField(required=False)
    dislike_vote = serializers.BooleanField(required=False)

    class Meta:
        model = CommentLike
        fields = ('id' ,'comment', 'user', 'like_vote', 'dislike_vote', 'created_at')

    # def validate(self, attrs):
    #     # Check if the comment exists and is active
    #     try:
    #         comment = Comment.objects.get(pk=attrs['comment'].id,)
    #     except Comment.DoesNotExist:
    #         raise serializers.ValidationError({'comment': 'Invalid or inactive comment.'})

    #     # Check if the user has already liked or disliked the comment
    #     user = attrs['user']
    #     try:
    #         comment_like = CommentLike.objects.get(comment=comment, user=user)
    #     except CommentLike.DoesNotExist:
    #         comment_like = None

    #     if 'like_vote' in attrs:
    #         like_vote = attrs['like_vote']
    #         if like_vote and comment_like and not comment_like.dislike_vote:
    #             raise serializers.ValidationError({'like_vote': 'You have already liked this comment.'})
    #         attrs['dislike_vote'] = False
    #     elif 'dislike_vote' in attrs:
    #         dislike_vote = attrs['dislike_vote']
    #         if dislike_vote and comment_like and not comment_like.like_vote:
    #             raise serializers.ValidationError({'dislike_vote': 'You have already disliked this comment.'})
    #         attrs['like_vote'] = False

    #     attrs['comment'] = comment
    #     attrs['user'] = user
    #     return attrs

    # def create(self, validated_data):
    #     like_vote = validated_data.pop('like_vote', False)
    #     dislike_vote = validated_data.pop('dislike_vote', False)
    #     comment_like = CommentLike.objects.create(
    #         like_vote=like_vote,
    #         dislike_vote=dislike_vote,
    #         **validated_data
    #     )
    #     return comment_like

    # def update(self, instance, validated_data):
    #     instance.like_vote = validated_data.get('like_vote', instance.like_vote)
    #     instance.dislike_vote = validated_data.get('dislike_vote', instance.dislike_vote)
    #     instance.save()
    #     return instance