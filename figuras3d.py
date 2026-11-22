# -*- coding: utf-8 -*-
# =============================================================================
# Curso: Programación (213023) - UNAD
# Fase 4 - Componente práctico: Manejo de excepciones
# Proyecto: Sistema Avanzado de Figuras 3D (continuación de la Fase 3)
# Estudiante: Ashley Caroline Cera Yopasá - Grupo 213023_571
# Descripción: el sistema crea cubos, esferas y cilindros, calcula su volumen y
# su área superficial y ahora controla los errores con excepciones para que el
# programa sea estable y robusto (no se cierra ante datos incorrectos).
# =============================================================================

import math                          # Importa math para usar la constante pi
import sys                           # Importa sys para leer argumentos de la consola
from abc import ABC, abstractmethod  # Importa herramientas para clases abstractas


# -----------------------------------------------------------------------------
# 1. EXCEPCIONES PERSONALIZADAS
# -----------------------------------------------------------------------------
class FiguraError(Exception):
    """Excepción base del sistema: todas las demás heredan de esta."""
    pass                             # No agrega nada nuevo, solo agrupa los errores propios


class DimensionInvalidaError(FiguraError):
    """Se lanza cuando una medida no es numérica o no es mayor que cero."""

    def __init__(self, nombre_dato, valor):          # Recibe el nombre del dato y el valor erróneo
        self.nombre_dato = nombre_dato               # Guarda qué dato falló (lado, radio, altura)
        self.valor = valor                           # Guarda el valor que causó el error
        mensaje = (f"La dimensión '{nombre_dato}' debe ser un número mayor que cero "
                   f"(valor recibido: {valor!r}).")  # Construye un mensaje claro para el usuario
        super().__init__(mensaje)                    # Envía el mensaje a la clase Exception


class TipoFiguraInvalidoError(FiguraError):
    """Se lanza cuando se pide crear una figura que el sistema no conoce."""

    def __init__(self, tipo):                        # Recibe el tipo de figura solicitado
        self.tipo = tipo                             # Guarda el tipo para consultarlo luego
        super().__init__(f"El tipo de figura '{tipo}' no existe. "
                         f"Use: cubo, esfera o cilindro.")  # Mensaje con las opciones válidas


# -----------------------------------------------------------------------------
# 2. CLASE ABSTRACTA (viene de la Fase 3, ahora con validación)
# -----------------------------------------------------------------------------
class Figura3D(ABC):
    """Clase abstracta que define lo que toda figura 3D debe tener."""

    def __init__(self, nombre):                      # Constructor común a todas las figuras
        self.nombre = nombre                         # Guarda el nombre de la figura

    @staticmethod
    def validar_dimension(nombre_dato, valor):
        """Revisa que una medida sea un número real positivo; si no, lanza error."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):  # True/False no son medidas
            raise DimensionInvalidaError(nombre_dato, valor)  # Lanza error si no es número
        if math.isnan(valor) or math.isinf(valor):   # Rechaza valores "nan" o infinitos
            raise DimensionInvalidaError(nombre_dato, valor)  # Lanza error por valor no finito
        if valor <= 0:                               # Una medida física no puede ser 0 ni negativa
            raise DimensionInvalidaError(nombre_dato, valor)  # Lanza error por valor no positivo
        return float(valor)                          # Si todo está bien, devuelve el valor como float

    @abstractmethod
    def volumen(self):                               # Cada figura debe definir su volumen
        pass                                         # Sin implementación en la clase abstracta

    @abstractmethod
    def area_superficial(self):                      # Cada figura debe definir su área
        pass                                         # Sin implementación en la clase abstracta

    def describir(self, decimales=2):
        """Devuelve un texto con los cálculos (parámetro opcional, como en la Fase 3)."""
        if not isinstance(decimales, int) or decimales < 0:   # Valida el número de decimales
            raise ValueError("El número de decimales debe ser un entero mayor o igual a 0.")
        return (f"{self.nombre}: volumen = {self.volumen():.{decimales}f}, "
                f"área superficial = {self.area_superficial():.{decimales}f}")  # Texto formateado


# -----------------------------------------------------------------------------
# 3. CLASES DERIVADAS (herencia y polimorfismo)
# -----------------------------------------------------------------------------
class Cubo(Figura3D):
    """Cubo definido por la longitud de su lado."""

    def __init__(self, lado):                        # Recibe el lado del cubo
        super().__init__("Cubo")                     # Llama al constructor de Figura3D
        self.lado = self.validar_dimension("lado", lado)  # Valida y guarda el lado

    def volumen(self):                               # Volumen del cubo
        return self.lado ** 3                        # V = lado³

    def area_superficial(self):                      # Área del cubo
        return 6 * self.lado ** 2                    # A = 6·lado²


class Esfera(Figura3D):
    """Esfera definida por su radio."""

    def __init__(self, radio):                       # Recibe el radio de la esfera
        super().__init__("Esfera")                   # Llama al constructor de Figura3D
        self.radio = self.validar_dimension("radio", radio)  # Valida y guarda el radio

    def volumen(self):                               # Volumen de la esfera
        return (4 / 3) * math.pi * self.radio ** 3   # V = 4/3·π·r³

    def area_superficial(self):                      # Área de la esfera
        return 4 * math.pi * self.radio ** 2         # A = 4·π·r²


class Cilindro(Figura3D):
    """Cilindro definido por su radio y su altura."""

    def __init__(self, radio, altura):               # Recibe radio y altura
        super().__init__("Cilindro")                 # Llama al constructor de Figura3D
        self.radio = self.validar_dimension("radio", radio)      # Valida y guarda el radio
        self.altura = self.validar_dimension("altura", altura)   # Valida y guarda la altura

    def volumen(self):                               # Volumen del cilindro
        return math.pi * self.radio ** 2 * self.altura  # V = π·r²·h

    def area_superficial(self):                      # Área del cilindro
        return 2 * math.pi * self.radio * (self.radio + self.altura)  # A = 2·π·r·(r + h)


# -----------------------------------------------------------------------------
# 4. GESTOR DE FIGURAS (aquí se concentra el manejo de errores)
# -----------------------------------------------------------------------------
class GestorFiguras:
    """Guarda las figuras creadas y realiza operaciones sobre ellas."""

    # Diccionario: nombre del tipo -> (clase, lista de dimensiones que necesita)
    TIPOS = {
        "cubo": (Cubo, ["lado"]),                    # El cubo necesita solo el lado
        "esfera": (Esfera, ["radio"]),               # La esfera necesita solo el radio
        "cilindro": (Cilindro, ["radio", "altura"]), # El cilindro necesita radio y altura
    }

    def __init__(self):                              # Constructor del gestor
        self.figuras = []                            # Lista vacía donde se guardarán las figuras

    def crear_figura(self, tipo, *dimensiones):
        """Crea una figura a partir de su tipo; lanza excepciones si algo falla."""
        tipo = str(tipo).strip().lower()             # Normaliza el texto (sin espacios, minúsculas)
        if tipo not in self.TIPOS:                   # Verifica que el tipo exista
            raise TipoFiguraInvalidoError(tipo)      # Si no existe, lanza el error propio
        clase, requeridas = self.TIPOS[tipo]         # Obtiene la clase y las medidas requeridas
        if len(dimensiones) != len(requeridas):      # Verifica la cantidad de medidas
            raise TypeError(f"El {tipo} necesita {len(requeridas)} dimensión(es): "
                            f"{', '.join(requeridas)}.")  # Error si faltan o sobran datos
        figura = clase(*dimensiones)                 # Crea el objeto (puede lanzar DimensionInvalidaError)
        self.figuras.append(figura)                  # Si no hubo error, lo agrega a la lista
        return figura                                # Devuelve la figura creada

    def obtener_figura(self, posicion):
        """Devuelve la figura de una posición (empezando en 1)."""
        try:
            if posicion < 1:                         # Las posiciones válidas empiezan en 1
                raise IndexError                     # Fuerza el error para posiciones 0 o negativas
            return self.figuras[posicion - 1]        # Convierte a índice de Python (empieza en 0)
        except IndexError:                           # Captura posiciones fuera del rango
            raise IndexError(f"No existe la figura número {posicion}. "
                             f"Hay {len(self.figuras)} figura(s) registrada(s).") from None

    def eliminar_figura(self, posicion):
        """Elimina la figura indicada y la devuelve."""
        figura = self.obtener_figura(posicion)       # Reutiliza la validación de la posición
        self.figuras.remove(figura)                  # Quita la figura de la lista
        return figura                                # Devuelve la figura eliminada

    def volumen_promedio(self):
        """Calcula el volumen promedio de todas las figuras."""
        try:
            total = sum(f.volumen() for f in self.figuras)  # Suma polimórfica de volúmenes
            return total / len(self.figuras)         # Divide entre la cantidad (puede ser 0)
        except ZeroDivisionError:                    # Captura la división entre cero
            raise FiguraError("No hay figuras registradas para calcular el promedio.") from None

    def listar(self, decimales=2):
        """Devuelve la descripción de todas las figuras (polimorfismo)."""
        if not self.figuras:                         # Si la lista está vacía
            return ["(No hay figuras registradas)"]  # Devuelve un aviso en lugar de fallar
        return [f"{i}. {f.describir(decimales)}"     # Cada figura se describe a sí misma
                for i, f in enumerate(self.figuras, start=1)]

    def guardar_reporte(self, ruta):
        """Guarda las figuras en un archivo de texto usando try/except/else/finally."""
        archivo = None                               # Variable para saber si el archivo se abrió
        try:
            archivo = open(ruta, "w", encoding="utf-8")  # Intenta abrir el archivo para escribir
            for linea in self.listar():              # Recorre cada línea del listado
                archivo.write(linea + "\n")          # Escribe la línea en el archivo
        except OSError as error:                     # Captura errores del sistema de archivos
            print(f"  [ERROR] No se pudo guardar el reporte: {error}")  # Informa el problema
            return False                             # Indica que no se guardó
        else:                                        # Se ejecuta solo si NO hubo error
            print(f"  [OK] Reporte guardado en '{ruta}'.")  # Confirma que se guardó
            return True                              # Indica que sí se guardó
        finally:                                     # Se ejecuta SIEMPRE, con o sin error
            if archivo is not None:                  # Si el archivo llegó a abrirse
                archivo.close()                      # Lo cierra para liberar el recurso


# -----------------------------------------------------------------------------
# 5. FUNCIONES DE ENTRADA SEGURA
# -----------------------------------------------------------------------------
def leer_numero(mensaje):
    """Pide un número al usuario y repite la pregunta hasta que sea válido."""
    while True:                                      # Repite hasta obtener un dato correcto
        texto = input(mensaje)                       # Lee el texto escrito por el usuario
        try:
            valor = float(texto.replace(",", "."))   # Convierte a número (acepta coma decimal)
            return Figura3D.validar_dimension("valor", valor)  # Valida que sea positivo
        except ValueError:                           # El texto no se pudo convertir a número
            print("  [ERROR] Debe escribir un número (ejemplo: 3.5).")
        except DimensionInvalidaError:               # El número es 0, negativo o no finito
            print("  [ERROR] El número debe ser mayor que cero.")


def leer_entero(mensaje):
    """Pide un número entero (para opciones del menú y posiciones)."""
    while True:                                      # Repite hasta obtener un entero
        try:
            return int(input(mensaje))               # Intenta convertir el texto a entero
        except ValueError:                           # Si no es un entero válido
            print("  [ERROR] Debe escribir un número entero.")


# -----------------------------------------------------------------------------
# 6. DEMOSTRACIÓN AUTOMÁTICA DE ERRORES (para validar el código paso a paso)
# -----------------------------------------------------------------------------
def demostracion():
    """Ejecuta casos correctos e incorrectos y muestra cómo se controla cada error."""
    gestor = GestorFiguras()                         # Crea un gestor vacío
    print("=" * 70)
    print(" DEMOSTRACIÓN DEL MANEJO DE EXCEPCIONES - SISTEMA DE FIGURAS 3D")
    print("=" * 70)

    # Lista de pruebas: (descripción, tipo, dimensiones)
    pruebas = [
        ("Cubo válido de lado 3", "cubo", (3,)),
        ("Esfera válida de radio 2.5", "esfera", (2.5,)),
        ("Cilindro válido r=2, h=5", "cilindro", (2, 5)),
        ("Cubo con lado negativo", "cubo", (-4,)),
        ("Esfera con radio cero", "esfera", (0,)),
        ("Cilindro con texto como altura", "cilindro", (2, "diez")),
        ("Cilindro con una sola medida", "cilindro", (2,)),
        ("Figura que no existe (pirámide)", "piramide", (3,)),
    ]

    for descripcion, tipo, dims in pruebas:          # Recorre cada caso de prueba
        print(f"\n-> {descripcion}")                 # Muestra qué se va a probar
        try:
            figura = gestor.crear_figura(tipo, *dims)  # Intenta crear la figura
        except DimensionInvalidaError as e:          # Medida incorrecta
            print(f"  [DimensionInvalidaError] {e}")
        except TipoFiguraInvalidoError as e:         # Tipo de figura desconocido
            print(f"  [TipoFiguraInvalidoError] {e}")
        except TypeError as e:                       # Cantidad de medidas incorrecta
            print(f"  [TypeError] {e}")
        else:                                        # Solo si no hubo ninguna excepción
            print(f"  [OK] {figura.describir()}")

    print("\n-> Listado de figuras válidas registradas (polimorfismo):")
    for linea in gestor.listar(3):                   # Lista con 3 decimales
        print("  " + linea)

    print("\n-> Buscar la figura número 10 (no existe)")
    try:
        gestor.obtener_figura(10)                    # Posición fuera de rango
    except IndexError as e:                          # Captura el error de posición
        print(f"  [IndexError] {e}")

    print("\n-> Describir con decimales negativos")
    try:
        gestor.figuras[0].describir(-1)              # Parámetro inválido
    except ValueError as e:                          # Captura el error de valor
        print(f"  [ValueError] {e}")

    print("\n-> Promedio de volumen con un gestor vacío")
    try:
        GestorFiguras().volumen_promedio()           # Gestor sin figuras -> división por cero
    except FiguraError as e:                         # Se captura como error propio del sistema
        print(f"  [FiguraError] {e}")

    print(f"\n-> Promedio de volumen de las figuras válidas: "
          f"{gestor.volumen_promedio():.3f}")

    print("\n-> Guardar reporte en una carpeta que no existe")
    gestor.guardar_reporte("carpeta_inexistente/reporte.txt")  # Provoca OSError controlado
    print("\n-> Guardar reporte en una ruta válida")
    gestor.guardar_reporte("reporte_figuras.txt")    # Se guarda correctamente

    print("\n" + "=" * 70)
    print(" Fin de la demostración: el programa nunca se detuvo por un error.")
    print("=" * 70)


# -----------------------------------------------------------------------------
# 7. MENÚ INTERACTIVO
# -----------------------------------------------------------------------------
def menu():
    """Menú principal; cualquier error se informa sin cerrar el programa."""
    gestor = GestorFiguras()                         # Crea el gestor de figuras
    opciones = ("\n===== SISTEMA AVANZADO DE FIGURAS 3D =====\n"
                "1. Crear cubo\n2. Crear esfera\n3. Crear cilindro\n"
                "4. Listar figuras\n5. Eliminar figura\n6. Volumen promedio\n"
                "7. Guardar reporte\n8. Demostración de errores\n0. Salir")
    while True:                                      # El menú se repite hasta elegir salir
        print(opciones)                              # Muestra las opciones
        opcion = leer_entero("Elija una opción: ")   # Lee la opción de forma segura
        try:
            if opcion == 1:                          # Crear cubo
                f = gestor.crear_figura("cubo", leer_numero("Lado: "))
                print(f"  [OK] {f.describir()}")
            elif opcion == 2:                        # Crear esfera
                f = gestor.crear_figura("esfera", leer_numero("Radio: "))
                print(f"  [OK] {f.describir()}")
            elif opcion == 3:                        # Crear cilindro
                f = gestor.crear_figura("cilindro", leer_numero("Radio: "),
                                        leer_numero("Altura: "))
                print(f"  [OK] {f.describir()}")
            elif opcion == 4:                        # Listar figuras
                for linea in gestor.listar():
                    print("  " + linea)
            elif opcion == 5:                        # Eliminar figura
                f = gestor.eliminar_figura(leer_entero("Número de la figura: "))
                print(f"  [OK] Se eliminó: {f.nombre}")
            elif opcion == 6:                        # Volumen promedio
                print(f"  Volumen promedio: {gestor.volumen_promedio():.2f}")
            elif opcion == 7:                        # Guardar reporte
                gestor.guardar_reporte(input("Nombre del archivo: ").strip() or "reporte.txt")
            elif opcion == 8:                        # Demostración automática
                demostracion()
            elif opcion == 0:                        # Salir
                print("Hasta pronto.")
                break                                # Rompe el ciclo y termina
            else:                                    # Número que no está en el menú
                print("  [ERROR] Opción no válida, elija un número del 0 al 8.")
        except (FiguraError, IndexError, ValueError, TypeError) as e:  # Errores esperados
            print(f"  [ERROR] {e}")                  # Se informa y el menú continúa
        except Exception as e:                       # Cualquier error inesperado
            print(f"  [ERROR INESPERADO] {type(e).__name__}: {e}")


# -----------------------------------------------------------------------------
# 8. PUNTO DE ENTRADA DEL PROGRAMA
# -----------------------------------------------------------------------------
if __name__ == "__main__":                           # Solo se ejecuta si se corre este archivo
    try:
        if "--demo" in sys.argv:                     # python figuras3d.py --demo
            demostracion()                           # Ejecuta solo la demostración
        else:
            menu()                                   # Ejecuta el menú interactivo
    except (KeyboardInterrupt, EOFError):            # Ctrl+C o fin de entrada
        print("\nPrograma interrumpido por el usuario. Hasta pronto.")
