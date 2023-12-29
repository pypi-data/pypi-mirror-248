from .api import AnimeFLV
import tty, sys, termios
from .utils import  Anime
from .ui import clear, printb, error

def search_anime(anime_name: str):
  """
  Busca animes por nombre utilizando la librearía animeflv-api

  Args:
      anime_name (str): El nombre del anime a buscar.

  Returns:
      List[Anime]: Una lista de objetos Anime con los resultados de la búsqueda.
  """
  api = AnimeFLV()

  clear()

  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  tty.setcbreak(sys.stdin)

  try:
    printb(f'Buscando "{anime_name}"...')

    attempts, response = 0, None

    while attempts <= 3:
      response = api.search(query=anime_name.strip())
      if len(response) > 0:
        break
      else:
          attempts += 1

    if(len(response) == 0):
      error(f'No se encontraron resultados para "{anime_name}"')
  
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

  return [Anime(
    anime.id,
    anime.title,
    'TV' if anime.type == 'Anime' else anime.type,
    ) for anime in response]