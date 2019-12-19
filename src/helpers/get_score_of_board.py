from src.game_objects.building import Building, SpecialBuilding
from src.game_objects.tiles.tile import TimePodTile
from src.game_objects.vek import Vek

# points for each player controlled unit
player_u_pts = 200
# points for each player lost health
player_lost_health_pts = -50
# points for each health point in buildings
building_health_bar_points = 25
# points for each special building
special_building_pts = 100
# points for each vek
vek_pts = -100
# points for each vek lost health
vek_lost_health_pts = 15
# Extra point for having a time pod
time_pod_present = 100
# And extra more for picking it up
time_pod_picked_up = 150
# Penalty for destroyed time pod
time_pod_destroyed = -100


def get_score_of_board(board):
    points = 0
    for x in range(0, board.BOARD_X_SIZE):
        for y in range(0, board.BOARD_Y_SIZE):
            if isinstance(board[(x, y)], TimePodTile):
                points += time_pod_present
            obj = board[(x, y)].get_object()
            if obj is not None and obj.is_player_controlled():
                if obj.is_player_controlled():
                    points += player_u_pts
                    lost_health = obj.get_max_health() - obj.get_health()
                    points += lost_health * player_lost_health_pts

            elif isinstance(obj, Vek):
                points += vek_pts
                lost_health = obj.get_max_health() - obj.get_health()
                points += lost_health * vek_lost_health_pts

            elif isinstance(obj, SpecialBuilding):
                points += special_building_pts
                points += obj.get_health() * building_health_bar_points

            elif isinstance(obj, Building):
                points += obj.get_health() * building_health_bar_points

    if board.is_time_pod_destroyed():
        points += time_pod_destroyed
    elif board.is_time_pod_picked_up():
        points += time_pod_picked_up

    return points
