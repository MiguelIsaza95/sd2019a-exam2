# Examen Parcial 2

**Integrantes:** Jonathan Arias, Marisol Giraldo y Miguel Isaza

**Códigos:**  A00315328 , A00246380 y A00054628

**Emails:**  jonathan.arias@correo.icesi.edu.co, marisol.giraldo@correo.icesi.edu.co y miguel11andres@hotmail.com

**Curso:** Sistemas Distribuidos

**Tema:** Automatización de Infraestructura

**Profesor:** Daniel Barragán

# OBJETIVOS:
- Realizar de forma autónoma el aprovisionamiento automático de infraestructura.
- Diagnosticar y ejecutar de forma autónoma las acciones necesarias para lograr infraestructuras estables
- Integrar servicios ejecutándose en nodos distintos

# APROVISIONAMIENTO INICIAL
El aprovisionamiento inicial se realizará empleando la herramienta Ansible sobre las máquinas virtuales desplegadas con vagrant.
Para ello se configura el Vagrantfile que permitirá el despliegue de 4 máquinas virtuales que cumplirán las siguientes funciones:

(1) CENTOS7 Master

(3) CENTOS7 Worker
  
**confi g.ssh.insert_key = false** => Deshabilitar el nuevo comportamiento por defecto introducido en Vagrant 1.7, para asegúrarse de que todas las máquinas Vagrant utilicen el mismo par de claves SSH.

**conf.vm.define** => indicamos el nombre de la máquina virtual.

**master.vm.network** => se configura la interfaz de red.

**master.vm.provider** => El proveedor de VirtualBox expone algunas opciones de configuración adicionales que permiten controlar con más precisión el entorno Vagrant.

**vb.customize** => VBoxManage es una utilidad que se puede usar para realizar modificaciones a las máquinas virtuales de VirtualBox desde la línea de comandos. Por ejemplo: modificar memoria, cpu's entre otros.

Cada máquina virtual tiene un **disco extra de 5 Gigabytes** para las configuraciones del sistema de ficheros distribuido **(volumen)** donde se almacenarán los datos de la base de datos. Con **¿File.exist? (firstDisk)** verifica si existe o no un archivo o directorio con el nombre firstDisk. Esta función devuelve VERDADERO si el archivo o directorio existe, de lo contrario, devuelve FALSO. Esto se realiza para cada máquina virtual.

# CONTENEDORES PARA EL BACKEND Y LA BASE DE DATOS

Se considera una práctica recomendada que un contenedor solo tenga una responsabilidad y un proceso, por lo que para nuestro examen utilizaremos al menos dos contenedores, uno para ejecutar la aplicación y otro para ejecutar la base de datos. La coordinación de estos contenedores se realizará a traves del docker-compose.

**PASO 1: Crear un Docker image para la app.**

Es necesario crear un Dockerfile en el directorio de la aplicación, que contendrá un conjunto de instrucciones que describen la imagen deseada de la app y que permiten su creación automática.
En la configuración del Dockerfile se especifica: 
* La imagen base de una imagen de Python 3.6
* Expone el puerto 5000 (para Flask)
* Crea un directorio de trabajo en el que se copiarán Requirements.txt y app.py
* E instala los paquetes necesarios y ejecuta la aplicación

![DockerFile](https://user-images.githubusercontent.com/35766585/57173656-f74f5800-6df8-11e9-87ec-d075e7bb57f2.png)

Tambien es necesario que (Flask y mysql-connector) se instalen y se ejecuten con la imagen, por lo que se creó el archivo Requirements.txt 

![Captura de pantalla de 2019-05-03 17-47-38](https://user-images.githubusercontent.com/35766585/57173748-2adeb200-6dfa-11e9-9cd7-2d9f87c4b667.png)

**PASO 2: Crear un docker-compose.yml**

Compose es una herramienta para definir y ejecutar aplicaciones Docker de múltiples contenedores. Con Compose, se utiliza un archivo YAML para configurar los servicios de la aplicación.
A continuación se muestra la configuración del archivo, docker-compose.yml, en el directorio raíz de nuestro proyecto:

![dockercomposeinicial](https://user-images.githubusercontent.com/35766585/57173394-e13f9880-6df4-11e9-911a-7692919ed00b.png)

En el archivo se puede observar, dos servicios, uno es un contenedor que expone la aplicación y el otro contiene la base de datos (db).

**build:** especifica el directorio que contiene el Dockerfile que contiene las instrucciones para construir el servicio.

**Enlaces:** vincula este servicio a otro contenedor. Esto también nos permite usar el nombre del servicio en lugar de tener que buscar la ip del contenedor de la base de datos y expresar una dependencia que determinará el orden de inicio del contenedor.

**ports:** mapeo de <Host>: <Container> ports.
  
**image:** En lugar de escribir un nuevo Dockerfile, estamos utilizando una imagen existente de un repositorio. 

**enviroment:** añade variables de entorno. Configura la contraseña para el usuario root de MySQL en este contenedor.

**ports:** Contenedor de servicio de aplicaciones utilizará el puerto 3306 para conectarse a la base de datos.

**volumes:** Cuando el contenedor se inicialice con nuestro esquema, conectaremos el directorio que contiene el script init.sql al punto de entrada de este contenedor, el cual, según la especificación, ejecuta todos los scripts .sql en el directorio dado.

**mem_lim:** Establece el limite de memoria

![dockercomposeinicial](https://user-images.githubusercontent.com/35766585/57173511-9757b200-6df6-11e9-88b9-21b398a78de0.png)


**Paso 2: Codigo Backend**

La app se conecta como root con la contraseña configurada en el archivo docker-compose. El host es el localhost por defecto, ya que el servicio de SQL se encuentra en un contenedor diferente al que ejecuta este código. Se define el nombre "db" como el nombre del servicio, y el puerto es 3306 y no 32000 ya que este código no se está ejecutando en el host.

![app_py](https://user-images.githubusercontent.com/35766585/57173206-c586c300-6df1-11e9-8b40-b03ca8896ee3.png)


**Paso 3: Ejecutar la App**

Se ejecuta con el comando **docker-compose up** e inmeditamente observar que la imagen se está construyendo, los paquetes instalados de acuerdo con los requisitos.txt, entre otros.

![docker_composeup](https://user-images.githubusercontent.com/35766585/57183900-b565f680-6e78-11e9-8a56-3c1c99ee505a.png)

De acuerdo a la siguiente pantalla se puede observar que la imagen de ambos contenedores se han constreuido y los paquetes instalados.

![port3306](https://user-images.githubusercontent.com/35766585/57183914-04139080-6e79-11e9-924a-d2a79726a9ea.png)


Se verifica mediante el comando **docker ps** la construcción de los contenedores de backend y app

![docker_ps](https://user-images.githubusercontent.com/35766585/57183909-e3e3d180-6e78-11e9-978e-69c1eee33333.png)


**Paso 4: Verficar BD**

Con el comando  **mysql --host=127.0.0.1 --port=32000 -u root -p**

![mysql](https://user-images.githubusercontent.com/35766585/57184705-eb10dc80-6e84-11e9-9562-5918701e6cce.png)

Con el  comando **show databases;** es posible verificar las bases de datos que existen en el contenedor

![showdatabases](https://user-images.githubusercontent.com/35766585/57184757-c6693480-6e85-11e9-850f-58a77de94ae8.png)

Con el comando **show tables;** es posible ver las tablas en la base de datos

![SHOWTABLES](https://user-images.githubusercontent.com/35766585/57184803-9bcbab80-6e86-11e9-8ffa-42001cc89db8.png)

Con el comando **describe favorite_colors;** evidencia los campos de la tabla

![describe](https://user-images.githubusercontent.com/35766585/57184822-0977d780-6e87-11e9-87f3-225fe7919be3.png)


**Paso 5: Visualizar**

![webchrome](https://user-images.githubusercontent.com/35766585/57184962-3927df00-6e89-11e9-9f90-038bc8456204.png)



# SOLUCIÓN PARA LA RECOLECCIÓN, CONVERSIÓN Y VISUALIACIÓN DE LOGS

**Fluentd:** Es un recolector de datos, es decir, se dedica a buscar y recoger toda la información que generan las diferentes aplicaciones de nuestro sistema.

**Elasticsearch:** Es el encargado de almacenar todos los Logs recolectados por Fluentd.

**Kibana:** Es la herramienta que me permite recibir los datos enviados por Elasticsearch, para posteriormente analizarlos y posibilitar su visualización. 

![fluentd-elasticsearch-kibana](https://user-images.githubusercontent.com/46909824/57183569-8a79a380-6e74-11e9-9a6d-1f468aaa15ae.jpg)

 
Con el archivo YAML **docker-compose.yml**, se crea e inician todos los servicios (en este caso, Apache, Fluentd, Elasticsearch, Kibana) con un solo comando.

![1](https://user-images.githubusercontent.com/46909824/57183637-813d0680-6e75-11e9-808b-eb866e5df190.png)

![2](https://user-images.githubusercontent.com/46909824/57183642-9023b900-6e75-11e9-8bc7-d11a7e1f1328.png)

La sección de **logging** del contenedor web especifica Docker Fluentd Logging Driver como un controlador de registro de contenedor predeterminado. Todos los logs del contenedor web se reenviarán automáticamente al host: puerto especificado por fluentd-address.

**Paso 1: Preparar la imagen Fluentd con su configuración + plugin**

Crear la carpeta **fluentd/Dockerfile** con el siguiente contenido, para poder utilizar la imagen oficial de Fluentd Docker oficial e instalar adicionalmente el complemento Elasticsearch.

![DockerFile fluentd](https://user-images.githubusercontent.com/46909824/57182593-79c23100-6e66-11e9-95f8-6a617ad0ccff.jpg)

En la ruta **fluentd/conf/fluent.conf** se elabora el archivo de configuración con el siguiente contenido:

![fluentd conf](https://user-images.githubusercontent.com/46909824/57182643-00770e00-6e67-11e9-9f9a-f8cd93527f58.jpg)

El primer fragmento in forward plugin se utiliza para recibir registros del controlador de registro de Docker, y el siguiente out_elasticsearch es para reenviar registros a Elasticsearch.

**Paso 2: Iniciar los Contenedores**

Se inicia los contenenedores con el comando **docker-compose up**

![docker-compose up](https://user-images.githubusercontent.com/46909824/57182693-8dba6280-6e67-11e9-8e6c-07ed2305e843.png)

Se verifica si los contenedores arrancan con el comando **docker ps**

![docker ps -a](https://user-images.githubusercontent.com/46909824/57183604-f0fec180-6e74-11e9-9888-845a6440b0a9.png)

**Paso 3: Generar Registros de Acceso HTTPD**

Para acceder a httpd y generar algunos registros de acceso, utilizamos el comando curl.

![curl](https://user-images.githubusercontent.com/46909824/57183673-fe687b80-6e75-11e9-949b-afbf82009443.png)

**Paso 4: Confirmar LOGS desde Kibana** 

Ingresar la dirección http://localhost:5601/ en el navegador. Luego se configura el index name pattern para Kibana. Se especifica fluentd-* en e Index name or pattern y se presiona Create button.

![k1](https://user-images.githubusercontent.com/46909824/57183777-826f3300-6e77-11e9-83ba-c82f752d7438.png)

![k2](https://user-images.githubusercontent.com/46909824/57183780-94e96c80-6e77-11e9-9adb-5cdee79ce407.png)

![k3](https://user-images.githubusercontent.com/46909824/57183784-9f0b6b00-6e77-11e9-989c-317eb1b22726.png)

![k4](https://user-images.githubusercontent.com/46909824/57183785-a894d300-6e77-11e9-895b-5ce3e1bfa49a.png)

![k5](https://user-images.githubusercontent.com/46909824/57183786-b0ed0e00-6e77-11e9-8a2a-a56adbb37210.png)

![k6](https://user-images.githubusercontent.com/46909824/57183788-b9dddf80-6e77-11e9-8828-2158267b7fab.png)
 
Luego se va la pestaña Discover y se verifica que los logs estan recolectados dentro de Elasticsearch + Kibana, via Fluentd.

![k 1 1](https://user-images.githubusercontent.com/46909824/57183800-d548ea80-6e77-11e9-99de-b951f86f0e37.png)

Luego aparecio la grafica con los tipos de consulta

![k1 2](https://user-images.githubusercontent.com/46909824/57183819-fad5f400-6e77-11e9-8b9d-aca2d9d59b4d.png)

Modificamos el tiempo que queriamos que refrescara por la interfaz la consultas hechas 

![k1 3](https://user-images.githubusercontent.com/46909824/57183825-1a6d1c80-6e78-11e9-8893-529882b78f75.png)

Luego realizamos varias consultas consecutivas para divisarlas con mayor detalle, con un comando por consola 

![lllll](https://user-images.githubusercontent.com/46909824/57184016-9e280880-6e7a-11e9-9db9-7784dfc1acdc.png)

![k1 4](https://user-images.githubusercontent.com/46909824/57183837-42f51680-6e78-11e9-93b2-8fc04977338e.png)

por web

![k 1 5](https://user-images.githubusercontent.com/46909824/57183921-1ee60500-6e79-11e9-8a39-0e0540115abf.png)

Las filtramos como consultas acertadas con el código 200

![k1 6](https://user-images.githubusercontent.com/46909824/57183928-37561f80-6e79-11e9-980a-f3ba5efbfff2.png)

Luego realizamos algunas consultas erróneas por consola  

![k1 7](https://user-images.githubusercontent.com/46909824/57183935-4f2da380-6e79-11e9-9535-34c98ad0fb19.png)

![k1 8](https://user-images.githubusercontent.com/46909824/57183939-5785de80-6e79-11e9-9fec-65495a0a9ce3.png)

por la web

![k1 9](https://user-images.githubusercontent.com/46909824/57183944-65d3fa80-6e79-11e9-842b-1d5517a2af83.png)

![k1 10](https://user-images.githubusercontent.com/46909824/57183949-7a17f780-6e79-11e9-9a8f-7590432b6468.png)

Verificamos que los parámetros de Limitación de memoria están establecidos con el comando

![mem](https://user-images.githubusercontent.com/46909824/57184246-615e1080-6e7e-11e9-961c-7205fa625370.png)

![mem2](https://user-images.githubusercontent.com/46909824/57184248-6ae77880-6e7e-11e9-9162-7f4cb8d7dc6e.png)


**Inconvenientes surgidos durante el examen:**

Al principio, se presentaron algunos errores dentro del Docker-compose.yml por tal motivo al acceder al servicio de Kibana, este abria pero no estaba leyendo ningun flujo del Elasticsearch que es donde se deberian guardar los Logs recolectados por el Fluentd. Realizamos varias consultas a la base de datos y por consola se observaban dichas consultas pero en Kibana no podian ver.

![e1](https://user-images.githubusercontent.com/46909824/57184178-1394d880-6e7d-11e9-8052-52eabb2dbf3a.png)

Para comprender la procedencia del error, nos dirigimos nuevamente a archivo .yml 

![e2](https://user-images.githubusercontent.com/46909824/57184185-2b6c5c80-6e7d-11e9-8e28-a044138aea5c.png)

![e3](https://user-images.githubusercontent.com/46909824/57184187-38894b80-6e7d-11e9-83a4-75336665aa1e.png)

Después de varios minutos comprendimos que estábamos construyendo la aplicación desde el servicio app y no desde web, que es el que estaba vinculado con Fluentd. 

Una vez solucionado

![e4](https://user-images.githubusercontent.com/46909824/57184192-5eaeeb80-6e7d-11e9-81ee-f68d01b79527.png)

Otro problema que ocurrió fue debido a que no ejecutamos el sistema anfitrión antes de desplegarlo

![e5](https://user-images.githubusercontent.com/46909824/57184217-e137ab00-6e7d-11e9-9504-06066ffc9134.png)

La solución propuesta por el profesor en el repositorio ds-docker

![e6](https://user-images.githubusercontent.com/46909824/57184218-f6acd500-6e7d-11e9-9a57-4c3cb32ac40f.png)

Antes ingresar el anterior comando bajamos los servicios

![e7](https://user-images.githubusercontent.com/46909824/57184222-0f1cef80-6e7e-11e9-8cd9-a184a7a45682.png)

Ingresamos la línea 

![e8](https://user-images.githubusercontent.com/46909824/57184228-1fcd6580-6e7e-11e9-8df9-8f67bd530fce.png)

Y lo volvemos a levantar

![e9](https://user-images.githubusercontent.com/46909824/57184231-2d82eb00-6e7e-11e9-8a11-898cd924239a.png)


# BIBLIOGRAFÍA


Docker Logging via EFK (Elasticsearch + Fluentd + Kibana) Stack with Docker Compose
https://docs.fluentd.org/v0.12/articles/docker-logging-efk-compose


