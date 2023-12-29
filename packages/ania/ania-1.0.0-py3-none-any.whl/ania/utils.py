class Anime:
  def __init__(self, id: str, title: str, type: str):
    self.id = id
    self.title = title
    self.type = type

class AnimeInfo:

  def __init__(self, id: str, title: str, episode: int, episodes: int):
    self.id = id
    self.title = title
    self.episodes = episodes
    self.episode = episode
