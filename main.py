import customtkinter as ctk
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ARCHIVO_TAREAS = "tareas.json"

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Todo App - Ignacio Burgos")
        self.geometry("600x500")

        #Título del Programa
        self.label_titulo = ctk.CTkLabel(
            self,
            text="Mis Tareas",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.label_titulo.pack(pady=20)

        #Datos de entrada
        self.frame_entrada = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_entrada.pack(pady=10)

        self.campo_tarea = ctk.CTkEntry(
            self.frame_entrada,
            placeholder_text="Escribe una tarea...",
            width=380,
            height=40
        )
        self.campo_tarea.pack(side="left", padx=10)

        self.boton_agregar = ctk.CTkButton(
            self.frame_entrada,
            text="Agregar",
            width=120,
            height=40,
            command=self.agregar_tarea
        )
        self.boton_agregar.pack(side="left")

        #Lista de las Tareas!!
        self.frame_tareas = ctk.CTkScrollableFrame(
            self,
            width=500,
            height=300,
            label_text="Lista de tareas"
        )
        self.frame_tareas.pack(pady=20)

        #Cargar tareas guardadas al iniciar
        self.cargar_tareas()

    #Funcion para agregar los datos al archivo Json
    def guardar_tareas(self, tareas):
        with open(ARCHIVO_TAREAS, "w", encoding="utf-8") as archivo:
            json.dump(tareas, archivo, ensure_ascii=False, indent=2)

    #Funcion para leer los datos desde Json
    def leer_tareas(self):
        if not os.path.exists(ARCHIVO_TAREAS):
            return []
        with open(ARCHIVO_TAREAS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    #Funcion para cargar y vizualizar los datos desde Json
    def cargar_tareas(self):
        tareas = self.leer_tareas()
        for tarea in tareas:
            self.crear_fila_tarea(tarea["texto"], tarea["completada"])

    #Funcion para crear visual
    def crear_fila_tarea(self, texto, completada=False):
        frame_fila = ctk.CTkFrame(self.frame_tareas)
        frame_fila.pack(fill="x", pady=5, padx=10)

        #Checkbox para marcar como completada
        var_check = ctk.BooleanVar(value=completada)

        checkbox = ctk.CTkCheckBox(
            frame_fila,
            text="",
            variable=var_check,
            width=30,
            command=lambda t=texto, v=var_check: self.toggle_completada(t, v)
        )
        checkbox.pack(side="left", padx=5)

        #Texto con tachado si está completada
        estilo = "overstrike" if completada else "normal"
        color = "gray" if completada else ("white", "black")

        label_tarea = ctk.CTkLabel(
            frame_fila,
            text=texto,
            anchor="w",
            width=350,
            text_color=color,
            font=ctk.CTkFont(overstrike=(completada))
        )
        label_tarea.pack(side="left", padx=5)

        boton_eliminar = ctk.CTkButton(
            frame_fila,
            text="\u2718",
            width=80,
            fg_color="red",
            hover_color="darkred",
            command=lambda f=frame_fila, t=texto: self.eliminar_tarea(f, t)
        )
        boton_eliminar.pack(side="right", padx=10)

    #Marcar como Completado!!
    def toggle_completada(self, texto, var_check):
        tareas = self.leer_tareas()
        for tarea in tareas:
            if tarea["texto"] == texto:
                tarea["completada"] = var_check.get()
                break
        self.guardar_tareas(tareas)

    #Funcion para agregar la tarea
    def agregar_tarea(self):
        texto = self.campo_tarea.get().strip()

        if texto == "":
            return

        self.crear_fila_tarea(texto)

        tareas = self.leer_tareas()
        tareas.append({"texto": texto, "completada": False})
        self.guardar_tareas(tareas)

        self.campo_tarea.delete(0, "end")

    #Funcion para eliminar
    def eliminar_tarea(self, frame_fila, texto):
        frame_fila.destroy()

        tareas = self.leer_tareas()
        tareas = [t for t in tareas if t["texto"] != texto]
        self.guardar_tareas(tareas)

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()