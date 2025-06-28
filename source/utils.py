import pygame

# I GOT A LOT OF THESE FROM STACKOVERFLOW BUT I MODIFIED THE FUCK OUT OF THEM TO FIT MY NEEDS FOR THIS PROJECT
# I GOT A LOT OF THESE FROM STACKOVERFLOW BUT I MODIFIED THE FUCK OUT OF THEM TO FIT MY NEEDS FOR THIS PROJECT
# I GOT A LOT OF THESE FROM STACKOVERFLOW BUT I MODIFIED THE FUCK OUT OF THEM TO FIT MY NEEDS FOR THIS PROJECT
# I GOT A LOT OF THESE FROM STACKOVERFLOW BUT I MODIFIED THE FUCK OUT OF THEM TO FIT MY NEEDS FOR THIS PROJECT
# I GOT A LOT OF THESE FROM STACKOVERFLOW BUT I MODIFIED THE FUCK OUT OF THEM TO FIT MY NEEDS FOR THIS PROJECT
# I GOT A LOT OF THESE FROM STACKOVERFLOW BUT I MODIFIED THE FUCK OUT OF THEM TO FIT MY NEEDS FOR THIS PROJECT
# I GOT A LOT OF THESE FROM STACKOVERFLOW BUT I MODIFIED THE FUCK OUT OF THEM TO FIT MY NEEDS FOR THIS PROJECT

# also fyi i did make a lot of these on my ow

# Scaling image without hassle
def size(img, scale):
    w, h = img.get_size()
    return pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))

def lerp(a, b, t):
    return a + (b - a) * t

def get_owner(cell):
    if isinstance(cell, int):
        return cell
    if hasattr(cell, 'owner'):
        return cell.owner
    return None


class Spritesheet:
    def __init__(self, surface):
        self.spritesheet = surface

    def get_image(self, x, y, w, h):
        image = pygame.Surface((w, h), pygame.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), (x, y, w, h))
        return image

# stole this off some nerd on stackoverflow lmao
# tho i did build a lot off of it
class SpriteSheetAtlas(Spritesheet):
    def __init__(self, image_surface, xml_root):
        super().__init__(image_surface)
        self.frames = {}

        for subtexture in xml_root.findall("SubTexture"):
            name = subtexture.attrib["name"]
            x = int(subtexture.attrib["x"])
            y = int(subtexture.attrib["y"])
            width = int(subtexture.attrib["width"])
            height = int(subtexture.attrib["height"])

            self.frames[name] = self.get_image(x, y, width, height)

    def get(self, name):
        return self.frames.get(name, None)

# this is very jank and honestly could be a lil reworked later on
# but idk if i can rework it since i have only 2 days left

# ok tutorial for me and myself on how to add sprite before i forget how to

    # define it and its xml
    # explosion_atlas = SpriteSheetAtlas(
    #     assets["images/explosion.png"],
    #     assets["images/explosion.xml"]
    # )
    #
    # define its position, animations etc
    # explosion_sprite = utils.Sprite(
    #     explosion_atlas,
    #     pos=(600, 300),
    #     animations=["explode bitch"],
    #     scale=1.0,
    #     frame_rate=24  # frames per second for animation speed
    # )

    # and finally we draw it

    # fire_sprite.update(dt)
    # fire_sprite.draw(scene_surface)

class Sprite:
    def __init__(self, atlas, pos, animations=None, scale=1.0, frame_rate=24):
        self.atlas = atlas
        self.pos = pos
        self.scale = scale
        self.frame_rate = frame_rate

        self.animations = self._group_frames() if animations is None else self._load_animations(animations)
        self.current_anim = next(iter(self.animations))
        self.frame_idx = 0
        self.time_accum = 0

    def _group_frames(self):
        anims = {}
        for name in self.atlas.frames:
            base = name.split("000")[0]
            if base not in anims:
                anims[base] = []
            anims[base].append(name)
        for key in anims:
            anims[key].sort()
        return anims

    def _load_animations(self, anim_names):
        anims = {}
        for name in anim_names:
            frames = [key for key in self.atlas.frames if key.startswith(name)]
            frames.sort()
            if frames:
                anims[name] = frames
        return anims

    def play(self, name):
        if name in self.animations and name != self.current_anim:
            self.current_anim = name
            self.frame_idx = 0
            self.time_accum = 0

    def update(self, dt):
        frames = self.animations[self.current_anim]
        self.time_accum += dt
        if self.time_accum >= 1000 / self.frame_rate:
            self.frame_idx = (self.frame_idx + 1) % len(frames)
            self.time_accum = 0

    def draw(self, surface):
        frame_name = self.animations[self.current_anim][self.frame_idx]
        img = self.atlas.get(frame_name)
        if img is None:
            return

        if self.scale != 1.0:
            img = pygame.transform.smoothscale(img,(int(img.get_width() * self.scale), int(img.get_height() * self.scale)))

        # Anchor to a consistent bottom-center, for example
        rect = img.get_rect()
        rect.midbottom = self.pos
        surface.blit(img, rect)

    def get_rect(self):
        img = self.atlas.get(self.animations[self.current_anim][self.frame_idx])
        return pygame.Rect(self.pos, img.get_size()) if img else pygame.Rect(self.pos, (0, 0))


class AnimatedButton:
    def __init__(self, atlas, name, pos, scale=1.0, frame_rate=24):
        self.atlas = atlas
        self.name = name
        self.pos = pos
        self.scale = scale
        self.frame_rate = frame_rate

        self.animations = self._group_frames()
        self.current_anim = f"normal_{self.name}"
        self.frame_idx = 0
        self.time_accum = 0

    def _group_frames(self):
        anims = {}
        for name in self.atlas.frames:
            base = name.split("000")[0]
            if base not in anims:
                anims[base] = []
            anims[base].append(name)
        for key in anims:
            anims[key].sort()
        return anims

    def update(self, dt, mouse_pos):
        rect = self.get_rect()
        hovered = rect.collidepoint(mouse_pos)

        self.current_anim = f"hover_{self.name}" if hovered else f"normal_{self.name}"
        frames = self.animations[self.current_anim]

        self.time_accum += dt
        if self.time_accum >= 1000 / self.frame_rate:
            self.frame_idx = (self.frame_idx + 1) % len(frames)
            self.time_accum = 0

    def draw(self, surface):
        frame_name = self.animations[self.current_anim][self.frame_idx]
        img = self.atlas.get(frame_name)
        if self.scale != 1.0:
            img = pygame.transform.smoothscale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
        surface.blit(img, self.pos)

    def get_rect(self):
        img = self.atlas.get(self.animations[self.current_anim][self.frame_idx])
        return pygame.Rect(self.pos, img.get_size())

class AnimatedButton:
    def __init__(self, atlas, name, pos, scale=1.0, frame_rate=24):
        self.atlas = atlas
        self.name = name
        self.pos = pos
        self.scale = scale
        self.frame_rate = frame_rate

        self.animations = {}
        self.current_anim = None
        self.frame_idx = 0
        self.time_accum = 0

    def add_animation(self, anim_name, prefix):
        frames = [key for key in self.atlas.frames if key.startswith(prefix)]
        frames.sort()
        if frames:
            self.animations[anim_name] = frames
            if self.current_anim is None:
                self.current_anim = anim_name

    def play(self, anim_name):
        if anim_name in self.animations and anim_name != self.current_anim:
            self.current_anim = anim_name
            self.frame_idx = 0
            self.time_accum = 0

    def update(self, dt, mouse_pos):
        rect = self.get_rect()
        hovered = rect.collidepoint(mouse_pos)
        self.play("hover" if hovered else "normal")

        frames = self.animations.get(self.current_anim, [])
        self.time_accum += dt
        if frames and self.time_accum >= 1000 / self.frame_rate:
            self.frame_idx = (self.frame_idx + 1) % len(frames)
            self.time_accum = 0

    def draw(self, surface):
        frames = self.animations.get(self.current_anim, [])
        if not frames:
            return

        img = self.atlas.get(frames[self.frame_idx])
        if self.scale != 1.0:
            img = pygame.transform.smoothscale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
        surface.blit(img, self.pos)

    def get_rect(self):
        frames = self.animations.get(self.current_anim, [])
        img = self.atlas.get(frames[self.frame_idx]) if frames else None
        return pygame.Rect(self.pos, img.get_size()) if img else pygame.Rect(self.pos, (0, 0))

class SM:  # sound manager
    def __init__(self, sound, tag):
        self.sound = sound
        self.tag = tag

    def play(self, loops=0):
        self.sound.play(loops=loops)

    def set_volume(self, volume):
        self.sound.set_volume(volume)

    def stop(self):
        self.sound.stop()

# how 2 use tutoriel:
# add this under your def: drag_debugger = DragDebugger()
# then register whatever sprite you want like so:
# drag_debugger.register("name", thing_you_want_to_move_in_real_time)
# and finally add this at the end of your loop:
# drag_debugger.update()

# if you press f7 it'll print out the positions of each thing you registered
# for text it works similarly however you have to do it like this
# yourtext = DebugText(value, x y, font, color)
# and then you register it pretty much the same way as above

# if youre wondering why you cant find it anywhere in the code
# its because i've already used it then reverted it back
# to before i added it debug text
# but in recap:

# drag_debugger = DragDebugger()
# drag_debugger.register("name", thing_you_want_to_move_in_real_time)
# drag_debugger.update()
# drag_debugger.handle_event(event)

class DragDebugger:
    def __init__(self):
        self.targets = []
        self.dragging = None
        self.offset = (0, 0)

    def register(self, name, obj):
        self.targets.append({
            "name": name,
            "obj": obj,
        })

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for target in reversed(self.targets):  # top-most first
                rect = target["obj"].get_rect()
                if rect.collidepoint(mx, my):
                    self.dragging = target
                    ox = mx - target["obj"].pos[0]
                    oy = my - target["obj"].pos[1]
                    self.offset = (ox, oy)
                    break

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = None

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F7:
            for t in self.targets:
                name = t["name"]
                x, y = t["obj"].pos
                print(f"{name}: ({x}, {y})")

    def update(self):
        if self.dragging:
            mx, my = pygame.mouse.get_pos()
            ox, oy = self.offset
            self.dragging["obj"].pos = (mx - ox, my - oy)

    def draw(self, surface):
        for t in self.targets:
            rect = t["obj"].get_rect()
            pygame.draw.rect(surface, (255, 0, 0), rect, 1)

class DebugText:
    def __init__(self, text, pos, font, color=(255, 255, 255)):
        self.text = text
        self.pos = pos
        self.font = font
        self.color = color
        self.surface = self.font.render(self.text, True, self.color)

    def set_text(self, new_text):
        self.text = new_text
        self.surface = self.font.render(self.text, True, self.color)

    def set_color(self, new_color):
        self.color = new_color
        self.surface = self.font.render(self.text, True, self.color)

    def get_rect(self):
        return self.surface.get_rect(topleft=self.pos)

    def draw(self, surface):
        surface.blit(self.surface, self.pos)

class DebugSprite:
    def __init__(self, surface, pos):
        self.surface = surface
        self.pos = pos

    def get_rect(self):
        rect = self.surface.get_rect()
        rect.topleft = self.pos
        return rect

    def draw(self, screen):
        screen.blit(self.surface, self.pos)
