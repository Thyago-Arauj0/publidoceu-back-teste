# cloudinary_utils.py
import uuid
from django.conf import settings
import cloudinary
import cloudinary.uploader
import cloudinary.api
from api.compress_utils import compress_file
import os
import time
import hashlib
import hmac
import re
from urllib.parse import unquote

def generate_cloudinary_signature(folder="files_cards", user_id=None):
    """
    Gera uma assinatura temporária para upload direto no Cloudinary (frontend)
    """
    try:
        timestamp = int(time.time())
        print(f"🕒 Timestamp gerado: {timestamp}")
        
        # Adiciona user_id ao folder para organização
        if user_id:
            folder = f"{folder}/user_{user_id}"
        
        # Parâmetros que serão usados na assinatura
        params_to_sign = {
            "timestamp": timestamp,
            "folder": folder
        }

        # Monta string para assinar - ORDEM É CRÍTICA
        sign_list = []
        for key in sorted(params_to_sign.keys()):
            sign_list.append(f"{key}={params_to_sign[key]}")
        sign_str = "&".join(sign_list)
        
        print(f"📝 String para assinar: '{sign_str}'")
        print(f"🔑 API Secret (primeiros 10 chars): {settings.CLOUDINARY_API_SECRET[:10]}...")

        # Gera assinatura HMAC-SHA1
        signature = hmac.new(
            settings.CLOUDINARY_API_SECRET.encode('utf-8'),
            sign_str.encode('utf-8'),
            hashlib.sha1
        ).hexdigest()

        print(f"✅ Assinatura gerada: {signature}")

        return {
            "timestamp": timestamp,
            "folder": folder,
            "signature": signature,
            "api_key": settings.CLOUDINARY_API_KEY,
            "cloud_name": settings.CLOUDINARY_CLOUD_NAME
        }
    
    except Exception as e:
        print(f"❌ Erro ao gerar assinatura: {e}")
        raise

def generate_cloudinary_signature_alternative(folder="files_cards", user_id=None):
    """
    Método alternativo para gerar assinatura - mais compatível
    """
    try:
        timestamp = int(time.time())
        print(f"🕒 Timestamp alternativo: {timestamp}")
        
        if user_id:
            folder = f"{folder}/user_{user_id}"

        # Método mais direto - apenas timestamp e folder
        params = f"folder={folder}&timestamp={timestamp}"
        
        print(f"📝 String alternativa para assinar: '{params}'")
        print(f"🔑 API Secret: {settings.CLOUDINARY_API_SECRET[:5]}...")

        signature = hmac.new(
            settings.CLOUDINARY_API_SECRET.encode('utf-8'),
            params.encode('utf-8'),
            hashlib.sha1
        ).hexdigest()

        print(f"✅ Assinatura alternativa: {signature}")

        return {
            "timestamp": timestamp,
            "folder": folder,
            "signature": signature,
            "api_key": settings.CLOUDINARY_API_KEY,
            "cloud_name": settings.CLOUDINARY_CLOUD_NAME
        }
    
    except Exception as e:
        print(f"❌ Erro na assinatura alternativa: {e}")
        raise

def extract_public_id_from_url(public_url):
    """
    Extrai o public_id de uma URL do Cloudinary de forma mais robusta
    """
    try:
        print(f"🔍 Extraindo public_id da URL: {public_url}")
        
        if 'cloudinary.com' not in public_url:
            print("❌ URL não é do Cloudinary")
            return None
        
        # Decodifica URL (remove encoding)
        decoded_url = unquote(public_url)
        
        # Regex para extrair public_id de diferentes formatos de URL do Cloudinary
        patterns = [
            # Padrão: /upload/v123456789/public_id.ext
            r'/upload/(?:v\d+/)?([^?]+)',
            # Padrão: /image/upload/v123456789/public_id.ext
            r'/(?:image|video|raw)/upload/(?:v\d+/)?([^?]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, decoded_url)
            if match:
                public_id_with_ext = match.group(1)
                # Remove extensão do arquivo
                public_id = public_id_with_ext.rsplit('.', 1)[0]
                print(f"✅ Public ID extraído: '{public_id}'")
                return public_id
        
        print("❌ Não foi possível extrair public_id da URL")
        return None
        
    except Exception as e:
        print(f"❌ Erro ao extrair public_id: {e}")
        return None

def delete_from_cloudinary(public_url):
    """
    Deleta arquivo do Cloudinary de forma mais robusta
    """
    try:
        print(f"🗑️ INICIANDO EXCLUSÃO - URL: {public_url}")
        
        public_id = extract_public_id_from_url(public_url)
        if not public_id:
            return False
        
        # Lista de resource_types para tentar
        resource_types = ['image', 'video', 'raw']
        
        for resource_type in resource_types:
            try:
                print(f"🔄 Tentando excluir como {resource_type}...")
                result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
                print(f"📊 Resultado ({resource_type}): {result}")
                
                if result.get('result') == 'ok':
                    print(f"✅ Arquivo excluído com sucesso (como {resource_type})!")
                    return True
                elif result.get('result') == 'not found':
                    print(f"⚠️ Arquivo não encontrado como {resource_type}")
                    continue
                    
            except Exception as type_error:
                print(f"❌ Erro ao excluir como {resource_type}: {type_error}")
                continue
        
        print("❌ Arquivo não encontrado em nenhum resource_type")
        return False
            
    except Exception as e:
        print(f"💥 ERRO CRÍTICO ao excluir arquivo: {e}")
        import traceback
        print(f"📋 Stack trace: {traceback.format_exc()}")
        return False