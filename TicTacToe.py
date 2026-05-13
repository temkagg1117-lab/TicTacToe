import turtle
import random

# --- Тоглоомын үндсэн тохиргоо ---
turtle.title("Tic Tac Toe")
turtle.speed(0)
turtle.hideturtle()
screen = turtle.Screen()

# --- Хувьсагчууд ---
board = [' '] * 10
score = {'x': 0, 'o': 0, 'draw': 0}
player1 = 'x'
player2 = 'o'
mode = 1
current_player = None
game_over = False

# --- Талбар зурах ---
def draw_board():
    turtle.clear()
    turtle.pensize(3)
    turtle.color("#333333")

    for x in [100, 200]:
        turtle.penup()
        turtle.goto(x, 0)
        turtle.setheading(90)
        turtle.pendown()
        turtle.forward(300)
        turtle.penup()

    for y in [100, 200]:
        turtle.penup()
        turtle.goto(0, y)
        turtle.setheading(0)
        turtle.pendown()
        turtle.forward(300)
        turtle.penup()

def draw_x(x, y):
    turtle.pensize(3)
    turtle.color("#E74C3C")
    offset = 30
    turtle.penup()
    turtle.goto(x - offset, y - offset)
    turtle.setheading(45)
    turtle.pendown()
    turtle.forward(offset * 2 * 1.414)
    turtle.penup()
    turtle.goto(x + offset, y - offset)
    turtle.setheading(135)
    turtle.pendown()
    turtle.forward(offset * 2 * 1.414)
    turtle.penup()

def draw_circle(x, y):
    turtle.pensize(3)
    turtle.color("#3498DB")
    turtle.penup()
    turtle.goto(x, y - 30)
    turtle.setheading(0)
    turtle.pendown()
    turtle.circle(30)
    turtle.penup()

def draw_win_line(combo):
    turtle.pensize(5)
    turtle.color("#27AE60")
    centers = {
        1: (50, 250), 2: (150, 250), 3: (250, 250),
        4: (50, 150), 5: (150, 150), 6: (250, 150),
        7: (50, 50),  8: (150, 50),  9: (250, 50)
    }
    a, b, c = combo
    x1, y1 = centers[a]
    x2, y2 = centers[c]
    turtle.penup()
    turtle.goto(x1, y1)
    turtle.pendown()
    turtle.goto(x2, y2)
    turtle.penup()

def draw_marker(player, pos):
    centers = {
        1: (50, 250), 2: (150, 250), 3: (250, 250),
        4: (50, 150), 5: (150, 150), 6: (250, 150),
        7: (50, 50),  8: (150, 50),  9: (250, 50)
    }
    x, y = centers[pos]
    if player == 'x':
        draw_x(x, y)
    else:
        draw_circle(x, y)

def draw_score():
    turtle.penup()
    turtle.goto(0, 320)
    turtle.color("#2C3E50")
    turtle.write(
        f"X: {score['x']}  Тэнцэл: {score['draw']}  O: {score['o']}",
        font=("Arial", 14, "bold")
    )

def show_message(msg, y_offset=-30):
    turtle.penup()
    turtle.goto(150, y_offset)
    turtle.color("#8E44AD")
    turtle.write(msg, align="center", font=("Arial", 16, "bold"))

# --- Тоглоомын логик ---
WIN_COMBOS = [
    (1,2,3),(4,5,6),(7,8,9),
    (1,4,7),(2,5,8),(3,6,9),
    (1,5,9),(3,5,7)
]

def check_winner(b, player):
    for combo in WIN_COMBOS:
        a, bb, c = combo
        if b[a] == b[bb] == b[c] == player:
            return combo
    return None

def is_full(b):
    return all(b[i] != ' ' for i in range(1, 10))

# --- Minimax AI (ялагдашгүй) ---
def minimax(b, is_maximizing):
    if check_winner(b, 'o'):
        return 10
    if check_winner(b, 'x'):
        return -10
    if is_full(b):
        return 0

    if is_maximizing:
        best = -1000
        for i in range(1, 10):
            if b[i] == ' ':
                b[i] = 'o'
                best = max(best, minimax(b, False))
                b[i] = ' '
        return best
    else:
        best = 1000
        for i in range(1, 10):
            if b[i] == ' ':
                b[i] = 'x'
                best = min(best, minimax(b, True))
                b[i] = ' '
        return best

def ai_move():
    best_score = -1000
    best_pos = None
    for i in range(1, 10):
        if board[i] == ' ':
            board[i] = 'o'
            score_val = minimax(board, False)
            board[i] = ' '
            if score_val > best_score:
                best_score = score_val
                best_pos = i
    return best_pos

# --- Хулганы клик боловсруулах ---
def get_cell(x, y):
    if not (0 <= x <= 300 and 0 <= y <= 300):
        return None
    col = int(x // 100) + 1
    row = 3 - int(y // 100)
    return (row - 1) * 3 + col

def on_click(x, y):
    global game_over, current_player

    if game_over:
        # Дахин тоглох
        reset_game()
        return

    if current_player != player1:
        return

    cell = get_cell(x, y)
    if cell is None or board[cell] != ' ':
        return

    make_move(player1, cell)

def make_move(player, pos):
    global game_over, current_player

    board[pos] = player
    draw_marker(player, pos)

    combo = check_winner(board, player)
    if combo:
        draw_win_line(combo)
        score[player] += 1
        draw_score()
        winner_name = "Тоглогч X" if player == 'x' else ("Компьютер" if mode == 1 else "Тоглогч O")
        show_message(f"{winner_name} хожлоо! Клик хийж дахин тоглоорой.")
        game_over = True
        return

    if is_full(board):
        score['draw'] += 1
        draw_score()
        show_message("Тэнцэл! Клик хийж дахин тоглоорой.")
        game_over = True
        return

    # Хоёр тоглогчийн горим
    if mode == 2:
        current_player = player2 if player == player1 else player1
        return

    # AI горим — хүн нүүсний дараа AI нүүнэ
    if player == player1:
        current_player = player2
        screen.ontimer(ai_turn, 300)

def ai_turn():
    global current_player
    if game_over:
        return
    pos = ai_move()
    make_move(player2, pos)
    current_player = player1

def reset_game():
    global board, game_over, current_player
    board = [' '] * 10
    game_over = False
    current_player = player1
    draw_board()
    draw_score()

# --- Тохиргоо ---
def setup():
    global mode, player1, player2, current_player

    print("\n╔══════════════════════════╗")
    print("║   Tic Tac Toe тоглоом    ║")
    print("╚══════════════════════════╝\n")
    print("1. Тоглогч VS Компьютер (Minimax AI)")
    print("2. Тоглогч VS Тоглогч")

    while True:
        try:
            mode = int(input("\nСонголтоо оруулна уу (1/2): "))
            if mode in (1, 2):
                break
            print("Зөвхөн 1 эсвэл 2 оруулна уу!")
        except ValueError:
            print("Тоо оруулна уу!")

    while True:
        p = input("Тоглогч 1 тэмдэгтээ сонгоно уу (x/o): ").lower()
        if p in ('x', 'o'):
            player1 = p
            player2 = 'o' if p == 'x' else 'x'
            break
        print("Зөвхөн x эсвэл o оруулна уу!")

    current_player = player1

    if mode == 1:
        print(f"\nТа {player1.upper()} тэмдэгтээр тоглоно. Компьютер {player2.upper()}-ийг тоглоно.")
    else:
        print(f"\nТоглогч 1: {player1.upper()},  Тоглогч 2: {player2.upper()}")

    print("Turtle цонхон дээр нүдэнд клик хийж нүүнэ үү!")
    print("Тоглоом дуусаад дахин тоглохыг хүсвэл цонхонд клик хийнэ үү.\n")

# --- Эхлэх ---
setup()
draw_board()
draw_score()

screen.onclick(on_click)
turtle.done()