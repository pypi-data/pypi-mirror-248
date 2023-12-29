from ania.ui import printb, clear, bye
from termcolor import colored
from flask import Flask, render_template, request, redirect

def web_player(animei, servers):
  port = 5666

  app = Flask(__name__)

  app.logger.warning('')

  @app.before_request
  def middleware():
    if request.endpoint != 'index':
        return redirect('/')
        
  @app.route('/')
  def index():
    return render_template('index.html', title=animei.title, servers=servers, episode=animei.episode)
  
  episode = colored(str(animei.episode), 'cyan', attrs=['bold'])
  title = colored(str(animei.title), 'yellow', attrs=['bold'])
    
  # UI
  clear()
  print(f'¡Ahora puedes ver el episodio {episode} de {title}!')
  printb('\nAbre este enlace en tu navegador:')
  print(f'http://localhost:{port} \n')
  
  if __package__ == 'ania.web_player':
      app.run(port=port, debug=False)
      bye()