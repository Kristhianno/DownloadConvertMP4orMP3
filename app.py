from pytube import YouTube
import moviepy.editor as mp
import re
import os


def download_video():
    link = input('Digite o link do vídeo que deseja baixar:')
    path = input('Digite a pasta que deseja salvar o arquivo:')
    yt = YouTube(link)
    print('Baixando...')
    yt.streams.get_highest_resolution().download(path)


download_video()

print('Dowload completo!')


def download_music():
    link = input('Digite o link do vídeo que deseja baixar:')
    path = input('Digite a pasta que deseja salvar o arquivo:')
    yt = YouTube(link)
    print('Baixando...')
    yt.streams.filter(only_audio=True).first().download(path)
    print('Convertendo arquivo...')
    for file in os.listdir(path):
        if re.search('mp4', file):
            mp4_path = os.path.join(path, file)
            mp3_path = os.path.join(path, os.path.splitext(file)[0]+'.mp3')
            new_file = mp.AudioFileClip(mp4_path)
            new_file.write_audiofile(mp3_path)
            os.remove(mp4_path)


download_music()

print('Conversão Completa!')

print('Arquivos Salvos e Convertidos com Sucesso,\
 obrigado por utilizar o programa')
