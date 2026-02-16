import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music = None

    def load_sound(self, name, path):
        self.sounds[name] = pygame.mixer.Sound(path)

    def play_sound(self, name, loops=0):
        if name in self.sounds:
            self.sounds[name].play(loops=loops)

    def load_music(self, path):
        self.music = path
        pygame.mixer.music.load(path)

    def play_music(self, loops=-1):
        """Music uses the `.mp3` format. It is a way to play looping music.

        # Values
        There is only 1 value/perameter which is `loops`

        ## loops
        loops is how many times it will loop, 0 means the music only plays once
        -1 means it loops forever until `stop_music()` manually cancells it.

        """
        if self.music:
            pygame.mixer.music.play(loops=loops)

    def stop_music(self):
        pygame.mixer.music.stop()
