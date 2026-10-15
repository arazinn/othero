def evaluate(matrix, ai):
    opponent = 1 if ai == 2 else 2

    ai_count = 0
    opponent_count = 0

    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == ai:
                ai_count += 1
            elif matrix[y][x] == opponent:
                opponent_count += 1

    return ai_count - opponent_count
