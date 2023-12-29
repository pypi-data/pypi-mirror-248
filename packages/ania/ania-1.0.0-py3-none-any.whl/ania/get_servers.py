from .api import AnimeFLV
from .ui import clear, error, printb
from .utils import AnimeInfo

def get_servers(animei: AnimeInfo):
  """
    Obtiene la lista de servidores para un episodio específico de un anime.

    Parameters:
        animei (AnimeInfo): Objeto AnimeInfo que contiene información sobre el anime y el episodio.

    Returns:
        List[str]: Lista de nombres de servidores disponibles para el episodio.
  """
  clear()
  printb(f'Cargando servidores para el episodio {animei.episode} de {animei.title}...')

  api = AnimeFLV()
  attempts, servers = 0, None
  while attempts <= 5:
    try:
      servers = api.get_video_servers(id=animei.id, episode=animei.episode)
      break
    except:
      attempts += 1
      continue
  
  if(servers is None):
    error(f'No se pudo cargar el episodio {animei.episode} de "{animei.title}"')
  
  return servers[0]