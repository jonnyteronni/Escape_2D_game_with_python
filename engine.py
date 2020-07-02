#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 17:45:28 2020

@author: jonnyteronni
"""



"""
No coins on the walls

Simple program to show basic sprite usage. Specifically, create coin sprites that
aren't on top of any walls, and don't have coins on top of each other.

Artwork from http://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_no_coins_on_walls
"""
import arcade
import random
import os

SPRITE_SCALING = 0.5
SPRITE_PLAYER_SCALING = 0.2
SPRITE_WALL_SCALING = 0.5
SPRITE_BAG_SCALING = 0.3
SPRITE_SCALING_COIN = 0.2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Escape Game"

NUMBER_OF_COINS = 50

MOVEMENT_SPEED = 5

INIT_GAME_STATE = {
    "key_exit": 0,
    "key_a": 0,
    "key_b": 0,
    "key_c": 0,
    "key_living": 0}

game_state = INIT_GAME_STATE.copy()
class game_class(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite lists
        self.all_sprites_list = None
        self.coin_list = None
        self.wall_list = None
        self.floor_list = None

        # Set up the player
        self.player_sprite = None

        self.physics_engine = None

        # Track the current state of what key is pressed
        self.E_pressed: bool = False
        self.O_pressed: bool = False



    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.door_exit_list = arcade.SpriteList()
        self.door_a_list = arcade.SpriteList()
        self.door_b_list = arcade.SpriteList()
        self.door_c_list = arcade.SpriteList()
        self.door_living_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()


        # Set up the player
        self.player_sprite = arcade.Sprite("character_malePerson_idle.png", SPRITE_PLAYER_SCALING)
        self.player_sprite.center_x = 18 + 32
        self.player_sprite.center_y = 540


        # Set up bag
        self.inventory_sprite = arcade.Sprite("bag.png", SPRITE_BAG_SCALING)
        self.inventory_sprite.center_x = 500
        self.inventory_sprite.center_y = 640

        # MAP design

        # Floor
        for y in range(50,550,32):
            for x in range(18, 760, 32):
                floor = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile016.png", SPRITE_SCALING)
                floor.center_x = x
                floor.center_y = y
                self.floor_list.append(floor)

        # Main walls
        # Vertical left main wall
        for y in range(50, 550, 32):
            wall = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile034.png", SPRITE_WALL_SCALING)
            wall.center_x = 18
            wall.center_y = y
            self.wall_list.append(wall)

        # Vertical right main wall
        for y in range(50, 550, 32):
            wall = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile034.png", SPRITE_SCALING)
            wall.center_x = 754
            wall.center_y = y
            self.wall_list.append(wall)

        # Horizontal top main wall
        for x in range(18, 760, 32):
            wall = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile034.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 562
            self.wall_list.append(wall)
        # Horizontal bottom main wall with exit door
        for x in range(18, 760, 32):
            wall = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile034.png", SPRITE_SCALING)
            door = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile048.png", SPRITE_SCALING)
            # Leave space for door if is equal to third block
            if x == 18+32*2:
                door.center_x = x
                door.center_y = 50
                self.door_exit_list.append(door)
            else:
                wall.center_x = x
                wall.center_y = 50
                self.wall_list.append(wall)

        # Build Room A
        # Walls Room A
        # Vertical wall Room A
        for y in range(402, 550, 32):
            wall = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile034.png", SPRITE_SCALING)
            wall.center_x = 18 + 32*5
            wall.center_y = y
            self.wall_list.append(wall)

        # Horizontal wall  Room A
        for x in range(18 + 32, 32*4, 32):
            wall = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile034.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 402
            self.wall_list.append(wall)

        #Furniture Room A
        self.sofa_a_sprinte = arcade.Sprite("kenney_topdown-shooter/PNG/Tiles/tile_450.png", SPRITE_SCALING)
        self.sofa_a_sprinte.center_x = 18 + 32
        self.sofa_a_sprinte.center_y = 402 + 32

        # Door Room A
        door_a = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile052.png", SPRITE_SCALING)
        door_a.center_x = 18 + 32*4
        door_a.center_y = 402
        self.door_a_list.append(door_a)

        # Build Room B
        # Walls Room B
        # Vertical wall Room B
        for y in range(402, 550, 32):
            wall = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile034.png", SPRITE_SCALING)
            wall.center_x = 18 + 32*10
            wall.center_y = y
            self.wall_list.append(wall)

        # Horizontal wall  Room B
        for x in range(18 + 32*5, 32*9, 32):
            wall = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile034.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 402
            self.wall_list.append(wall)

        # Door Room B
        door_b = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile050.png", SPRITE_SCALING)
        door_b.center_x = 18 + 32*9
        door_b.center_y = 402
        self.door_b_list.append(door_b)

        #Furniture Room B
        self.plant_b_sprinte = arcade.Sprite("kenney_topdown-shooter/PNG/Tiles/tile_134.png", SPRITE_SCALING)
        self.plant_b_sprinte.center_x = 18 + 32*9
        self.plant_b_sprinte.center_y = 402 + 32*3

        # Build Room C
        # Walls Room C
        # Vertical wall Room C
        for y in range(50+32*4, 402-32*2, 32):
            wall = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile034.png", SPRITE_SCALING)
            wall.center_x = 18 + 32*10
            wall.center_y = y
            self.wall_list.append(wall)

        # Top horizontal wall Room C
        for x in range(18 + 32*2, 32*10, 32):
            wall = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile034.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 402-32*3
            self.wall_list.append(wall)

        # Top bottom wall Room C
        for x in range(18 + 32, 32*11, 32):
            wall = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile034.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 402-32*7
            self.wall_list.append(wall)

        # Door Room C
        door_c = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile049.png", SPRITE_SCALING)
        door_c.center_x = 18 + 32
        door_c.center_y = 402-32*3
        self.door_c_list.append(door_c)

        # Build Living Room
        # Walls Living Room
        # Vertical wall Living Room
        for y in range(50+32, 50+32*3, 32):
            wall = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile034.png", SPRITE_SCALING)
            wall.center_x = 18 + 32*10
            wall.center_y = y
            self.wall_list.append(wall)

        # Door Room Living Room
        door_living = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile051.png", SPRITE_SCALING)
        door_living.center_x = 18 + 32*10
        door_living.center_y = 50+32*3
        self.door_living_list.append(door_living)

        #Furniture Living Room
        self.plant_living_sprinte = arcade.Sprite("kenney_simplifiedplatformer/PNG/Tiles/platformPack_tile045.png", SPRITE_SCALING)
        self.plant_living_sprinte.center_x = 18 + 32*22
        self.plant_living_sprinte.center_y = 50 + 32



        # -- Randomly place coins where there are no walls
        # Create the coiself.door_list.draw()ns
        for i in range(NUMBER_OF_COINS):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)

            # --- IMPORTANT PART ---

            # Boolean variable if we successfully placed the coin
            coin_placed_successfully = False

            # Keep trying until success
            while not coin_placed_successfully:
                # Position the coin
                coin.center_x = random.randrange(SCREEN_WIDTH)
                coin.center_y = random.randrange(SCREEN_HEIGHT)

                # See if the coin is hitting a wall
                wall_hit_list = arcade.check_for_collision_with_list(coin, self.wall_list)

                # See if the coin iswall hitting another coin
                coin_hit_list = arcade.check_for_collision_with_list(coin, self.coin_list)

                # Coin needs to be on the floor
                floor_hit_list = arcade.check_for_collision_with_list(coin, self.floor_list)

                if len(wall_hit_list) == 0 and len(coin_hit_list) == 0 and len(floor_hit_list) > 0:
                    # It is!
                    coin_placed_successfully = True

            # Add the coin to the lists
            self.coin_list.append(coin)

            # --- END OF IMPORTANT PART ---

        self.physics_engine_wall = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        if game_state["key_exit"] != 1:
            self.physics_engine_door_exit = arcade.PhysicsEngineSimple(self.player_sprite, self.door_exit_list)
        if game_state["key_a"] != 1:
            self.physics_engine_door_a = arcade.PhysicsEngineSimple(self.player_sprite, self.door_a_list)
        if game_state["key_b"] != 1:
            self.physics_engine_door_b = arcade.PhysicsEngineSimple(self.player_sprite, self.door_b_list)
        if game_state["key_c"] != 1:
            self.physics_engine_door_c = arcade.PhysicsEngineSimple(self.player_sprite, self.door_c_list)
        if game_state["key_living"] != 1:
            self.physics_engine_door_living = arcade.PhysicsEngineSimple(self.player_sprite, self.door_living_list)
        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.floor_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.door_exit_list.draw()
        self.door_a_list.draw()
        self.door_b_list.draw()
        self.door_c_list.draw()
        self.door_living_list.draw()
        self.sofa_a_sprinte.draw()
        self.plant_living_sprinte.draw()
        self.plant_b_sprinte.draw()
        self.inventory_sprite.draw()
        self.player_sprite.draw()

        # Draw keys on inventory next to bag image
        if game_state["key_exit"] == 1:
            self.key_exit_sprite.draw()
        if game_state["key_a"] == 1:
            self.key_a_sprite.draw()
        if game_state["key_b"] == 1:
            self.key_b_sprite.draw()
        if game_state["key_c"] == 1:
            self.key_c_sprite.draw()
        if game_state["key_living"] == 1:
            self.key_living_sprite.draw()


        if self.E_pressed:
            # If player is over a key it will return True
            # Find key A on sofa on room A
            key_a_hit = arcade.check_for_collision(self.player_sprite, self.sofa_a_sprinte)
            if key_a_hit:
                game_state["key_a"] = 1
                #arcade.draw_text("You found key A", SCREEN_WIDTH, SCREEN_HEIGHT-100, arcade.color.WHITE, font_size=40, anchor_x="center")
                #self.key_a_sprite.remove_from_sprite_lists()
                self.key_a_sprite = arcade.Sprite("kenney_simplifiedplatformer/PNG/Items/platformPack_item016.png", SPRITE_SCALING)
                self.key_a_sprite.center_x = 560
                self.key_a_sprite.center_y = 640
                # Play a sound
                # arcade.play_sound(self.collect_coin_sound)

            # Find key B on plant on living room
            key_b_hit = arcade.check_for_collision(self.player_sprite, self.plant_living_sprinte)
            if key_b_hit:
                game_state["key_b"] = 1
                #arcade.draw_text("You found key A", SCREEN_WIDTH, SCREEN_HEIGHT-100, arcade.color.WHITE, font_size=40, anchor_x="center")
                #self.key_a_sprite.remove_from_sprite_lists()
                self.key_b_sprite = arcade.Sprite("kenney_simplifiedplatformer/PNG/Items/platformPack_item014.png", SPRITE_SCALING)
                self.key_b_sprite.center_x = 560 + 32
                self.key_b_sprite.center_y = 640

            # Find key c on plant on room B
            key_c_hit = arcade.check_for_collision(self.player_sprite, self.plant_b_sprinte)
            if key_c_hit:
                game_state["key_c"] = 1
                #arcade.draw_text("You found key A", SCREEN_WIDTH, SCREEN_HEIGHT-100, arcade.color.WHITE, font_size=40, anchor_x="center")
                #self.key_a_sprite.remove_from_sprite_lists()
                self.key_c_sprite = arcade.Sprite("kenney_simplifiedplatformer/PNG/Items/platformPack_item013.png", SPRITE_SCALING)
                self.key_c_sprite.center_x = 560 + 32*2
                self.key_c_sprite.center_y = 640
        #if self.O_pressed:

                # Set up keys

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.E:
            self.E_pressed = True
        elif key == arcade.key.O:
            self.O_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.E:
            self.E_pressed = False
        elif key == arcade.key.O:
            self.O_pressed = False

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine_wall.update()
        if game_state["key_a"] != 1:
            self.physics_engine_door_a.update()

        elif game_state["key_b"] != 1:
            self.physics_engine_door_b.update()
            self.physics_engine_door_c.update()
            self.physics_engine_door_living.update()

        elif game_state["key_c"] != 1:
            self.physics_engine_door_c.update()
            self.physics_engine_door_living.update()

        elif game_state["key_living"] != 1:
            self.physics_engine_door_living.update()

        elif game_state["key_exit"] != 1:
            self.physics_engine_door_exit.update()




        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            #arcade.play_sound(self.collect_coin_sound)




def main():
    """ Main method """
    window = game_class(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
