from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from api.supabase_utils import delete_from_supabase
from api.cloudinary_utils import delete_from_cloudinary
from .models import Card, Feedback


@receiver(pre_delete, sender=Card)
def delete_card_files_from_cloudinary(sender, instance, **kwargs):
    arquivos = instance.files.all() 

    for arquivo in arquivos:
        if arquivo.file:
            # Verifica se é uma URL do Cloudinary
            if "cloudinary.com" in arquivo.file or "res.cloudinary.com" in arquivo.file:
                try:
                    delete_from_cloudinary(arquivo.file)
                    print(f"Arquivo deletado do Cloudinary: {arquivo.file}")
                except Exception as e:
                    print(f"Erro ao deletar arquivo do Cloudinary: {e}")
            # Opcional: manter compatibilidade com Supabase por um tempo
            elif "supabase.co" in arquivo.file:
                print(f"URL do Supabase ignorada (migrado para Cloudinary): {arquivo.file}")
            else:
                print(f"URL não reconhecida, não deletada: {arquivo.file}")

