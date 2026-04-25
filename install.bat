@echo off
echo Instalando Python...
winget install --id Python.Python.3.12 --silent --show-progres
if %errorlevel% equ 0 (
    echo Python instaladon correctamente.
) else (
    echo [!] Hubo un error al instalar python 
)
echo Creando entorno virtual...
python3 -m venv env && call .\env\Scripts\activate && echo Entorno virtul creado exitosamente
echo Instalando dependencias...
pip install -r requirements.txt && echo Instalacion de dependencias completada
echo Finalizada instalacion, ya puedess usar el programa COF
pause
