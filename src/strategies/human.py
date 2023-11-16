from wordle import Result, Wordle, GuessResult
from strategies.base import BaseStrategy
from util.probabilities import alphabet
from rich.console import Console

console = Console()

class HumanStrategy(BaseStrategy):
    def __init__(self, game: Wordle) -> None:
        self.letters = set(alphabet())
        super().__init__(game)

    def get_guess(self) -> str:
        guess = ''
        while True:
            guess = input(
                f'[{len(self.game.guesses)+1}/{self.game.num_tries_initial}] Enter guess:').upper()
            validation_result = self.game.is_valid_guess(guess)
            if validation_result.is_valid:
                break
            else:
                print(validation_result.error)
                print('Please try again.')
        return guess

    def make_guess(self, guess: str) -> GuessResult:
        guess_result = super().make_guess(guess)
        guess, result = guess_result
        colorized_guess = console.render_str(f"")
        for x in self.game.formatted_guesses:
            console.print(x)
        for i, r in enumerate(result):
            if r == Result.INVALID:
                formatted_str = console.render_str(f"[red]{guess[i]}[/red]")
                colorized_guess.append(formatted_str)
            elif r == Result.IN_WORD:
                formatted_str = console.render_str(f"[yellow]{guess[i]}[/yellow]")
                colorized_guess.append(formatted_str)
            else:
                formatted_str = console.render_str(f"[green]{guess[i]}[/green]")
                colorized_guess.append(formatted_str)
            if r == Result.INVALID and guess[i] in self.letters:
                self.letters.remove(guess[i])
            
        console.print(colorized_guess)
        self.game.formatted_guesses.append(colorized_guess)
        if not self.game.has_won() and not self.game.can_guess():
            print('You ran out of moves. The secret was:', self.game._secret_word)