import gzip
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile

def file_compress(file):

    compressed_buffer = BytesIO()
    
    with gzip.GzipFile(fileobj=compressed_buffer, mode='wb') as f_out:
        f_out.write(file.read())
    
    compressed_buffer.seek(0)
    
    compressed_file = InMemoryUploadedFile(
        file=compressed_buffer,
        field_name='file_upload',
        name=file.name + '.gz',
        content_type='application/gzip',
        size=compressed_buffer.getbuffer().nbytes,
        charset=None
    )

    return compressed_file