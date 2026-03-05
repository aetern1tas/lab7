import tkinter as tk
from tkinter import ttk
import requests
from io import BytesIO
from PIL import Image, ImageTk

def get_random_neko():
    response = requests.get("https://nekos.best/api/v2/neko")
    response.raise_for_status()
    
    data = response.json()
    
    image_url = data['results'][0]['url']
    
    img_response = requests.get(image_url)
    
    img_bytes = BytesIO(img_response.content)
    pil_image = Image.open(img_bytes)
    
    pil_image.thumbnail((500, 500))
    
    return ImageTk.PhotoImage(pil_image)

def update_image():
    new_img = get_random_neko()
    label.config(image=new_img)
    label.image = new_img

root = tk.Tk()
root.title("Генератор аниме девочек")
root.geometry("600x650")

label = ttk.Label(root)
label.pack(pady=10, expand=True)

btn = ttk.Button(root, text="Получить новую картинку :3", command=update_image)
btn.pack(pady=20)

update_image()

root.mainloop()