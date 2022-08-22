import cx_Freeze

executables = [cx_Freeze.Executable('programa.py')]

cx_Freeze.setup(
    name="Programa MP4 to MP3",
    options={'build_exe': {'packages': ['pytube', 'moviepy']}},

    executables=executables
               )