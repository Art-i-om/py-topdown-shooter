import moderngl
import pygame
from enemy import *
from settings import *
from array import array


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.quad_buffer = game.ctx.buffer(data=array('f', [
            -1.0, 1.0, 0.0, 0.0,  # Top left
            1.0, 1.0, 1.0, 0.0,  # Top right
            -1.0, -1.0, 0.0, 1.0,  # Bottom left
            1.0, -1.0, 1.0, 1.0   # Bottom right
        ]))

        # Main screen shaders
        vert_shader = open('shaders/vertex_shader.glsl').read()
        frag_shader = open('shaders/fragment_shader.glsl').read()
        self.program = game.ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
        self.render_object = game.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texCoord')])

        # Bullet-specific shaders and rendering setup
        try:
            bullet_vert_shader = open('shaders/bullet_vertex_shader.glsl').read()
            bullet_frag_shader = open('shaders/bullet_fragment_shader.glsl').read()
            self.bullet_program = game.ctx.program(vertex_shader=bullet_vert_shader, fragment_shader=bullet_frag_shader)

            # Bullet trail shaders
            trail_vert_shader = open('shaders/bullet_trail_vertex_shader.glsl').read()
            trail_frag_shader = open('shaders/bullet_trail_fragment_shader.glsl').read()
            self.trail_program = game.ctx.program(vertex_shader=trail_vert_shader, fragment_shader=trail_frag_shader)

            # Create bullet quad buffer
            self.bullet_quad_buffer = game.ctx.buffer(data=array('f', [
                -1.0, 1.0, 0.0, 0.0,  # Top left
                1.0, 1.0, 1.0, 0.0,   # Top right
                -1.0, -1.0, 0.0, 1.0, # Bottom left
                1.0, -1.0, 1.0, 1.0   # Bottom right
            ]))
            self.bullet_render_object = game.ctx.vertex_array(self.bullet_program, [(self.bullet_quad_buffer, '2f 2f', 'vert', 'texCoord')])
            self.trail_render_object = game.ctx.vertex_array(self.trail_program, [(self.bullet_quad_buffer, '2f 2f', 'vert', 'texCoord')])
            self.bullet_shaders_loaded = True
        except Exception as e:
            print(f"Failed to load bullet shaders: {e}")
            self.bullet_shaders_loaded = False

        self.player = game.player
        self.map = game.map

        # test params for ModernGL textures
        # =================================
        self.time = 0
        self.shake_intensity = 0.0
        self.health_effect = 0.0
        self.chromatic_aberration = 0.0
        # =================================

        self.frame_texture = self.game.ctx.texture(self.game.display.get_size(), 4)
        self.frame_texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.frame_texture.swizzle = 'BGRA'

        self.game.enemies = []

        add_enemy = self.add_enemy

        add_enemy(Kamikaze(game, pos=(HALF_WIDTH + 400, HALF_HEIGHT)))
        add_enemy(Kamikaze(game, pos=(HALF_WIDTH - 400, HALF_HEIGHT)))

    def surface_to_texture(self, surface):
        self.frame_texture.write(surface.get_view('1'))
        return self.frame_texture

    def draw_game_state(self):
        self.draw_map()
        self.draw_player()
        self.draw_bullet()
        self.draw_enemies()

        self.time += 1
        self.update_effects()

        self.apply_to_display()

    def draw_game_over_state(self):
        self.game.game_over.draw_to_surface()

        self.time = 0

        self.apply_to_display()

    def apply_to_display(self):
        self.surface_to_texture(self.game.display)
        self.frame_texture.use(0)
        self.program['tex'] = 0
        self.program['time'] = self.time
        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)

        pygame.display.flip()

    def draw_player(self):
        self.game.player.draw()

    def draw_bullet(self):
        if self.game.bullet and self.game.bullet.alive:
            if self.bullet_shaders_loaded:
                self.draw_bullet_with_shader()
            else:
                # Fallback to original bullet drawing
                self.game.bullet.draw()

    def draw_bullet_with_shader(self):
        """Draw bullet using dedicated bullet shaders with special effects"""
        bullet = self.game.bullet

        # Enable blending for transparency effects
        self.game.ctx.enable(moderngl.BLEND)
        self.game.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA

        # Draw trail first (behind the bullet)
        self.draw_bullet_trail()

        # Set bullet shader uniforms
        self.bullet_program['time'] = self.time
        self.bullet_program['position'] = (bullet.x, bullet.y)
        self.bullet_program['scale'] = (BULLET_SIZE / 2, BULLET_SIZE / 2)
        self.bullet_program['screen_size'] = (WIDTH, HEIGHT)
        self.bullet_program['bullet_color'] = (0.3, 0.8, 1.0)  # Cyan-blue color
        self.bullet_program['intensity'] = 1.0

        # Render the main bullet
        self.bullet_render_object.render(mode=moderngl.TRIANGLE_STRIP)

        # Disable blending
        self.game.ctx.disable(moderngl.BLEND)

    def draw_bullet_trail(self):
        """Draw the bullet trail using trail shaders"""
        bullet = self.game.bullet

        if not bullet.trail:
            return

        # Draw each trail segment
        for i, trail_pos in enumerate(bullet.trail):
            # Set trail shader uniforms
            self.trail_program['time'] = self.time
            self.trail_program['position'] = (trail_pos.centerx, trail_pos.centery)
            self.trail_program['scale'] = (BULLET_SIZE / 2, BULLET_SIZE / 2)
            self.trail_program['screen_size'] = (WIDTH, HEIGHT)
            self.trail_program['bullet_color'] = (0.3, 0.8, 1.0)  # Same color as bullet
            self.trail_program['trail_index'] = float(i)
            self.trail_program['max_trail_length'] = float(bullet.max_trail_length)

            # Render this trail segment
            self.trail_render_object.render(mode=moderngl.TRIANGLE_STRIP)

    def draw_enemies(self):
        for enemy in self.game.enemies:
            enemy.draw()

    def add_enemy(self, enemy: Enemy):
        self.game.enemies.append(enemy)

    def draw_map(self):
        [pygame.draw.rect(self.game.display, DARKGRAY, (pos[0] * 100, pos[1] * 100, 100, 100))
         for pos in self.map.world_map]

    def update_effects(self):
        pass
