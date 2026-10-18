from board import get_legal_moves


def stone(matrix, ai, opponent):
    stone_score = 0
    for row in matrix:
        for cell in row:
            if cell == ai:
                stone_score += 1
            elif cell == opponent:
                stone_score -= 1
    return stone_score


def corner(matrix, ai, opponent, height, width):

    corners = [(0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)]

    corner_score = 0

    for y, x in corners:
        if matrix[y][x] == ai:
            corner_score += 1
        elif matrix[y][x] == opponent:
            corner_score -= 1
    return corner_score


def legal(matrix, ai, opponent):
    vs_legal_move = 0
    ai_moves = get_legal_moves(ai, matrix)
    opponent_moves = get_legal_moves(opponent, matrix)
    vs_legal_move = len(ai_moves) - len(opponent_moves)
    return vs_legal_move


def edge(matrix, ai, opponent, height, width):
    edge_score = 0
    edge_list = []
    for i in range(len(matrix)):
        edge_list.append((0, i))
        edge_list.append((height - 1, i))
        edge_list.append((i, 0))
        edge_list.append((i, width - 1))
    for y, x in edge_list:
        if matrix[y][x] == ai:
            edge_score += 1
        elif matrix[y][x] == opponent:
            edge_score -= 1
    return edge_score


def evaluate_new(matrix, ai, weights):
    opponent = 3 - ai

    height = len(matrix)
    width = len(matrix[0])
    stone_score = stone(matrix, ai, opponent)
    corner_score = corner(matrix, ai, opponent, height, width)
    vs_legal_move = legal(matrix, ai, opponent)
    edge_score = edge(matrix, ai, opponent, height, width)
    return_move = (
        weights["stone"] * stone_score
        + weights["corner"] * corner_score
        + weights["legal"] * vs_legal_move
        + weights["edge"] * edge_score
    )

    return return_move


def evaluate_new_eve5(matrix, ai):
    opponent = 3 - ai

    corner_weight = 10
    stone_weight = 3
    vs_legal_weight = 1
    edge_weight = 7
    height = len(matrix)
    width = len(matrix[0])
    stone_score = stone(matrix, ai, opponent)
    corner_score = corner(matrix, ai, opponent, height, width)
    vs_legal_move = legal(matrix, ai, opponent)
    edge_score = edge(matrix, ai, opponent, height, width)
    return_move = (
        (stone_weight * stone_score)
        + (corner_weight * corner_score)
        + (vs_legal_weight * vs_legal_move)
        + (edge_weight * edge_score)
    )

    return return_move
