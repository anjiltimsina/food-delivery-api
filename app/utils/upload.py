import os
import uuid
import aiofiles

#aiofiles allows: non-blocking file operations
#User A upload file: server keeps handling User B, C, D simultaneously

from fastapi import UploadFile , HTTPException , status

#folders where the uploads will be saved
UPLOAD_DIR = "uploads"

#aloowed file types
ALLOWED_TYPES = ["image/jpeg" , "image/jpg" , "image/png", "image/webo"]

#Max file size 5 MB
MAX_FILE_SIZE = 5*1024 * 1024

async def save_upload_files(file:UploadFile , folder:str) ->str:
    #Check file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= f"file type not allowed. Allowed types : jpeg , jpg , webp , png")
    
    #read file content
    content = await file.read()

    #check file size
    if len(content) >MAX_FILE_SIZE:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "File size too large. Maximum size is 5MB"
        )
    
    #create folder if not exists
    upload_path = os.path.join(UPLOAD_DIR , folder)
    os.makedirs(upload_path , exist_ok= True)

    #generate unique filename
    extension = file.filename.split(".")[-1] # paxadi ko file type extaract garya jp , jpeg 
    filename = f"{uuid.uuid4()}.{extension}"
    file_path = os.path.join(upload_path, filename)

    #save file
    async with aiofiles.open(file_path , "wb") as f:
        await f.write(content)
    
    #return the url path 
    return f"/{UPLOAD_DIR}/{folder}/{filename}"

async def delete_upload_file(file_path :str):
    #removet leading slash
    path = file_path.lstrip("/")
    if os.path.exists(path):
        os.remove(path)




