from distutils.command.build_scripts import build_scripts
from re import T
import sqlite3
from types import NoneType

from pymysql import NULL

class ProgramaPrincipal:

    def menu(self):
        while True:
            print("Menu de opciones")
            print("0- Salir de menu")
            print("1- Cargar Monopatin")
            print("2- Modificar Monopatin")
            print("3- Borrar Monopatin")
            print("4- Cargar disponibilidad")
            print("5- Mostrar lista ordenada")
            print("6- Actualizar al precio del dolar")
            print("7- Mostrar lista antes de actualizacion del dolar")
            print("8- Mostrar lista actualizada al valor del dolar")
            print("9- Mostrar lista previa a una fecha")

            nro = int(input("Por favor ingrese un número \n"))

            if nro == 1:
                marca = input("Por favor ingrese la marca del monopatin: ")
                precio = input("Por favor ingrese el precio del monopatin: ")
                cantidadDisponibles = input("Por favor ingrese la cantidad de unidades disponibles: ")
                potencia = input("Por favor ingrese la potencia del monopatin: ")
                color = input("Por favor ingrese el color del monopatin: ")
                fecha = input("Por favor ingrese la fecha del ultimo precio del monopatin: ")
                nuevo_monopatin = Monopatin(marca,precio, cantidadDisponibles,potencia, color, fecha)
                nuevo_monopatin.cargar_monopatin()
            if nro ==2:
                marca = input("Por favor ingrese el nombre de la marca: ")
                precio = input("Por favor ingrese el nuevo precio: ")
                monopatin_a_modificar=Monopatin(marca,precio)
                monopatin_a_modificar.modificar_monopatin()
            if nro ==3:
                marca = ""
                monopatin_a_eliminar=Monopatin(marca)
                monopatin_a_eliminar.borrar_monopatin()
            if nro == 4:
                marca = input("Por favor ingrese la marca del monopatin: ")
                dispo_monopatin = Monopatin(marca)
                dispo_monopatin.disponibilidad_monopatin()
            if nro == 5:
                marca=0
                listaordenada_monopatin = Monopatin(marca)
                listaordenada_monopatin.lista_monopatin()
            if nro == 6:
                listaordenada_monopatin = Monopatin(marca)
                listaordenada_monopatin.actualizar_dolar()
            if nro == 7:
                listaordenada_monopatin = Monopatin(marca)
                listaordenada_monopatin.lista_gistorico_mono()
            if nro == 8:
                listaordenada_monopatin = Monopatin(marca)
                listaordenada_monopatin.lista_actualizadadolar()
            if nro == 9:
                marca = 0
                listaPorFecha = Monopatin(marca)
                listaPorFecha.lista_porfecha()
            if nro==0:
                break
    
    def crearTablas(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        ##TABLA 2(EJERCIO 6 EN ADELANTE)
        #TABLA MONOPATIN2
        conexion.miCursor.execute("CREATE TABLE MONOPATIN2 (id_mono INTEGER PRIMARY KEY , marca VARCHAR(30), precio FLOAT NOT NULL, cantidadDisponibles INTEGER NOT NULL, potencia VARCHAR(30), color VARCHAR(30), fecha DATETIME)")
        conexion.miConexion.commit()
        
        ##tabla HISTORICO_MONO
        conexion.miCursor.execute("CREATE TABLE HISTORICO_MONO (id_mono INTEGER PRIMARY KEY, identificador INTEGER NOT NULL , marca VARCHAR(30), precio FLOAT NOT NULL, cantidadDisponibles INTEGER NOT NULL, potencia VARCHAR(30), color VARCHAR(30), fecha DATETIME)")
        conexion.miConexion.commit()

class Monopatin:
    def __init__(self, marca, precio= None, cantidadDisponibles=None, color=None, potencia=None, fecha= None):
        self.marca = marca
        self.precio=precio
        self.cantidadDisponibles= cantidadDisponibles
        self.potencia= potencia
        self.color= color
        self.fecha= fecha



########### FUNCION PARA CARGAR ELEMENTOS A LA LISTA
    def cargar_monopatin(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("INSERT INTO MONOPATIN2(marca,precio,cantidadDisponibles,potencia,color,fecha) VALUES('{}','{}','{}', '{}', '{}', '{}')".format(self.marca,self.precio, self.cantidadDisponibles,self.potencia, self.color, self.fecha))
            conexion.miConexion.commit()

            conexion.miCursor.execute("SELECT max(id_mono) FROM MONOPATIN2")
            tupla_fetch = conexion.miCursor.fetchone()
            identificador = tupla_fetch[0]
            
            conexion.miCursor.execute("INSERT INTO HISTORICO_MONO(identificador, marca,precio,cantidadDisponibles,potencia,color,fecha) VALUES('{}','{}','{}','{}', '{}', '{}', '{}')".format(identificador,self.marca,self.precio, self.cantidadDisponibles,self.potencia, self.color, self.fecha))
            conexion.miConexion.commit()
            print("monopatin cargado exitosamente")
        except:
            print("Error al agregar un monopatin")
        finally:
            conexion.cerrarConexion()
    
    
############# FUNCION PARA MODIFICAR UN ELEMENTO DE LA LISTA
    def modificar_monopatin(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        fechahoy = input("Ingrese la fecha actual: ")
        try:
            conexion.miCursor.execute("SELECT * FROM MONOPATIN2 WHERE marca='{}'".format(self.marca))
            if conexion.miCursor.fetchone():
                conexion.miCursor.execute("UPDATE MONOPATIN2 SET precio='{}' where marca='{}' ".format(self.precio,self.marca))
                conexion.miConexion.commit()

                conexion.miCursor.execute("INSERT INTO HISTORICO_MONO(identificador, marca,precio,cantidadDisponibles,potencia,color) SELECT id_mono, marca, precio, cantidadDisponibles, potencia, color FROM MONOPATIN2 WHERE marca = '{}'".format(self.marca))
                conexion.miCursor.execute("UPDATE HISTORICO_MONO SET fecha='{}' WHERE fecha IS NULL".format(fechahoy))
                conexion.miConexion.commit()

                print("monopatin modificado correctamente")
            else:
                print("No existen registros para la marca indicada. Fallo la modificacion.")
        except:
            print('Error al actualizar un monopatin')
        finally:
            conexion.cerrarConexion()  
            
            
######## FUNCION PARA BORRAR UN ELEMENTO DE LA LISTA
    def borrar_monopatin(self):
        identificador = input("Ingrese el id del monopatin a eliminar: ")
        conexion= Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("SELECT * FROM MONOPATIN2 where id_mono='{}'".format(identificador))
            if conexion.miCursor.fetchone():
                conexion.miCursor.execute("delete from MONOPATIN2 where id_mono='{}' ".format(identificador))
                conexion.miConexion.commit()
                print("monopatin removido de MONOPATIN2 correctamente")
            else:
                print("El id ingresado no pertenece a ningun monopatin dentro del registro actualizado.")

            conexion.miCursor.execute("SELECT * FROM HISTORICO_MONO where identificador='{}'".format(identificador))
            if conexion.miCursor.fetchone():
                conexion.miCursor.execute("delete from HISTORICO_MONO where identificador='{}' ".format(identificador))
                conexion.miConexion.commit()
                print("monopatin removido de HISTORICO_MONO correctamente")
            else:
                print("El id ingresado no pertenece a ningun monopatin dentro del registro historico.")
        except:
            print('Error al remover un monopatin')
        finally:
            conexion.cerrarConexion()  
            
######## FUNCION PARA AGREGAR DISPO
    def disponibilidad_monopatin(self):
        conexion = Conexiones()
        conexion.abrirConexion()

        try:
            conexion.miCursor.execute("UPDATE MONOPATIN2 SET cantidadDisponibles=cantidadDisponibles+1 WHERE marca='{}' ".format(self.marca))
            conexion.miConexion.commit()
            print("Disponibilidad actualizada correctamente")
        except:
            print("Error al actualizar disponibilidad")
        finally:
            conexion.cerrarConexion()
            
######### FUNCION PARA IMRIMIR LA LISTA POR DEFECTO
    def lista_monopatin(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("SELECT * FROM MONOPATIN2")
            conexion.miConexion.commit()
            tablas= conexion.miCursor.fetchall()
            print("ID / MARCA / PRECIO/ CANT DISPO / COLOR / POTENCIA / FECHA ULTIMO PRECIO")
            for t in tablas:
                print(t)
            print("--------------------------------")
            print("Lista cargada exitosamente")
        except:
            print("Error al mostrar lista")
        finally:
            conexion.cerrarConexion()



############### FUNCION PARA ACTUALIZAR AL PRECIO DEL DOLAR
    def actualizar_dolar(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        fechahoy = input("Ingrese la fecha actual: ")
        try:
            conexion.miCursor.execute("UPDATE MONOPATIN2 SET precio=(precio+(precio*0.23))")
            conexion.miConexion.commit()
            conexion.miCursor.execute("INSERT INTO HISTORICO_MONO(identificador, marca,precio,cantidadDisponibles,potencia,color) SELECT id_mono, marca, precio, cantidadDisponibles, potencia, color FROM MONOPATIN2")
            conexion.miCursor.execute("UPDATE HISTORICO_MONO SET fecha='{}' WHERE fecha IS NULL".format(fechahoy))
            conexion.miConexion.commit()
            print("\n==========================================================")
            print("Precio actualizado al dolar correctamente")
            print("============================================================")
        except:
            print("Error al actualizar el precio")
        finally:
            conexion.cerrarConexion()
            
            
########### FUNCION QUE COPIA LA TABLA CON LOS VALORES ANTERIORES A SER ACTUALIZADOS AL DOLAR
    def copiar_tabla(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
             #TABLA HISTORICO PRECIO
            conexion.miCursor.execute("INSERT INTO HISTORICO_MONO (precio) SELECT precio FROM MONOPATIN2 WHERE precio!='' ")    
            conexion.miConexion.commit()              
            conexion.cerrarConexion()
            print("Tabla copiada correctamente")
        except:
            print("Error al crear la copia de la tabla default")
        finally:
            conexion.cerrarConexion()
            
            
############# FUNCION QUE IMPRIME LA LISTA ANTES DE SER ACTUALIZADA AL VALOR DEL DOL.AR
    def lista_gistorico_mono(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("SELECT * FROM HISTORICO_MONO")
            conexion.miConexion.commit()
            tablas= conexion.miCursor.fetchall()
            print("id / id_origen / MARCA / PRECIO / CANT DISPO / COLOR / POTENCIA / FECHA ULTIMO PRECIO")
            for t in tablas:
                print(t)
            print("--------------------------------")
            print("Lista cargada exitosamente")
        except:
            print("Error al mostrar lista")
        finally:
            conexion.cerrarConexion()
####### FUNCION QUE ACTUALIZA TODOS LOS PRECIOS AL VALOR DEL DOLAR
    def lista_actualizadadolar(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("SELECT * FROM MONOPATIN2")
            conexion.miConexion.commit()
            tablas= conexion.miCursor.fetchall()
            print("ID / MARCA / PRECIO / COLOR / POTENCIA / FECHA ULTIMO PRECIO")
            for t in tablas:
                print(t)
            print("--------------------------------")
            print("Lista cargada exitosamente")
        except:
            print("Error al mostrar lista")
        finally:
            conexion.cerrarConexion()
    
    def lista_porfecha(self):
            conexion = Conexiones()
            conexion.abrirConexion()
            fecha1 = ""
            print("Ingrese la fecha hasta la cual se desea obtener los datos.")
            print("El formato debe ser como el siguiente: AAAA-MM-DD")
            print("Fecha: ")
            fecha1 = input()
            fecha1 = str(fecha1)

            try:
                conexion.miCursor.execute("SELECT * FROM MONOPATIN2 WHERE fecha < '{}'".format(fecha1))
                conexion.miConexion.commit()
                tablas = conexion.miCursor.fetchall()
                print("ID / MARCA / PRECIO / COLOR / POTENCIA / FECHA ULTIMO PRECIO")
                for t in tablas:
                    print(t)
                print("--------------------------------")
                print("Lista cargada exitosamente")
            except:
                print("Error al mostrar lista")
            finally:
                conexion.cerrarConexion()

class Conexiones:
    
    def abrirConexion(self):
        self.miConexion = sqlite3.connect("Concesionaria")
        self.miCursor = self.miConexion.cursor()
        
    def cerrarConexion(self):
        self.miConexion.close()


            
programa = ProgramaPrincipal()
try:
    programa.crearTablas()
except:
    print("La tabla ya existe.")
programa.menu()




#Si necesitamos almacenar la fecha y hora actual utilizamos la función datetime:
#
#insert into asistencia(dni, fechahora) values ('11111111', datetime('now','localtime'));
#Se almacena en el campo fechahora la fecha y hora local del equipo donde se ejecuta el programa.


#select FECHA from [TuTabla] where date(FECHA ) < date('2016-06-23');