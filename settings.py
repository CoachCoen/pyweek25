from vector import Vector


class Settings:
    # TODO: Calculate locations from spacings, etc

    screen_size = (1800, 1000)

    tiles_data_file = 'data/tiles.txt'
    tile_size = Vector(50, 50)

    map_columns = 10
    map_rows = 15

    line_colour = (127, 127, 127)

    image_path = 'images/'
    light_tiles_path = image_path + 'tiles_light/'
    dark_tiles_path = image_path + 'tiles_dark/'
    light_workers_path = image_path + 'workers_light/'
    dark_workers_path = image_path + 'workers_dark/'

    light_map_location = Vector(0, 10)
    dark_map_location = Vector(900, 10)

    player_details_location = Vector(520, 10)
    player_details_height = 50
    player_workers_offset = Vector(80, 0)

    workers_per_player = 6
    worker_size = Vector(20, 35)


settings = Settings()
