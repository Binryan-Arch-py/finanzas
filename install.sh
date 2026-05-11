#!/bin/env bash

detectar_sudo() {
    if command -v sudo >/dev/null 2>&1; then
        SUDO="sudo"
    else
        SUDO=""
    fi
}

detect_base() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS_BASE="macos"
    elif [ -n "$TERMUX_VERSION" ]; then
        OS_BASE="termux"
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
            PAQUETES="python3-dev python3 python3-pip python3-venv build-essential"
            $SUDO apt update && $SUDO apt install -y $PAQUETES
            ;;
        *arch*)
            PAQUETES="python python-pip base-devel"
            $SUDO pacman -Sy --noconfirm $PAQUETES
            ;;
        *fedora*)
            $SUDO dnf check-update && $SUDO dnf install -y $PAQUETES && $SUDO dnf groupinstall "Development Tools"
            ;;
        *void*)
            $SUDO xbps-install -Sy $PAQUETES base-devel
            ;;
        *alpine*)
            PAQUETES="python3 python3-dev py3-pip build-base"
            $SUDO apk update && $SUDO apk add $PAQUETES
            $SUDO apk add --no-cache ca-certificates
            ;;
        *termux*)
            PAQUETES="python python-dev build-essential clang"
            pkg update && pkg install $PAQUETES
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

detectar_sudo
detect_base
echo "ejecutar instalacion para sistemas base: $OS_BASE"
install_packages
dependencias
