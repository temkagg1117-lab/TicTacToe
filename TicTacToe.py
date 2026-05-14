import random
import turtle

def setup_turtle():
    turtle.clearscreen()
    turtle.title("Tic Tac Toe")
    turtle.speed(0)
    turtle.hideturtle()

def draw_board():
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

def draw_marker(player, pos):
    col = pos % 3
    row = pos // 3
    x = col * 100 + 50
    y = (2 - row) * 100 + 50
    if player == 'x':
        draw_x(x, y)
    else:
        draw_circle(x, y)

def draw_horizontal_line(y):
    turtle.pensize(5)
    turtle.color("green")
    turtle.penup()
    turtle.goto(0, y)
    turtle.setheading(0)
    turtle.pendown()
    turtle.forward(300)
    turtle.penup()

def draw_vertical_line(x):
    turtle.pensize(5)
    turtle.color("green")
    turtle.penup()
    turtle.goto(x, 0)
    turtle.setheading(90)
    turtle.pendown()
    turtle.forward(300)
    turtle.penup()

def draw_left_angle_line():
    turtle.pensize(5)
    turtle.color("green")
    turtle.penup()
    turtle.goto(0, 0)
    turtle.setheading(45)
    turtle.pendown()
    turtle.forward(420)
    turtle.penup()

def draw_right_angle_line():
    turtle.pensize(5)
    turtle.color("green")
    turtle.penup()
    turtle.goto(300, 0)
    turtle.setheading(135)
    turtle.pendown()
    turtle.forward(420)
    turtle.penup()

def check_win(board, player):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in wins:
        if all(board[i] == player for i in combo):
            if combo == [0,1,2]: draw_horizontal_line(250)
            elif combo == [3,4,5]: draw_horizontal_line(150)
            elif combo == [6,7,8]: draw_horizontal_line(50)
            elif combo == [0,3,6]: draw_vertical_line(50)
            elif combo == [1,4,7]: draw_vertical_line(150)
            elif combo == [2,5,8]: draw_vertical_line(250)
            elif combo == [0,4,8]: draw_right_angle_line()
            elif combo == [2,4,6]: draw_left_angle_line()
            return True
    return False

def has_empty(board):
    return any(b is None for b in board)

def user_input(board):
    while True:
        try:
            a = int(input("Нүүдлээ оруулна уу (1-9): "))
            if a < 1 or a > 9:
                print("1-ээс 9-ийн хооронд тоо оруулна уу!")
            elif board[a - 1] is not None:
                print("Тэр байрлал аль хэдийн бөглөгдсөн!")
            else:
                return a - 1
        except ValueError:
            print("Зөвхөн тоо оруулна уу!")

def ai_move(board):
    empty = [i for i in range(9) if board[i] is None]
    return random.choice(empty)

def play_game():
    setup_turtle()
    print("Tic Tac Toe тоглоомд тавтай морил!\n")
    print("1. Тоглогч VS Компьютер")
    print("2. Тоглогч VS Тоглогч")

    while True:
        try:
            mode = int(input("Сонголтоо оруулна уу (1/2): "))
            if mode in (1, 2):
                break
            print("Зөвхөн 1 эсвэл 2 оруулна уу!")
        except ValueError:
            print("Тоо оруулна уу!")

    while True:
        player1 = input("Тоглогч 1 тэмдэгтээ сонгоно уу (x/o): ").lower()
        if player1 in ('x', 'o'):
            break
        print("Зөвхөн x эсвэл o оруулна уу!")

    player2 = 'o' if player1 == 'x' else 'x'

    board = [None] * 9
    draw_board()

    while has_empty(board):
        pos1 = user_input(board)
        board[pos1] = player1
        draw_marker(player1, pos1)

        if check_win(board, player1):
            print(f"Тоглогч {player1.upper()} хожлоо!")
            print("Тоглоом дууслаа!")
            return

        if not has_empty(board):
            print("Тэнцлээ!")
            print("Тоглоом дууслаа!")
            return

        if mode == 1:
            pos2 = ai_move(board)
            print(f"Компьютер {pos2 + 1}-р байрлалд нүүлээ.")
        else:
            pos2 = user_input(board)

        board[pos2] = player2
        draw_marker(player2, pos2)

        if check_win(board, player2):
            if mode == 1:
                print("Компьютер хожлоо!")
            else:
                print(f"Тоглогч {player2.upper()} хожлоо!")
            print("Тоглоом дууслаа!")
            return

        if not has_empty(board):
            print("Тэнцлээ!")
            print("Тоглоом дууслаа!")
            return

while True:
    play_game()
    again = input("Дахин тоглох уу? (y/n): ").lower()
    if again != 'y':
        print("Баярлалаа, тоглоом дууслаа!")
        break

turtle.done()
