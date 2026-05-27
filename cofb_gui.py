#################################################################################
# Copyright (C) 2026 Binryan-void
#
# Este programa es software libre: puedes redistribuirlo y/o modificarlo
# bajo los terminos de la Licencia Publica General GNU publicada por la 
# Free Software Foundation, ya sea la version 3 de la Licencia o 
# (a tu eleccion) cualquier version posterior
#
# Este programa se distribuye con la esperanza de que sea util, pero 
# SIN GARANTIA ALGUNA; ni siquiera garantia implicita de 
# MERCANTILIDAD o APTITUD PARA UN PROPOSITO DETERMINADO.
# Consulte la Licencia Publica General GNU para obtener mas detalles.
#
# Deberias haber recibido una copia de la Licencia Publica General GNU 
# junto con este programa. Si no es asi, consulta <https://www.gnu.org/licenses/>.
##################################################################################

import sqlite3
from datetime import date
import os
import pandas as pd
import re
import tkinter as tk
from tkinter import messagebox

class Database:
    def __init__(self, carpeta):
        self.carpeta = carpeta
        self.conexion = None
        self.cursor = None
        self.conectar()
        self.tabla()


    def conectar(self):
        if not os.path.exists(self.carpeta):
            os.makedirs(self.carpeta)
        self.conexion = sqlite3.connect(os.path.join(self.carpeta, 'finanzas.db'))
        self.cursor = self.conexion.cursor()


    def tabla(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS finanzas (
            id INTEGER PRIMARY KEY,
            user TEXT,
            fecha TEXT,
            monto REAL,
            descripcion TEXT
            )
        ''')


    def insertar(self, fecha, dinero, descripcion):
        if (not isinstance(fecha, date) 
            or not isinstance(dinero, float) 
            or not isinstance(descripcion, str)
        ):
            messagebox.showerror("Error de Formato", "El formato de los datos es incorrecto")
        
        try:
            self.cursor.execute("INSERT INTO finanzas (fecha, monto, descripcion) VALUES (?, ?, ?)", (str(fecha), dinero, descripcion))
            self.conexion.commit()
            messagebox.showerror("Exito", "Movimiento registrado exitosamente")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error de Duplicado", f"Ocurrio un error de duplicado de los datos \nEl error es {e}")

    def ver_todos(self):
        self.cursor.execute("SELECT * FROM finanzas")
        filas = self.cursor.fetchall()
        return filas


    def ver_fechas(self, dia):
        self.cursor.execute("SELECT * FROM finanzas WHERE fecha = ?", (dia,))
        filas = self.cursor.fetchall()
        return filas


    def ver_meses(self, inicio, fin):
        self.cursor.execute("SELECT * FROM finanzas WHERE fecha >= ? AND fecha < ?", (str(inicio), str(fin)))
        filas = self.cursor.fetchall()
        return filas


    def mes_total(self, inicio, fin):
        self.cursor.execute("SELECT SUM(monto) FROM finanzas WHERE fecha >= ? AND fecha < ?", (str(inicio), str(fin)))
        total = self.cursor.fetchone()[0] or -0 
        return total


    def excel(self):
        data = pd.read_sql_query("SELECT * FROM finanzas", self.conexion)
        for col in data.select_dtypes(include=['object']):
            data[col] = data[col].apply(lambda x: re.sub(r'[\x00-\x1f\x7f-\x9f]', '', str(x)) if x else x)
        data.to_excel('finanzas.xlsx', index=False, engine='openpyxl')


    def usuario(self, usuario):
        self.cursor.execute("""
            UPDATE finanzas 
            SET user = ? 
            WHERE id = 1
        """, (usuario,))
        self.conexion.commit()


    def ver_usuario(self):
        self.cursor.execute("SELECT user FROM finanzas WHERE id = 1")
        usuario = self.cursor.fetchone()
        if usuario:
            return usuario[0]
        return ""


    def comp_usuario(self):
        self.cursor.execute("SELECT 1 FROM finanzas WHERE id = 1")
        resultado = self.cursor.fetchone()
        if resultado is None or resultado[0] is None or resultado[0] == '':
            return True
        else:
            return False


    def cerrar(self):
        self.conexion.close()


class Ventana:
    def __init__(self, operaciones, base_datos):
        self.op = operaciones 
        self.db = base_datos
        self.root = self.root()
        self.seleccion = None
        self.continuar = tk.BooleanVar(value=False)


    def root(self):
        root = tk.Tk()
        root.title("Control de Operaciones Financieras Basicas")
        root.geometry("400x250")
        return root


    def menu(self):
        self.esperar = tk.BooleanVar(value=False)
        self.seleccion = (None)

        def devolver_seleccion():
            self.seleccion = seleccion.get()
            self.esperar.set(True)

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu Principal", menu=menu)

        bienvenida = tk.Label(self.root, text=f"BIENVENIDO A LA CALCULADORA DE FINANZAS {self.db.ver_usuario()}", font=("Arial", 15))
        bienvenida.pack(pady=10)
        pregunta = tk.Label(self.root, text="que quieres hacer", font=("Arial", 12))
        pregunta.pack(pady=15)

        opciones = [
            "registrar movimiento",
            "ver todos los movimientos",
            "ver movimientos por fecha",
            "ver movimientos por mes",
            "ver total de un mes",
            "pasar datos a excel",
            "cambiar usuario",
            "salir"
        ]
        seleccion = tk.StringVar(value="1")

        for indice, opcion in enumerate(opciones):
            indice += 1 
            if opcion != "salir":
                radio = tk.Radiobutton(
                    self.root,
                    text=opcion,
                    variable=seleccion,
                    value=str(indice),
                )
            else:
                radio = tk.Radiobutton(
                    self.root,
                    text=opcion,
                    variable=seleccion,
                    value="0" 
                )
        radio.pack(anchor=tk.W, padx=20, pady=10)

        tk.Frame(self.root, height=10).pack()
        boton = tk.Button(self.root, text="Aceptar", command=devolver_seleccion)
        boton.pack(pady=10)
        self.root.wait_variable(self.esperar)
        return self.seleccion


    def movimiento(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Registrar Movimiento", menu=menu)
        self.mov_monto()

        
    def mov_monto(self):
        for widget in self.root.winfo_children():
            if widget.winfo_name() == "menu":
                continue
            else:
                widget.destroy()
        
        def validar_monto():
            try:
                float(self.monto.get())
            except ValueError:
                messagebox.showerror("ERROR", "Ingresa unicamente numeros")
            else:
                self.mov_confirmacion()


        pedir_monto = tk.Label(self.root, text="Ingresa el monto que quieres registrar:", font=("Arial", 12))
        pedir_monto.pack(pady=10)
        self.monto = tk.Entry(self.root)
        self.monto.pack(pady=10)
        self.enviar = tk.Button(self.root, text="Enviar", command=validar_monto)
        self.enviar.pack(pady=10)


    def mov_confirmacion(self):
        self.enviar.destroy()

        confirmacion = tk.Label(self.root, text=f"Ingresaste {self.monto.get()}", font=("Arial", 12))
        confirmacion.pack(pady=10)
        self.aceptar = tk.Button(self.root, text="Aceptar", command=self.mov_descripcion)
        self.aceptar.grid(row=0, column=0, padx=10, pady=10)
        self.volver = tk.Button(self.root, text="Volver", command=self.mov_monto)
        self.volver.grid(row=0, column=1, padx=10, pady=10)


    def mov_descripcion(self):
        self.aceptar.destroy()
        self.volver.destroy()

        pedir_descripcion = tk.Label(self.root, text="Ingresa una descripcion:", font=("Arial", 12))
        pedir_descripcion.pack(pady=10)
        self.descripcion = tk.Entry(self.root)
        self.descripcion.pack(pady=10)
        self.enviar = tk.Button(self.root, text="Enviar", command=self.mov_registrar)


    def mov_registrar(self):
        self.continuar.set(False)
        def volver():
            self.continuar.set(True)

        self.enviar.destroy()
        monto = float(self.monto.get().strip())
        descripcion = self.descripcion.get().strip()
        hoy = date.today()

        self.db.insertar(hoy, monto, descripcion)
        volver_menu = tk.Button(self.root, text="Continuar", command=volver)
        volver_menu.pack(side=tk.BOTTOM, pady=(50, 10), padx=(40, 5))
        # funcion de limpiar pantalla cunado este


    def ver_todo(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver Todos Los Movimientos", menu=menu)

        self.continuar.set(False)
        def volver():
            self.continuar.set(True)
        filas = self.db.ver_todos()
        for fila in filas:
            datos = tk.Label(self.root, text=fila, font=("Arial", 12))
            datos.pack(pady=10)
        volver_menu = tk.Button(self.root, text="Continuar", command=volver)
        volver_menu.pack(side=tk.BOTTOM, pady=(50, 10), padx=(40, 5))
