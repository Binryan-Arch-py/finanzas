# <p align="center"> <img src="logo.png" width="100"> <br> **COF** </p>

programa que ayuda a gestionar las finanzas del usuario registrando todos los movimintos financieros que realice

## Significado
El acronimo *C.O.F.* significa **Control de Operaciones Financieras**

## Descripcion
Es un porgrama pensado para ayudar al usuario a gestionar su dinero guardando lso movimientos economicos que realice el usuario guardandolos en una base de datos local y registrando la fecha, asi contando tambien con funciones para ver los moviientos realizados y pudiendo crear un archivo de excel para poder visualizar los datos de forma mas visual

## Funciones
* **SQLite** para la base de datos
* **OS** para crear la carpeta
* **datetime** para poder guardar la fecha
* **POO** codigo hecho utilizando la POO (programacion orientada a objetos)
* **Pandas** para crear el excel

## Tecnologias
* **Lenguaje:** Python
* **Sistema:** Arch Linux
* **Editor:** Neovim

## Como ejecutar
### instalar necesario:
deberas tener instalado **python** **python-pip** y **python-devel** (en ocasiones ese ultimo suele venir junto con python), puedes instalarlos con estos comandos
* **Arch** y derivados: ``sudo pacman -S python python-pip``
* **Debian** y derivados: ``sudo apt install python3 python3-pip python3-venv``
* **Fedora** y derivados: ``sudo dnf groupinstall "Development Tools" && sudo dnf install python3-devel``
* **MacOS:** ``xcode-select --install``
* **Windows:** descarga e instala python desde python.org
### configuracion de entorno:
ejecuta los siguientes comandos segun tu sistema:
* ``python3 -m venv venv``
* **Linux/MacOS:** ``source venv/bin/activate``
* **Windows:** ``.\venv\Scripts\activate
### instalar dependencias
pip install -r requirements.txt

### ejecutar:
para ejecutar el programa solo ejecuta esto:
python3 cof.py

## Desarrollado por *Bryan David Pérez Arana*
