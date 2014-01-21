================================
Aplicaci�n de Canales de Twitter
================================

La aplicaci�n de *Canales de Twitter* permite asociar una o m�s cuentas de twitter, con el fin de proveer una serie de 
funcionalidades como *retweets autom�ticos*, *tweets programados* e *inserci�n de hashtags*, entre otras.

El funcionamiento de la aplicaci�n se basa principalmente en el uso de Celery_, el cual permite la ejecuci�n de varias 
tareas simult�neas de manera as�ncrona y controlada.

.. _Celery: http://www.celeryproject.org/

Contenido
=========

* Proyecto Django
* API de Twitter
* Celery - RabbitMQ
* Configuraci�n del servidor

Proyecto Django
---------------

Para la interfaz web de la aplicaci�n se utiliz� el framework Django_ (versi�n 1.5.5). Mediante esta aplicaci�n el usuario puede
registrar y configurar las funcionalidades de cada canal.

.. _Django: https://www.djangoproject.com/

Estructura del proyecto
~~~~~~~~~~~~~~~~~~~~~~~

El proyecto consta de los siguientes m�dulos

* **accounts**: manejo y autenticaci�n de los canales.
* **control**: funcionalidades de control de las tareas de celery.
* **filtering**: m�dulo de retweets autom�ticos.
* **hashtags**: m�dulo de inserci�n de hashtags.
* **notifications**: notificaciones dentro del sistema.
* **scheduling**: m�dulo de tweets programados.
* **twitter**: interfaz con el API de twitter.

API de Twitter
--------------

El API (*Application Programming Interface*) de Twitter permite a los programadores invocar remotamente funciones de
Twitter. En el caso de la aplicaci�n de Canales de Twitter, se requiere abrir un stream_ de un usuario para escuchar 
en tiempo real todos los mensajes que lleguen a su *timeline*, incluyendo los mensajes directos (DM). Luego de que 
un tweet pasa por el proceso de filtrado, se invoca la funci�n update_ para enviarlo (retweet autom�tico).

Para efectuar las conexiones al API, la aplicaci�n utiliza Twython_, que es una biblioteca de twython que se encarga
de facilitar todos los procesos de conexi�n con Twitter.

.. _stream: https://dev.twitter.com/docs/streaming-apis/streams/user
.. _update: https://dev.twitter.com/docs/api/1.1/post/statuses/update
.. _Twython: https://github.com/ryanmcgrath/twython

Celery
------

Celery es una plataforma de gesti�n automatizada de colas de tareas. La ejecuci�n de dichas tareas se realiza
de manera as�ncrona y concurrente.

Se puede instalar desde este enlace_, o directamente usando pip:

.. code-block:: bash

    $ pip install celery
	

.. _enlace: https://pypi.python.org/pypi/celery/

RabbitMQ
~~~~~~~~

Celery requiere interactuar con un *broker*, es decir, una plataforma que sirva la cola de mensajes. 
En este caso hemos utilizado RabbitMQ_, que es el broker por defecto. �ste puede instalarse en Debian ejecutando 
la siguiente instrucci�n:

.. code-block:: bash

	$ sudo apt-get install rabbitmq-server

Una vez instalado, ya el servidor deber�a estar ejecut�ndose en segundo plano. Para detener el servicio manualmente:

.. code-block:: bash

	$ sudo rabbitmqctl stop
	
Y para volver a iniciarlo:

.. code-block:: bash

	$ sudo rabbitmq-server

Tambi�n puede invocarse con la opci�n ``-detached`` para que se ejecute en segundo plano.
	
Es necesario entonces definir en el ``settings.py`` de la aplicaci�n, el URL del servicio de rabbitMQ: 

.. code-block:: python

	BROKER_URL = 'amqp://guest:guest@localhost:5672/'

Para m�s informaci�n, revisar la documentaci�n_ de RabbitMQ.


.. _RabbitMQ: http://www.rabbitmq.com/
.. _documentaci�n: http://www.rabbitmq.com/admin-guide.html
	

Tareas
~~~~~~

Una tarea ejecutable por Celery se define como una funci�n con el decorador ``@task``. Por ejemplo:

.. code-block:: python

	from celery.task.base import task
	
	@task(queue="tweets", ignore_result=True)
	def schedule_tweet(channel_id, text):
		channel = Channel.objects.filter(screen_name=channel_id)[0]
		if channel.scheduling_enabled:
			twitter = Twitter(
				key=settings.TWITTER_APP_KEY,
				secret=settings.TWITTER_APP_SECRET,
				token=channel.oauth_token,
				token_secret=channel.oauth_secret)
			twitter.tweet(text)

La funci�n anterior recibe el nombre de un canal y un texto, y simplemente instancia un objeto de la clase Twitter,
el cual es la interfaz entre la aplicaci�n y el API de Twitter. Posteriormente, env�a un tweet con el texto recibido.

Si quisi�ramos ejecutar esta tarea desde alg�n punto del programa, basta con la siguiente l�nea: 

.. code-block:: python

	schedule_tweet.delay('TrafficTesting4', "esto es una prueba")

Esto coloca una instancia de la tarea ``schedule_tweet`` en la cola "tweets" en RabbitMQ, 
y el *worker* correspondiente se encargar� de ejecutarla. Sin embargo, usaremos esta tarea para ejemplificar el uso 
de *celerybeat* (tareas peri�dicas).

Para m�s informaci�n acerca de la ejecuci�n de tareas, ver la documentaci�n oficial_.


.. _oficial: http://docs.celeryproject.org/en/latest/userguide/calling.html#guide-calling


Tareas peri�dicas
~~~~~~~~~~~~~~~~~

Para la ejecuci�n de tareas peri�dicas, Celery cuenta con la herramienta *celerybeat*, la cual se encarga de encolar
ciertas tareas para que sean ejecutadas en intervalos de tiempo dados, o peri�dicamente seg�n alg�n horario definido.

Una tarea peri�dica se define como cualquier otra tarea (usando el decorador ``@task``), y adicionalmente

.. code-block:: python

	# Ac� va el c�digo de la clase ScheduledTweet
	
Workers
~~~~~~~

Para que Celery ejecute las tareas definidas anteriormente, se necesita activar al menos una instancia de la clase 
*Worker*. Un worker es un servicio que se encarga de inspeccionar las colas correspondientes en el broker (RabbitMQ) 
y ejecutar concurrentemente cada una de las tareas.

En el caso de la aplicaci�n de *Canales de Twitter*, se define una arquitectura con 3 workers.

``stream-worker1``
..................

Se encarga de gestionar la cola *streaming*, para los procesos de streaming de cada canal. 
Se inicia de la siguiente manera:

.. code-block:: bash

	$ python manage.py celery worker --autoscale=150,15 -Q streaming --hostname "stream-worker1" -Ofair

``logging-worker1``
...................

Se encarga de la cola de logging, para escritura en los archivos de bit�cora:

.. code-block:: bash

	$ python manage.py celery worker --concurrency=1 -Q logging --hostname logging-worker1
	
``celery-worker1``
..................

Se encarga de ejecutar las tareas en las colas *tweets*, *scheduling* y *notifications*. 
Este worker utiliza *gevent*, que es una biblioteca para el manejo de concurrencia en python. 
Se requiere el uso de esta biblioteca como medida de optimizaci�n, y para evitar problemas de concurrencia 
encontrados con la configuraci�n por defecto (multiprocessing):

.. code-block:: bash

	$ python manage.py celery worker --pool=gevent --autoscale=300,20 -Q tweets,scheduling,notifications 
	--hostname celery-worker1