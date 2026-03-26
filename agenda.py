import tkinter as tk
from tkinter import messagebox
import db #Importa el archivo db.py

# Variable global para la ventana de agenda
ventana_agenda = None

def abrir_agenda(usuario):
    global ventana_agenda
    
    if ventana_agenda is None or not ventana_agenda.winfo_exists():
        ventana_agenda = tk.Toplevel()
        ventana_agenda.title(f"Agenda de {usuario}")
        ventana_agenda.geometry("500x650")
        
        # Campo para nueva tarea
        label_tarea = tk.Label(ventana_agenda, text="Nueva Tarea:")
        label_tarea.pack()
        entrada_tarea = tk.Entry(ventana_agenda, width=40)
        entrada_tarea.pack()
        
        # lista de tareas
        lista_tareas = tk.Listbox(ventana_agenda, width=50, height=10)
        lista_tareas.pack()
        
        #funcion para guardar tarea
        def guardar_tarea():
            tarea = entrada_tarea.get()
            if tarea:
                db.insertar_tarea(usuario, tarea)
                lista_tareas.insert(tk.END, tarea)
                entrada_tarea.delete(0, tk.END)
                messagebox.showinfo("Tarea guardada", "La tarea se ha guardado correctamente.")
            else:
                messagebox.showwarning("Error", "Por favor, ingresa una tarea.")
        
    boton_guardar = tk.Button(ventana_agenda, text="Guardar Tarea", command=guardar_tarea)
    boton_guardar.pack()
    
    # función para eliminar tarea
    def eliminar_tarea():
        seleccion = lista_tareas.curselection()
        if seleccion:
            tarea = lista_tareas.get(seleccion)
            db.eliminar_tarea(usuario, tarea)
            lista_tareas.delete(seleccion)
            messagebox.showinfo("Tarea eliminada", "La tarea se ha eliminado correctamente.")
        else:
            messagebox.showwarning("Error", "Por favor, selecciona una tarea para eliminar.")
    
    boton_eliminar = tk.Button(ventana_agenda, text="Eliminar tarea", command=eliminar_tarea)
    boton_eliminar.pack()
    
    #cargar tareas existentes
    tareas = db.obtener_tareas(usuario)
    for t in tareas:
        lista_tareas.insert(tk.END, t)
    else:
    # Si ya existe, la trae al frente
        ventana_agenda.lift()