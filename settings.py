import tkinter as tk
from tkinter import messagebox
from tkinter.constants import *
from config import _bgcolor, _fgcolor
from PIL import Image, ImageTk


class Settings:
    def __init__(self, top):
    
        
        self.top = top
        top.geometry("600x520+512+341")
        top.minsize(120, 1)
        top.resizable(0, 0)
        top.title("Configuración")
        
        self.left_hand_mode = "keyboard"
        self.right_hand_mode = "mouse"
        
        self.left_blink_mode = "left_click"   # Can be "left_click" or "right_click"
        self.right_blink_mode = "right_click" # Can be "left_click" or "right_click"
        
        self.main_frame = tk.Frame(top)
        self.main_frame.configure(background="#d9d9d9")

        self.main_frame.grid_columnconfigure(0, weight=1)
        for i in range(4):
            self.main_frame.grid_rowconfigure(i, weight=1)

        top.grid_columnconfigure(0, weight=1)
        for i in range(4):
            top.grid_rowconfigure(i, weight=1)

        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=3, column=0, pady=20)
        self.button_frame.configure(background="#d9d9d9")
        self.Button1 = tk.Button(self.button_frame)
        self.Button1.grid(row=0, column=0, padx=10)
        self.Button1.configure(background="#d9d9d9", text='Guardar', command=self.save_settings)

        self.Button2 = tk.Button(self.button_frame)
        self.Button2.grid(row=0, column=1, padx=10)
        self.Button2.configure(background="#d9d9d9", text='Restablecer', command=self.reset_settings)

        self.facial_frame = tk.LabelFrame(self.main_frame)
        self.facial_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        self.facial_frame.configure(relief='groove', text='Gestos faciales', background="#d9d9d9")


        for i in range(3):
            self.facial_frame.grid_columnconfigure(i, weight=1, uniform='col')

        self.frame_facial_group_left = tk.Frame(self.facial_frame)
        self.frame_facial_group_left.grid(row=0, column=0, sticky='nsew')
        self.frame_facial_group_left.grid_rowconfigure(0, weight=1)
        self.frame_facial_group_left.grid_columnconfigure(0, weight=1)
        self.Label3 = tk.Label(self.frame_facial_group_left)
        self.Label3.grid(row=0, column=0, padx=5, pady=5)
        self.Label3.configure(text='Parpadeo izquierdo', justify='center', font="-family {Segoe UI} -weight bold")

        def load_and_resize_image(path, size=(80, 80)):
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        self.keyboard_icon = load_and_resize_image('assets/keyboard.png')
        self.left_click_icon = load_and_resize_image('assets/left_click.png')
        self.right_click_icon = load_and_resize_image('assets/right_click.png')
        self.mouse_movement_icon = load_and_resize_image('assets/mouse_movement.png')
        
        self.Message2 = tk.Label(self.frame_facial_group_left, image=self.left_click_icon)
        self.Message2.image = self.left_click_icon
        self.Message2.grid(row=1, column=0)
        self.Message2.configure(background="#ffffff")


        self.frame_facial_group_center = tk.Frame(self.facial_frame)
        self.frame_facial_group_center.grid(row=0, column=1, sticky='nsew')
        self.frame_facial_group_center.grid_rowconfigure(0, weight=1)
        self.frame_facial_group_center.grid_columnconfigure(0, weight=1)
        self.Button4 = tk.Button(self.frame_facial_group_center)
        self.Button4.grid(row=0, column=0)
        self.Button4.configure(background="#d9d9d9", text='Intercambiar', command=self.swap_facial_modes)

        
        self.frame_facial_group_right = tk.Frame(self.facial_frame)
        self.frame_facial_group_right.grid(row=0, column=2, sticky='nsew')
        self.frame_facial_group_right.grid_rowconfigure(0, weight=1)
        self.frame_facial_group_right.grid_columnconfigure(0, weight=1)
        self.Label4 = tk.Label(self.frame_facial_group_right)
        self.Label4.grid(row=0, column=0, padx=5, pady=5)
        self.Label4.configure(text='Parpadeo derecho', justify='center', font="-family {Segoe UI} -weight bold")

        self.Message3 = tk.Label(self.frame_facial_group_right, image=self.right_click_icon)
        self.Message3.image = self.right_click_icon
        self.Message3.grid(row=1, column=0, padx=5, pady=5)
        self.Message3.configure(background="#ffffff")

        self.hand_frame = tk.LabelFrame(self.main_frame)
        self.hand_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        self.hand_frame.configure(relief='groove', text='Gestos de las manos', background="#d9d9d9")


        for i in range(3):
            self.hand_frame.grid_columnconfigure(i, weight=1)

        self.frame_hand_group_left = tk.Frame(self.hand_frame)
        self.frame_hand_group_left.grid(row=0, column=0, sticky='nsew')
        self.frame_hand_group_left.grid_rowconfigure(0, weight=1)
        self.frame_hand_group_left.grid_columnconfigure(0, weight=1)
        self.Label5 = tk.Label(self.frame_hand_group_left)
        self.Label5.grid(row=0, column=0, padx=5, pady=5)
        self.Label5.configure(text='Mano izquierda', justify='center', font="-family {Segoe UI} -weight bold")

        self.Message4 = tk.Label(self.frame_hand_group_left, image=self.keyboard_icon)
        self.Message4.image = self.keyboard_icon
        self.Message4.grid(row=1, column=0)
        self.Message4.configure(background="#ffffff")

        self.frame_hand_group_center = tk.Frame(self.hand_frame)
        self.frame_hand_group_center.grid(row=0, column=1, sticky='nsew')
        self.frame_hand_group_center.grid_rowconfigure(0, weight=1)
        self.frame_hand_group_center.grid_columnconfigure(0, weight=1)
        self.Button3 = tk.Button(self.frame_hand_group_center)
        self.Button3.grid(row=0, column=0)
        self.Button3.configure(background="#d9d9d9", text='Intercambiar', command=self.swap_hand_modes)

        self.frame_hand_group_right = tk.Frame(self.hand_frame)
        self.frame_hand_group_right.grid(row=0, column=2, sticky='nsew')
        self.frame_hand_group_right.grid_rowconfigure(0, weight=1)
        self.frame_hand_group_right.grid_columnconfigure(0, weight=1)
        self.Label6 = tk.Label(self.frame_hand_group_right)
        self.Label6.grid(row=0, column=0, padx=5, pady=5)
        self.Label6.configure(text='Mano derecha', justify='center', font="-family {Segoe UI} -weight bold")

        self.Message5 = tk.Label(self.frame_hand_group_right, image=self.mouse_movement_icon)
        self.Message5.image = self.mouse_movement_icon
        self.Message5.grid(row=1, column=0, padx=5, pady=5)
        self.Message5.configure(background="#ffffff")

        self.Frame2 = tk.Frame(self.main_frame)
        self.Frame2.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        self.Frame2.configure(relief='groove', borderwidth="2", background="#d9d9d9")
        
        self.Label2 = tk.Label(self.Frame2)
        self.Label2.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.Label2.configure(
            background="#d9d9d9",
            font="-family {Segoe UI} -size 20 -weight bold -slant italic",
            text='Configuración'
        )
        
        self.main_frame.pack(fill='both', expand=True)
        
    def swap_hand_modes(self):
        self.left_hand_mode, self.right_hand_mode = self.right_hand_mode, self.left_hand_mode

        self.Message4.configure(image=self.mouse_movement_icon if self.left_hand_mode == "mouse" else self.keyboard_icon)
        self.Message5.configure(image=self.keyboard_icon if self.right_hand_mode == "keyboard" else self.mouse_movement_icon)
    
    def swap_facial_modes(self):
        self.left_blink_mode, self.right_blink_mode = self.right_blink_mode, self.left_blink_mode
        
        temp_image = self.Message2.cget('image')
        self.Message2.configure(image=self.Message3.cget('image'))
        self.Message3.configure(image=temp_image)

    def save_settings(self):
        import json
        
        config = {
        'left_hand_mode': self.left_hand_mode,
        'right_hand_mode': self.right_hand_mode,
        'left_blink_mode': self.left_blink_mode,
        'right_blink_mode': self.right_blink_mode
    }
        
        try:
            with open('config.json', 'w') as f:
                json.dump(config, f)
            tk.messagebox.showinfo("Éxito", "Configuración guardada exitosamente")
            
            self.top.destroy()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error al guardar la configuración: {str(e)}")
            
    def reset_settings(self):
        if tk.messagebox.askyesno("Confirmar", "¿Está seguro de que desea restablecer la configuración?"):
            self.left_hand_mode = "keyboard"
            self.right_hand_mode = "mouse"
 
            self.left_blink_mode = "left_click"
            self.right_blink_mode = "right_click"

            self.Message4.configure(image=self.keyboard_icon)
            self.Message5.configure(image=self.mouse_movement_icon)

            self.Message2.configure(image=self.left_click_icon)
            self.Message3.configure(image=self.right_click_icon)
            
            tk.messagebox.showinfo("Éxito", "Configuración restablecida")
