# cloudinary_utils.py
import uuid
from django.conf import settings
import cloudinary
import cloudinary.uploader
import cloudinary.api
from api.compress_utils import compress_file
import os

def upload_to_cloudinary(file, original_name=None, content_type=None, resource_type="auto"):
    """
    Faz upload de arquivo para o Cloudinary
    """
    if file.size > 100 * 1024 * 1024:
        raise ValueError("O arquivo é muito grande. O limite é 100MB.")
    
    try:
        # Comprime o arquivo (mantém a mesma lógica)
        compressed_file_path = compress_file(file)
        
        # Prepara o nome único
        short_uuid = str(uuid.uuid4())[:8]
        unique_filename = f'files_cards/{short_uuid}'
        
        # Faz upload para o Cloudinary
        upload_result = cloudinary.uploader.upload(
            compressed_file_path,
            public_id=unique_filename,
            resource_type=resource_type,  # "auto" detecta automaticamente
            overwrite=True,
            quality="auto:good"  # Compressão adicional no Cloudinary
        )
        
        # Limpa o arquivo temporário
        os.unlink(compressed_file_path)
        
        # Retorna a URL pública
        return upload_result['secure_url']
        
    except Exception as e:
        print(f"Erro na compressão/upload, tentando upload direto: {e}")
        
        # Fallback: upload direto sem compressão
        short_uuid = str(uuid.uuid4())[:8]
        unique_filename = f'files_cards/{short_uuid}'
        
        upload_result = cloudinary.uploader.upload(
            file,
            public_id=unique_filename,
            resource_type=resource_type,
            overwrite=True,
            quality="auto:good"
        )
        
        return upload_result['secure_url']
    
# cloudinary_utils.py
def delete_from_cloudinary(public_url):
    """
    Deleta arquivo do Cloudinary
    """
    try:
        print(f"INICIANDO EXCLUSÃO - URL recebida: {public_url}")
        
        # Verifica se a URL é do Cloudinary
        if 'cloudinary.com' not in public_url:
            print("URL não é do Cloudinary")
            return False
        
        # Extrai o public_id da URL do Cloudinary
        # Padrão: https://res.cloudinary.com/cloud_name/tipo/upload/version/public_id.ext
        parts = public_url.split('/upload/')
        if len(parts) < 2:
            print("Não foi possível extrair public_id da URL")
            return False
        
        # Pega tudo após '/upload/'
        path_after_upload = parts[1]
        
        # Remove parâmetros de query string se existirem
        path_after_upload = path_after_upload.split('?')[0]
        
        # Divide o caminho por '/'
        path_parts = path_after_upload.split('/')
        
        # Remove o parâmetro de versão se existir (começa com 'v')
        if path_parts and path_parts[0].startswith('v'):
            # Se tem versão, o public_id é tudo depois da versão
            public_id = '/'.join(path_parts[1:])
        else:
            # Se não tem versão, tudo é o public_id
            public_id = '/'.join(path_parts)
        
        # Remove a extensão do arquivo para obter o public_id correto
        public_id = public_id.rsplit('.', 1)[0]
        
        print(f"Public ID extraído: '{public_id}'")
        
        # Tenta deletar como imagem primeiro
        try:
            result = cloudinary.uploader.destroy(public_id, resource_type='image')
            print(f"Tentativa como imagem: {result}")
            if result.get('result') == 'ok':
                print("Arquivo excluído com sucesso do Cloudinary (como imagem)!")
                return True
        except Exception as img_error:
            print(f" Não é imagem: {img_error}")
        
        # Tenta deletar como vídeo
        try:
            result = cloudinary.uploader.destroy(public_id, resource_type='video')
            print(f"Tentativa como vídeo: {result}")
            if result.get('result') == 'ok':
                print("Arquivo excluído com sucesso do Cloudinary (como vídeo)!")
                return True
        except Exception as video_error:
            print(f" Não é vídeo: {video_error}")
        
        # Tenta deletar como raw/arquivo
        try:
            result = cloudinary.uploader.destroy(public_id, resource_type='raw')
            print(f"Tentativa como raw: {result}")
            if result.get('result') == 'ok':
                print("Arquivo excluído com sucesso do Cloudinary (como raw)!")
                return True
        except Exception as raw_error:
            print(f" Não é raw: {raw_error}")
        
        print("Arquivo não encontrado em nenhum resource_type")
        return False
            
    except Exception as e:
        print(f"ERRO CRÍTICO ao excluir arquivo do Cloudinary: {e}")
        import traceback
        print(f"Stack trace: {traceback.format_exc()}")
        return False
    
def get_cloudinary_resource_type(file):
    """
    Determina o resource_type baseado na extensão do arquivo
    """
    if hasattr(file, 'name'):
        filename = file.name.lower()
    else:
        filename = str(file).lower()
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff']
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv']
    raw_extensions = ['.pdf', '.doc', '.docx', '.txt', '.zip', '.rar']
    
    ext = os.path.splitext(filename)[1]
    
    if ext in image_extensions:
        return "image"
    elif ext in video_extensions:
        return "video"
    elif ext in raw_extensions:
        return "raw"
    else:
        return "auto"  # Cloudinary detecta automaticamente