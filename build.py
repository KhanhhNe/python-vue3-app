import os
import shutil
import subprocess
import zipfile

import PyInstaller.__main__

from app import app


def get_files_recursive(folder: str):
    for root, dirs, files in os.walk(folder):
        relative_path = os.path.relpath(root, os.getcwd()).replace('\\', '/')
        folder = os.path.dirname(relative_path)
        yield f"--add-binary={folder}/*.*{os.pathsep}{folder}"


def compile_to_exe():
    app_name = ''.join([c.lower() for c in app.title if c.isascii() or c.isdigit()]).replace(' ', '-')
    version = app.version
    work_path = 'build/pyinstaller'
    dist_path = 'build/dist'

    shutil.rmtree(dist_path, ignore_errors=True)
    shutil.rmtree(work_path, ignore_errors=True)

    if return_code := subprocess.run('npm run build', cwd='web_src', shell=os.name == 'nt').returncode:
        print(f"NPM build failed! (return code: {return_code})")
        exit(return_code)

    PyInstaller.__main__.run([
        'main.py', f'--name={app_name}', '--icon=public/favicon.ico',
        f'--distpath={dist_path}/{app_name}', f'--workpath={work_path}', '--onefile', '--noconfirm',

        '--hidden-import=app',

        # Websockets
        '--hidden-import=websockets.legacy',
        '--hidden-import=websockets.legacy.server',

        # Databases
        '--hidden-import=databases.backends.sqlite',

        *get_files_recursive('executables'),
        *get_files_recursive('public'),
    ])

    print("Zipping files...")

    current_dir = os.getcwd()
    os.chdir(dist_path)
    dist_file = zipfile.ZipFile(f'{app_name}-v{version}.zip', 'w',
                                compression=zipfile.ZIP_DEFLATED, compresslevel=9)

    for folder, _, filenames in os.walk(app_name):
        for filename in filenames:
            filepath = os.path.join(folder, filename)
            print(f"Zipping {filepath}")
            dist_file.write(filepath)

    os.chdir(current_dir)

    if os.path.exists(f"{app_name}.spec"):
        os.remove(f"{app_name}.spec")

    print("Done!")


if __name__ == '__main__':
    compile_to_exe()
