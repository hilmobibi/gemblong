import random
import time
import cowsay
import os
import signal


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def press_enter_to_continue(prompt):
    while True:
        try:
            input(prompt)
            return
        except KeyboardInterrupt:
            continue


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
        return random.uniform(1,1.5)
    
    elif region <= 650:
        return random.uniform(1.5, 2)

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

    previous_sigint_handler = signal.signal(signal.SIGINT, signal.default_int_handler)
    cashed_out = False
    cashout_multiplier = 0
    payout = 0
    try:
        while True:
            try:
                rank = get_rank(multiplier)

                if multiplier >= cp:
                    if cashed_out:
                        clear_screen()
                        print("YOU CASHED OUT!")
                        print(f"Cash out multiplier : {cashout_multiplier:.2f}x")
                        print(f"Your payout         : {payout:,.2f}")
                        print(f"New balance         : {balance:,.2f}")
                        print()
                        print(f"BOOM! CRASHED AT {cp:.2f}x")
                        getattr(cowsay, level[get_rank(cp)])(f"BOOM! {cp:.2f}x")
                        press_enter_to_continue("press enter to continue.. ")
                    break

                clear_screen()

                if cashed_out:
                    print("YOU CASHED OUT!")
                    print(f"Cash out multiplier : {cashout_multiplier:.2f}x")
                    print(f"Your payout         : {payout:,.2f}")
                    print(f"New balance         : {balance:,.2f}")
                    print("Watching until crash...")
                else:
                    print(f"Balance : {balance:,.2f}")
                    print(f"Bet     : {bet:,.2f}")
                    print(f"Potential payout : {bet * multiplier:,.2f}")
                    print("[CTRL + C] → CASH OUT")
                print()

                getattr(cowsay, level[rank])(f"{multiplier:.2f}x")

                time.sleep(DELAY)

                multiplier += increment[rank]
            except KeyboardInterrupt:
                if not cashed_out:
                    cashout_multiplier = multiplier
                    payout = bet * cashout_multiplier
                    balance += payout
                    cashed_out = True
    finally:
        signal.signal(signal.SIGINT, previous_sigint_handler)

    if cashed_out:
        return

    # Lose
    clear_screen()

    press_enter_to_continue(
        "YOU LOST!\n"
        f"BOOM! CRASHED AT {cp:.2f}x\n"
        f"Lost bet : {bet:,.2f}\n"
        f"Balance  : {balance:,.2f}\n"
        "press enter to continue.."
    )


# =========================
# MAIN MENU
# =========================

def main():
    global balance

    signal.signal(signal.SIGINT, signal.SIG_IGN)
    clear_screen()

    while True:

        if balance < MIN_BALANCE:
            balance = MIN_BALANCE

        clear_screen()

        print("==========================")
        print("       CRASH GAME")
        print("==========================")
        print(f"BALANCE: {balance:,.2f}")
        print("==========================")

        try:
            bet_input = input("\nEnter your bet: ")
        except KeyboardInterrupt:
            continue

        if bet_input.strip().lower() in ("allin", "all in"):
            bet = balance
        else:
            try:
                bet = float(bet_input)
            except ValueError:
                print("Invalid bet!")
                time.sleep(1)
                continue

        if bet <= 0:
            print("Bet must be greater than 0!")
            time.sleep(1)
            continue

        if bet > balance:
            print("Insufficient balance!")
            time.sleep(1)
            continue

        play(bet)


if __name__ == "__main__":
    main()











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