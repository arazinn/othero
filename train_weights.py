import json
import random

from board import init_postion, get_legal_moves, serch
from earch_ai import new_ai, DEFAULT_WEIGHTS

# =========================
# 学習設定
# =========================

BOARD_SIZE = 6
DEPTH = 5
POPULATION_SIZE = 5
GENERATIONS = 5

# 乱数を固定し、実験を再現しやすくする
random.seed(42)


# =========================
# 1試合を実行する
# =========================


def play_game(weights_black, weights_white, depth=DEPTH):
    """
    黒(1)と白(2)で1試合行う。
    戻り値：
        winner: 勝者 (1、2、引き分けなら0)
        margin: 黒の石数 - 白の石数
    """

    matrix = init_postion(BOARD_SIZE, BOARD_SIZE)
    current_player = 1
    consecutive_passes = 0

    while consecutive_passes < 2:
        legal_moves = get_legal_moves(current_player, matrix)

        # 着手できなければパス
        if not legal_moves:
            consecutive_passes += 1
            current_player = 3 - current_player
            continue

        consecutive_passes = 0

        # 手番に応じて重みを選ぶ
        if current_player == 1:
            weights = weights_black
        else:
            weights = weights_white

        # AIが着手を選ぶ
        move = new_ai(
            matrix,
            current_player,
            depth=depth,
            weights=weights,
        )

        if move is None:
            raise RuntimeError("合法手があるのにAIが着手を返しませんでした。")

        # 盤面を更新
        if not serch(move, current_player, matrix):
            raise RuntimeError(f"不正な着手です: {move}")

        # 手番交代
        current_player = 3 - current_player

    # 最終的な石数を数える
    black_count = int((matrix == 1).sum())
    white_count = int((matrix == 2).sum())
    margin = black_count - white_count

    if margin > 0:
        winner = 1
    elif margin < 0:
        winner = 2
    else:
        winner = 0

    return winner, margin


# =========================
# 重み候補を作る
# =========================


def mutate_weights(parent):
    """親の重みを少し変えて新しい候補を作る"""

    child = {}

    for name, value in parent.items():
        # 各重みを元の値の±30%程度変化させる
        change = random.uniform(-0.3, 0.3)
        new_value = value * (1 + change)

        # 重みが0以下にならないようにする
        child[name] = max(0.1, round(new_value, 2))

    return child


def create_population(parent, population_size):
    """親を含む候補集団を作る"""

    population = [parent.copy()]

    while len(population) < population_size:
        population.append(mutate_weights(parent))

    return population


# =========================
# 候補同士を対局させる
# =========================


def evaluate_population(population):
    """
    全候補を総当たりで対局させる。
    各組み合わせで先手・後手を入れ替える。
    """

    results = []

    for i, weights_a in enumerate(population):
        points = 0.0
        total_margin = 0

        for j, weights_b in enumerate(population):
            if i == j:
                continue

            # Aが黒、Bが白
            winner, margin = play_game(weights_a, weights_b)

            if winner == 1:
                points += 1.0
            elif winner == 0:
                points += 0.5

            total_margin += margin

            # Bが黒、Aが白
            winner, margin = play_game(weights_b, weights_a)

            if winner == 2:
                points += 1.0
            elif winner == 0:
                points += 0.5

            # この試合ではAは白なので、符号を反転
            total_margin -= margin

        results.append(
            {
                "weights": weights_a,
                "points": points,
                "margin": total_margin,
            }
        )

    # 勝敗ポイントを優先し、同点なら石数差で比較
    results.sort(
        key=lambda result: (
            result["points"],
            result["margin"],
        ),
        reverse=True,
    )

    return results


# =========================
# 学習を実行する
# =========================


def train():
    best_weights = DEFAULT_WEIGHTS.copy()

    print("学習開始")
    print("初期重み:", best_weights)

    for generation in range(1, GENERATIONS + 1):
        print(f"\n===== 世代 {generation} =====")

        population = create_population(
            best_weights,
            POPULATION_SIZE,
        )

        results = evaluate_population(population)

        for rank, result in enumerate(results, start=1):
            print(
                f"{rank}位: "
                f"重み={result['weights']}, "
                f"勝敗ポイント={result['points']}, "
                f"石数差合計={result['margin']}"
            )

        # 最も成績の良い候補を次世代の親にする
        best_weights = results[0]["weights"].copy()

        print("現在の最良重み:", best_weights)

    # 学習結果を保存
    with open(
        "best_weights.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            best_weights,
            file,
            ensure_ascii=False,
            indent=4,
        )

    print("\n学習終了")
    print("最終重み:", best_weights)
    print("best_weights.json に保存しました。")


if __name__ == "__main__":
    train()
