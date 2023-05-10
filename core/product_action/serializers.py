from rest_framework import serializers
from .models import Comment,CommentLike


class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['user_alias_name','product', 'user','content', 'suggest_me','kefiyat_rate','arzesh_rate',]
        read_only_fields = ['id', 'created_at']





class CommentLikeSerializer(serializers.ModelSerializer):
    like_vote = serializers.BooleanField(required=False)
    dislike_vote = serializers.BooleanField(required=False)

    class Meta:
        model = CommentLike
        fields = ('id', 'comment', 'user', 'like_vote', 'dislike_vote', 'created_at')

    def create(self, validated_data):
        like_vote = validated_data.pop('like_vote', False)
        dislike_vote = validated_data.pop('dislike_vote', False)
        comment_like = CommentLike.objects.create(
            like_vote=like_vote,
            dislike_vote=dislike_vote,
            **validated_data
        )
        return comment_like

    def update(self, instance, validated_data):
        instance.like_vote = validated_data.get('like_vote', instance.like_vote)
        instance.dislike_vote = validated_data.get('dislike_vote', instance.dislike_vote)
        instance.save()
        return instance
