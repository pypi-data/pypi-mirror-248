import pygame
from tkinter import Tk, filedialog

pygame.init()

defaults = {
    "unselect":(190,227,219),
    "hover": (137,176,174),
    "select": (85,91,110),

    "txt": (0, 0, 0),
    "prompt": (30, 30, 30)
}

class textBox:
    def __init__(self, x, y, width=140, height=32, prompt="", fontSize=32, theme=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.finalText = ""
        self.font = pygame.font.Font(None, fontSize)
        self.selected = False
        self.hovering = False
        self.prompt = prompt
        self.theme = theme or defaults

    def draw(self, screen):
        cUnselect = self.theme['unselect']
        cHover = self.theme['hover']
        cSelect = self.theme['select']

        cText = self.theme['txt']
        cPrompt = self.theme['prompt']

        if self.selected:
            self.colour = cSelect
        elif self.hovering:
            self.colour = cHover
        else:
            self.colour = cUnselect

        pygame.draw.rect(screen, self.colour, self.rect, 2)
        if self.text:
            textSurface = self.font.render(self.text, True, cText)
        else:
            textSurface = self.font.render(self.prompt, True, cPrompt)
        screen.blit(textSurface, (self.rect.x + 5, self.rect.y + 5))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.selected = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self.hovering = self.rect.collidepoint(event.pos)  # Moved from the if condition
        elif event.type == pygame.KEYDOWN and self.selected:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.finalText = self.text
                self.text = ""
                self.selected = False
            else:
                self.text += event.unicode

class slider:
    def __init__(self, x, y, width, height=32, maxValue=100, theme=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.maxValue = maxValue
        self.theme = theme or defaults

        self.dragging = False

        self.value = maxValue
        self.percent = 100
        self.knobRad = self.height
        self.knobColour = self.theme["unselect"]

    def draw(self, screen):
        pygame.draw.rect(screen, self.theme["hover"], (self.x, self.y, self.width, self.height))

        knobX = int(self.x + self.width * (self.value / self.maxValue))
        pygame.draw.circle(screen, self.knobColour, (knobX, self.y + self.height // 2), self.knobRad)

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the click is within the slider's bounds
            if self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height:
                self.knobColour = self.theme["select"]
                self.dragging = True  # Start dragging
                # Just looks nicer to have it set where clicked instead of just when moving
                self.value = int((event.pos[0] - self.x) / self.width * self.maxValue)
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Update the current value based on the mouse position while dragging
                self.value = int((event.pos[0] - self.x) / self.width * self.maxValue)
                # Ensure the current value is within bounds
                self.value = max(0, min(self.value, self.maxValue))
        elif event.type == pygame.MOUSEBUTTONUP:
            self.knobColour = self.theme["unselect"]
            self.dragging = False  # Stop dragging when the mouse button is released

        self.percent = round((self.value/self.maxValue)*100, 2)

class button:
    def __init__(self, x, y, action, path=None, toggleable=False, scale=1.0):
        self.x = x
        self.y = y
        self.action = action
        self.toggleable = toggleable

        self.hovering = False
        self.selected = False

        if path:
            self.texture = pygame.image.load(path)
            self.texture = pygame.transform.scale(self.texture, (self.texture.get_width()*scale, self.texture.get_height()*scale))
        else:
            self.texture = pygame.Surface((50, 50))
            self.texture.fill((255, 255, 255))

    def draw(self, screen):
        darken = 1
        if self.selected:
            darken = 0.5
        elif self.hovering:
            darken = 0.7
        darkenedTex = self.darkenTexture(self.texture, darken)
        screen.blit(darkenedTex, (self.x, self.y))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.x <= event.pos[0] <= self.x + self.texture.get_width() and \
               self.y <= event.pos[1] <= self.y + self.texture.get_height():
                if self.toggleable:
                    self.selected = not self.selected  # Toggle the selected state
                    self.action()
                else:
                    self.selected = True  # Set to selected if not toggleable
                    self.action()
        elif event.type == pygame.MOUSEMOTION:
            if self.x <= event.pos[0] <= self.x + self.texture.get_width() and \
               self.y <= event.pos[1] <= self.y + self.texture.get_height():
                self.hovering = True
            else:
                self.hovering = False
        elif event.type == pygame.MOUSEBUTTONUP and not self.toggleable:
            self.selected = False

    def darkenTexture(self, texture, darken):
        darkenedTexture = texture.copy()
        darkenedTexture.fill((darken * 255, darken * 255, darken * 255), special_flags=pygame.BLEND_MULT)
        return darkenedTexture
    
class checkBox:
    def __init__(self, x, y, action, textures=None, scale=1.0):
        self.x = x
        self.y = y
        self.action = action

        # Set default textures if not provided
        self.textures = textures or {
            "on": pygame.Surface((50, 50)),
            "off": pygame.Surface((20, 20)),
        }

        # Fill default textures if not provided
        for key in self.textures:
            if not self.textures[key]:
                self.textures[key].fill((255, 255, 255))
            else:
                self.textures[key] = pygame.transform.scale(self.textures[key], (self.textures[key].get_width()*scale, self.textures[key].get_height()*scale))

        self.state = "off"
        self.hovering = False

    def draw(self, screen):
        darken = 0.7 if self.state == "on" or self.hovering else 1
        darkened_tex = self.darken_texture(self.textures[self.state], darken)
        screen.blit(darkened_tex, (self.x, self.y))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.x <= event.pos[0] <= self.x + self.textures["on"].get_width() and \
               self.y <= event.pos[1] <= self.y + self.textures["on"].get_height():
                self.state = "on" if self.state == "off" else "off"  # Toggle state
                self.action()

        elif event.type == pygame.MOUSEMOTION:
            if self.x <= event.pos[0] <= self.x + self.textures["on"].get_width() and \
               self.y <= event.pos[1] <= self.y + self.textures["on"].get_height():
                self.hovering = True
            else:
                self.hovering = False

    def darken_texture(self, texture, darken):
        darkened_texture = texture.copy()
        darkened_texture.fill((darken * 255, darken * 255, darken * 255), special_flags=pygame.BLEND_MULT)
        return darkened_texture
    
class fileUploader:
    def __init__(self, x, y, width=140, height=32, fontSize=32, fileOnly=True, theme=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fileOnly = fileOnly
        self.theme = theme or defaults
        self.text = "Select a file" if fileOnly else "Select a file/folder"
        self.font = pygame.font.Font(None, fontSize)
        self.selected = False
        self.hovering = False

    def draw(self, screen):
        cUnselect = self.theme['unselect']
        cHover = self.theme['hover']
        cSelect = self.theme['select']
        cText = self.theme['txt']

        if self.selected:
            color = cSelect
        elif self.hovering:
            color = cHover
        else:
            color = cUnselect

        pygame.draw.rect(screen, color, self.rect)
        textSurface = self.font.render(self.text, True, cText)
        screen.blit(textSurface, (self.rect.x + 5, self.rect.y + 5))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.selected = self.rect.collidepoint(event.pos)
            if self.selected:
                self.browseFile()

        elif event.type == pygame.MOUSEMOTION:
            self.hovering = self.rect.collidepoint(event.pos)

    def browseFile(self):
        root = Tk()
        root.withdraw()  # Hide the main window

        # Configure the file dialog based on fileOnly parameter
        filetypes = [("All Files", "*.*")] if self.fileOnly else []

        filePath = filedialog.askopenfilename(
            title="Select a file" if self.fileOnly else "Select a file or folder",
            filetypes=filetypes,
            initialdir="/",  # You can set the initial directory if needed
        )

        root.destroy()  # Close the hidden main window

        if filePath:
            print("Selected file or folder:", filePath)