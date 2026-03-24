import sqlite3
from datetime import date
import os

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
            fecha TEXT,
            monto REAL,
            descripcion TEXT
            )
        ''')


    def insertar(self, fecha, dinero, descripcion):
        self.cursor.execute("INSERT INTO finanzas (fecha, monto, descripcion) VALUES (?, ?, ?)", (str(fecha), dinero, descripcion))
        self.conexion.commit()

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


    def cerrar(self):
        self.conexion.close()


class Operaciones:
    def __init__ (self, base):
        self.base = base


    def movimiento(self):
        while True:
            while True:
                try:
                    monto = float(input("ingresa el monto que quieres registrar: "))
                except ValueError:
                    print("ERROR, ingresa solo numeros")
                else:
                    break
            confirm = input(f"ingresaste ${monto}, es correcto? (s/n) ")
            if confirm == 's':
                break
        fecha = date.today()
        descripcion = input("ingresa la descripcion del gasto: ")
        self.base.insertar(fecha, monto, descripcion)


    def ver_todo(self):
        filas = self.base.ver_todos()
        for fila in filas:
            print(fila)


    def ver_fecha(self):
        dia = input("ingresa la fecha de la que quieres conocer los movimientos (ejemplo: 2026-03-21) ")
        filas = self.base.ver_fechas(dia)
        for fila in filas:
            print(fila)


    def ver_mes(self):
        while True:
            try:
                anio = int(input("ingresa el anio: "))
                mes = int(input("ingresa el mes: "))
            except ValueError:
                print("ERROR, vuelve a intentarlo/n")
            else:
                break
        inicio = date(anio, mes, 1)
        if mes == 12:
            fin = date(anio + 1, 1, 1)
        else:
            fin = date(anio, mes + 1, 1)
        filas = self.base.ver_meses(inicio, fin)
        for fila in filas:
            print(fila)


base_datos = Database('db')
operacion = Operaciones(base_datos)
def main(db, op):
    db.conectar()
    db.tabla()
    print("\nBIENVENIDO A LA CALCULADORA DE FINANZAS")
    print("que quieres hacer? \n1 = registrar movimiento \n2 = ver todos los movimientos \n3 = ver movimeintos por fecha \n4 = ver movimientos por mes")
    modo = input()
    if modo == '1':
        op.movimiento()
        print("movimiento registrado")
    elif modo == '2':
        op.ver_todo()
    elif modo == '3':
        op.ver_fecha()
    elif modo == '4':
        op.ver_mes()
    else:
        print("opcion no disponible")
    db.cerrar()


if __name__ == "__main__":
    main(base_datos, operacion)
