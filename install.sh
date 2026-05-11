#!/bin/env bash

detect_base() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS_BASE="macos"
    elif [ -f /etc/os-release ]; then
        . /etc/os-release
        OS_BASE=$(echo "${ID_LIKE:-$ID}"  | tr '[:upper:]' '[:lower:]')
    else
        echo "Error: no se pude detectar el sistema operativo."
        exit 1
    fi
}
install_packages() {
    PAQUETES="python3 python3-pip python3-devel"
    case "$OS_BASE" in 
        *debian*)
            PAQUETES="python3 python3-pip python3-venv"
            sudo apt update && sudo apt install -y $PAQUETES
            ;;
        *arch*)
            PAQUETES="python python-pip"
            sudo pacman -Sy --noconfirm $PAQUETES
            ;;
        *fedora*)
            sudo dnf check-update && sudo dnf install -y $PAQUETES
            ;;
        *void*)
            sudo xbps-install -Sy $PAQUETES
            ;;
        *alpine*)
            PAQUETES="python3 python3-dev py3-pip"
            sudo apk update && sudo apk add $PAQUETES
            sudo apk add --no-cache ca-certificates
            ;;
        *macos*)
            echo "sistema MacOS detectado"
            echo "instalando paquetes..."
            xcode-select --install
            curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py
            ;;
        *)
            echo "Base '$OS_BASE' no soportada, favor de instalar manualmente '$PAQUETES'"
            exit 1
            ;;
    esac
}
dependencias() {
    echo "creando entrono virtual..."
    python3 -m venv env && source env/bin/activate && echo "entorno virtual creado con exito" || { echo "error al crear entorno virtual"; exit 1; }
    echo "instalando dependencias..."
    python3 -m pip install -r requirements.txt && echo "dependencias instaladas exitosamente" || { echo "error al instalar dependencias"; exit 1; }
}
detect_base
echo "ejecutar instalacion para sistemas base: $OS_BASE"
install_packages
dependencias
