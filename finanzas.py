import sqlite3
from datetime import date
import time
import os

db_dir = 'db'
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
conexion = sqlite3.connect(os.path.join(db_dir, 'finanzas.db'))
cursor = conexion.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS finanzas (
    id INTEGER PRIMARY KEY,
    fecha TEXT,
    dinero REAL,
    descripcion TEXT
    )
''')
while True:
    print("\nBIENVENIDO A LA CALCULADORA DE FINANZAS")
    x = input("quieres registrar un movimiento? (s/n) ")
    if x == 's':
        while True:
            monto = int(input("ingresa el monto que quieres registrar: "))
            conf = input(f"ingresaste ${monto}, es correcto? (s/n) ")
            if conf == 's': break
        hoy = date.today()
        descripcion = input("ingresa la descripcion del gasto ")
        cursor.execute("INSERT INTO finanzas (fecha, dinero, descripcion) VALUES (?, ?, ?)", (str(hoy), monto, descripcion))
        conexion.commit()
        print("movimiento registrado")
        salir = input("\nquieres salir del programa? (s/n) ")
        if salir == 's': break
    elif x == 'n':
        y = input("quieres ver los movimientos regstrados? (s/n) ")
        if y == 's':
            print("1 = ver todos los movimientos \n2 = seleccionar por fecha")
            z = input()
            if z == '1':
                cursor.execute("SELECT * FROM finanzas")
                filas = cursor.fetchall()
                for fila in filas: print(fila)
            elif z == '2':
                fecha_x = input("ingresa la fecha de la que quieres conocer los movimientos (ejemplo: 2026-03-20) ")
                cursor.execute("SELECT * FROM finanzas WHERE fecha = ?", (fecha_x,))
                filas = cursor.fetchall()
                for fila in filas: print(fila)
        elif y == 'n': break
    else: print("ERROR, OPCION NO DISPONIBLE")
