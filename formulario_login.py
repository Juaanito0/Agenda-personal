import tkinter as tk
from tkinter import messagebox, ttk
import db
import agenda

db.crear_tabla()
ventana_registro = None

# ── PALETA ────────────────────────────────────────────────────────────────────
BG          = "#1a2740"       # Fondo principal azul oscuro
CARD        = "#223354"       # Tarjeta / panel
CARD_SHADOW = "#131e30"       # Sombra de tarjeta
ACCENT      = "#2979ff"       # Azul brillante (botones primarios)
ACCENT_HOV  = "#5393ff"       # Hover botón primario
ACCENT2     = "#1a2740"       # Botón secundario
TEXT        = "#e8edf5"       # Texto principal
TEXT_DIM    = "#7a8fad"       # Texto secundario / placeholder
ENTRY_BG    = "#1a2e4a"       # Fondo de entradas
ENTRY_BD    = "#2979ff"       # Borde de entradas al foco
LIST_SEL    = "#2979ff"       # Selección en lista
DANGER      = "#e53935"       # Botón eliminar
DANGER_HOV  = "#ff5f52"

FONT        = "Segoe UI"
# ─────────────────────────────────────────────────────────────────────────────

ventana = tk.Tk()
ventana.title("Agenda Personal")
ventana.geometry("360x460")
ventana.configure(bg=BG)
ventana.resizable(False, False)

# ── HELPERS ───────────────────────────────────────────────────────────────────
def make_label(parent, text, size=10, color=TEXT, bold=False):
    weight = "bold" if bold else "normal"
    return tk.Label(parent, text=text, font=(FONT, size, weight),
                    bg=parent.cget("bg") if hasattr(parent, 'cget') else BG,
                    fg=color)

def make_entry(parent, show=None, width=28):
    e = tk.Entry(parent, font=(FONT, 10), bg=ENTRY_BG, fg=TEXT,
                 insertbackground=TEXT, relief="flat",
                 highlightthickness=1, highlightbackground=CARD_SHADOW,
                 highlightcolor=ACCENT, width=width, show=show or "")
    return e

def make_button(parent, text, command, color=ACCENT, hover=ACCENT_HOV, width=20):
    btn = tk.Button(parent, text=text, command=command,
                    font=(FONT, 10, "bold"), bg=color, fg=TEXT,
                    activebackground=hover, activeforeground=TEXT,
                    relief="flat", cursor="hand2", width=width,
                    pady=8, bd=0)
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn

def card(parent, top=130):
    shadow = tk.Frame(parent, bg=CARD_SHADOW)
    shadow.place(relx=0.5, y=top+6, anchor="n", width=310, height=380)
    frm = tk.Frame(parent, bg=CARD)
    frm.place(relx=0.5, y=top, anchor="n", width=310, height=380)
    return frm

def divider(parent):
    tk.Frame(parent, bg=ACCENT, height=2).pack(fill="x", padx=0, pady=(0, 16))
# ─────────────────────────────────────────────────────────────────────────────

def build_login():
    """Construye la pantalla de login."""
    for w in ventana.winfo_children():
        w.destroy()
    ventana.geometry("360x460")

    tk.Label(ventana,
             text="📋 AGENDA PERSONAL",
             font=(FONT, 18, "bold"),
             bg=BG, fg="#70b7ff").pack(pady=(16, 4), fill="x")
    tk.Label(ventana,
             text="Inicia sesión para continuar",
             font=(FONT, 10, "normal"),
             bg=BG, fg=TEXT_DIM).pack(pady=(0, 12), fill="x")

    frm = card(ventana, top=110)  # baja la tarjeta

    # --- eliminar este bloque duplicado ---
    # tk.Label(ventana, text="📋  AGENDA PERSONAL",
    #          font=(FONT, 13, "bold"), bg=BG, fg=ACCENT).pack(pady=(28, 0))
    # tk.Label(ventana, text="Inicia sesión para continuar",
    #          font=(FONT, 9), bg=BG, fg=TEXT_DIM).pack(pady=(2, 14))
    # --- fin duplicado ---

    # Tarjeta
    tk.Label(frm, text="USUARIO", font=(FONT, 8, "bold"),
             bg=CARD, fg=TEXT_DIM).pack(anchor="w", padx=28, pady=(28, 2))
    ent_usr = make_entry(frm)
    ent_usr.pack(padx=28, fill="x")

    tk.Frame(frm, bg=ACCENT, height=1).pack(fill="x", padx=28, pady=(0, 14))

    tk.Label(frm, text="CONTRASEÑA", font=(FONT, 8, "bold"),
             bg=CARD, fg=TEXT_DIM).pack(anchor="w", padx=28, pady=(0, 2))
    ent_pwd = make_entry(frm, show="*")
    ent_pwd.pack(padx=28, fill="x")
    tk.Frame(frm, bg=ACCENT, height=1).pack(fill="x", padx=28, pady=(0, 24))

    def do_login():
        u, p = ent_usr.get(), ent_pwd.get()
        if db.validar_usuario(u, p):
            messagebox.showinfo("Bienvenido", f"Hola, {u} 👋")
            global ventana_registro
            if ventana_registro and ventana_registro.winfo_exists():
                ventana_registro.destroy()
                ventana_registro = None
            db.crear_tabla_tareas()
            build_agenda(u)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    ventana.bind("<Return>", lambda e: do_login())

    make_button(frm, "  INGRESAR  →", do_login, width=24).pack(padx=28, fill="x")
    tk.Frame(frm, bg=CARD, height=10).pack()
    tk.Button(frm, text="¿No tienes cuenta? Regístrate",
              font=(FONT, 8), bg=CARD, fg=ACCENT,
              activebackground=CARD, activeforeground=ACCENT_HOV,
              relief="flat", cursor="hand2", bd=0,
              command=abrir_registro).pack()

# ── AGENDA ────────────────────────────────────────────────────────────────────
def build_agenda(usuario):
    for w in ventana.winfo_children():
        w.destroy()
    ventana.geometry("500x560")
    ventana.resizable(True, True)

    # Header
    header = tk.Frame(ventana, bg="#162242", height=50)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="📋 AGENDA PERSONAL",
             font=(FONT, 20, "bold"),
             bg="#162242", fg="#84c7ff").pack(expand=True)

    # Cuerpo
    body = tk.Frame(ventana, bg=BG)
    body.pack(fill="both", expand=True, padx=20, pady=16)

    # Entrada de tarea con sombra
    input_shadow = tk.Frame(body, bg=CARD_SHADOW)
    input_shadow.pack(fill="x", pady=(0, 2))
    input_frame = tk.Frame(input_shadow, bg=CARD)
    input_frame.pack(fill="x", padx=0, pady=0, ipady=14, ipadx=14)

    tk.Label(input_frame, text="NUEVA TAREA", font=(FONT, 8, "bold"),
             bg=CARD, fg=TEXT_DIM).pack(anchor="w", padx=14, pady=(8, 2))

    row = tk.Frame(input_frame, bg=CARD)
    row.pack(fill="x", padx=14, pady=(0, 8))
    ent_tarea = make_entry(row, width=36)
    ent_tarea.pack(side="left", fill="x", expand=True)

    def guardar_tarea():
        t = ent_tarea.get().strip()
        if t:
            db.insertar_tarea(usuario, t)
            lista_tareas.insert(tk.END, f"  {t}")
            ent_tarea.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Escribe una tarea primero.")

    tk.Button(row, text=" ＋ ", font=(FONT, 13, "bold"),
              bg=ACCENT, fg="white",
              activebackground=ACCENT_HOV, activeforeground="white",
              relief="flat", cursor="hand2", bd=0,
              command=guardar_tarea).pack(side="left", padx=(8, 0))

    # Lista con sombra
    list_shadow = tk.Frame(body, bg=CARD_SHADOW)
    list_shadow.pack(fill="both", expand=True, pady=(14, 0))
    list_frame = tk.Frame(list_shadow, bg=CARD)
    list_frame.pack(fill="both", expand=True, padx=0, pady=0)

    tk.Label(list_frame, text="MIS TAREAS", font=(FONT, 8, "bold"),
             bg=CARD, fg=TEXT_DIM).pack(anchor="w", padx=14, pady=(10, 4))

    scrollbar = tk.Scrollbar(list_frame, bg=CARD, troughcolor=CARD, width=8)
    scrollbar.pack(side="right", fill="y", padx=(0, 4), pady=4)

    lista_tareas = tk.Listbox(list_frame,
                              font=(FONT, 10), bg=CARD, fg=TEXT,
                              selectbackground=ACCENT, selectforeground="white",
                              relief="flat", bd=0,
                              highlightthickness=0,
                              activestyle="none",
                              yscrollcommand=scrollbar.set)
    lista_tareas.pack(fill="both", expand=True, padx=14, pady=(0, 8))
    scrollbar.config(command=lista_tareas.yview)

    def eliminar_tarea():
        sel = lista_tareas.curselection()
        if sel:
            tarea = lista_tareas.get(sel).strip()
            db.eliminar_tarea(usuario, tarea)
            lista_tareas.delete(sel)
        else:
            messagebox.showwarning("Aviso", "Selecciona una tarea para eliminar.")

    # Botones inferiores
    btn_row = tk.Frame(body, bg=BG)
    btn_row.pack(fill="x", pady=(12, 0))
    make_button(btn_row, "🗑  Eliminar seleccionada", eliminar_tarea,
                color=DANGER, hover=DANGER_HOV, width=26).pack(fill="x")

    # Cargar tareas
    for t in db.obtener_tareas(usuario):
        lista_tareas.insert(tk.END, f"  {t}")

# ── REGISTRO ──────────────────────────────────────────────────────────────────
def abrir_registro():
    global ventana_registro
    if ventana_registro and ventana_registro.winfo_exists():
        ventana_registro.lift(); return

    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registro")
    ventana_registro.geometry("360x480")
    ventana_registro.configure(bg=BG)
    ventana_registro.resizable(False, False)

    tk.Label(ventana_registro, text="CREAR CUENTA",
             font=(FONT, 13, "bold"), bg=BG, fg=ACCENT).pack(pady=(24, 2))
    tk.Label(ventana_registro, text="Completa los campos para registrarte",
             font=(FONT, 9), bg=BG, fg=TEXT_DIM).pack(pady=(0, 14))

    # Tarjeta
    shadow = tk.Frame(ventana_registro, bg=CARD_SHADOW)
    shadow.place(relx=0.5, rely=0.55, anchor="center", width=310, height=340, x=4, y=6)
    frm = tk.Frame(ventana_registro, bg=CARD)
    frm.place(relx=0.5, rely=0.55, anchor="center", width=310, height=340)

    def campo(label_text, show=None):
        tk.Label(frm, text=label_text, font=(FONT, 8, "bold"),
                 bg=CARD, fg=TEXT_DIM).pack(anchor="w", padx=28, pady=(14, 2))
        e = make_entry(frm)
        e.pack(padx=28, fill="x")
        tk.Frame(frm, bg=ACCENT, height=1).pack(fill="x", padx=28, pady=(0, 2))
        return e

    ent_usr  = campo("USUARIO")
    ent_pwd  = campo("CONTRASEÑA")
    ent_pwd.config(show="*")
    ent_conf = campo("CONFIRMAR CONTRASEÑA")
    ent_conf.config(show="*")

    def toggle(e, btn):
        if e.cget("show") == "*":
            e.config(show=""); btn.config(text="🙈 Ocultar")
        else:
            e.config(show="*"); btn.config(text="👁 Mostrar")

    btn_show = tk.Button(frm, text="👁 Mostrar", font=(FONT, 8),
                         bg=CARD, fg=TEXT_DIM, activebackground=CARD,
                         relief="flat", cursor="hand2", bd=0)
    btn_show.config(command=lambda: toggle(ent_pwd, btn_show))
    btn_show.pack(anchor="e", padx=28)

    def registrar():
        global ventana_registro
        u, p, c = ent_usr.get(), ent_pwd.get(), ent_conf.get()
        if not (u and p and c):
            messagebox.showerror("Error", "Llena todos los campos."); return
        if p != c:
            messagebox.showerror("Error", "Las contraseñas no coinciden."); return
        if len(p) < 4:
            messagebox.showerror("Error", "Mínimo 4 dígitos."); return
        if not p.isdigit():
            messagebox.showerror("Error", "Solo se permiten números."); return
        if db.insertar_usuario(u, p):
            messagebox.showinfo("✅ Listo", f"Usuario '{u}' creado.")
            ventana_registro.destroy(); ventana_registro = None
        else:
            messagebox.showerror("Error", f"'{u}' ya existe.")

    make_button(frm, "  CREAR CUENTA  ", registrar, width=24).pack(padx=28, fill="x", pady=(16, 0))

# ── ARRANQUE ──────────────────────────────────────────────────────────────────
build_login()
ventana.mainloop()

