import os
import mimetypes
from email.message import EmailMessage

def attach_file(msg: EmailMessage, file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Attachment not found at {file_path}")
        
    ctype, encoding = mimetypes.guess_type(file_path)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    
    with open(file_path, 'rb') as f:
        msg.add_attachment(f.read(),
                           maintype=maintype,
                           subtype=subtype,
                           filename=os.path.basename(file_path))
