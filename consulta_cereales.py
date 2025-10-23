### En este programa se podra consultar varias opcoines de informacion sobre los cereales que se entregan a la industria Argentina desde que se empezo a tomar registro de los mismos, podras optar por una lectura completa del registro del cereal elegido, como los rindes totales entregados por año, el año con menos entrega y el año con mas entrega. También se podra completar en caso de tener la info oficial y autorizada los años que faltan ya que el ultimo registro fue en el año 2018.


### Librerias ###
import pandas as pd
from tabulate import tabulate
import os


### Archicvos Utilizados ###

sorgo = 'sorgo.csv'
trigo_pan = 'trigo_pan.csv'
trigo_candal = 'trigo_candal.csv'
maiz = 'maiz.csv'


###FUNCIONES DEL SUBMENU###

def lectura_cereal(archivo):
    '''Toma el archivo csv y lo arma para la vista con los detalles que se van a mostrar en pantalla'''
    columnas_interes = [2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    ar = pd.read_csv(archivo, header = None)[columnas_interes]
    
    print("\n****************************************\n")
    print('Los valores estan expresados en toneladas \n')
    print (tabulate(ar, headers=['Año','enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'], tablefmt='fancy_grid'))


def rinde_total_anual(archivo):
    '''Realiza la suma de los rinde aportados por meses y muestra el total del rinde por año del cereal seleccionado'''
    columnas_interes = ['año', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto','septiembre', 'octubre', 'noviembre', 'diciembre']
    ar = pd.read_csv(archivo, header = 0)[columnas_interes]
  
    rinde = []
    for index, fila in ar.iterrows():
        anio = int(fila.iloc[0])   
        suma_meses = float(fila.iloc[1:].sum())
        rinde.append([anio, "{:,.2f}".format(suma_meses)])

    print(tabulate(rinde, headers=['Año', 'Rinde total '], tablefmt='fancy_grid' ))


def min_rinde_anual(archivo):
    '''Esta función nos dara el año que menos rinde se aporto a la industria Argentina'''
    columnas_interes = ['año', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto','septiembre', 'octubre', 'noviembre', 'diciembre']
    ar = pd.read_csv(archivo, header = 0)[columnas_interes]

    rinde = {}
    for index, fila in ar.iterrows():
        anio = int(fila.iloc[0])   
        suma_meses = fila.iloc[1:].sum()
        rinde [anio] = suma_meses
    minimo_rinde = min(rinde, key=rinde.get)
    min_rinde = rinde[minimo_rinde]
    print('Fue en', minimo_rinde,'con un rinde de ', "{:,.2f}".format(min_rinde), 'toneladas')


def max_rinde_anual(archivo):
    '''Esta función nos dara el año que más rinde se aporto a la industria Argentina'''
    columnas_interes = ['año', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto','septiembre', 'octubre', 'noviembre', 'diciembre']
    ar = pd.read_csv(archivo, header = 0)[columnas_interes]

    rinde = {}
    for index, fila in ar.iterrows():
        anio = int(fila.iloc[0])   
        suma_meses = fila.iloc[1:].sum()
        rinde [anio] = suma_meses
    maximo_rinde = max(rinde, key=rinde.get)
    max_rinde = rinde[maximo_rinde]
    print('Fue en', maximo_rinde,'con un rinde de ', "{:,.2f}".format(max_rinde), 'toneladas')


def actualizar_archivo(archivo):
    ''' Esta funcion permitira la actualizacion del archivo CSV ya que hay registros hasta el 2018, ojo las actualizaciones deben ser oficiales '''
    ar = pd.read_csv(archivo, header = 0)
    
    nueva_fila = {}
    print("Ingresa los datos para la nueva fila:")
    print('''
             !!! Tener en cuenta que los datos a ingresar deben ser oficiales !!!
     ''')

    for col in ar:
         if col == 'cod_pais':
             dato = int(input(f"Ingresa '{col}' (si es Argentina es 32): "))
         elif col == 'nom_pais':
             dato = str(input(f"Ingrese Argentina '{col}': ").strip())
         elif col == 'año':
             año_existentes = ar['año'].values
             while True:
                 dato = int(input(f"Ingrese el '{col}' que va a actualizar: "))
                 if dato in año_existentes:
                    print("El año ya existe. Por favor ingrese un año válido.")
                 else:
                    break
         elif col == 'producto':
             dato = str(input(f"Ingrese el grano de cereal a actualizar en la columna '{col}': ").strip().lower())
         elif col == 'unidad_id':
                dato = str(input(f"Ingrese el '{col}' (es t para tonelada): ").strip().lower())
         elif col == 'nom_unidad':
                dato = str(input(f"Ingrese el '{col}': ").strip().lower())
         else:
                dato = float(input(f"Ingrese el valor en toneladas de '{col}': "))
        
         nueva_fila[col]=dato
    print(nueva_fila)

    input('Presione enter para continuar')

    ing = pd.DataFrame([nueva_fila])
    df_actualizado = pd.concat([ar, ing], ignore_index=True)
    print(tabulate(df_actualizado))
    while True:
        guardar = str(input('''
            ¿Desea guardar los datos ingresado?
            (S/N):  ''').strip().lower())
        
        if guardar == 's':
            df_actualizado.to_csv(archivo, index=False)
            print('Los datos han sido guradados con exito')
            break
        elif guardar == 'n' :
            print('''
                Los datos no se han guardado
                Gracias !!!
                ''')
            break
        else: 
            print('\nPOR FAVOR DEBE INGRESAR UNA OPCIÓN VALIDA')
            break


def borrar_actualizaciones(archivo):
    ''' Esta funcion es para borra las filas que se cargaron mal o no deseamo tenerla'''
    ar = pd.read_csv(archivo, header=0)
    print(tabulate(ar, headers='keys', tablefmt='psql'))

    fila_a_eliminar = int(input('Por favor ingrese el año de la fila que desea eliminar: '))
    
    while True:
        opcion = input(f'Usted ingresó {fila_a_eliminar}. '
                       'Si es correcto presione S, de lo contrario presione N: ').strip().upper()
        
        if opcion == 'S':
            if fila_a_eliminar in ar['año'].values:
                if fila_a_eliminar <= 2018:
                    print(f'No se permite eliminar filas del año {fila_a_eliminar} o anteriores.')
                    return
                else:
                    ar.drop(ar[ar['año'] == fila_a_eliminar].index, inplace=True)
                    print(f'La fila del año {fila_a_eliminar} fue eliminada.')
                    ar.to_csv(archivo, index=False)
                    print(tabulate(ar, headers="keys", tablefmt="psql"))
            else:
                print(f'No se encontró ninguna fila con el año {fila_a_eliminar}.')
            break
        elif opcion== 'N':
            print('No se a eliminado la fila')
            break
        else:
            print('POr favos ingrese una opción valida')

    print (tabulate(ar))    
    
   

def principal():
    
    while True:
        os.system('clear')
        print(80*'*')
        print('''\n En este programa podrá informarse sobre la cantidad de cereal expresada 
        en toneladas que se aporto a la industria argentina\n
        ''')
        print(80*'*')
        print(" MENU ".center(80,'='))
        
        
        print('Elija el cereal que desea consultar'.center(80,' '))
        
        print ('''
               - 1 - Sorgo 
               - 2 - Trigo Pan
               - 3 - Trigo Candal
               - 4 - Maíz
               - 5 - SALIR
               ''')
        print(80*'*')

        opcion = input(' Ingrece una opción: ').strip()
        global archivo
       
        if opcion == '1':
             os.system('clear')
             archivo = sorgo
             print(80*'*')
             print('SORGO'.center(80,' '))
             print(80*'*')
             
             print(80*'*')
             print (''' 
                    - 1 : Lectura completo de los rinde del sorgo
                    - 2 : Rinde total anual del Sorgo  
                    - 3 : Rinde Minimo anual
                    - 4 : Rinde Maximo anual 
                    - 5 : Actualizar archivo
                    - 6 : Borrado de fila actualizada
                    - 7 : Volver al menu anterior
                    ''')  
             print(80*'*')

             opcion_sorgo = input(' Ingrece una opción: ').strip()
             
             while True:
                if opcion_sorgo == '1': 
                    print(80*'*')
                    print('SORGO'.center(80,' '))
                    print(80*'*')
                    lectura_cereal(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()
                
                elif opcion_sorgo == '2':
                    print("\n*************************************************\n")
                    print('         Rinde total por año del sorgo                      ')
                    print('*****************************************************')
                    rinde_total_anual(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()
                    
                elif opcion_sorgo == '3':
                    print(70*'*')
                    print('El año que menos Rinde se aporto'.center(80,' '))
                    print(70*'*')
                    min_rinde_anual(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()
                                    
                elif opcion_sorgo == '4':
                    print(70*'*')
                    print('El año que más Rinde se aporto'.center(80,' '))
                    print(70*'*')
                    max_rinde_anual(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()
                
                elif opcion_sorgo == '5':
                    actualizar_archivo(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()
                
                elif opcion_sorgo == '6':
                    borrar_actualizaciones(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()

                elif opcion_sorgo == '7':
                    os.system('clear')
                    print('Gracias')
                    return principal()
                else:
                    input('''\nPOR FAVOR DEBE INGRESAR UNA OPCIÓN VALIDA
                  \nPresione enter para continuar\n''')
                    return
             
           
        elif opcion == '2':
             os.system('clear')
             archivo = trigo_pan
             print(80*'*')
             print('TRIGO PAN'.center(80,' '))
             print(80*'*')
             
             print(80*'*')
             print (''' 
                    - 1 : Lectura completo de los rinde
                    - 2 : Rinde total anual 
                    - 3 : Rinde Minimo anual
                    - 4 : Rinde Maximo anual 
                    - 6 : Volver al menu anterior
                    ''')  
             print(80*'*')
             opcion_trigopan = input(' Ingrece una opción: ').strip()
             
             while True:
                if opcion_trigopan == '1':
                    print("*****************************************************")
                    print('                     TRIGO PAN                       ')
                    print('*****************************************************') 
                    lectura_cereal(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()
                    
                elif opcion_trigopan == '2':
                    print("*****************************************************")
                    print('       Rinde total de entrega por año del Trigo Pan                   ')
                    print('*****************************************************') 
                    rinde_total_anual(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()

                elif opcion_trigopan == '3':
                    print(70*'*')
                    print('El año que menos Rinde se aporto'.center(80,' '))
                    print(70*'*')
                    min_rinde_anual(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()
                                    
                elif opcion_trigopan == '4':
                    print(70*'*')
                    print('El año que más Rinde se aporto'.center(80,' '))
                    print(70*'*')
                    max_rinde_anual(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()
                    
                elif opcion_trigopan == '6':
                    os.system('clear')
                    print('Gracias')
                    return principal()
                
                else:
                    input('''\nPOR FAVOR DEBE INGRESAR UNA OPCIÓN VALIDA
                  \nPresione enter para continuar\n''')
                             
        elif opcion == '3':
            os.system('clear')
            archivo = trigo_candal
            print(80*'*')
            print('TRIGO CANDAL'.center(80,' '))
            print(80*'*')
             
            print(80*'*')
            print (''' 
                    - 1 : Lectura completo de los rinde
                    - 2 : Rinde total anual 
                    - 3 : Rinde Minimo anual
                    - 4 : Rinde Maximo anual 
                    - 6 : Volver al menu anterior
                    ''')  
            print(80*'*')
            opcion_trigocandal = input(' Ingrece una opción: ').strip()
            
            while True:
                if opcion_trigocandal == '1': 
                    print("*****************************************************")
                    print('                     TRIGO CANDAL                     ')
                    print('*****************************************************') 
                    lectura_cereal(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()
                    
                elif opcion_trigocandal == '2':
                    print("*****************************************************")
                    print('       Rinde total de entrega por año del Trigo Candal')
                    print('*****************************************************') 
                    rinde_total_anual(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()

                elif opcion_trigocandal == '3':
                    print(70*'*')
                    print('El año que menos Rinde se aporto'.center(80,' '))
                    print(70*'*')
                    min_rinde_anual(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()
                                
                elif opcion_trigocandal == '4':
                    print(70*'*')
                    print('El año que más Rinde se aporto'.center(80,' '))
                    print(70*'*')
                    max_rinde_anual(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()
                    
                elif opcion_trigocandal == '6':
                    os.system('clear')
                    print('Gracias')
                    return principal()
                
                else:
                    input('''\nPOR FAVOR DEBE INGRESAR UNA OPCIÓN VALIDA
                            \nPresione enter para continuar\n''')
                    return
                
        elif opcion == '4':
            os.system('clear')
            archivo = maiz
            os.system('clear')
            archivo = trigo_candal
            print(80*'*')
            print('MAÍZ'.center(80,' '))
            print(80*'*')
             
            print(80*'*')
            print (''' 
                    - 1 : Lectura completo de los rinde
                    - 2 : Rinde total anual 
                    - 3 : Rinde Minimo anual
                    - 4 : Rinde Maximo anual 
                    - 6 : Volver al menu anterior
                    ''')  
            print(80*'*')
            
            opcion_maíz = input(' Ingrece una opción: ').strip()
            
            while True:
                if opcion_maíz == '1': 
                    print("*****************************************************")
                    print('                     MAÍZ                     ')
                    print('*****************************************************') 
                    lectura_cereal(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()
                    
                elif opcion_maíz == '2':
                    print("*****************************************************")
                    print('       Rinde total de entrega por año del Maíz                   ')
                    print('*****************************************************') 
                    rinde_total_anual(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()
                    
                elif opcion_maíz == '3':
                    print(70*'*')
                    print('El año que menos Rinde se aporto'.center(80,' '))
                    print(70*'*')
                    min_rinde_anual(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()
                                    
                elif opcion_maíz == '4':
                    print(70*'*')
                    print('El año que más Rinde se aporto'.center(80,' '))
                    print(70*'*')
                    max_rinde_anual(archivo)
                    input('\nprecione enter para volver al menu Principal\n')
                    return principal()                   
                    
                elif opcion_maíz == '6':
                    os.system('clear')
                    print('Gracias')
                    return principal()
                
                else:
                    input('''\nPOR FAVOR DEBE INGRESAR UNA OPCIÓN VALIDA
                            \nPresione enter para continuar\n''')

        elif opcion == '5':
            os.system('clear')
            break
        else:
            input('''\nPOR FAVOR DEBE INGRESAR UNA OPCIÓN VALIDA
                  \nPresione enter para continuar\n''')

    print('\nGracias\n'.center(30,' '))

principal()







