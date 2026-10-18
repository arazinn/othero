import json

from earch_ai import DEFAULT_WEIGHTS
from train_weights import play_game

# 学習前の重み
initial_weights = DEFAULT_WEIGHTS.copy()

# 学習後の重みを読み込む
with open("best_weights.json", "r", encoding="utf-8") as file:
    trained_weights = json.load(file)

# 対戦結果
initial_wins = 0
trained_wins = 0
draws = 0
total_margin = 0

# 先手・後手を入れ替えて10組、合計20局対戦
for game in range(3):
    # 1局目：学習前が黒、学習後が白
    winner, margin = play_game(initial_weights, trained_weights)

    if winner == 1:
        initial_wins += 1
    elif winner == 2:
        trained_wins += 1
    else:
        draws += 1

    total_margin += margin

    # 2局目：学習後が黒、学習前が白
    winner, margin = play_game(trained_weights, initial_weights)

    if winner == 2:
        initial_wins += 1
    elif winner == 1:
        trained_wins += 1
    else:
        draws += 1

    total_margin -= margin

# 結果を表示
print("===== 対戦結果 =====")
print(f"学習前AIの勝利数: {initial_wins}")
print(f"学習後AIの勝利数: {trained_wins}")
print(f"引き分け数: {draws}")
print(f"学習前AIの平均石数差: {total_margin / 20:.2f}")
