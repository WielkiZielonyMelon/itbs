from src.game_objects.building import Building, SpecialBuilding
from src.game_objects.vek import Vek

# +100 points for each player controlled unit
player_u_pts = 200
# -15 points for each player lost health
player_lost_health_pts = -50
# 25 points for each health point in buildings
building_health_bar_points = 25
# 100 points for each special building
special_building_pts = 100
# -20 points for each vek
vek_pts = -100
# +10 points for each vek lost health
vek_lost_health_pts = +15

# TODO: Should be part of board
def get_score_of_board(board):
    points = 0
    for x in range(0, board.BOARD_MAX_X_SIZE):
        for y in range(0, board.BOARD_MAX_Y_SIZE):
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

            elif isinstance(obj, Building):
                points += obj.get_health() * building_health_bar_points

    return points


def get_best_possible_score_of_board(board):
    points = 0

    for x in range(0, board.BOARD_MAX_X_SIZE):
        for y in range(0, board.BOARD_MAX_Y_SIZE):
            obj = board[(x, y)].get_object()
            if obj is not None and obj.is_player_controlled():
                if obj.is_player_controlled():
                    points += player_u_pts
                    lost_health = obj.get_max_health() - obj.get_health()
                    points += lost_health * player_lost_health_pts

            elif isinstance(obj, SpecialBuilding):
                points += special_building_pts

            elif isinstance(obj, Building):
                points += obj.get_health() * building_health_bar_points

    return points
