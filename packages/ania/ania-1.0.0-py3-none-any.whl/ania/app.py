from .ui import clear, get_input, check_connection
from .search_anime import search_anime
from .select_anime import select_anime
from .select_episode import select_episode
from .get_servers import get_servers
from .web_player import web_player

def ania():
  """
  Ejecuta la aplicación Ania para buscar y seleccionar animes.
  """
  check_connection()
  clear()
  search = get_input('Buscar: ')
  animes = search_anime(search)
  anime = select_anime(animes, search)
  animei = select_episode(anime)
  servers = get_servers(animei)
  web_player(animei, servers)