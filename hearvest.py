def evaluate_old(matrix, ai):
    """旧評価関数：石の枚数差"""
    opponent = 3 - ai
    score = 0

    for row in matrix:
        for cell in row:
            if cell == ai:
                score += 1
            elif cell == opponent:
                score -= 1

    return score


def evaluate_new(matrix, ai):
    """新評価関数：石の枚数差＋角の評価"""
    opponent = 3 - ai

    stone_score = 0
    for row in matrix:
        for cell in row:
            if cell == ai:
                stone_score += 1
            elif cell == opponent:
                stone_score -= 1

    height = len(matrix)
    width = len(matrix[0])

    corners = [(0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)]

    corner_score = 0
    for y, x in corners:
        if matrix[y][x] == ai:
            corner_score += 10
        elif matrix[y][x] == opponent:
            corner_score -= 10

    return stone_score + corner_score
