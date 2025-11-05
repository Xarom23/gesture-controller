"""
Menu Bar Example
-----------------
Demonstrates a basic Tkinter application with a menu bar and canvas toggle functionality.
This is a standalone demo file for testing menu bar features.
"""

import tkinter as tk
from tkinter import messagebox

# Create the main window
root = tk.Tk()
root.title("Ejemplo de Menu Bar")
root.geometry("600x400")

# Variable to control canvas visibility
canvas_visible = tk.BooleanVar(value=True)

def toggle_canvas():
    """Toggle canvas visibility and resize window accordingly"""
    if canvas_visible.get():
        canvas.pack(fill=tk.BOTH, expand=True)
        root.geometry("600x400")
    else:
        canvas.pack_forget()
        root.geometry("600x1")

# Create the menu bar
menubar = tk.Menu(root)

# Create "File" menu
menu_archivo = tk.Menu(menubar, tearoff=0)
menu_archivo.add_command(label="Nuevo", command=lambda: messagebox.showinfo("Nuevo", "Crear nuevo archivo"))
menu_archivo.add_command(label="Abrir", command=lambda: messagebox.showinfo("Abrir", "Abrir archivo"))
menu_archivo.add_command(label="Guardar", command=lambda: messagebox.showinfo("Guardar", "Guardar archivo"))
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=root.quit)
menubar.add_cascade(label="Archivo", menu=menu_archivo)

# Create "Edit" menu
menu_editar = tk.Menu(menubar, tearoff=0)
menu_editar.add_command(label="Cortar", command=lambda: messagebox.showinfo("Cortar", "Cortar seleccin"))
menu_editar.add_command(label="Copiar", command=lambda: messagebox.showinfo("Copiar", "Copiar seleccin"))
menu_editar.add_command(label="Pegar", command=lambda: messagebox.showinfo("Pegar", "Pegar contenido"))
menubar.add_cascade(label="Editar", menu=menu_editar)

# Create "View" menu
menu_ver = tk.Menu(menubar, tearoff=0)
menu_ver.add_checkbutton(label="Mostrar Canvas", variable=canvas_visible, command=toggle_canvas)
menubar.add_cascade(label="Ver", menu=menu_ver)

# Create "Help" menu
menu_ayuda = tk.Menu(menubar, tearoff=0)
menu_ayuda.add_command(label="Documentacin", command=lambda: messagebox.showinfo("Ayuda", "Ver documentacin"))
menu_ayuda.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Acerca de", "Ejemplo de Menu Bar v1.0"))
menubar.add_cascade(label="Ayuda", menu=menu_ayuda)

# Configure the menu bar in the window
root.config(menu=menubar)

# Create the canvas
canvas = tk.Canvas(root, bg="lightblue", highlightthickness=1, highlightbackground="gray")
canvas.pack(fill=tk.BOTH, expand=True)

# Add some example elements to the canvas
canvas.create_text(300, 100, text="Este es el Canvas", font=("Arial", 20), fill="darkblue")
canvas.create_rectangle(50, 150, 150, 250, fill="coral", outline="black", width=2)
canvas.create_oval(200, 150, 300, 250, fill="lightgreen", outline="black", width=2)
canvas.create_line(350, 150, 450, 250, fill="red", width=3)

# Start the main loop
root.mainloop()
