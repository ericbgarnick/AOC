from hashlib import md5
from collections import deque
from sys import argv
from typing import Deque, Tuple, Set


def read_decks(filename: str) -> Tuple[Deque, Deque]:
    raw_deck1, raw_deck2 = open(filename, "r").read().strip().split("\n\n")
    deck1 = deque(int(card) for card in raw_deck1.split('\n')[1:])
    deck2 = deque(int(card) for card in raw_deck2.split('\n')[1:])
    return deck1, deck2


# PART 1
def combat(deck1: Deque, deck2: Deque) -> Deque:
    winning_deck = None
    while len(deck1) and len(deck2):
        card1, card2 = deck1.popleft(), deck2.popleft()
        if card1 > card2:
            winning_card, losing_card = card1, card2
            winning_deck = deck1
        else:
            winning_card, losing_card = card2, card1
            winning_deck = deck2
        winning_deck.append(winning_card)
        winning_deck.append(losing_card)
    return winning_deck


# PART 2
def recursive_combat(deck1: Deque, deck2: Deque) -> Tuple[Deque, int]:
    history = set()
    winning_deck = winning_deck_num = None
    while len(deck1) and len(deck2):
        card1, card2 = deck1.popleft(), deck2.popleft()
        if repeat_configuration(deck1, deck2, history):
            return deck1, 1
        if card1 <= len(deck1) and card2 <= len(deck2):
            # Recurse
            _, winning_deck_num = recursive_combat(deque(list(deck1)[:card1]), deque(list(deck2)[:card2]))
            if winning_deck_num == 1:
                winning_deck = deck1
                winning_card = card1
                losing_card = card2
            else:
                winning_deck = deck2
                winning_card = card2
                losing_card = card1
        else:
            # No recursion possible, directly compare card values
            if card1 > card2:
                winning_deck_num = 1
                winning_deck = deck1
                winning_card, losing_card = card1, card2
            else:
                winning_deck_num = 2
                winning_deck = deck2
                winning_card, losing_card = card2, card1
        winning_deck.append(winning_card)
        winning_deck.append(losing_card)
    return winning_deck, winning_deck_num


def repeat_configuration(deck1: Deque, deck2: Deque, history: Set[str]) -> bool:
    """Return True if this deck configuration has occurred before. Otherwise return False."""
    stringified = ",".join(str(card) for card in deck1) + ",".join(str(card) for card in deck2)
    hashed = md5(stringified.encode("utf8")).hexdigest()
    if hashed in history:
        return True
    else:
        history.add(hashed)
        return False


def score_deck(deck: Deque) -> int:
    total = 0
    for i, card in enumerate(reversed(deck)):
        total += card * (i + 1)
    return total


if __name__ == "__main__":
    input_file = argv[1]
    print("PART 1:", score_deck(combat(*read_decks(input_file))))
    w_deck, w_num = recursive_combat(*read_decks(input_file))
    print("PART 2:", score_deck(w_deck))
