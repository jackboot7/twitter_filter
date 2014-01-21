=========================================================
Requerimientos Aplicación de Canales de Twitter (Fase 1)
=========================================================
-------------------------------------
Módulos funcionales de la aplicación.
-------------------------------------

* **Gestión de usuarios**: Se refiere al manejo de usuarios dentro de la aplicación. Debe ser posible definir 
  distintos roles por usuario.

* **Tweets por posteo automático** ('Posteo automático'): El sistema hace tweets automáticamente basándose en un conjunto de 
  reglas defininadas por el usuario. Esta configuración incluye filtros, bloqueo de usuarios/contenido, etc.

* **Tweets por posteo programado** ('Parrilla de posteo'): Permite al usuario hacer la programación de un tweet para ser enviado luego.

* **Tweets por posteo manual** ('Scanner'):

* **Gestión de Followers**: Gestión automática de follows/unfollows; búsqueda de followers por canal, 
  ficha de cada follower.

* **Notificaciones**: Notificaciones de la actividad del sitio.

* **Reportes**: Reportes de cada funcionalidad de la aplicación.

* **Dashboard**: Página de inicio por canal. Debe presentar información resumida de los distintos módulos de la aplicación.


---------------------
Gestión de Usuarios
---------------------

Módulo para el registro y gestión de usuarios de la aplicación.

++++++++++++++++++
Roles de usuario
++++++++++++++++++
Un usuario puede tener uno de los siguientes 3 roles:

    - Administrador: Administrador general de la aplicación, tiene acceso a todos los datos de todos los usuarios y canales definidos.
      Usa la interfaz de adminstrador de Django, adaptada para su uso.

    - Cliente: Cliente de la apicación. Define y registra canales, puede administrar toda la funcionalidad para el canal, ver reportes y notificaciones, y definir
      usuarios colaboradores para esa cuenta. La cantidad de canales y funcionalidad dependerá siempre del plan que haya comprado el cliente.

    - Colaborador: Usuarios con vistas limitadas, son cuentas creadas por el «Cliente». El «Cliente» debe configurar qué limitaciones tiene cada uno de sus colaboradores.
      La cantidad de colaboraores de cada «Cliente» dependerá del plan que se haya comprado.

++++++++++++++++++++++++++++++++++++++
Requerimientos funcionales del módulo
++++++++++++++++++++++++++++++++++++++

- Como `usuario`, quiero poder registrarme en el sistema.
- Como `usuario`, puedo tener diferentes roles en la aplicación.
- Como `usuario`, puedo acceder a distintas funcionalidades dependiendo de mi rol.
- Como `usuario`, tengo un perfil básico en la aplicación el cual puedo visitar.
- Como `usuario`, puedo actualizar datos en mi perfil.
- Como `usuario`, puedo cambiar mi contraseña.

- Como `«Cliente»`, 
    + puedo agregar uno (o más) cuentas de Twitter para ser gestionada desde la aplicación.
    + puedo ver todos los módulos funcionales de la aplicación.
    + puedo configurar todos los módulos funcionales de la aplicación.
    + puedo agregar colaboradores con su dirección de correo/contraseña.
    + puedo ver el perfil y la actividad en la aplicación de cada uno de mis colaboradores.
    + puedo configurar los módulos con los que cada «Colaborador» puede interactuar.

- Como `«Colaborador»`, tengo acceso a los módulos definidos por el `«Cliente»` para mi.

- Como `«Administrador»`,
    + tengo acceso total a las distintos módulos de la aplicación.


-------------------------------
Tweets por posteo automático
-------------------------------
Se define un módulo de posteo automático `por canal`.

Este módulo define una funcionalidad de bloqueo automático de tweets basado en las siguientes condiciones:

    - El tweet contiene palabras en la lista de filtros.
    - El tweet es repetido.
    - El contenido del tweet se puede identificar como spam (¿?)

Este módulo puede bloquear automáticamente followers del canal basado en las siguientes condiciones:

    - El follower del canal envía mensaje en ráfaga/spam.
    - El follower se encuentra en una lista de bots.

El módulo puede modificar el contenido de los tweets antes del RT:

    - Solo se permitirá la primera palabra de una frase en mayúsculas.
    - Si una palabra (o frase) está en la lista de equivalentes, se hará el cambio correspondiente.

++++++++++++++++++++++++++++++++++++++
Requerimientos funcionales del módulo
++++++++++++++++++++++++++++++++++++++

- Como `usuario`, puedo agregar palabras a la lista de disparadores del canal.
- Como `usuario`, puedo agregar palabras a la lista de filtradas del canal.
- Como `usuario`, puedo agregar pares de palabras (o frases) en una lista de "equivalentes".
- Como `usuario`, puedo agregar palabras a una lista de palabras para enfatizar.
    + El énfasis se hace colocando la palabra en mayúsculas y entre tres paréntesis.
- 



-------------------------------
Tweets por posteo programado
-------------------------------
Se define un módulo de posteo programado `por canal`. Se puede programar un tweet para ser enviado
a futuro, en una fecha/hora específica, o de manera cíclica (ej. todos los jueves a las 3 p.m.)

Este módulo está disponible para el `«Cliente»`  y para los `«Colaboradores»` que éste elija.


++++++++++++++++++++++++++++++++++++++
Requerimientos funcionales del módulo
++++++++++++++++++++++++++++++++++++++

- Como `«Cliente»`, puedo definir bloques de tiempo a nivel general por aplicación.
- Como `«Cliente»`, puedo editar o eliminar bloques de tiempo definidos anteriormente.
- Como `«Cliente»`, puedo activar o desactivar bloques de tiempo para un canal específico.
- Como `usuario`, puedo agregar un tweet para ser enviado a futuro.
- Como `usuario`, puedo editar la configuración de un tweet programado anteriormente.
- Como `usuario`, puedo borrar/cancelar el envío de un tweet programado anteriormente.
- Como `usuario`, puedo ver una lista de tweets programados para enviarse.
- Como `usuario`, puedo ver una lista de tweets programdos enviados anteriormente (historial)

----------------------
Gestión de Followers
----------------------
El módulo de gestión de followers tiene un componente automático y un componente manual.

El componente automático debe encargarse de seguir y dejar de seguir «usuarios en Twitter»,


++++++++++++++++++++++++++++++++++++++
Requerimientos funcionales del módulo
++++++++++++++++++++++++++++++++++++++

- Como `usuario`, quiero listar los seguidores de una cuenta de mis cuentas de twitter (canal).
- Como `usuario`, quiero crear listas de seguidores.
- Como `usuario`, quero crear una lista de followers bloqueados a nivel de aplicación.
- Como `usuario`, quiero buscar «usuarios de Twitter» por ubicación geográfica (en la bio).
- Como `usuario`, quiero ver una ficha de cada follower de mi canal.
    + La ficha de un follower debe mostrar la información básica del mismo (cantidad de tweets, número de seguidores, biografía, ubicación, etc).
    + La ficha de un follower muestra si este se enecuentra en alguna lista.
- 

----------------------
Reportes
----------------------

- Como `«Cliente»`, quiero ver un conjunto de reportes con gráficos a partir de los datos sacados de cada módulo funcional de la aplicación.

---------------------
Dashboard (Monitor)
---------------------

- Como `usuario`, quiero ver un resumen de la actividad de los distintos módulos activos para cada canal.
- Como `usuario`, quiero ver este resumen presentado de forma legible.
- Como `usuario`, quiero tener acceso a los módulos que generaron la información desde el monitor.
