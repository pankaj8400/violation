from fastapi import FastAPI, File, UploadFile, HTTPException, Form
import os
import shutil

app = FastAPI()

# Directory to save uploaded images on your system
UPLOAD_FOLDER = "C:\\Users\\Pankaj Kumar Dubey\\Desktop\\report\\myproject\\media\\uploaded_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_images(
    folder_name: str = Form(...),  # Accept folder_name as part of the form data
    files: list[UploadFile] = File(...)
):
    # Create a specific folder to store the uploaded images
    folder_path = os.path.join(UPLOAD_FOLDER, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    try:
        for file in files:
            # Check if the file is a valid image format
            if not (file.filename.endswith('.png') or file.filename.endswith('.jpg') or file.filename.endswith('.jpeg')):
                raise HTTPException(status_code=400, detail=f"Only image files are supported (.png, .jpg, .jpeg): {file.filename}")
            
            # Save each image file to the specified folder
            file_location = os.path.join(folder_path, file.filename)
            with open(file_location, "wb") as f:
                f.write(await file.read())
        
        return {"message": f"All files successfully uploaded and saved to '{folder_path}'."}
    
    except Exception as e:
        # If an error occurs, delete the created folder to clean up
        shutil.rmtree(folder_path)  
        raise HTTPException(status_code=500, detail=f"An error occurred while uploading files: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Run the server on your local IP address with port 8000
    uvicorn.run(app, host="192.168.1.12", port=8000)













# from fastapi import FastAPI, File, UploadFile, HTTPException
# import os
# import zipfile
# from io import BytesIO

# app = FastAPI()

# # Directory to save uploaded images
# UPLOAD_FOLDER = "uploaded_images"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.post("/upload/")
# async def upload_zip(file: UploadFile = File(...)):
#     if not file.filename.endswith('.zip'):
#         raise HTTPException(status_code=400, detail="Only ZIP files are supported")
    
#     try:
#         # Extract ZIP file
#         with zipfile.ZipFile(BytesIO(await file.read())) as zip_file:
#             for file_info in zip_file.infolist():
#                 if file_info.filename.endswith(('.png', '.jpg', '.jpeg')):
#                     # Ensure the folder exists before saving files
#                     file_location = os.path.join(UPLOAD_FOLDER, file_info.filename)
#                     os.makedirs(os.path.dirname(file_location), exist_ok=True)  # Create directories if missing
                    
#                     # Save each file from ZIP to the folder
#                     with zip_file.open(file_info.filename) as source, open(file_location, 'wb') as target:
#                         target.write(source.read())
    
#         return {"message": "Files successfully uploaded and extracted"}
    
#     except zipfile.BadZipFile:
#         raise HTTPException(status_code=400, detail="The file is not a valid ZIP file.")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
