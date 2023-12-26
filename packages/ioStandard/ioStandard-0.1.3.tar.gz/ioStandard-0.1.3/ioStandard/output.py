import pygame

defaults = {
    "unselect":(190,227,219),
    "hover": (137,176,174),
    "select": (85,91,110),

    "txt": (0, 0, 0),
    "prompt": (30, 30, 30)
}

class text:
    def __init__(self, x, y, text="", theme=None, fontSize = 32):
        self.rect = pygame.Rect(x, y, 0, 0)
        self.text = text
        self.font = pygame.font.Font(None, fontSize)

        self.theme = theme or defaults

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.theme["txt"])
        screen.blit(text_surface, (self.rect.x, self.rect.y))

class progressBar:
    def __init__(self, x, y, width, height=32, progress=0, maxValue=100, theme=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.progress = progress
        self.maxValue = maxValue
        self.theme = theme or defaults

    def draw(self, screen):
        pygame.draw.rect(screen, self.theme["unselect"], (self.x, self.y, self.width, self.height))

        progressWidth = int(self.width * (self.progress / self.maxValue))
        pygame.draw.rect(screen, self.theme["select"], (self.x, self.y, progressWidth, self.height))

    def setValue(self, progress):
        self.progress = max(0, min(progress, self.maxValue))