import os
import subprocess
import sys
from multiprocessing import freeze_support

import uvicorn

if __name__ == '__main__':
    freeze_support()
    process = None

    if os.environ.get('DEBUG'):
        process = subprocess.Popen(['npm', 'run', 'dev'], shell=True, cwd='web_src')
        args = {
            'reload': True,
            'port': 8080
        }
    else:
        if not getattr(sys, 'frozen', False):
            subprocess.Popen(['npm', 'run', 'build'], shell=True, cwd='web_src').wait()

        args = {
            'workers': os.cpu_count(),
            'port': os.environ.get('WEB_PORT', 3000)  # Take over port 5000 from Vite
        }

    try:
        uvicorn.run('app:app', host='0.0.0.0', **args)
    finally:
        if process is not None:
            process.kill()
