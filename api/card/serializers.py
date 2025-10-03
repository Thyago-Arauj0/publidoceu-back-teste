import json
from rest_framework import serializers
from .models import Card, Feedback
from api.file.models import FileCard
from api.file.serializers import FileCardSerializer
from api.supabase_utils import upload_to_supabase, delete_from_supabase

import re
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
        files_data = validated_data.pop('files', [])

        card = Card.objects.create(**validated_data)

        for idx, fdata in enumerate(files_data):

            upload = request.FILES.get(f"files[{idx}].file_upload")

            if not upload:

                continue

            file_serializer = FileCardSerializer(
                data={**fdata, "card": card.pk, "file_upload": upload}
            )

            file_serializer.is_valid(raise_exception=True)
            file_serializer.save()

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
        files_data = validated_data.pop('files', None)

        print(files_data)
        
        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        if feedback_data is not None:

            if isinstance(feedback_data, str):

                feedback_data = json.loads(feedback_data)

            feedback, _ = Feedback.objects.get_or_create(card=instance)

            for attr, value in feedback_data.items():

                setattr(feedback, attr, value)

            feedback.save()

        # Se vier files_data, processa exclusões/atualizações/criações
        if files_data is not None:
            # coleta uploads por índice (padrão: files[0].file_upload, files[1].file_upload, ...)
            uploads_by_index = {}
            if request is not None and hasattr(request, 'FILES'):
                for key, f in request.FILES.items():
                    m = re.match(r'files\[(\d+)\]\.file_upload', key)
                    if m:
                        uploads_by_index[int(m.group(1))] = f

            for idx, fdata in enumerate(files_data):
                file_id = fdata.get('id')
                delete_flag = fdata.get('delete', False)
                clear_file = fdata.get('clear_file', False)
                upload = uploads_by_index.get(idx) if uploads_by_index else request.FILES.get(f"files[{idx}].file_upload")

                if file_id:
                    # atualizar ou deletar existente
                    try:
                        file_instance = instance.files.get(id=file_id)
                    except FileCard.DoesNotExist:
                        continue

                    if delete_flag:
                        # exclui o arquivo do storage e o registro
                        if file_instance.file:
                            delete_from_supabase(file_instance.file)
                        file_instance.delete()
                        continue

                    if clear_file:
                        if file_instance.file:
                            delete_from_supabase(file_instance.file)
                        file_instance.file = None
                        # atualiza outros campos que vieram
                        for k, v in fdata.items():
                            if k in ('id', 'delete', 'clear_file'):
                                continue
                            setattr(file_instance, k, v)
                        file_instance.save()
                        continue

                    # caso normal: update (pode conter upload novo)
                    serializer_data = {**fdata, "card": instance.pk}
                    if upload:
                        serializer_data["file_upload"] = upload

                    file_serializer = FileCardSerializer(file_instance, data=serializer_data, partial=True)
                    file_serializer.is_valid(raise_exception=True)
                    file_serializer.save()

                else:
                    # criação de novo arquivo (precisa de upload)
                    if not upload:
                        # sem upload não criamos
                        continue

                    file_serializer = FileCardSerializer(
                        data={**fdata, "card": instance.pk, "file_upload": upload}
                    )
                    file_serializer.is_valid(raise_exception=True)
                    file_serializer.save()

        return instance


    def delete(self, instance):

        for f in instance.files.all():

            FileCardSerializer().delete(f)

