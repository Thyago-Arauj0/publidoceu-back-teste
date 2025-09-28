import json
from rest_framework import serializers
from .models import Card, Feedback, FileCard
from api.supabase_utils import upload_to_supabase, delete_from_supabase

from api.card.utils import file_compress

class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:

        model = Feedback
        fields = '__all__'

        extra_kwargs = {
            'card': {'required': False},
            'created_at': {'required': False},
            'updated_at': {'required': False},
        }

        read_only_fields = [
            'card', 'created_at', 'updated_at'
        ]


class FileCardSerializer(serializers.ModelSerializer):

    file_upload = serializers.FileField(write_only=True, required=False)

    class Meta:

        model = FileCard
        fields = '__all__'
        read_only_fields = ('id',)
        extra_kwargs = {
            'card': {'required': False}
        }

    def create(self, validated_data):

        file = validated_data.pop('file_upload', None)

        if file:

            validated_data['file'] = upload_to_supabase(file)

        return super().create(validated_data)

    def update(self, instance, validated_data):

        file = validated_data.pop('file_upload', None)

        if file:

            if instance.file:

                delete_from_supabase(instance.file)

            validated_data['file'] = upload_to_supabase(file)

        return super().update(instance, validated_data)

    def delete(self, instance):

        if instance.file:

            delete_from_supabase(instance.file)

        instance.delete()

class CardSerializer(serializers.ModelSerializer):

    files = FileCardSerializer(many=True, required=False)
    feedback = FeedbackSerializer(required=False)

    class Meta:

        model = Card
        fields = '__all__'
        extra_kwargs = {
            'board': {'required': False},
            'feedback': {'required': False},
            'is_active': {'required': False},
            'approved_date': {'required': False},
            'deleted_at': {'required': False},
            'created_at': {'required': False},
            'updated_at': {'required': False},
        }

        read_only_fields = [
            'board', 'is_active', 'approved_date',
            'deleted_at', 'created_at', 'updated_at'
        ]

    def get_feedback(self, obj):

        feedback = obj.feedbacks.first()

        return FeedbackSerializer(feedback).data if feedback else None
    
    def get_all_files(self, obj):
        
        return FileCardSerializer(obj.files.all(), many=True).data

    def create(self, validated_data):

        request = self.context.get('request')
        feedback_data = validated_data.pop('feedback', None)

        validated_data.pop('files', None)

        card = Card.objects.create(**validated_data)
        files = request.FILES.getlist('files')

        print(files)

        for f in files:

            FileCard.objects.create(card=card,
                file=upload_to_supabase(f))

        if feedback_data:

            if isinstance(feedback_data, str):

                feedback_data = json.loads(feedback_data)

            Feedback.objects.create(card=card, **feedback_data)

        else:

            Feedback.objects.create(card=card)

        return card

    def update(self, instance, validated_data):

        request = self.context.get('request')
        feedback_data = validated_data.pop('feedback', None)

        validated_data.pop('files', None)

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        keep_file_ids = request.data.getlist('keep_files')

        if keep_file_ids:

            instance.files.exclude(id__in=keep_file_ids).delete()

        files = request.FILES.getlist('files')

        for f in files:

            FileCard.objects.create(card=instance, file_upload=f)

        if feedback_data is not None:
            
            if isinstance(feedback_data, str):

                feedback_data = json.loads(feedback_data)

            feedback, _ = Feedback.objects.get_or_create(card=instance)

            for attr, value in feedback_data.items():

                setattr(feedback, attr, value)

            feedback.save()

        return instance

    def delete(self, instance):

        for f in instance.files.all():

            FileCardSerializer().delete(f)

