# PracticaU2
#Sistema de Reservas para un Cine

**¿Cómo ejecutar el Programa?**
Al iniciar el programa, deberás identificarte como USUARIO o ADMINISTRADOR

**USUARIO**
Al hacer click en USUARIO, deberemos ingresar:
  -Nombre(usuario)
  -Correo
  -Contraseña
Si es la primera vez que entras al sistema, deberás dar click en _Registrar_
Si ya estás registrado, solo da click en _Ingresar_.

**Pagina de inicio:**
En esta página encontraras las _Pelíuclas_ disponibles, podrás ver:
    -Nombre de la película
    -Poster
    -Días y horarios disponibles
    -Más información:
      +Título
      +Duración
      +Clasificación
      +Precio
**¿Cómo reservar?**
1. Da click en el horario y día de tu preferencia.
2. Seleciona los asientos.
3. Confirma tu reserva.
4. Si exsiste alguna promoción vigente, el sistema aplicará el decuento.

También está la pestaña _Mis reservas_
Allí podrás visualizar tus reservas con:
    -Pelicula
    -Día
    -Hora
    -Asientos
    -Total
Incluye el boton de _Cancelar reserva_. 

Por último la pestaña _Promociones_
En ella verás las promociones vigentes, con descripción.

**ADMINISTRADOR**
Al momento solo existe un administrador
Después de ingresar nombre(usuario) y contraseña, encontrarás el panel de control con las opciones:
  -_Agregar película_:
  Abrirá una ventana donde requieres:
    +Título
    +Duración
    +Clasificación
    +Género
    +Ruta de la Imagen
    +Precio del boleto
    +Horarios(estos deberán ser separados por comas, en caso de no haber funciones un día, dejar vacío)
    +"Guardar"

  -_Agregar promoción_:
  Abrirá una ventana donde requieres:
    +Título
    +Porcentaje
    +Cantidad de boletos(nuestro criterio de descuentos)
    +"Guardar"

  -_Asientos ocupados_:
  En esta ventana verás las películas y acientos reservados por día y hora

  -_Ver usuarios_:
  Lista de los usuarios registrados

  -_Estadísticas_:
  Solo se muestra la cantidad de usuarios y la cantidad de reservas

  -_Ver detalles de la película_
  Se enlistan las películas disponibles y se despliegan dos botones:
    +Ver detalles: 
      _Título
      _Duración
      _Género
      _Clasificación
      _Imagen
      _Precio
      _Horarios

    +Eliminar
      Muestra una pestaña yes/no, para eliminar la película seleccionada
      
  **AMBOS** 
  Tienen "opciones"
  Salir: cerrar el programa
  Cerrar sesión: regresa a la página inicial
