import os
import requests
import time

def upload_folder(server_ip, folder_path):
    url = f"http://{server_ip}:8000/upload/"
    folder_name = os.path.basename(folder_path)
    
    uploaded_files = set()  # To keep track of already uploaded files

    while True:
        files = []
        
        # Collect image files to send
        for filename in os.listdir(folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')) and filename not in uploaded_files:
                filepath = os.path.join(folder_path, filename)
                files.append(('files', (filename, open(filepath, 'rb'), 'image/jpeg')))
                uploaded_files.add(filename)  # Mark file as uploaded

        if files:
            # Send folder_name as form data, not in the URL
            response = requests.post(url, data={'folder_name': folder_name}, files=files)
            
            if response.status_code == 200:
                print(response.json()['message'])
            else:
                print(f"Failed to upload images: {response.status_code} - {response.text}")
        else:
            print("No new images found.")

        time.sleep(10)  # Wait for 10 seconds before checking again

if __name__ == "__main__":
    # Replace with the server IP address (your system's IP)
    server_ip = "192.168.1.4"
    # Specify the path to the folder on the client system
    folder_path = r"C:\\Users\\Pankaj Kumar Dubey\\Music\\images"
    
    upload_folder(server_ip, folder_path)










# import os
# import requests

# def upload_folder(server_ip, folder_path):
#     url = f"http://{server_ip}:8000/upload/"
#     folder_name = os.path.basename(folder_path)
#     files = []

#     # Collect image files to send
#     for filename in os.listdir(folder_path):
#         if filename.endswith(('.png', '.jpg', '.jpeg')):
#             filepath = os.path.join(folder_path, filename)
#             files.append(('files', (filename, open(filepath, 'rb'), 'image/jpeg')))
    
#     if not files:
#         print("No images found in the folder.")
#         return
    
#     # Send folder_name as form data, not in the URL
#     response = requests.post(url, data={'folder_name': folder_name}, files=files)
    
#     if response.status_code == 200:
#         print(response.json()['message'])
#     else:
#         print(f"Failed to upload images: {response.status_code} - {response.text}")

# if __name__ == "__main__":
#     # Replace with the server IP address (your system's IP)
#     server_ip = "192.168.1.7"
#     # Specify the path to the folder on the client system
#     folder_path = r"C:\\Users\\Pankaj Kumar Dubey\\Music\\images"
    
#     upload_folder(server_ip, folder_path)
