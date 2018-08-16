from vector import Vector


class Settings:
    # TODO: Calculate locations from spacings, etc

    debug = True
    random = True

    screen_size = (1800, 1000)

    tiles_data_file = 'data/tiles.txt'
    tile_size = Vector(48, 48)

    map_columns = 11
    map_rows = 15

    tiles_area_size = Vector(tile_size.x * map_columns, tile_size.y * map_rows)

    line_colour = (127, 127, 127)

    image_path = 'images/'
    light_tiles_path = image_path + 'tiles_light/'
    dark_tiles_path = image_path + 'tiles_dark/'
    light_workers_path = image_path + 'workers_light/'
    dark_workers_path = image_path + 'workers_dark/'
    background_path = image_path + 'backgrounds/'

    worker_circle_size = 4

    light_map_location = Vector(0, 10)
    dark_map_location = Vector(950, 10)

    player_details_location = Vector(570, 10)
    player_details_height = 50
    player_workers_offset = Vector(80, 0)

    workers_per_player = 6
    worker_size = Vector(20, 35)
    worker_space_size = Vector(12, 12)

    next_tile_location = Vector(570, 500)

    active_button_colour = 255, 80, 80

    rotation_button_offset = Vector(tile_size.x + 10, 5)
    rotation_button_size = Vector(30, 25)

    confirmation_button_offset = Vector(tile_size.x + 10, 35)
    confirmation_button_size = Vector(40, 25)

    button_text_offset = Vector(5, 5)
    button_background_colour = (200, 255, 200)


settings = Settings()
