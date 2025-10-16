# from rest_framework import serializers
# from .models import FileCard
# from api.cloudinary_utils import delete_from_cloudinary

# class FileCardSerializer(serializers.ModelSerializer):

#     file_upload = serializers.FileField(write_only=True, required=False)
#     clear_file = serializers.BooleanField(write_only=True, required=False)
#     delete = serializers.BooleanField(write_only=True, required=False)

#     class Meta:
#         model = FileCard
#         fields = '__all__'
#         read_only_fields = ('id',)
#         extra_kwargs = {'card': {'required': False}}

#     def create(self, validated_data):
#         validated_data.pop('clear_file', None)
#         validated_data.pop('delete', None)
#         file = validated_data.pop('file_upload', None)



#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         file = validated_data.pop('file_upload', None)
#         clear_file = validated_data.pop('clear_file', False)
#         validated_data.pop('delete', None)

#         if file:
#             if instance.file:
#                 # delete_from_supabase(instance.file)
#                 delete_from_cloudinary(instance.file)

#         elif clear_file:
#             if instance.file:
#                 # delete_from_supabase(instance.file)
#                 delete_from_cloudinary(instance.file)
#             validated_data['file'] = None

#         return super().update(instance, validated_data)

#     def delete(self, instance):
#         if instance.file:
#             # delete_from_supabase(instance.file)
#             delete_from_cloudinary(instance.file)
#         instance.delete()



from rest_framework import serializers
from .models import FileCard
from api.cloudinary_utils import delete_from_cloudinary

class FileCardSerializer(serializers.ModelSerializer):
    # REMOVA estes campos se não está usando upload direto para o Django
    # file_upload = serializers.FileField(write_only=True, required=False)
    # clear_file = serializers.BooleanField(write_only=True, required=False)
    # delete = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = FileCard
        fields = '__all__'
        read_only_fields = ('id',)
        extra_kwargs = {'card': {'required': False}}

    def create(self, validated_data):
        """
        Cria um novo FileCard com a URL do Cloudinary
        """
        print(f"🎯 Criando FileCard com dados: {validated_data}")
        
        # Validar que temos a URL do arquivo
        if not validated_data.get('file'):
            raise serializers.ValidationError({"file": "URL do arquivo é obrigatória"})
        
        try:
            instance = super().create(validated_data)
            print(f"✅ FileCard criado com sucesso: {instance.id}")
            return instance
        except Exception as e:
            print(f"❌ Erro ao criar FileCard: {e}")
            raise

    def update(self, instance, validated_data):
        """
        Atualiza FileCard - remove lógica antiga de upload
        """
        print(f"🔄 Atualizando FileCard {instance.id}: {validated_data}")
        return super().update(instance, validated_data)

    # REMOVA o método delete do serializer - isso é responsabilidade da view