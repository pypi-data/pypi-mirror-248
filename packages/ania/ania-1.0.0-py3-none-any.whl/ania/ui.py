from termcolor import colored
import os

def clear():
  """
  Limpia la pantalla de la terminal.

  Utiliza el comando 'clear' en sistemas tipo Unix (Linux y macOS)
  o 'cls' en sistemas Windows para limpiar la pantalla.
  """

  clear = "clear" if os.name == "posix" else "cls"
  os.system(clear)

def get_input(msg: str):
  """
  Obtiene la entrada del usuario desde la terminal.

  Args:
      msg (str): El mensaje que se muestra al usuario.

  Returns:
      str: La entrada del usuario después de eliminar espacios adicionales.
  """
  user_input = input(colored(msg, 'cyan', attrs=['bold']))
  user_input = filter(None, user_input.split(' '))
  
  return ' '.join(user_input)

def error(msg: str, cls: bool = True , kill: bool = True):
  """
  Muestra un mensaje de error y, opcionalmente, limpia la pantalla y sale del programa.

  Args:
      msg (str): El mensaje de error.
      cls (bool): Indica si se debe limpiar la pantalla. Por defecto es True.
      kill (bool): Indica si se debe salir del programa. Por defecto es True.
  """
  if cls:
    clear()
    
  print(colored(f'Error: {msg}', 'red', attrs=['bold']))

  if kill:
    exit(1)

def printb (msg: str, color: str ='cyan'):
  """
  Imprime un mensaje con formato en negrita y color.

  Args:
      msg (str): El mensaje a imprimir.
      color (str): El color del texto. Por defecto es 'cyan'.
  """
  if os.name == "posix":
    print(colored(msg, color, attrs=['bold']))
    
    return msg

def get_number(msg: str, max_len: int):
  """
  Obtiene un número del usuario dentro de un rango específico.

  Args:
      msg (str): El mensaje que indica al usuario qué ingresar.
      max_len (int): El valor máximo permitido. Por defecto es 0.

  Returns:
      int: El número ingresado por el usuario.
  """
  user_input = input(colored(msg, 'cyan', attrs=['bold']))
  
  if not user_input.isdigit():
    error('Debe ser un numero', cls=False, kill=False)
    return get_number(msg, max_len)

  user_input = int(user_input)

  if user_input < 1 or user_input > max_len:
    error(f'Debe estar en rango de 1 a {max_len}', cls=False, kill=False)
    return get_number(msg, max_len)

  return user_input - 1


def numberf(number: int, color: str = 'yellow'):
  """
  Retorna una cadena formateada como un número con color.

  Parameters:
      number (int): Número a formatear.
      color (str, optional): Color del número. Por defecto, 'yellow'.

  Returns:
      str: Cadena formateada con el número y color.
  """
  number = f'[{number}]'

  if os.name == "posix":
    return colored(number.ljust(4), color)
  
  return number.ljust(4)

def bye():
  """
  Muestra un mensaje de despedida y sale del programa.
  """
  clear()
  printb('Vuelve pronto!')
  exit(0)

import requests
def check_connection():
  """
  Verifica la conexión a Internet mediante una solicitud a 'google.com'.
  """
  try:
    requests.get('https://google.com', timeout=5)

  except requests.ConnectionError:
    error('no tienes conexion a internet', cls=False)
  
  except requests.ReadTimeout:
    error('no tienes conexion a internet', cls=False)
