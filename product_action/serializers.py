from rest_framework import serializers

from .models import Comment
from .models import CommentLike
from .models import Question
from .models import Reply


class CreateCommentSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return {'date': obj.created_at.strftime('%Y-%m-%d'), 'time': obj.created_at.strftime('%H:%M:%S'),
                'timestamp': int(obj.created_at.timestamp())}

    class Meta:
        model = Comment
        fields = ('id', 'user_alias_name', 'product', 'user', 'title',
                  'content', 'suggest_me', 'kefiyat_rate', 'arzesh_rate', 'created_at')
        read_only_fields = ('id', 'created_at',)

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Comment.objects.all(),
                fields=('user', 'product'),
                message="Some custom message."
            )]


class CreateQuestionSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return {'date': obj.created_at.strftime('%Y-%m-%d'), 'time': obj.created_at.strftime('%H:%M:%S'),
                'timestamp': int(obj.created_at.timestamp())}

    class Meta:
        model = Question
        fields = ('id', 'user', 'content', 'product', 'created_at')
        read_only_fields = ('id', 'created_at',)


class CreateReplySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return {'date': obj.created_at.strftime('%Y-%m-%d'), 'time': obj.created_at.strftime('%H:%M:%S'),
                'timestamp': int(obj.created_at.timestamp())}

    class Meta:
        model = Reply
        fields = ('id', 'user', 'question', 'content', 'created_at')
        read_only_fields = ('id', 'created_at',)


class CommentLikeSerializer(serializers.ModelSerializer):
    like_vote = serializers.BooleanField(required=False)
    dislike_vote = serializers.BooleanField(required=False)
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return {'date': obj.created_at.strftime('%Y-%m-%d'), 'time': obj.created_at.strftime('%H:%M:%S'),
                'timestamp': int(obj.created_at.timestamp())}

    class Meta:
        model = CommentLike
        fields = ('id', 'comment', 'user', 'like_vote',
                  'dislike_vote', 'created_at')
