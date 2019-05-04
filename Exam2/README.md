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


**Paso 4: Visualizar

![docker_ps](https://user-images.githubusercontent.com/35766585/57183909-e3e3d180-6e78-11e9-978e-69c1eee33333.png)

