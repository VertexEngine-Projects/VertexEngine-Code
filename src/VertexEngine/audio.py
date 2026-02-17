import pygame

class AudioManager:
    """The `AudioManager` class allows you to play audio in your VertexEngine app. It has only 4 functions for sound and music."""
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music = None

    def load_sound(self, name, path):
        """
        This function allows you to load the sound with `name` and `path`.

        # Values
        There's 2 values/perameters for this function: `name` and `path`.
        
        :param name: An identity that points to the file path
        :param path: The actual path to get the audio from.
        """
        self.sounds[name] = pygame.mixer.Sound(path)

    def play_sound(self, name, loops=0):
        if name in self.sounds:
            self.sounds[name].play(loops=loops)

    def load_music(self, path):
        """ This function loads the music track that you will currently use. You cannot have multiple
        tracks playing at once.

        # Values
        There is only 1 value/perameter which is `path`

        ## path
        This refers to the path that we will load the track from. It has to be a filepath instead of a generic path.
        """
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
