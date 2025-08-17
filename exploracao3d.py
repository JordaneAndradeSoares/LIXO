from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()
window.title = 'Exploração 3D - Ursina'
window.borderless = False
window.fullscreen = False
window.fps_counter.enabled = True

# Luzes
DirectionalLight(y=2, z=3, shadows=True, rotation=(45, -30, 0))
AmbientLight(color=color.rgba(255, 255, 255, 40))

# Chão
chao = Entity(
    model='plane',
    scale=256,
    collider='box',
    texture='white_cube',
    texture_scale=(256, 256),
    color=color.lime.tint(-.35)
)

# Objetos no cenário
decor_parent = Entity()
random.seed(2)
for _ in range(180):
    x = random.uniform(-110, 110)
    z = random.uniform(-110, 110)
    if random.random() < .7:
        tronco = Entity(parent=decor_parent, model='cube', position=(x, .75, z), scale=(.5, 1.5, .5), color=color.rgb(120, 72, 35))
        Entity(parent=decor_parent, model='sphere', position=(x, 2.2, z), scale=2.2, color=color.rgb(30, 120, 30))
    else:
        Entity(parent=decor_parent, model='sphere', position=(x, .5, z), scale=.9, color=color.gray)

# Jogador
player = FirstPersonController(position=(0, 2, 0), speed=6)
player.cursor.color = color.azure

# Obstáculos
for _ in range(60):
    x = random.uniform(-90, 90)
    z = random.uniform(-90, 90)
    h = random.uniform(1.2, 3.5)
    Entity(model='cube', position=(x, h/2, z), scale=(2, h, 2), collider='box', color=color.rgb(100, 100, 110))

# Controle do mapa
mapa_ativo = False
_backup = {}
texto_mapa = Text('MAPA', parent=camera.ui, scale=2, position=(.75, .43), origin=(.5, .5))
texto_mapa.visible = False

def entrar_mapa():
    global mapa_ativo, _backup
    mapa_ativo = True
    _backup = dict(
        fov=camera.fov,
        ortho=camera.orthographic,
        pos=camera.position,
        rot=camera.rotation,
        parent=camera.parent,
        sens=player.mouse_sensitivity,
        speed=player.speed,
        cursor=mouse.locked
    )
    player.mouse_sensitivity = Vec2(0, 0)
    player.speed = 0
    mouse.locked = False
    camera.parent = scene
    camera.orthographic = True
    camera.fov = 20
    camera.position = (player.x, 80, player.z)
    camera.rotation = (90, 0, 0)
    texto_mapa.visible = True

def sair_mapa():
    global mapa_ativo, _backup
    mapa_ativo = False
    camera.fov = _backup['fov']
    camera.orthographic = _backup['ortho']
    camera.position = _backup['pos']
    camera.rotation = _backup['rot']
    camera.parent = _backup['parent']
    player.mouse_sensitivity = _backup['sens']
    player.speed = 6 if _backup['speed'] == 0 else _backup['speed']
    mouse.locked = _backup['cursor']
    texto_mapa.visible = False

def toggle_mapa():
    if mapa_ativo:
        sair_mapa()
    else:
        entrar_mapa()

# Texto de ajuda
ajuda = Text(
    text="[WASD] mover  |  [Space] pular  |  [Shift] correr\n[M] alterna mapa top-down  |  [Esc] sair",
    position=(-.5, .45),
    origin=(-.5, .5),
    background=True
)

def update():
    if mapa_ativo:
        camera.x = lerp(camera.x, player.x, 6 * time.dt)
        camera.z = lerp(camera.z, player.z, 6 * time.dt)

def input(key):
    if key == 'escape':
        application.quit()
    if key == 'm':
        toggle_mapa()
    if key == 'f':
        EditorCamera()

app.run()