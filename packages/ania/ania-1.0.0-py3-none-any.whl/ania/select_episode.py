from .api import AnimeFLV
from .ui import clear, printb, get_number, error
from .utils import AnimeInfo, Anime

def select_episode(anime: Anime):
  """
  Muestra información detallada sobre un anime y permite al usuario seleccionar un episodio específico.

  Parameters:
  - anime (Anime()): Un objeto que contiene información del anime, incluyendo 'id' y 'title'.

  Returns:
  - AnimeInfo(): Un objeto AnimeInfo
  """
  clear()
  printb(f'Cargando informacion...')

  api = AnimeFLV()
  attempts, anime_info = 0, None
  while attempts <= 5:
    try:
      anime_info = api.get_anime_info(id=anime.id)
      break
    except:
      attempts += 1
      continue
  
  if anime_info is None:
    error(f'No se pudo cargar la informacion de "{anime.title}"')
    
  clear()
  printb(f'{anime_info.title}')
  print(f'Episodios: {len(anime_info.episodes)}'); print()

  episode = get_number('Introcucir numero de episodio: ', len(anime_info.episodes)) + 1

  return AnimeInfo(
    id = anime_info.id,
    title =  anime_info.title,
    episode =  episode,
    episodes =  len(anime_info.episodes)
  )