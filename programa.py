from PySimpleGUI import PySimpleGUI as sg
from pytube import YouTube
from pytube import Playlist
import moviepy.editor as mp
import re
import os
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_left_right import audio_left_right
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.audio.fx.volumex import volumex
from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.colorx import colorx
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.freeze import freeze
from moviepy.video.fx.freeze_region import freeze_region
from moviepy.video.fx.gamma_corr import gamma_corr
from moviepy.video.fx.headblur import headblur
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.loop import loop
from moviepy.video.fx.lum_contrast import lum_contrast
from moviepy.video.fx.make_loopable import make_loopable
from moviepy.video.fx.margin import margin
from moviepy.video.fx.mask_and import mask_and
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.mask_or import mask_or
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.painting import painting
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.scroll import scroll
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.supersample import supersample
from moviepy.video.fx.time_mirror import time_mirror
from moviepy.video.fx.time_symmetrize import time_symmetrize


# Funções para Downloads
def download_video(dict):
    link = dict['video']
    path = dict['path']
    yt = YouTube(link)
    yt.streams.get_highest_resolution().download(path)
    sg.popup("Download Completo")


def download_music(dict):
    link = dict['music']
    path = dict['path']
    yt = YouTube(link)
    yt.streams.filter(only_audio=True).first().download(path)

    # Converter o video(mp4) para mp3
    for file in os.listdir(path):                  
        if re.search('mp4', file):                                    
            mp4_path = os.path.join(path, file)  
            mp3_path = os.path.join(path, os.path.splitext(file)[0]+'.mp3')
            new_file = mp.AudioFileClip(mp4_path)
            new_file.write_audiofile(mp3_path)    
            os.remove(mp4_path)                 
    sg.popup("Download Completo")


def download_playlist(dict):
    link = dict['playlist']
    path = dict['path']

    playlist = Playlist(link)
    for indice, video in enumerate(playlist.videos):
        print(f'Baixando vídeo {indice + 1}/{len(playlist)}')
        video.streams.filter(only_audio=True).first().download(path)
    
    for file in os.listdir(path):                  
        if re.search('mp4', file):                                    
            mp4_path = os.path.join(path, file)   
            mp3_path = os.path.join(path, os.path.splitext(file)[0]+'.mp3') 
            new_file = mp.AudioFileClip(mp4_path) 
            new_file.write_audiofile(mp3_path)     
            os.remove(mp4_path)                   
    sg.popup("Download Completo")


# Interface
def janela_inicio():
    sg.theme('Reddit')
    layout = [
        [sg.Button('Vídeo', size=(30, 3), button_color=('#000000', '#48D1CC'))],
        [sg.Button('Música', size=(30, 3), button_color=('#000000', '#48D1CC'))],
        [sg.Button('Playlist', size=(30, 3), button_color=('#000000', '#48D1CC'))]
    ]
    return sg.Window('Download Youtube', layout=layout, font=("Bodoni ", 13), finalize=True, size=(280, 250))


def janela_video():
    sg.theme('Reddit')
    layout = [
    [sg.Text('Digite o Link do Vídeo:', size=(24,0)), sg.Input(key = 'video', size=(45,0))], 
    [sg.Text('Selecione a pasta:', size=(24,0)), sg.InputText('', size= (35, 0),key = 'path'), sg.FolderBrowse('Arquivo', button_color=('#000000','#48D1CC'),font=("Bodoni ", 12),size = (7,0)),],
    [sg.Text( size=(24,1)),sg.Button('Baixar',font=("Bodoni", 12), size=(20,1),button_color=('#000000','#48D1CC'))]
    ]
    return sg.Window('Dowloader Vídeo',layout=layout,font=("Bodoni", 10), finalize=True)


def janela_musica():
    sg.theme('Reddit')
    layout = [
    [sg.Text('Digite o Link da música:', size=(24, 0)), sg.Input(key='music', size=(45, 0))], 
    [sg.Text('Selecione a pasta:', size=(24, 0)), sg.InputText('', size= (35, 0),key = 'path'), sg.FolderBrowse('Arquivo', button_color=('#000000','#48D1CC'),font=("Bodoni ", 12),size = (7,0)),],
    [sg.Text(size=(24, 1)), sg.Button('Baixar', font=("Bodoni ", 12), size=(20,1),button_color=('#000000','#48D1CC'))]
    ]
    return sg.Window('Dowloader Music',layout=layout,font=("Bodoni ", 10), finalize=True)


def janela_playlist():
    sg.theme('Reddit')
    layout = [
    [sg.Text('Digite o Link da Playlist:', size=(24, 0)), sg.Input(key = 'playlist', size=(45, 0))],
    [sg.Text('Selecione a pasta:', size=(24, 0)), sg.InputText('', size=(35, 0), key = 'path'), sg.FolderBrowse('Arquivo', button_color=('#000000','#48D1CC'),font=("Bodoni ", 12),size = (7,0)),],
    [sg.Text( size=(24,1)),sg.Button('Baixar',font=("Bodoni ", 12), size=(20,1),button_color=('#000000','#48D1CC'))]
    ]
    return sg.Window('Dowloader Playlist',layout=layout,font=("Bodoni", 10), finalize=True)


#Criar as janelas
janela,JanelaVideo,janelaMusic,janelaPlaylist = janela_inicio(),None,None,None

#ler as janelas
while True:
    window,event,values = sg.read_all_windows()

    

    #quando a janela principal for fechada
    if window == janela and event == sg.WIN_CLOSED:
        break
    #Quando clicar em Música:
    if window == janela and event == 'Música':
        janelaMusic = janela_musica()
        janela.hide()
    #Quando clicar em fechar a tela musica
    if window == janelaMusic and (event == sg.WIN_CLOSED or event == None):
        janelaMusic.hide()
        janela.un_hide()
    #Quando clicar em Baixar da tela Musica
    if window == janelaMusic and event =='Baixar':
        download_music(values)
        janelaMusic.hide()
        janela.un_hide()
    #Quando clicar em Playlist da tela principal
    if window == janela and event == 'Playlist':
        janelaPlaylist = janela_playlist()
        janela.hide()
    #Quando clicar em fechar da tela playlist
    if window == janelaPlaylist and event == sg.WIN_CLOSED:
        janelaPlaylist.hide()
        janela.un_hide()
    #Quando clicar em baixar da tela playlist
    if window == janelaPlaylist and event =='Baixar':
        download_playlist(values)
        janelaPlaylist.hide()
        janela.un_hide()
        #Quando clicar em video da tela principal
    if window == janela and event == 'Vídeo':
        JanelaVideo = janela_video()
        janela.hide()
    #Quando clicar em fechar da tela video
    if window == JanelaVideo and event == sg.WIN_CLOSED:
        JanelaVideo.hide()
        janela.un_hide()
    #Quando clicar em baixar da tela video
    if window == JanelaVideo and event =='Baixar':
        download_video(values)
        JanelaVideo.hide()
        janela.un_hide()