import os
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import easygui
import tkinter as tk

main_window = tk.Tk()
main_window.geometry('600x600')
main_window.title('Cartoonify Your Image!')
main_window.configure(background='white')

display_frame = tk.Frame(main_window, bg='white')
display_frame.pack(pady=20)

controls_frame = tk.Frame(main_window, bg='white')
controls_frame.pack(pady=20)

image_display_label = tk.Label(display_frame, bg='#CDCDCD')
image_display_label.pack()

save_image_button = tk.Button(controls_frame, text="Save Cartoon Image", padx=25, pady=5, state=tk.DISABLED)
save_image_button.configure(background='#3A4A63', foreground='white', font=('Comic Sans MS', 10))
save_image_button.pack()


def save_cartoon_image(cartoon_image, original_image_path):
    base_name = "cartoon_image_"
    directory = os.path.dirname(original_image_path)
    file_extension = os.path.splitext(original_image_path)[1]
    original_filename = os.path.basename(original_image_path)
    name_without_extension, _ = os.path.splitext(original_filename)
    new_image_path = os.path.join(directory, base_name + name_without_extension + file_extension)

    cv2.imwrite(new_image_path, cartoon_image)
    messagebox.showinfo(title=None, message="Image saved as " + base_name + " at " + new_image_path)


def create_cartoon(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, blockSize=9, C=4)
    smoothed_image = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    cartoon_image = cv2.bitwise_and(smoothed_image, edges_colored)

    cartoon_lab = cv2.cvtColor(cartoon_image, cv2.COLOR_BGR2Lab)
    l_channel, a_channel, b_channel = cv2.split(cartoon_lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)
    lab_merged = cv2.merge((cl, a_channel, b_channel))
    cartoon_image = cv2.cvtColor(lab_merged, cv2.COLOR_Lab2BGR)

    return cartoon_image


def upload_image():
    file_path = easygui.fileopenbox()
    if file_path:
        cartoon_image = create_cartoon(file_path)

        cartoon_pil_image = Image.fromarray(cv2.cvtColor(cartoon_image, cv2.COLOR_BGR2RGB))
        resized_cartoon_pil_image = cartoon_pil_image.resize((400, 400), Image.LANCZOS)

        cartoon_tk_image = ImageTk.PhotoImage(resized_cartoon_pil_image)

        image_display_label.config(image=cartoon_tk_image)
        image_display_label.image = cartoon_tk_image

        save_image_button.config(command=lambda: save_cartoon_image(cartoon_image, file_path), state=tk.NORMAL)


upload_image_button = tk.Button(main_window, text="Cartoonify an Image", command=upload_image, padx=10, pady=5)
upload_image_button.configure(background='#3A4A63', foreground='white', font=('Comic Sans MS', 10))
upload_image_button.pack(side=tk.TOP, pady=20)

main_window.mainloop()
