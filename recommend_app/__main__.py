"""
Entrypoint to the app
"""

# Local imports
from .schema.card import Card


def main() -> None:
    """Main function"""
    card = Card("https://www.netflix.com/gb/title/81767635", "Godzilla Minus One")
    print(card)


if __name__ == "__main__":
    main()
