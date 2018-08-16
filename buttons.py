from drawing import draw_rectangle, draw_text, map_location_to_screen_location
from draw_game import draw_all, worker_space_offset
from settings import settings
from global_states import g


class AbstractButton:
    def clicked(self, mouse_position):
        return self.rect[0] <= mouse_position[0] <= self.rect[0] + self.rect[2] and self.rect[1] <= mouse_position[1] <= self.rect[1] + self.rect[3]


class TilePlacementButton(AbstractButton):
    def __init__(self, location, is_dark):
        self.location = location
        self.is_dark = is_dark

        screen_location = map_location_to_screen_location(self.location, self.is_dark)
        self.rect = screen_location.to_rect(settings.tile_size)

    def draw(self):
        draw_rectangle(self.rect, frame_colour=settings.active_button_colour, width=3)

    def action(self):
        if g.turn_state.next_tile.location:
            g.map[g.turn_state.next_tile.location].tile_in_progress = None
        g.map[self.location].tile_in_progress = g.turn_state.next_tile
        g.turn_state.next_tile.location = self.location
        return True


class TileRotationButton(AbstractButton):
    def __init__(self, is_dark):
        self.is_dark = is_dark

        self.location = map_location_to_screen_location(g.turn_state.next_tile.location, self.is_dark) \
                        + settings.rotation_button_offset

        self.rect = self.location.to_rect(settings.rotation_button_size)

    def draw(self):
        draw_rectangle(self.rect, background_colour=settings.button_background_colour)

        text_location = self.location + settings.button_text_offset
        draw_text(text_location, 'R')

    def action(self):
        """
        Rotate the tile clockwise to the next available rotation
        """
        g.turn_state.rotate_next_tile()
        return True


class ConfirmationButton(AbstractButton):
    def __init__(self, is_dark):
        self.is_dark = is_dark

        self.location = map_location_to_screen_location(g.turn_state.next_tile.location, self.is_dark) \
                        + settings.confirmation_button_offset

        self.rect = self.location.to_rect(settings.confirmation_button_size)

    def draw(self):
        draw_rectangle(self.rect, background_colour=settings.button_background_colour)

        text_location = self.location + settings.button_text_offset
        draw_text(text_location, 'Ok')

    def action(self):
        g.turn_state.next_tile.place(g.turn_state.next_tile.location, g.turn_state.next_tile_orientation)
        if g.turn_state.next_worker_space is not None:
            space = g.turn_state.next_worker_space if g.turn_state.next_worker_space == 'G' \
                else (g.turn_state.next_worker_space + g.turn_state.next_tile_orientation) % 4
            g.turn_state.next_worker.place(g.turn_state.next_tile, space)

        g.turn_state.clear()
        g.turn_state.next_player()

        return True


class WorkerPlacementButton(AbstractButton):
    def __init__(self, space, worker, rotation):
        self.space = space
        self.worker = worker
        self.rotation = rotation

        # TODO: Refactor this into its own function - used in multiple places
        if space != 'G':
            space = (space + rotation) % 4
        worker_offset = worker_space_offset(space)
        self.location = map_location_to_screen_location(g.turn_state.next_tile.location, not self.worker.alive) \
                        + worker_offset

        self.rect = self.location.to_rect(settings.worker_space_size)

    def draw(self):
        draw_rectangle(self.rect, background_colour=g.current_player.colour_code, width=2)

    def action(self):
        g.turn_state.next_worker_space = self.space
        g.turn_state.next_worker = self.worker
        return True


class Buttons:
    def __init__(self):
        self.buttons = []

    def add(self, button):
        self.buttons.append(button)

    def clear(self):
        self.buttons = []

    def draw(self):
        for button in self.buttons:
            button.draw()

    def process_mouse_click(self, mouse_position):
        if any(button.action() for button in self.buttons if button.clicked(mouse_position)):
            draw_all()

        print('mouse clicked at {}'.format(mouse_position))

    @property
    def waiting(self):
        return len(self.buttons) > 0

    def refresh(self):
        """
        Create the correct set of buttons, depending on the game state
        """
        # TODO: Put this somewhere more sensible, i.e. not in buttons.py

        # Start afresh
        self.clear()

        # AI players don't have any buttons
        if g.current_player.AI:
            return

        # If tile was placed, show confirmation button
        if g.turn_state.next_tile and g.turn_state.next_tile.location:
            self.add(ConfirmationButton(False))
            self.add(ConfirmationButton(True))

        # If tile was placed and multiple orientations possible, show rotation button
        if g.turn_state.next_tile and g.turn_state.next_tile.location and len(g.turn_state.possible_orientations) > 1:
            self.add(TileRotationButton(False))
            self.add(TileRotationButton(True))

        # If no worker placed yet, show possible locations
        for location in g.turn_state.possible_locations:
            if not g.turn_state.next_tile.location or g.turn_state.next_tile.location != location:
                self.add(TilePlacementButton(location, False))
                self.add(TilePlacementButton(location, True))

        # If current player has workers available, and next tile placed,
        # and available spots on the tile, show worker placement buttons
        if g.turn_state.next_tile and g.turn_state.next_tile.location:
            workers = []
            for alive in (True, False):
                available_workers = g.current_player.unplaced_workers(alive=alive)
                if available_workers:
                    workers.append(available_workers[0])

            for space in g.turn_state.possible_worker_spaces:
                for worker in workers:
                    # Skip the space where we've just placed a worker, if any
                    if space == g.turn_state.next_worker_space and worker.alive == g.turn_state.next_worker.alive:
                        continue

                    self.add(WorkerPlacementButton(
                        space=space, worker=worker, rotation=g.turn_state.next_tile_orientation
                    ))

        # If tile placed and next_worker selected, show worker placement cancellation button
        # this should return the next worker to the player's supply


g.buttons = Buttons()
