================================
Aplicación de Canales de Twitter
================================

La aplicación de *Canales de Twitter* permite asociar una o más cuentas de twitter, con el fin de proveer una serie de 
funcionalidades como *retweets automáticos*, *tweets programados* e *inserción de hashtags*, entre otras.

El funcionamiento de la aplicación se basa principalmente en el uso de Celery_, el cual permite la ejecución de varias 
tareas simultáneas de manera asíncrona y controlada.

.. _Celery: http://www.celeryproject.org/


.. contents:: Contenido
   :depth: 2


Proyecto Django
---------------

Para la interfaz web de la aplicación se utilizó el framework Django_ (versión 1.5.5). Mediante esta aplicación el usuario puede registrar y configurar las funcionalidades de cada canal.

.. _Django: https://www.djangoproject.com/


El proyecto consta de los siguientes módulos

* **accounts**: manejo y autenticación de los canales.
* **control**: funcionalidades de control de las tareas de celery.
* **filtering**: módulo de retweets automáticos.
* **hashtags**: módulo de inserción de hashtags.
* **notifications**: notificaciones dentro del sistema.
* **scheduling**: módulo de tweets programados.
* **twitter**: interfaz con el API de twitter.


API de Twitter
--------------

El API (*Application Programming Interface*) de Twitter permite a los programadores invocar remotamente funciones de
Twitter. En el caso de la aplicación de Canales de Twitter, se requiere abrir un stream_ de un usuario para escuchar 
en tiempo real todos los mensajes que lleguen a su *timeline*, incluyendo los mensajes directos (DM). Luego de que 
un tweet pasa por el proceso de filtrado, se invoca la función update_ para enviarlo (retweet automático).

Para efectuar las conexiones al API, la aplicación utiliza Twython_, que es una biblioteca de twython que se encarga
de facilitar todos los procesos de conexión con Twitter.

.. _stream: https://dev.twitter.com/docs/streaming-apis/streams/user
.. _update: https://dev.twitter.com/docs/api/1.1/post/statuses/update
.. _Twython: https://github.com/ryanmcgrath/twython


Celery
------

Celery es una plataforma de gestión automatizada de colas de tareas. La ejecución de dichas tareas se realiza
de manera asíncrona y concurrente.

Se puede instalar desde este enlace_, o directamente usando pip:

.. code-block:: bash

    $ pip install celery
	

.. _enlace: https://pypi.python.org/pypi/celery/


Django-Celery
~~~~~~~~~~~~~

A partir de la versión 3.1 de Celery, no es requerido el paquete *django-celery* para integrar Celery con el 
framework Django. Sin embargo, es necesario para poder manipular directamente la base de datos de tareas periódicas,
lo cual es necesario para la funcionalidad de *tweets programados*.

Para instalar django-celery, seguir las instrucciones_ en la documentación oficial del paquete.

.. _instrucciones: https://pypi.python.org/pypi/django-celery


RabbitMQ
~~~~~~~~

Celery requiere interactuar con un *broker*, es decir, una plataforma que sirva la cola de mensajes. 
En este caso hemos utilizado RabbitMQ_, que es el broker por defecto. Éste puede instalarse en Debian ejecutando 
la siguiente instrucción:

.. code-block:: bash

	$ sudo apt-get install rabbitmq-server

Una vez instalado, ya el servidor debería estar ejecutándose en segundo plano. Para detener el servicio manualmente:

.. code-block:: bash

	$ sudo rabbitmqctl stop
	
Y para volver a iniciarlo:

.. code-block:: bash

	$ sudo rabbitmq-server

También puede invocarse con la opción ``-detached`` para que se ejecute en segundo plano.
	
Es necesario entonces definir en el ``settings.py`` de la aplicación, el URL del servicio de rabbitMQ: 

.. code-block:: python

	BROKER_URL = 'amqp://guest:guest@localhost:5672/'

Para más información, revisar la documentación_ de RabbitMQ.


.. _RabbitMQ: http://www.rabbitmq.com/
.. _documentación: http://www.rabbitmq.com/admin-guide.html
	

Tareas
~~~~~~

Una tarea ejecutable por Celery se define como una función con el decorador ``@task``:

.. code-block:: python

	from celery.task.base import task
	
	@task(queue="tweets", ignore_result=True)
	def send_tweet(channel_id, text):
		channel = Channel.objects.filter(screen_name=channel_id)[0]	
		twitter = Twitter(
			key=settings.TWITTER_APP_KEY,
			secret=settings.TWITTER_APP_SECRET,
			token=channel.oauth_token,
			token_secret=channel.oauth_secret)
		twitter.tweet(text)

La función anterior recibe el nombre de un canal y un texto, y simplemente instancia un objeto de la clase Twitter,
que sirve como interfaz entre la aplicación y el API de Twitter. Luego, la instrucción ``twitter.tweet(text)`` 
envía un tweet a través del API con el texto recibido.

Si quisiéramos ejecutar esta tarea desde algún punto del programa, basta con la siguiente línea, por ejemplo: 

.. code-block:: python

	send_tweet.delay('TrafficTesting4', "esto es una prueba")

Esto coloca una instancia de la tarea ``send_tweet`` en la cola "tweets" en RabbitMQ, con los argumentos específicos, 
y el *worker* correspondiente se encargará de ejecutarla.

Se especifica la opción ``ignore_results=True`` porque en el caso de la aplicación no es necesario guardar el 
resultado de la ejecución de la tarea. Además, si los resultados no se ignoran, RabbitMQ crea una cola innecesaria
por cada resultado, y nadie se encarga de limpiarla. Esto puede ocasionar una fuga de memoria con el tiempo.

Para más información acerca de la ejecución de tareas, ver la documentación oficial_.

.. _oficial: http://docs.celeryproject.org/en/latest/userguide/calling.html#guide-calling


Tareas periódicas
~~~~~~~~~~~~~~~~~

Para la ejecución de tareas periódicas, Celery cuenta con la herramienta *celerybeat*, la cual se encarga de encolar
ciertas tareas para que sean ejecutadas en intervalos de tiempo regulares, o periódicamente según algún horario definido.

Una tarea periódica se define como cualquier otra tarea (usando el decorador ``@task``), y adicionalmente incluyendo 
en ``settings.py`` la configuración de celerybeat:

.. code-block:: python

	from datetime import timedelta

	CELERYBEAT_SCHEDULE = {
		'test-every-30-seconds': {
			'task': 'test_task',
			'schedule': timedelta(seconds=30),
			'args': ('arg1', 2)
		},
	}

Esto define ``test_task`` como una tarea periódica por intervalos, ejecutándose cada 30 segundos. 
Para esto es necesario ejecutar *celerybeat* 

.. code-block:: bash

	$ python manage.py celerybeat
	
*Celerybeat* se encargará de enviar a la cola respectiva la tarea cada 30 segundos para su ejecución.

También es posible definir tareas periódicas usando un *crontab*, para definir de manera más concreta el momento
de ejecución de las tareas. Por ejemplo, podemos especificar un día de la semana y una hora.

.. code-block:: python

	CELERYBEAT_SCHEDULE = {
		# Se ejecuta los lunes a las 7:30 A.M
		'test-every-monday-morning': {
			'task': 'test_task',
			'schedule': crontab(hour=7, minute=30, day_of_week=1),
			'args': ('arg1', 2),
		},
	}
	

**Definir tareas periódicas dinámicamente**


Para la funcionalidad de envío de *tweets programados*, es necesario crear tareas periódicas definiendo horarios
dinámicamente, para esto es necesario instanciar manualmente las clases ``PeriodicTask`` y ``CrontabSchedule`` 
del módulo ``djcelery`` (*django-celery*). 

.. code-block:: python

	from djcelery.models import PeriodicTask, CrontabSchedule
	
	cron = CrontabSchedule(
		minute=30,
		hour=7,
		day_of_week='sunday,monday,friday')
	cron.save()

	ptask = PeriodicTask(
		name="scheduled_tweet_%s" % cron.id,
		task="send_tweet",
		crontab=cron,
		queue="tweets",
		kwargs=json.dumps({
			'channel_id': 'TrafficTesting4',
			'text': "ola ke ase?"}))
	ptask.save()

Puede leerse más detalle sobre las tareas periódicas en la `documentación oficial`_.


.. _documentación oficial: http://docs.celeryproject.org/en/master/userguide/periodic-tasks.html


Workers
~~~~~~~

Para que Celery ejecute las tareas definidas anteriormente, se necesita activar al menos una instancia de la clase 
*Worker*. Un worker es un servicio que se encarga de inspeccionar las colas correspondientes en el broker (RabbitMQ) 
y ejecutar concurrentemente cada una de las tareas.

En el caso de la aplicación de *Canales de Twitter*, se define una arquitectura con 3 workers.


``stream-worker1``
..................

Se encarga de gestionar la cola *streaming*, para los procesos de streaming de cada canal. 
Se inicia de la siguiente manera:

.. code-block:: bash

	$ python manage.py celery worker --autoscale=150,15 -Q streaming --hostname stream-worker1 -Ofair

Se colocó la opción ``-Ofair`` para evitar que el worker reserve más tareas de las que puede resolver en un instante
dado. Esto ocasionaba que algunos procesos de streaming no se iniciaran al activar el canal.

	
``logging-worker1``
...................

Se encarga de la cola de logging, para escritura en los archivos de bitácora:

.. code-block:: bash

	$ python manage.py celery worker --concurrency=1 -Q logging --hostname logging-worker1
	

``celery-schedule``
...................

Se encarga de atender las colas scheduling y notifications, para tweets programados y notificaciones, respectivamente.

.. code-block:: bash

    $ python manage.py celery worker --pool=gevent --autoscale=100,1 -Q scheduling,notifications --hostname celery-schedule

Workers para tareas de filtrado y tweets
........................................

Actualmente se ejecutan 6 workers para atender la cola de tweets, para garantizar un flujo constante en la resolución 
de estas tareas. Todos se invocan con una configuración como la siguiente:

.. code-block:: bash

	$ python manage.py celery worker --loglevel=ERROR --pool=gevent --autoscale=500,1 -Q tweets --hostname celery-worker1

Estos workers utilizan `gevent <http://www.gevent.org/>`_, que es una biblioteca para el manejo de concurrencia en python. 
Se requiere el uso de esta biblioteca como medida de optimización, y para evitar problemas de concurrencia 
encontrados con la configuración por defecto (multiprocessing). El parámetro "loglevel" define qué nivel de mensajes se
registran en la bitácora, actualmente se admiten únicamente errores, para evitar el crecimiento desmedido de los 
archivos de log.

Según la documentación de Celery, el número de workers óptimo debe ser no más del doble de núcleos de procesamiento de
la máquina que hospeda el servicio. Para el momento de la redacción de este documento, el servidor cuenta con 4 núcleos.
Es importante tomar en cuenta este factor en caso de hacer un cambio en la plataforma de hardware. La mayoría de los
casos, las optimizaciones a realizarse consisten en la configuración de estos workers.


======================
Información de soporte
======================

La siguiente información está destinada al manejo de configuraciones y procesos del lado de servidor, para monitoreo 
o desarrollo posterior.

Por motivos de confidencialidad, los usuarios y contraseñas correspondientes a los distintos servicios se han 
entregado en un documento aparte a quien sea responsable del soporte de sistema.

Amazon AWS
----------

Actualmente la aplicación está corriendo en un servidor provisto por el servicio AWS de Amazon. Para entrar en el 
panel de configuración, debe ingresarse el usuario y clave correspondiente en la dirección http://aws.amazon.com/es .

Esto permite el manejo de los parámetros del servicio AWS, como capacidad de cómputo de los servidores, y la 
posibilidad de suscripción a otros servicios de Amazon. También provee el acceso a una interfaz de monitoreo de 
actividad del servidor.


Arquitectura de sistema
-----------------------

La plataforma que sostiene la operatividad de la aplicación de Canales de Twitter consiste en los siguientes 
servicios fundamentales:

* Nginx
* uWSGI
* Supervisor


Nginx
~~~~~

Nginx es el servicio que recibe las solicitudes HTTP y sirve los archivos estáticos (imágenes, archivos de estilo, 
etc). La página oficial de nginx se encuentra en nginx.org.

Para reiniciar, detener o iniciar el servicio de nginx, se ejecuta el siguiente script, con la opción 
correspondiente a la acción deseada (``restart``, ``stop`` o ``start``):

.. code-block:: bash

	sudo /etc/init.d/nginx (restart|stop|start)


Los parámetros de configuración de nginx están definidos en "tweet_filter/server_config/nginx.conf".


uWSGI 
~~~~~

uWSGI es el servicio encargado de ejecutar la aplicación Django, y se integra con nginx para dar acceso externo a 
la aplicación. 

En `esta página <http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html>`_ puede verse una 
documentación acerca de cómo poner en funcionamiento un proyecto django usando nginx y uwsgi.

Los parámetros de configuración de uWSGI están definidos en "tweet_filter/server_config/marcaonline.ini".


Supervisor
~~~~~~~~~~

Supervisor es un sistema de control de procesos, y es el servicio que se encarga de mantener activos todos los 
servicios básicos, como los workers de celery y el servidor de aplicación uWSGI.

Para saber el estado de los procesos manejados por supervisor, se ejecuta la siguiente instrucción:

.. code-block:: bash

	$ sudo supervisorctl status


Para iniciar o detener algún servicio en particular, se ejecuta:

.. code-block:: bash

	$ sudo supervisorctl (stop|start) (<nombre_servicio>|all)


Los parámetros para su configuración se encuentran en "tweet_filter/server_config/supervisor.conf", esto incluye 
cada servicio disponible para su manejo.

Supervisor se encargará de mantener activos todos los servicios, y restablecer los mismos en caso de falla.

Cuando se efectúan cambios en la configuración de supervisor, éste debe reiniciarse con los siguientes comandos:

.. code-block:: bash

	sudo supervisorctl reread
	sudo supervisorctl update


Para reiniciar la aplicación por completo, se recomienda no sólo detener los servicios mediante supervisor, sino 
también hacer un *flush* de la cache (memcache) y detener todos los procesos python que queden aún ejecutándose. 
La secuencia sería la siguiente:

.. code-block:: bash

	sudo supervisorctl stop all
	sudo pkill python
	echo 'flush_all' | netcat localhost 11211
	sudo supervisorctl start all


Logging
-------

Todos los eventos relevantes a la funcionalidad de la aplicación son registrados en el log ubicado en 
"tweet_filter/server_logs/dev/twitter-all.log". En este archivo se registra cada tweet de entrada por canal 
y el resultado del proceso de filtrado (tweet bloqueado o enviado exitosamente). Para monitorear el log en 
tiempo real, se puede usar la herramienta ``tail`` de unix, posiblemente filtrando con ``egrep``:

.. code-block:: bash

	$ tail -f twitter-all.log | egrep "trafficMIRANDA"

Pueden encontrarse en el mismo directorio de logs, otras bitácoras concernientes al funcionamiento de celery, 
útiles en caso de falla.

La configuración de logging se encuentra en el archivo principal de configuración del proyecto Django 
("tweet_filter/tweetfilter/tweetfilter/settings/common.py"). Para entender el mecanismo de bitácoras de Django, 
es necesario referirse a la `documentación oficial <https://docs.djangoproject.com/en/dev/topics/logging/>`_.
