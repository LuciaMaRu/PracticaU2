import tkinter as tk
from tkinter import ttk, messagebox 
from Personas import Personas, Usuario, Empleado, Pelicula, Promociones
from datetime import datetime
from PIL import Image, ImageTk

#ADMINISTRADOR: Lucía/ 123

Personas.cargar_personas()
Usuario.cargar_usuarios()
Empleado.cargar_empleados()
Pelicula.cargar_peliculas()
Promociones.cargar_promociones()

current_user= None
ventana = None
peli_seleccionada=None
hora_seleccionada= None
asientos_seleccionados=[]
asientos_ocupados={}
butacas_disponibles=[[f"{chr(65+i)}{j+1}" for j in range(10)] for i in range(5)]
lbl_asientos= None
peliculas=[]
promociones=[]

def clear_window():
    global ventana
    for widget in ventana.winfo_children():
        widget.destroy()

def pagina_inicial():
    global ventana
    clear_window()
    ventana.geometry("600x400")
    ventana.title("Inicio")
    ventana.configure(background="#2651a7")

    tk.Label(
        ventana,
        text= f'BIENVENIDO\n'
            f'\n'
            f'Soy un...',
        font=("Aachen", 30, "bold"),
        bg="#2651a7",
        fg="white"
    ).pack(pady=40)
    
    frame_botones=tk.Frame(ventana, bg="#2651a7")
    frame_botones.pack(pady=20)

    btn_usuario= tk.Button(
        frame_botones,
        text= "USUARIO",
        font=("Arial", 14, "bold"),
        bg="#5e7fc1",
        fg="white",
        width=15,
        height=2,
        command=ventana_inicio
    )
    btn_usuario.pack(side=tk.LEFT, padx=20)

    btn_admin= tk.Button(
        frame_botones,
        text="ADMINISTRADOR",
        font=("Arial", 14, "bold"),
        bg="#5e7fc1",
        fg="white",
        width=15,
        height=2,
        command=ventana_login_admin
    )
    btn_admin.pack(side=tk.LEFT, padx=20)

def ventana_login_admin():
    global ventana
    clear_window()
    ventana.geometry("600x400")
    ventana.configure(background="#2651a7")
    ventana.grid_columnconfigure(0, weight=1)

    CINE = tk.Label(
        ventana, 
        bg="#2651a7",
        text="CINE",
        font=("Aachen", 50, "bold"), 
        fg="white")
    CINE.grid(row=0, column=0, sticky="n", pady=20) 

    ADMIN = tk.Label(
        ventana,
        bg="#2651a7",
        text="ADMINISTRADOR",
        font=("Arial", 14, "bold"),
        fg="white")
    ADMIN.grid(row=1, column=0, sticky="n", pady=5)

    USUARIO = tk.Entry(
        ventana, 
        bg="#5e7fc1",
        fg="#e8e8e8",
        font=("Arial",12),
        bd=0,
        highlightthickness=0,
        width=30,)
    USUARIO.grid(row=2, column=0, sticky="n", pady=20, ipady=5)
    USUARIO.insert(0, "Usuario")
    USUARIO.bind("<FocusIn>", lambda e: on_entry_click(USUARIO, "Usuario"))
    USUARIO.bind("<FocusOut>", lambda e: on_focus_out(USUARIO, "Usuario"))

    CONTRASEÑA = tk.Entry(
        ventana,
        bg="#5e7fc1",
        fg="#e8e8e8",
        font=("Arial", 12),
        bd=0,
        highlightthickness=0,
        width=30,
        show="")
    CONTRASEÑA.grid(row=3, column=0, sticky="n", pady=10, ipady=5)
    CONTRASEÑA.insert(0, "Contraseña")
    CONTRASEÑA.bind("<FocusIn>", lambda e: on_entry_click(CONTRASEÑA, "Contraseña", True))
    CONTRASEÑA.bind("<FocusOut>", lambda e: on_focus_out(CONTRASEÑA, "Contraseña", True))

    button_frame = tk.Frame(ventana, bg="#2651a7")
    button_frame.grid(row=4, column=0, sticky="n", pady=20)

    BOTONINGRESO = tk.Button(
        button_frame,
        text="Ingresar",
        bg="#5e7fc1",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=20,
        pady=5,
        command=lambda: validar_admin(USUARIO.get(), CONTRASEÑA.get())
    )
    BOTONINGRESO.pack(side="left", padx=10)

    BOTONVOLVER = tk.Button(
        button_frame,
        text="Volver",
        bg="#5e7fc1",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=20,
        pady=5,
        command=pagina_inicial
    )
    BOTONVOLVER.pack(side="left", padx=10)

    ventana.bind('<Return>', lambda event: validar_admin(USUARIO.get(), CONTRASEÑA.get()))

def crear_admin():
    admin_default= Empleado("Lucía", "123", "admin")
    Empleado.Lista_empleados.append(admin_default)
    Empleado.guardar_empleados()

def validar_admin(username, password):
    global current_user
    
    if not username or not password:
        messagebox.showerror("Error", "Ingrese usuario y contraseña")
        return
    
    for emp in Empleado.Lista_empleados:
        if emp.nombre == username and emp.contraseña == password and emp.rol == "admin":
            current_user = emp
            ventana_admin_principal()
            return
    
    messagebox.showerror("Error", "Credenciales incorrectas o no tiene privilegios de administrador")

def ventana_admin_principal():
    global ventana
    clear_window()
    ventana.geometry("1000x700")
    ventana.title(f"Panel de Administración - {current_user.nombre}")
    ventana.configure(background="#2651a7")

    menubar = tk.Menu(ventana)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Cerrar Sesión", command=pagina_inicial)
    file_menu.add_separator()
    file_menu.add_command(label="Salir", command=ventana.quit)
    menubar.add_cascade(label="Opciones", menu=file_menu)
    ventana.config(menu=menubar)

    main_frame = tk.Frame(ventana, bg="#2651a7")
    main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    titulo = tk.Label(
        main_frame,
        text=f"Administrador {current_user.nombre}",
        font=("Arial", 24, "bold"),
        bg="#2651a7",
        fg="white"
    )
    titulo.pack(pady=20)

    opciones_frame = tk.Frame(main_frame, bg="#2651a7")
    opciones_frame.pack(pady=10)

    def crear_boton(texto, comando):
        return tk.Button(
            opciones_frame,
            text=texto,
            font=("Arial", 14),
            bg="#4a7abc",
            fg="white",
            width=25,
            height=2,
            command=comando
        )

    crear_boton("Agregar película", agregar_pelicula).pack(pady=10)
    crear_boton("Agregar promoción", agregar_promocion).pack(pady=10)
    crear_boton("Ver asientos ocupados", ver_asientos_ocupados).pack(pady=10)
    crear_boton("Ver usuarios", ver_usuarios_registrados).pack(pady=10)
    crear_boton("Ver Estadísticas", ver_estadisticas).pack(pady=10)
    crear_boton("Ver detalles de la Pelicula", ver_detalles_pelicula).pack(pady=10)

def ver_detalles_pelicula():
    detalles_window = tk.Toplevel(ventana)
    detalles_window.title("Ver detalles de la película")
    detalles_window.geometry("500x400")
    detalles_window.configure(background="#486296")

    tk.Label(detalles_window, text="Selecciona una película:", font=("Arial", 14), bg="#486296", fg="white").pack(pady=10)

    listbox = tk.Listbox(detalles_window, font=("Arial", 12))
    listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    for idx, peli in enumerate(Pelicula.Lista_peliculas):
        listbox.insert(idx, peli.titulo)

    def mostrar_info():
        seleccion = listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una película primero.")
            return
        idx = seleccion[0]
        peli = Pelicula.Lista_peliculas[idx]
        messagebox.showinfo("Detalles", peli.detalles())

    def eliminar_peli():
        pelicula= listbox.curselection()
        if not pelicula:
            messagebox.showwarning("Advertencia", "Selecciones una pelicula")
            return
        idx= pelicula[0]
        peli=Pelicula.Lista_peliculas[idx]

        confirmar= messagebox.askyesno("Confirmar eliminación", f'¿Está seguro de eliminar {peli.titulo}?')
        if confirmar:
            if Pelicula.eliminar_pelicula(peli):

                eliminar_reservas(peli.titulo)
                messagebox.showinfo("Éxito", f"Se eliminó {peli.titulo}")
                detalles_window.destroy()
                show_main_app(current_user.rol if hasattr(current_user, 'rol') else "user")
            else:
                messagebox.showerror("Error", "No se pudo eliminar")

    btn_frame = tk.Frame(detalles_window, bg="#486296")
    btn_frame.pack(pady=10)

    tk.Button(
        btn_frame,
        text="Ver detalles",
        command=mostrar_info,
        bg="green",
        fg="white",
        font=("Arial", 12)
    ).pack(side=tk.LEFT, padx=10)

    tk.Button(
        btn_frame,
        text="Eliminar",
        command=eliminar_peli,
        bg="red",
        fg="white",
        font=("Arial", 12)
    ).pack(side=tk.LEFT, padx=10)

def eliminar_reservas(titulo):
    cambios= False
    for usuario in Usuario.Lista_usuarios:
        if hasattr(usuario, 'reservas') and usuario.reservas:
            reservas_actualizadas = [r for r in usuario.reservas if r["pelicula"] != titulo]
            if len(reservas_actualizadas) != len(usuario.reservas):
                usuario.reservas = reservas_actualizadas
                cambios = True
    if cambios:
        Usuario.guardar_usuarios()
        print(f"Reservas relacionadas a '{titulo}' eliminadas.")

def actualizar_asientos_ocupados():
    global asientos_ocupados
    asientos_ocupados={}

    for user in Usuario.Lista_usuarios:
        if hasattr(user, 'reservas'):
            for reserva in user.reservas:
                if 'pelicula' not in reserva:
                    print(f"Advertencia: La reserva no contiene la clave 'pelicula': {reserva}")
                    continue

                pelicula = reserva["pelicula"]
                dia= reserva.get("dia", "Desconocido")
                hora = reserva["hora"]
                asientos = reserva["asientos"].split(", ")

                if pelicula not in asientos_ocupados:
                    asientos_ocupados[pelicula]= {}

                if dia not in asientos_ocupados[pelicula]:
                    asientos_ocupados[pelicula][dia]= {}

                if hora not in asientos_ocupados[pelicula][dia]:
                    asientos_ocupados[pelicula][dia][hora] = []

                asientos_ocupados[pelicula][dia][hora].extend(asientos)
        
def seleccion_asiento(pelicula, dia,  hora):
    global ventana, peli_seleccionada, dia_seleccionado, hora_seleccionada, asientos_seleccionados, lbl_asientos

    peli_seleccionada= pelicula
    dia_seleccionado= dia
    hora_seleccionada= hora
    asientos_seleccionados=[]

    clear_window()
    ventana.title(f'Selección de asientos - {pelicula} -{dia} {hora}')

    main_frame= tk.Frame(ventana)
    main_frame.pack(expand=True, fill= tk.BOTH, padx=20, pady=20)

    tk.Label(
        main_frame,
        text=f'Selecciona tus asientos para {pelicula}\n{dia} - {hora}',
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    tk.Label(
        main_frame,
        text="P A N T A L L A",
        font=("Arial", 10),
        bg="black",
        fg="white",
        width=50
    ).pack(pady=10)

    container= tk.Frame(main_frame)
    container.pack()

    actualizar_asientos_ocupados()

    asientos_ocupados_funcion= asientos_ocupados.get(pelicula, {}).get(dia,{}).get(hora,[])

    
    for i, fila in enumerate(butacas_disponibles):
        row_frame=tk.Frame(container)
        row_frame.pack(fill=tk.X, pady=5)
        for asiento in fila:
            btn= tk.Button(
                row_frame,
                text= asiento,
                width=4,
                command=lambda s=asiento: toggle_seat(s), 
                bg="SystemButtonFace"
            )
            if asiento in asientos_ocupados_funcion:
                btn.config(bg="red", state="disabled")
            btn.pack(side=tk.LEFT, padx=2, pady=2)

    selected_frame= tk.Frame(main_frame)
    selected_frame.pack(pady=10)

    tk.Label(selected_frame, text="Asientos seleccionados: ", 
            font=("Arial",12)).pack()
    
    lbl_asientos=tk.Label(selected_frame, text="Ninguno", font=("Arial",12))
    lbl_asientos.pack()

    btn_frame = tk.Frame(main_frame)
    btn_frame.pack(pady=20)

    tk.Button(
        btn_frame,
        text="Confirmar Reserva",
        command=confirmar_reserva,
        bg="green",
        fg="white",
        font=("Arial", 12)
    ).pack(side=tk.LEFT, padx=10)

    tk.Button(
        btn_frame,
        text="Cancelar",
        command=show_main_app,
        bg="red",
        fg="white", 
        font=("Arial", 12)
    ).pack(side=tk.LEFT, padx=10)

def toggle_seat(asiento):
    global asientos_seleccionados, lbl_asientos, asientos_ocupados, peli_seleccionada, dia_seleccionado, hora_seleccionada

    if asiento in asientos_ocupados.get(peli_seleccionada, {}).get(dia_seleccionado,{}).get(hora_seleccionada, []):
        messagebox.showwarning("Asiento Ocupado", f"El asiento {asiento} ya está ocupado")
        return
    
    if asiento in asientos_seleccionados:
        asientos_seleccionados.remove(asiento)
        
        for child in ventana.winfo_children():
            if isinstance(child, tk.Frame):
                for frame in child.winfo_children():
                    if isinstance(frame, tk.Frame):
                        for btn in frame.winfo_children():
                            if isinstance(btn, tk.Button) and btn['text'] == asiento:
                                btn.config(bg="SystemButtonFace")
    else:
        asientos_seleccionados.append(asiento)
        
        for child in ventana.winfo_children():
            if isinstance(child, tk.Frame):
                for frame in child.winfo_children():
                    if isinstance(frame, tk.Frame):
                        for btn in frame.winfo_children():
                            if isinstance(btn, tk.Button) and btn['text'] == asiento:
                                btn.config(bg="lightblue")

    if asientos_seleccionados:
        lbl_asientos.config(text=", ".join(asientos_seleccionados))
    else:
        lbl_asientos.config(text="Ninguno")

def confirmar_reserva():
    global current_user, peli_seleccionada, dia_seleccionado,  hora_seleccionada, asientos_seleccionados

    if not asientos_seleccionados:
        messagebox.showwarning("Advertencia", "Selecciona al menos un asiento")
        return
    
    if not hasattr(current_user, 'reservas'):
        current_user.reservas=[]
    
    precio_pelicula= None
    for peli in Pelicula.Lista_peliculas:
        if peli.titulo == peli_seleccionada:
            precio_pelicula= peli.precio
            break

    if precio_pelicula is None:
        messagebox.showerror("Error", "No se encontró el precio de la pelicula")
        return
    
    cantidad_asientos= len(asientos_seleccionados)

    total_sin_descuento = precio_pelicula * cantidad_asientos

    descuento_aplicado=0
    promo_aplicada=None

    for promo in Promociones.Lista_promociones:
        if promo.condicion(cantidad_asientos):
            descuento_aplicado = total_sin_descuento * (promo.porcentaje / 100)
            promo_aplicada = promo.nombre
            break

    total_pagar = total_sin_descuento - descuento_aplicado

    nueva_reserva = {
        "pelicula": peli_seleccionada,
        "dia": dia_seleccionado,
        "hora": hora_seleccionada,
        "asientos": ", ".join(asientos_seleccionados),
        "total": total_pagar
    }
    print(f"Reservando: {nueva_reserva}")

    current_user.reservas.append(nueva_reserva)
    actualizar_asientos_ocupados()

    for i, u in enumerate(Usuario.Lista_usuarios):
        if u.correo == current_user.correo:
            Usuario.Lista_usuarios[i]= current_user
            break        

    Usuario.guardar_usuarios()
    

    resumen = f"Reserva confirmada!\n\n"
    resumen += f"Película: {peli_seleccionada}\n"
    resumen += f"Día: {dia_seleccionado}\n"
    resumen += f"Horario: {hora_seleccionada}\n"
    resumen += f"Asientos: {', '.join(asientos_seleccionados)}\n"
    resumen += f"Subtotal: ${total_sin_descuento:.2f}\n"

    
    if promo_aplicada:
        resumen+= f'Promoción aplicada: {promo_aplicada}\n' 
        resumen+= f'Descuento: -${descuento_aplicado:.2f}\n'

    resumen+= f"Total a pagar: ${total_pagar:.2f}"
    
    messagebox.showinfo("Exito", resumen)

    show_main_app(current_user.rol if hasattr(current_user, 'rol') else "user")

def ver_asientos_ocupados():
    
    asientos_window= tk.Toplevel(ventana)
    asientos_window.title("Asientos Ocupados")
    asientos_window.geometry("800x600")

    actualizar_asientos_ocupados()

    for pelicula, dias in asientos_ocupados.items():
        frame_peli = tk.Frame(asientos_window, bd=1, relief=tk.GROOVE)
        frame_peli.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(
            frame_peli,
            text=f"Película: {pelicula}",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)

        for dia, horarios in dias.items():
            frame_dia = tk.Frame(frame_peli)
            frame_dia.pack(fill=tk.X, padx=20, pady=5)

            tk.Label(
                frame_dia,
                text=f"Día: {dia}",
                font=("Arial", 11, "italic")
            ).pack(anchor="w", padx=10, pady=3)

            for hora, asientos in horarios.items():
                frame_hora = tk.Frame(frame_dia)
                frame_hora.pack(fill=tk.X, padx=20, pady=2)

                tk.Label(
                    frame_hora,
                    text=f"Horario: {hora}",
                    font=("Arial", 11)
                ).pack(side=tk.LEFT)

                tk.Label(
                    frame_hora,
                    text=f"Asientos ocupados: {', '.join(asientos)}",
                    font=("Arial", 11)
                ).pack(side=tk.LEFT, padx=20)

def on_entry_click(entry, default_text, is_password=False):
    if entry.get() == default_text:
        entry.delete(0, "end")
        entry.config(fg="black")
        if is_password:
            entry.config(show="*")

def on_focus_out(entry, default_text, is_password=False):
    if entry.get() == "":
        entry.insert(0, default_text)
        entry.config(fg="#e8e8e8")
        if is_password:
            entry.config(show="")

def ventana_inicio():
    global ventana
    clear_window()
    ventana.geometry("600x400")
    ventana.configure(background="#2651a7")
    ventana.grid_columnconfigure(0, weight=1)

    CINE = tk.Label(
    ventana, 
    bg="#2651a7",
    text="CINE",
    font=("Aachen", 50, "bold"), 
    fg="white")
    CINE.grid(row=0, column=0, sticky="n", pady=20) 

    USUARIO = tk.Entry(
    ventana, 
    bg="#5e7fc1",
    fg="#e8e8e8",
    font=("Arial",12),
    bd=0,
    highlightthickness=0,
    width=30,)
    USUARIO.grid(row=1, column=0, sticky="n", pady=10, ipady=5)
    USUARIO.insert(0, "Usuario")
    USUARIO.bind("<FocusIn>", lambda e: on_entry_click(USUARIO, "Usuario"))
    USUARIO.bind("<FocusOut>", lambda e: on_focus_out(USUARIO, "Usuario"))

    CORREO=tk.Entry(
    ventana, 
    bg="#5e7fc1",
    fg="#e8e8e8",
    font=("Arial",12),
    bd=0,
    highlightthickness=0,
    width=30,)
    CORREO.grid(row=2, column=0, sticky="n", pady=10, ipady=5)
    CORREO.insert(0, "Correo")
    CORREO.bind("<FocusIn>", lambda e: on_entry_click(CORREO, "Correo"))
    CORREO.bind("<FocusOut>", lambda e: on_focus_out(CORREO, "Correo"))

    CONTRASEÑA = tk.Entry(
    ventana,
    bg="#5e7fc1",
    fg="#e8e8e8",
    font=("Arial", 12),
    bd=0,
    highlightthickness=0,
    width=30,
    show="")
    CONTRASEÑA.grid(row=3, column=0, sticky="n", pady=10, ipady=5)
    CONTRASEÑA.insert(0, "Contraseña")
    CONTRASEÑA.bind("<FocusIn>", lambda e: on_entry_click(CONTRASEÑA, "Contraseña", True))
    CONTRASEÑA.bind("<FocusOut>", lambda e: on_focus_out(CONTRASEÑA, "Contraseña", True))

    button_frame = tk.Frame(ventana, bg="#2651a7")
    button_frame.grid(row=4, column=0, sticky="n", pady=20)

    BOTONINGRESO = tk.Button(
    button_frame,
    text="Ingresar",
    bg="#5e7fc1",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=5,
    command=lambda: ingreso(USUARIO.get(), CORREO.get(),CONTRASEÑA.get())
    )
    BOTONINGRESO.pack(side="left", padx=10)

    BOTONREGISTRO = tk.Button(
    button_frame,
    text="Registrar",
    bg="#5e7fc1",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=5,
    command=lambda: registrar(USUARIO.get(), CORREO.get(), CONTRASEÑA.get())
    )
    BOTONREGISTRO.pack(side="left", padx=10)

def ingreso(usuario, correo, contraseña):
    global current_user
    
    if correo == "Correo" or contraseña == "Contraseña":
        messagebox.showerror("Error", "Ingrese un correo y contraseña válidos")
        return
    
    for user in Usuario.Lista_usuarios:
        if user.correo == correo and user.contraseña == contraseña:
            current_user = user
            show_main_app(user.rol if hasattr(user, 'rol') else "user")
            return
        
    for emp in Empleado.Lista_empleados:
        if emp.usuario == usuario and emp.contraseña == contraseña:
            current_user = emp
            show_main_app(emp.rol)
            return
        
    
    messagebox.showerror("Error", "Correo o contraseña incorrectos")

def registrar(nombre,correo,contraseña):
    global current_user

    if nombre == "Nombre" or correo == "Correo" or contraseña == "Contraseña":
        messagebox.showerror("Error", "Complete todos los campos")
        return
    
    if any(u.correo == correo for u in Usuario.Lista_usuarios):
        messagebox.showerror("Error", "El correo ya está registrado")
        return
    
    nuevo_usuario = Usuario(nombre, correo, contraseña)
    Usuario.guardar_usuarios()

    Personas.guardar_personas()
    messagebox.showinfo("Éxito","Registro exitoso")
    current_user= nuevo_usuario
    show_main_app("user")

def show_main_app(user_type= "user"):
    global ventana, current_user

    clear_window()
    ventana.geometry("1000x700")

    if user_type == "admin":
        ventana_admin_principal()
        return
    
    Pelicula.cargar_peliculas()

    menubar = tk.Menu(ventana)
    
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Cerrar Sesión", command=pagina_inicial)
    file_menu.add_separator()
    file_menu.add_command(label="Salir", command=ventana.quit)
    menubar.add_cascade(label="Opciones", menu=file_menu)
    
    if user_type in ["admin", "taquillero"]:
        admin_menu = tk.Menu(menubar, tearoff=0)
        admin_menu.add_command(label="Agregar Función", command=agregar_pelicula)
        admin_menu.add_command(label="Agregar Promoción", command=agregar_promocion)
        menubar.add_cascade(label="Administración", menu=admin_menu)
    
    ventana.config(menu=menubar)

    main_frame = tk.Frame(ventana)
    main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    BIENVENIDO = f"Bienvenid@, {current_user.nombre}"
    if user_type != "user":
        BIENVENIDO += f" ({user_type})"
    
    tk.Label(main_frame, text=BIENVENIDO, font=("Arial", 16)).pack(pady=10)

    notebook = ttk.Notebook(main_frame)
    notebook.pack(expand=True, fill=tk.BOTH)

    tab_peliculas=tk.Frame(notebook)
    tab_reservas=tk.Frame(notebook)
    tab_promos=tk.Frame(notebook)

    notebook.add(tab_peliculas, text="Películas")
    notebook.add(tab_reservas, text="Mis reservas")
    notebook.add(tab_promos, text= "Promociones")

    setup_movies_tab(tab_peliculas)
    setup_reservations_tab(tab_reservas)
    setup_promos_tab(tab_promos)

def setup_movies_tab(parent):
    
    if not Pelicula.Lista_peliculas:
        tk.Label(parent, text="No hay películas disponibles.", font=("Arial", 14)).pack(pady=50)
        return
    
    canvas = tk.Canvas(parent, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)

    scroll_frame = tk.Frame(canvas, bg="white")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for movie in Pelicula.Lista_peliculas:
        movie_frame = tk.Frame(scroll_frame, bd=2, relief=tk.GROOVE, padx=10, pady=10, bg="white")
        movie_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(movie_frame, text=movie.titulo, font=("Arial", 14),bg="white", fg="black").pack(anchor="w")
        
        try:
            img = Image.open(movie.imagen) if movie.imagen else None
            if img:
                img = img.resize((100, 150), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                img_label = tk.Label(movie_frame, image=img)
                img_label.image = img
                img_label.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            print(f'Error al cargar la imagen de {movie.titulo}: {e}')

        buttons_frame = tk.Frame(movie_frame, bg="white")
        buttons_frame.pack(fill=tk.X, pady=5)

        tk.Label(buttons_frame, text="Horarios:",bg="white", fg="black").pack(side=tk.LEFT)

        for dia, horarios in movie.horarios.items():
            for hora in horarios:
                tk.Button(
                    buttons_frame,
                    text=f"{dia} {hora}",
                    command=lambda d=dia, h=hora, m=movie.titulo: reservar(m, d, h),
                    bg="#5e7fc1",
                    fg="white",
                    font=("Arial", 10)
                ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            movie_frame,
            text="Más información",
            command=lambda m=movie: ver_detalles_usuario(m),
            bg="#4caf50",
            fg="white",
            font=("Arial", 10)
        ).pack(pady=5) 
            
def ver_detalles_usuario(movie):
    messagebox.showinfo("Detalles de la película", movie.detalles_usuario())
  
def setup_promos_tab(parent):
    if not Promociones.Lista_promociones:
        tk.Label(parent, text="No hay promociones disponibles.", font=("Arial", 14)).pack(pady=50)
        return
    for promo in Promociones.Lista_promociones:
        promo_frame = tk.Frame(parent, bd=2, relief=tk.GROOVE, padx=10, pady=10)
        promo_frame.pack(fill=tk.X, pady=5, padx=10)

        tk.Label(
            promo_frame,
            text=f"{promo.nombre}",
            font=("Arial", 14, "bold")
        ).pack(anchor="w")

        tk.Label(
            promo_frame,
            text=f"Descripción: {promo.descripcion()}",
            font=("Arial", 12)
        ).pack(anchor="w", pady=2)

        tk.Label(
            promo_frame,
            text=f"Descuento: {promo.porcentaje}%",
            font=("Arial", 12)
        ).pack(anchor="w", pady=2)

def setup_reservations_tab(parent):
    global current_user

    print("DEBUG RESERVAS:", getattr(current_user, 'reservas', 'No tiene reservas'))
    
    if not hasattr(current_user, 'reservas') or not current_user.reservas:
        tk.Label(parent, text="No tienes reservaciones",font=("Arial", 14)).pack(pady=50)
        return
    
    for reserva in current_user.reservas:
        res_frame = tk.Frame(parent, bd=2, relief=tk.GROOVE, padx=10, pady=10)
        res_frame.pack(fill=tk.X, pady=5)

        detalles=(
            f"Película: {reserva['pelicula']}\n"
            f"Día: {reserva['dia']}\n"
            f"Horario: {reserva['hora']}\n"
            f"Asientos: {reserva['asientos']}\n"
            f"Total: ${reserva.get('total',0.0):.2f}"
        )

        tk.Label(res_frame, text=detalles, font=("Arial", 12), anchor="w", justify="left").pack(fill=tk.X, pady=10)
        
        btn_frame= tk.Frame(res_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        tk.Button(
            btn_frame, 
            text="Cancelar reserva", 
            command=lambda r=reserva: cancelar_reservacion(r),
            bg="#ff6b6b",
            fg="white",
            font=("Arial", 10)
            ).pack(side=tk.RIGHT, padx=10)

def reservar(pelicula, dia, hora):
    seleccion_asiento(pelicula, dia, hora)
    
def cancelar_reservacion(reservation):
    global current_user   

    if messagebox.askyesno("Confirmar", "¿Cancelar esta reservación?"):
        current_user.reservas.remove(reservation)
        Usuario.guardar_usuarios()
        show_main_app("user" if not hasattr(current_user, 'rol') else current_user.rol)

def agregar_pelicula():
    nueva_ventana = tk.Toplevel(ventana)
    nueva_ventana.title("Agregar Película")
    nueva_ventana.geometry("700x800")
    nueva_ventana.configure(background="#486296")

    canvas= tk.Canvas(nueva_ventana, bg="#486296", highlightthickness=0)
    scrollbar = tk.Scrollbar(nueva_ventana, orient="vertical", command=canvas.yview)

    scroll_frame = tk.Frame(canvas, bg="#486296")

    contenido_frame= tk.Frame(scroll_frame, bg="#486296")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    contenido_frame.pack(pady=20, padx=20)

    def crear_campo(label_text):
        tk.Label(contenido_frame, text=label_text, font=("Arial", 12), bg="#486296", fg="white").pack(pady=5, anchor="w")
        entry = tk.Entry(contenido_frame, font=("Arial", 12),width=40)
        entry.pack(pady=5)
        return entry
    
    entry_titulo = crear_campo("Título:")
    entry_duracion = crear_campo("Duración (minutos):")
    entry_genero = crear_campo("Género:")
    entry_clasificacion = crear_campo("Clasificación (G, PG, PG-13, R, etc):")
    entry_imagen = crear_campo("Ruta de la Imagen:")
    entry_precio = crear_campo("Precio del Boleto:")

    tk.Label(contenido_frame, text="Horarios por día (separados por comas):", font=("Arial", 12), bg="#486296", fg="white").pack(pady=10)

    dias_semana=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    entradas_horarios = {}

    for dia in dias_semana:
        tk.Label(contenido_frame, text=dia + ":", font=("Arial", 11), bg="#486296", fg="white").pack(pady=2)
        entrada = tk.Entry(contenido_frame, font=("Arial", 11),width=40)
        entrada.pack(pady=3)
        entradas_horarios[dia] = entrada

    def guardar_nueva_pelicula():
        titulo = entry_titulo.get().strip()
        duracion = entry_duracion.get().strip()
        genero = entry_genero.get().strip()
        clasificacion = entry_clasificacion.get().strip()
        imagen = entry_imagen.get().strip()
        precio = entry_precio.get().strip()

        if not (titulo and duracion and genero and clasificacion and imagen and precio):
            messagebox.showerror("Error", "¡Todos los campos deben ser completados!")
            return
        try:
            duracion= int(duracion)
            precio= float(precio)
        except ValueError:
            messagebox.showerror("Error", "Duración debe ser un número entero y precio un número decimal.")
            return
        
        horarios={}

        for dia, entrada in entradas_horarios.items():
            horas_texto= entrada.get().strip()
            if horas_texto:
                horas_lista= [h.strip() for h in horas_texto.split(",") if h.strip()]
                horarios[dia]= horas_lista
    

        nueva_pelicula = Pelicula(
            titulo,
            duracion,
            genero,
            clasificacion,
            imagen,
            precio,
            horarios
        )
            
        Pelicula.Lista_peliculas.append(nueva_pelicula)
        Pelicula.guardar_peliculas()
        messagebox.showinfo("Éxito", f"Película '{titulo}' agregada correctamente.")

        nueva_ventana.destroy()

        if hasattr(current_user, 'rol') and current_user.rol == "admin":
            ventana_admin_principal()
        else:
            show_main_app(current_user.rol if hasattr(current_user, 'rol') else "user")
    
    tk.Button(
        contenido_frame,
        text="Guardar",
        command=guardar_nueva_pelicula,
        bg="green",
        fg="white",
        font=("Arial", 12),
        width=20
    ).pack(pady=20)

def agregar_promocion():
    promo_window = tk.Toplevel(ventana)
    promo_window.title("Agregar Promoción")
    promo_window.geometry("500x400")
    promo_window.configure(bg="#486296")
    
    tk.Label(promo_window, text="Título:", font=("Arial", 12), bg="#486296", fg="white").pack(pady=5)
    entry_titulo = tk.Entry(promo_window, font=("Arial", 12))
    entry_titulo.pack(pady=5)

    tk.Label(promo_window, text="Descuento (%):", font=("Arial", 12), bg="#486296", fg="white").pack(pady=5)
    entry_descuento = tk.Entry(promo_window, font=("Arial", 12))
    entry_descuento.pack(pady=5)

    tk.Label(promo_window, text="Cantidad mínima de boletos:", font=("Arial", 12), bg="#486296", fg="white").pack(pady=5)
    entry_compra = tk.Entry(promo_window, font=("Arial", 12))
    entry_compra.pack(pady=5)

    def guardar_promocion():
        titulo = entry_titulo.get().strip()
        descuento = entry_descuento.get().strip()
        compra = entry_compra.get().strip()

        if not titulo or not descuento or not compra:
            messagebox.showerror("Error", "¡Todos los campos son obligatorios!")
            return

        try:
            descuento = float(descuento)
            compra = int(compra)
        except ValueError:
            messagebox.showerror("Error", "Descuento debe ser un número y compra debe ser un número entero.")
            return
        
        if descuento <= 0 or descuento > 100 or compra <= 0:
            messagebox.showerror("Error", "Ingrese valores válidos para descuento (1-100%) y cantidad (mínimo 1).")
            return

        nueva_promo = Promociones(titulo, descuento, compra)
        Promociones.guardar_promociones()

        messagebox.showinfo("Éxito", f"Promoción '{titulo}' agregada exitosamente.")
        promo_window.destroy()

    tk.Button(
        promo_window,
        text="Guardar",
        command=guardar_promocion,
        bg="green",
        fg="white",
        font=("Arial", 12)
    ).pack(pady=20)

def ver_usuarios_registrados():
    usuarios_window = tk.Toplevel(ventana)
    usuarios_window.title("Usuarios Registrados")
    usuarios_window.geometry("600x400")

    for usuario in Usuario.Lista_usuarios:
        tk.Label(usuarios_window, text=f"Usuario: {usuario.nombre}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=2)

def ver_estadisticas():
    estadisticas_window = tk.Toplevel(ventana)
    estadisticas_window.title("Estadísticas")
    estadisticas_window.geometry("400x300")

    total_usuarios = len(Usuario.Lista_usuarios)
    total_reservas = sum(len(u.reservas) for u in Usuario.Lista_usuarios if hasattr(u, 'reservas'))

    tk.Label(estadisticas_window, text=f"Total de usuarios: {total_usuarios}", font=("Arial", 14)).pack(pady=10)
    tk.Label(estadisticas_window, text=f"Total de reservas: {total_reservas}", font=("Arial", 14)).pack(pady=10)

crear_admin()

if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("Sistema de Cine")
    pagina_inicial()
    ventana.mainloop()
