import csv
import os
from typing import List, Tuple


class FlashcardManager:
    """
    handles loading, adding, and removing flashcards thorugh CSV
    """

    def __init__(self, filename: str = 'cards.csv') -> None:
        """
        ensure cards.csv exists with a header
        """
        base_dir: str = os.path.dirname(__file__)
        self.filename: str = os.path.join(base_dir, filename)
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['front', 'back'])

    def load_cards(self) -> List[Tuple[str, str]]:
        """
        read all flashcards returns the  list of front and back
        """
        cards: List[Tuple[str, str]] = []
        with open(self.filename, newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            for front, back in reader:
                cards.append((front, back))
        return cards

    def add_card(self, front: str, back: str) -> None:
        """
        append a new flashcard to the CSV
        """
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([front, back])

    def remove_card(self, index: int) -> None:
        """
        delete card at index and rewrite the CSV
        """
        cards = self.load_cards()
        if 0 <= index < len(cards):
            cards.pop(index)
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['front', 'back'])
                for front, back in cards:
                    writer.writerow([front, back])
