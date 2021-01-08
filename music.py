import pygame

pygame.init()

mus_lib = {'1': 'data/music/Intro.mp3',
           '2': ''}


class Music:
    def change_music(self, scene_key):
        if scene_key in mus_lib:
            pygame.mixer.music.load(mus_lib[scene_key])
            pygame.mixer.music.play(loops=-1)
