from random import randint, choice
from collections import defaultdict

from global_states import g
from settings import settings

from location import Location, WorkerLocation
from simple_logger import log
from components import flip_edge


def draw_starting_tile():
    tile = g.components.filter(starting_tile=True)[0]
    tile.place(
        location=Location(int(settings.map_columns/2), int(settings.map_rows/2)),
        orientation=randint(0, 3) if settings.random else 0
    )


def next_player():
    g.current_player += 1
    if g.current_player == len(g.players):
        g.current_player = 0


def draw_random_tile():
    log('Draw random tile from {} possible tiles'.format(len(g.components.filter(klass='tile', placed=False))))
    return choice(g.components.filter(klass='tile', placed=False)) if settings.random \
        else g.components.filter(klass='tile', placed=False)[0]


def suitable_locations_and_orientations(tile):
    tile_set = {
        orientation: tile.orientated_copy(orientation)
        for orientation in range(4)
    }

    result = []
    for location in g.map.all_locations:
        if g.map[location].tile is None and g.map[location].has_neighbours:
            for o, t in tile_set.items():
                if t.fits(location):
                    result.append((location, o))

    return result


def score_graveyard(worker):
    score = 1
    # TODO: Tidy this up?
    for n in worker.location.tile.location.all_neighbours:
        if g.map[n].tile:
            score += 1
    return score


def find_road_segment(worker_location, backwards=False):
    log('find_road_segment, starting at {}'.format(worker_location))
    # Return a list of WorkerLocation's
    result = []

    # For the first tile we should ignore anything 'before' the starting location
    first_step = True

    # Start from worker_location
    current_location = worker_location

    # Loop until we've hit the end
    while True:
        tile, space = current_location.tile, current_location.space
        log('At {}, {}'.format(tile, space))

        # Find which road the space is on
        # And make a copy of it, so that if we reverse it, it doesn't change the original
        road = [r for r in tile.roads if space in r][0][:]
        log('Which is on road: {}'.format(road))

        # If the road is only 1 long, it means we've reached a start/end segment
        # Add this to the list, then stop
        # For the first tile we still need to check the neighbours - but only in one direction
        if len(road) == 1:
            if first_step:
                if not backwards:
                    # First step, going forwards, we're done
                    log('Road of length 1, first step, going forwards - done')
                    result.append(WorkerLocation(tile, road[0]))
                    return True, result
                else:
                    # First step, going backwards, keep going
                    log('Road of length 1, first step, going backwards so keep going')
            else:
                log('Road of length 1, not the first step - done')
                result.append(WorkerLocation(tile, road[0]))
                return True, result

        # If necessary, follow the road in reverse
        if first_step:
            # If this is our first step, and we should be going backwards, reverse the road
            if backwards:
                log("First step and backwards, reversing the road")
                road.reverse()
                log("Reversed road: {}".format(road))
        else:
            # If we just came from another tile, make sure the road is orientated correctly,
            # The start of the road should be our current space
            if road[0] != current_location.space:
                log('Entry space not the start of the road, reversing the road')
                road.reverse()
                log('Reversed road: {}'.format(road))

        # For the first tile we should ignore anything 'before' the starting location
        if first_step:
            i = road.index(current_location.space)
            road = road[i:]
            log('First step, so ignore rest of the road. New road: {}'.format(road))
            first_step = False

        # Add all of the road's edges to the results list
        for s in road:
            result.append(WorkerLocation(tile, s))

        # Find the neighbour at the edge at the end of the road
        neighbour_location = g.map[tile.location].neighbour_at_edge(road[-1])
        log('Neighbour location at edge {}: {}'.format(road[-1], neighbour_location))

        # If the neighbour is off the map or an empty space
        if neighbour_location is None or not g.map[neighbour_location].tile:
            log('No neighbour found or off the map - done')
            return False, result

        # Move to the neighbour, ready to start again
        current_location = WorkerLocation(g.map[neighbour_location].tile, flip_edge(road[-1]))
        log('Moved to the neighbour {}'.format(current_location))


def find_road_tiles(worker_location):
    log('Getting details for left segment')
    left_segment_complete, left_segment = find_road_segment(worker_location, True)
    if left_segment_complete:
        log('left segment done: ')
    else:
        log('left segment in progress')

    for l in left_segment:
        log(l)

    log('')

    log('Getting details for right segment')
    right_segment_complete, right_segment = find_road_segment(worker_location, False)
    if right_segment_complete:
        log('right segment done: ')
    else:
        log('right segment in progress')

    for l in right_segment:
        log(l)

    log('')

    # There may be an overlap between the left and right segment, but that doesn't matter in the counting
    return left_segment_complete and right_segment_complete, left_segment + right_segment


def score_feature_tiles(feature_complete, feature_locations, scores):
    log('Feature found:')
    tiles, workers = set(), set()
    for l in feature_locations:
        tiles.add(l.tile)
        for worker in g.components.filter(on_tile=l.tile):
            if worker.location.space == l.space:
                workers.add(worker)
        log(l)
    log('')

    # TODO: Use a Counter for this?
    workers_by_player = defaultdict(int)
    for worker in workers:
        workers_by_player[worker.player] += 1

    max_workers_for_player = max(c for c in workers_by_player.values())
    log('Highest number of workers: {}'.format(max_workers_for_player))
    score = 2 * len(tiles) if feature_complete else len(tiles)
    for player, workers_for_player in workers_by_player.items():
        if workers_for_player != max_workers_for_player:
            continue

        log('{} points for player {}'.format(score, player))
        if feature_complete:
            player.removed_workers_score += score
        else:
            scores[player] += score

    if feature_complete:
        log('Feature complete, returning all workers')
        for worker in workers:
            worker.retire()

    return workers


def score_road(worker, scores):
    road_complete, road = find_road_tiles(worker.location)

    return score_feature_tiles(road_complete, road, scores)


def find_city_tiles(worker_location):
    tiles_found = {worker_location.tile}
    locations_found = set()
    city_complete = True

    # Keep a stack of locations that still need checking
    unprocessed = [worker_location]

    # While any more work to be done
    while unprocessed:
        # Grab the next location to check
        current_location = unprocessed.pop()
        tile, space = current_location.tile, current_location.space

        # Find the city this is on
        city = [r for r in tile.cities if space in r][0]

        # Find all the neighbours
        for c in city:
            locations_found.add(WorkerLocation(tile, c))
            # Get the location at that edge
            neighbour_location = g.map[tile.location].neighbour_at_edge(c)

            if not neighbour_location:
                # Off the map, city incomplete
                city_complete = False
                # Off the map, continue
                continue

            neighbour_tile = g.map[neighbour_location].tile

            if not neighbour_tile:
                # Neighbouring city tile missing, city incomplete
                city_complete = False
                # Empty space, continue
                continue

            # Already found, ignore
            if neighbour_tile in tiles_found:
                continue

            # Find the edge on the neighbour which is part of this city
            neighbour_edge = flip_edge(c)

            # To be processed
            unprocessed.append( WorkerLocation(neighbour_tile, neighbour_edge))

            # Found another tile
            tiles_found.add(neighbour_tile)

    return city_complete, locations_found


def score_city(worker, scores):
    # Find all the tiles which make up the city that this worker is standing on
    city_complete, city = find_city_tiles(worker.location)
    # Keep a list of all the tiles we found

    return score_feature_tiles(city_complete, city, scores)


def get_scores():
    log('Calculating scores')
    workers_scored = set()
    result = {
        player: player.removed_workers_score
        for player in g.players
    }
    for worker in g.components.filter(klass='worker', placed=True):
        if worker in workers_scored:
            continue

        workers_scored.add(worker)

        if worker.location.space == 'G':
            worker_score = score_graveyard(worker)
            if worker_score == 9:
                worker.retire()
                worker.player.removed_workers_score += 9
            else:
                result[worker.player] += worker_score
            continue

        if worker.location.tile.edges[worker.location.space] == 'R':
            workers_on_road = score_road(worker, result)
            for worker_on_road in workers_on_road:
                workers_scored.add(worker_on_road)
            continue

        if worker.location.tile.edges[worker.location.space] == 'C':
            workers_in_city = score_city(worker, result)
            for worker_in_city in workers_in_city:
                workers_scored.add(worker_in_city)
            continue

    return result


def worker_space_is_valid(tile, space, player):
    """
    For a temporarily placed tile, for each space, see if it is part of a feature which already has workers
    of another player on it
    """
    if space == 'G':
        return True

    # TODO: This can probably be a bit tidier
    if tile.space_on_road(space):
        _, locations = find_road_tiles(WorkerLocation(tile, space))
    else:
        assert tile.space_in_city(space)
        _, locations = find_city_tiles(WorkerLocation(tile, space))

    for l in locations:
        for worker in g.components.filter(on_tile=l.tile):
            if worker.location.space == l.space and worker.player != player:
                return False

    return True
