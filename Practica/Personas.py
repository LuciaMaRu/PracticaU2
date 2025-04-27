from datetime import datetime
import json
import os

Personas_JSON= "personas.json"
Usuarios_JSON= "usuarios.json"
Empleados_JSON= "empleados.json"
Reservas_JSON= "reservas.json"
 
if not os.path.exists("data"):
    os.makedirs("data")

class Personas:
    Lista_personas = []

    def __init__(self, nombre, contraseña):
        self.nombre = nombre
        self.contraseña = contraseña
        Personas.Lista_personas.append(self)

    @classmethod
    def cargar_personas(cls):
        try:
            if os.path.exists(f"data/{Personas_JSON}"):
                with open(f"data/{Personas_JSON}", "r") as file:
                    data = json.load(file)
                    for item in data:
                        cls(item["nombre"], item["contraseña"])
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error cargando personas: {str(e)}")
            cls.Lista_personas = []

    @classmethod
    def guardar_personas(cls):
        data = [{"nombre": p.nombre, "contraseña": p.contraseña} 
               for p in cls.Lista_personas]
        with open(f"data/{Personas_JSON}", "w") as file:
            json.dump(data, file, indent=4)

class Usuario(Personas):
    Lista_usuarios = []

    def __init__(self, nombre, correo, contraseña):
        super().__init__(nombre, contraseña)
        self.correo=correo
        self.reservas = []
        Usuario.Lista_usuarios.append(self)

    @classmethod
    def cargar_usuarios(cls):
        try:
            if os.path.exists(f"data/{Usuarios_JSON}"):
                with open(f"data/{Usuarios_JSON}", "r") as file:
                    data = json.load(file)
                    for item in data:
                        usuario = cls(item["nombre"], item["correo"], item["contraseña"])
                        usuario.reservas = item.get("reservas", [])
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error cargando usuarios: {str(e)}")
            cls.Lista_usuarios = []

    @classmethod
    def guardar_usuarios(cls):
        data = []
        for usuario in cls.Lista_usuarios:
            data.append({
                "nombre": usuario.nombre,
                "correo": usuario.correo,  # << AÑADIDO
                "contraseña": usuario.contraseña,
                "reservas": usuario.reservas
            })
        with open(f"data/{Usuarios_JSON}", "w") as file:
            json.dump(data, file, indent=4)

class Empleado(Personas):
    Lista_empleados = []

    def __init__(self, nombre, contraseña, rol):
        super().__init__(nombre, contraseña)
        self.rol = rol
        Empleado.Lista_empleados.append(self)

    @classmethod
    def cargar_empleados(cls):
        try:
            if os.path.exists(f"data/{Empleados_JSON}"):
                with open(f"data/{Empleados_JSON}", "r") as file:
                    data = json.load(file)
                    for item in data:
                        cls(item["nombre"], item["contraseña"], item["rol"])
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error cargando empleados: {str(e)}")
            cls.Lista_empleados = []

    @classmethod
    def guardar_empleados(cls):
        data = [{
            "nombre": e.nombre,
            "contraseña": e.contraseña,
            "rol": e.rol
        } for e in cls.Lista_empleados]
        with open(f"data/{Empleados_JSON}", "w") as file:
            json.dump(data, file, indent=4)

class Pelicula:
    Lista_peliculas=[]

    def __init__(self, titulo, duracion, genero, clasificacion, imagen, precio, horarios=None):
        self.titulo= titulo.strip().title()
        self.duracion= int(duracion)
        self.genero= genero.strip().title()
        self.clasificacion= clasificacion.strip().upper()
        self.imagen= imagen.strip()
        self.precio= float(precio)
        self.horarios= horarios if horarios else {}

    def detalles(self):
        horarios_texto = "\n".join([f"  {dia}: {', '.join(horas)}" for dia, horas in self.horarios.items()])
        return (
            f"Título: {self.titulo}\n"
            f"Duración: {self.duracion} min\n"
            f"Género: {self.genero}\n"
            f"Clasificación: {self.clasificacion}\n"
            f"Imagen: {self.imagen}\n"
            f"Precio: ${self.precio:.2f}\n"
            f"Horarios:\n{horarios_texto}"
    )

    def detalles_usuario(self):
        return (
            f"Título: {self.titulo}\n"
            f"Duración: {self.duracion} min\n"
            f"Clasificación: {self.clasificacion}\n"
            f"Precio: ${self.precio:.2f}"
        )
    
    @classmethod
    def eliminar_pelicula(cls, pelicula):
        try:
            cls.Lista_peliculas.remove(pelicula)
            cls.guardar_peliculas()
            return True
        except ValueError:
            return False

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "duracion": self.duracion,
            "genero": self.genero,
            "clasificacion": self.clasificacion,
            "imagen": self.imagen,
            "precio": self.precio,   
            "horarios": self.horarios
    }

    @classmethod
    def guardar_peliculas(cls):
        with open("peliculas.json", "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in cls.Lista_peliculas], f, ensure_ascii=False, indent=4)

    @classmethod
    def cargar_peliculas(cls):
        try:
            with open("peliculas.json", "r", encoding="utf-8") as f:
                peliculas_data = json.load(f)
                cls.Lista_peliculas = []
                for p in peliculas_data:
                    precio= p.get("precio", 100.0)
                    if isinstance(precio, dict):
                        precio=100.0

                    pelicula=Pelicula(
                        p["titulo"],
                        p["duracion"],
                        p["genero"],
                        p["clasificacion"],
                        p["imagen"],
                        precio, 
                        p.get("horarios",{})
                    )
                    cls.Lista_peliculas.append(pelicula)
        except FileNotFoundError:
            cls.Lista_peliculas = []

class Promociones:
    Lista_promociones= []

    def __init__(self, nombre, porcentaje, compra):
        self.nombre= nombre
        self.porcentaje= porcentaje
        self.compra= compra
        Promociones.Lista_promociones.append(self)
    
    def descripcion(self):
        return f"Aplica {self.porcentaje}% de descuento al comprar {self.compra} boletos."

    def condicion(self, cantidad_boletos):
        return cantidad_boletos == self.compra

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "porcentaje": self.porcentaje,
            "compra": self.compra
        }

    @classmethod
    def guardar_promociones(cls):
        data = [promo.to_dict() for promo in cls.Lista_promociones]
        with open("data/promos.json", "w") as file:
            json.dump(data, file, indent=4)

    @classmethod
    def cargar_promociones(cls):
        try:
            with open("data/promos.json", "r") as file:
                data = json.load(file)
                cls.Lista_promociones = []
                for item in data:
                    Promociones(item["nombre"], item["porcentaje"], item["compra"])
        except (FileNotFoundError, json.JSONDecodeError):
            cls.Lista_promociones = []
                

if __name__ == "__main__":
    Personas.cargar_personas()
    Usuario.cargar_usuarios()
    Empleado.cargar_empleados()
    Pelicula.cargar_peliculas()
    Promociones.cargar_promociones()
    print("Datos cargados exitosamente!")