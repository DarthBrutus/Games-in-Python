from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise

app = Ursina()
grass_texture = load_texture('grass')
stone_texture = load_texture('Assets/stone_block.png')
dirt_texture  = load_texture('Assets/dirt_block.png')
brick_texture  = load_texture('Assets/brick_block.png')
arm_texture   = load_texture('Assets/arm_texture.png')
punch_sound   = Audio('assets/punch_sound',loop = False, autoplay = False)
block_pick = 1
noise = PerlinNoise(octaves = 2, seed = 101)
freq = 25
amp  = 5
window.borderless = False

window.fps_counter.enabled = False
window.exit_button.visible = False

def update():
	global block_pick

	if held_keys['left mouse'] or held_keys['right mouse']:
		hand.active()
	else:
		hand.passive()

	if held_keys['1']: block_pick = 1
	if held_keys['2']: block_pick = 2
	if held_keys['3']: block_pick = 3
	if held_keys['4']: block_pick = 4

class Voxel(Button):
	def __init__(self, position = (0,0,0), texture = grass_texture, color = color.color(0,0,random.uniform(0.9,1)), model = load_model('Assets/block')):
		super().__init__(
			parent = scene,
			position = position,
			model = load_model('Assets/block'),
			origin_y = 0.5,
			texture = texture,
			color = color,
			scale = 0.5)

	def input(self,key):
		if self.hovered:
			if key == 'left mouse down':
				punch_sound.play()
				if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
				if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
				if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
				if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)

			if key == 'right mouse down':
				punch_sound.play()
				destroy(self)

class Hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/arm',
			texture = arm_texture,
			scale = 0.2,
			rotation = Vec3(150,-10,0),
			position = Vec2(0.4,-0.6))

	def active(self):
		self.position = Vec2(0.3,-0.5)

	def passive(self):
		self.position = Vec2(0.4,-0.6)
  
terrain = Entity(model = None, collider = None)
terrain_width = 50
for i in range(terrain_width ** 2):
    voxel = Voxel()
    voxel.x = floor(i / terrain_width)
    voxel.z = floor(i % terrain_width)
    voxel.y = floor(noise([voxel.x / freq, voxel.z / freq]) * amp)

player = FirstPersonController()
sky = Sky(texture = 'sky_sunset')
hand = Hand()
terrain.combine()
terrain.collider = 'mesh'

print('''Grass: 1
        Stone: 2
        Brick: 3
        Dirt: 4''')

app.run()