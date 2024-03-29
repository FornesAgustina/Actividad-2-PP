from re import I
import sqlite3
import datetime

"""
datetime.datetime.now().replace(microsecond=0).isoformat()

devuelve fecha hora actual en formato ISO8601 simple

yyyymmddThh:mm:ss

"""

class Persona:
    def __init__(self, dni, apellido, nombre='', movil=''):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.movil= movil


def ingresa_visita(persona):
    """Guarda los datos de una persona al ingresar"""
    conn = sqlite3.connect('recepcion.db')

    q = f"""SELECT dni FROM personas WHERE dni = '{persona.dni}'"""

    resu = conn.execute(q)

    if resu.fetchone():
        print("ya existe, no es necesario volver a ingresarlo.")
    else:
        q = f"""INSERT INTO personas (dni, nombre, apellido, movil)
                VALUES ('{persona.dni}',
                        '{persona.nombre}',
                        '{persona.apellido}',
                        '{persona.movil}');"""
        conn.execute(q)
        destino = input("destino> ")
    

    ingreso = datetime.datetime.now().replace(microsecond=0).isoformat()

    p = f"""INSERT INTO ingresos_egresos (dni, fechahora_in, fechahora_out, destino)
            VALUES ('{persona.dni}',
                    '{ingreso}',
                    'null',
                    '{destino}');"""
    print(p)
    print(q)
    conn.execute(p)
    conn.commit()    

    conn.close()
    
                        
    

def egresa_visita (dni):
    """Coloca fecha y hora de egreso al visitante con dni dado"""  
    conn = sqlite3.connect('recepcion.db')
   
    q = f"""SELECT fechahora_out FROM ingresos_egresos WHERE dni = '{dni}'"""
    
    resu = conn.execute(q)

    egreso = datetime.datetime.now().replace(microsecond=0).isoformat()

    if resu.fetchone():
        q = (f"""UPDATE ingresos_egresos SET fechahora_out = ('{egreso}') WHERE dni =  ('{dni}')""")  
        print(q)
        conn.execute(q)
        conn.commit()  
    conn.close()


def lista_visitantes_en_institucion ():
    """Devuelve una lista de objetos Persona presentes en la institución"""
    
    conn = sqlite3.connect('recepcion.db')
    q = f"""SELECT nombre, apellido, personas.dni, movil, destino, fechahora_in FROM personas
            INNER JOIN ingresos_egresos 
            ON personas.dni = ingresos_egresos.dni WHERE fechahora_out = 'null';"""
    r = conn.execute(q)
    conn.commit()  

    for fila in r:
        print(fila)
    conn.close()


def busca_vistantes(fecha_desde, fecha_hasta,destino, dni):
    """ busca visitantes segun criterios """
    conn = sqlite3.connect('recepcion.db')
    
    q = f"""SELECT nombre, apellido, personas.dni, movil, destino, fechahora_in, fechahora_out FROM ingresos_egresos INNER JOIN personas ON personas.dni = ingresos_egresos.dni
            WHERE fechahora_in LIKE '{fecha_desde}%' or fechahora_out LIKE '{fecha_hasta}%' or 
            destino = '{destino}' or ingresos_egresos.dni = '{dni}'"""
    
   
    r = conn.execute(q)
    conn.commit()

    for fila in r:
        print(fila)
    conn.close()


def iniciar():
    conn = sqlite3.connect('recepcion.db')

    qry = '''CREATE TABLE IF NOT EXISTS
                            personas
                    (dni TEXT NOT NULL PRIMARY KEY,
                     nombre   TEXT,
                     apellido TEXT  NOT NULL,
                     movil    TEXT  NOT NULL

           );'''

    conn.execute(qry)

    qry = '''CREATE TABLE IF NOT EXISTS
                            ingresos_egresos
                    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                     dni TEXT NOT NULL,
                     fechahora_in TEXT  NOT NULL,
                     fechahora_out TEXT,
                     destino TEXT

           );'''

    conn.execute(qry)


if __name__ == '__main__':
    iniciar()

    

   
    doc = input("Ingrese dni> ")
    apellido = input("Ingrese apellido> ")
    nombre = input("nombre> ")
    movil = input("móvil > ")

    p = Persona(doc, apellido, nombre, movil)
    ingresa_visita(p)
    

    dni = input("dni> ")
    egresa_visita(dni)

    """
    lista_visitantes_en_institucion()
    

    dni = input("dni> ")
    destino = input("destino> ")
    # (yyyymmddThh:mm:ss) --> fechahora
    fechaDesde = input("En que fecha/hora ingreso a la institución> ")
    fechaHasta = input("En que fecha/hora egreso de la institución> ")

    busca_vistantes(fechaDesde, fechaHasta, destino, dni)
    """
    
