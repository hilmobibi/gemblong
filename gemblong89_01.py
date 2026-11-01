import random
import time
import cowsay
import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


clear_screen()

# =========================
# CONFIGURATION
# =========================

balance = 10000
MIN_BALANCE = 2000

increment = [
    0.025, 0.05, 0.15, 0.5, 1.75,
    5.0, 17.5, 50.0, 50.0
]

level = [
    "cow", "fox", "pig", "tux", "kitty",
    "stegosaurus", "turtle", "dragon", "trex"
]

intervals = [
    2, 4, 10, 30, 100,
    300, 1000, 3000, 5000
]

DELAY = 0.25


# =========================
# CRASH POINT
# =========================

def crash_point():

    region = random.randint(1, 1000)

    if region <= 50:
        return 1

    elif region <= 400:
        return random.uniform(1, 2)

    elif region <= 800:
        return random.uniform(2, 4)

    elif region <= 900:
        return random.uniform(4, 10)

    elif region <= 950:
        return random.uniform(10, 30)

    elif region <= 970:
        return random.uniform(30, 100)

    elif region <= 980:
        return random.uniform(100, 300)

    elif region <= 990:
        return random.uniform(300, 1000)

    elif region <= 995:
        return random.uniform(1000, 5000)

    else:
        return 5000


# =========================
# GET LEVEL
# =========================

def get_rank(multiplier):

    for rank, upper in enumerate(intervals):
        if multiplier < upper:
            return rank

    return 8


# =========================
# GAME
# =========================

def play(bet):

    global balance

    cp = crash_point()
    multiplier = 1.0

    balance -= bet

    clear_screen()

    print("GAME STARTED!")
    time.sleep(1)

    try:

        while True:

            rank = get_rank(multiplier)

            # Crash check
            if multiplier >= cp:
                break

            clear_screen()

            print(f"Balance : {balance:,.2f}")
            print(f"Bet     : {bet:,.2f}")
            print(f"Potential payout : {bet * multiplier:,.2f}")
            print()
            
            print(
                getattr(cowsay, level[rank])(
                    f"{multiplier:.2f}x"
                )
            )

            time.sleep(DELAY)

            multiplier += increment[rank]

    except KeyboardInterrupt:

        # Cash out
        payout = bet * multiplier
        balance += payout

        clear_screen()

        input(
            "YOU CASHED OUT!\n"
            f"Cash out multiplier : {multiplier:.2f}x\n"
            f"Your payout         : {payout:,.2f}\n"
            f"New balance         : {balance:,.2f}\n"
            "press enter to continue.. "
        )
        return

    # Lose
    clear_screen()

    input(
        "YOU LOST!\n"
        f"BOOM! CRASHED AT {cp:.2f}x\n"
        f"Lost bet : {bet:,.2f}\n"
        f"Balance  : {balance:,.2f}\n"
        "press enter to continue.."
    )


# =========================
# MAIN MENU
# =========================

while True:

    if balance < MIN_BALANCE:
        balance = MIN_BALANCE

    clear_screen()

    print("==========================")
    print("       CRASH GAME")
    print("==========================")
    print(f"BALANCE: {balance:,.2f}")
    print("==========================")

    print("\n1. PLAY")
    print("2. EXIT")

    choice = input("\nSelect menu: ")

    if choice == "1":

        try:
            bet = float(input("Enter your bet: "))

            if bet <= 0:
                print("Bet must be greater than 0!")
                time.sleep(1)
                continue

            if bet > balance:
                print("Insufficient balance!")
                time.sleep(1)
                continue

            play(bet)

        except ValueError:
            print("Invalid bet!")
            time.sleep(1)

    elif choice == "2":
        clear_screen()
        print("Thanks for playing!")
        break

    else:
        print("Invalid menu!")
        time.sleep(1)











"""def crash_point():
    x = random.uniform(1,5000)
    while True:
        x = random.uniform(1, 5000)

        if x <= 2:
            weight = math.sqrt(x - 1)

        elif x <= 3:
            weight = math.sqrt(3 - x)

        else:
            weight = 1 / (x - 2)**2

        if random.random() < weight:
            return x
"""