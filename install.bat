o off
echo Instalando Python...
winget install --id Python.Python.3.12 --silent --show-progress

:: Refrescar variables de entorno para esta sesión (truco para que reconozca python)
set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python312\;%LOCALAPPDATA%\Programs\Python\Python312\Scripts\"

if %errorlevel% equ 0 (
    echo Python instalado correctamente.
) else (
	echo [!] Hubo un error al instalar python o ya estaba instalado.
)

echo Creando entorno virtual...
python -m venv env && call .\env\Scripts\activate && echo Entorno virtual creado exitosamente.

echo Instalando dependencias...
pip install -r requirements.txt && echo Instalacion de dependencias completada.

echo Finalizada instalacion, ya puedes usar el programa COF.
pause

