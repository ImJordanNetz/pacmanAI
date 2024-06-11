# Jordan Netz
# EPS TICS/AIML
# Jan 16 2024
# The code for minimax and alpha-beta pruning for pacman.

import itertools
import copy

def generate_ghost_move_combinations(game):
    # Possible moves for each ghost (1-4 representing four directions)
    possible_moves = [1, 2, 3, 4]

    # Generating all possible combinations for n ghosts
    all_combinations = list(itertools.product(possible_moves, repeat=len(game.ghost_data)))

    return all_combinations



def heuristic(game):
    # Score based on the number of remaining dots
    score = game.total_starting_dots - len(game.dots)

    # Calculate the average Manhattan distance between Pac-Man and all ghosts
    total_distance = 0
    num_ghosts = len(game.ghost_data)
    map_width = game.grid_square_size_x 
    map_height = game.grid_square_size_y  

    for ghost in game.ghost_data:
        # Calculate the direct Manhattan distance
        direct_distance_x = abs(game.pacman_data["x"] - ghost["x"])
        direct_distance_y = abs(game.pacman_data["y"] - ghost["y"])

        # Adjust for teleportation (wrapping around the map)
        distance_x = min(direct_distance_x, abs(map_width - direct_distance_x))
        distance_y = min(direct_distance_y, abs(map_height - direct_distance_y))

        # Add to the total distance
        total_distance += distance_x + distance_y

    # Compute the average distance
    average_distance = total_distance

    # Incorporate the average distance into the heuristic
    weighted_distance =3* average_distance  #
    score += weighted_distance


    num_ghosts = len(game.ghost_data)
    if num_ghosts < 2:
        # If there are fewer than 2 ghosts, the average distance is not defined
        return 0

    total_distance = 0
    count = 0

    # Iterate over each pair of ghosts
    for i in range(num_ghosts):
        for j in range(i + 1, num_ghosts):
            ghost1 = game.ghost_data[i]
            ghost2 = game.ghost_data[j]

            # Calculate the direct Manhattan distance
            direct_distance_x = abs(ghost1["x"] - ghost2["x"])
            direct_distance_y = abs(ghost1["y"] - ghost2["y"])

            # Adjust for teleportation (wrapping around the map)
            distance_x = min(direct_distance_x, map_width - direct_distance_x)
            distance_y = min(direct_distance_y, map_height - direct_distance_y)

            # Add to the total distance
            total_distance += distance_x + distance_y
            count += 1

    # Compute the average distance
    average_distance = total_distance / count

    score += 0.5*-average_distance
    # Combine the score and the weighted distance
    return score

def generate_ghost_move_combinations(game):
    # Possible moves for each ghost (1-4 representing four directions)
    possible_moves = [1, 2, 3, 4]

    # Generating all possible combinations for n ghosts
    all_combinations = list(itertools.product(possible_moves, repeat=len(game.ghost_data)))

    return all_combinations


def minimax(game, depth, is_maximizing_player):

    if game.running == 0:
        return -1, None

    if depth == 0:
        return heuristic(game), None  # No move to make at depth 0

    if is_maximizing_player:
        best_score = float('-inf')
        best_move = None
        for move in [1, 2, 3, 4]:  # Assuming these are Pac-Man's moves
            new_game = copy.deepcopy(game)
            new_game.pacman_data["dir"] = move
            new_game.move_pacman()
            score, _ = minimax(new_game, depth - 1, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move
    else:  # Minimizing for ghosts
        best_score = float('inf')
        best_move = None
        for moves in generate_ghost_move_combinations(game):
            new_game = game.copy_game_state()
            for ghost_idx, move in enumerate(moves):
                new_game.ghost_data[ghost_idx]["dir"] = move
            new_game.move_ghosts()
            score, _ = minimax(new_game, depth - 1, True)  # Next turn is Pac-Man's
            if score < best_score:
                best_score = score
                best_move = moves  # moves is a tuple representing the moves for all ghosts
        return best_score, best_move


#SAME AI, just using Alpha beta pruning now
def ab_pruning(game, depth, is_maximizing_player, alpha=float('-inf'), beta=float('inf')):
    # Check if the game is over
    if game.running == 0:
        return -1, None

    # Base case: If depth is 0, return the heuristic value of the game
    if depth == 0:
        return heuristic(game), None

    if is_maximizing_player:
        # Initialize best score for maximizing player (Pac-Man) as negative infinity
        best_score = float('-inf')
        best_move = None

        # Iterate through possible moves for Pac-Man
        for move in [1, 2, 3, 4]: 
            # Create a new game state for each move
            new_game = copy.deepcopy(game)
            new_game.pacman_data["dir"] = move
            new_game.move_pacman()

            # Recursive call to minimax for the new state with decreased depth
            score, _ = ab_pruning(new_game, depth - 1, False, alpha, beta)

            # Update best score and best move if a better score is found
            if score > best_score:
                best_score = score
                best_move = move

            # Update alpha value
            alpha = max(alpha, best_score)

            # Alpha-beta pruning condition
            if beta <= alpha:
                break

        return best_score, best_move
    else:  # Minimizing for ghosts
        best_score = float('inf')
        best_move = None

        # Iterate through all possible combinations of ghost moves
        for moves in generate_ghost_move_combinations(game):
            # Create a new game state for each combination of ghost moves
            new_game = game.copy_game_state()
            for ghost_idx, move in enumerate(moves):
                new_game.ghost_data[ghost_idx]["dir"] = move
            new_game.move_ghosts()

            # Recursive call to minimax for the new state with decreased depth
            score, _ = ab_pruning(new_game, depth - 1, True, alpha, beta)

            # Update best score and best move if a better score is found
            if score < best_score:
                best_score = score
                best_move = moves  # Record the moves for all ghosts

            # Update beta value
            beta = min(beta, best_score)

            # Alpha-beta pruning condition
            if beta <= alpha:
                break

        return best_score, best_move





# Using the Minimax function
# game = pacman_game()
# best_score, best_move = minimax(game, 3, True)
# print("Best move:", best_move, "with score:", best_score)



  # Print the first 5 combinations for demonstration

