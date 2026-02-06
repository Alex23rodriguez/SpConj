"""Spanish Verb Conjugation Quiz Application.

This application creates separate quizzes for each tense (present, preterite,
imperfect, future, conditional) with all 10 verbs. It uses ezquiz for the
quiz framework and implements a conjugation system with irregular overrides.

Run with:
    python main.py

Then visit http://localhost:8000/ to see the lobby with all tense quizzes.
"""

from random import choice

from ezquiz import APIGame, Q

from conjugation_utils import conjugate, format_context, format_question_text
from verb_data import ALL_VERBS, PERSONS, TENSES


def create_tense_question(tense: str) -> Q:
    """Create a Q object for a specific tense quiz.

    This generates random fill-in-the-blank questions asking users to
    conjugate one of the 10 verbs for a randomly selected person.

    Args:
        tense: The tense name (e.g., "present", "preterite")

    Returns:
        Q object configured for the tense
    """

    def get_seed():
        """Randomly select a verb and person."""
        verb = choice(ALL_VERBS)
        person = choice(PERSONS)
        return (verb, person)

    def ask(seed):
        """Create the question prompt."""
        verb, person = seed
        return {
            "text": format_question_text(person, verb),
            "type": "fill",
            "context": format_context(person, verb, tense),
        }

    def correct(seed):
        """Return the correct conjugation."""
        verb, person = seed
        return conjugate(verb, tense, person)

    return Q[tuple](
        get_seed=get_seed,
        ask=ask,
        correct=correct,
    )


def create_all_tense_quizzes(game: APIGame) -> None:
    """Create a separate quiz for each tense.

    Args:
        game: The APIGame instance to add quizzes to
    """
    for tense in TENSES:
        # Create one Q object for this tense that handles all verbs
        tense_q = create_tense_question(tense)

        # Add quiz at subpath corresponding to the tense
        # All 10 verbs are in one category "all verbs"
        game.add_quiz(
            subpath=tense,
            title=tense.replace("_", " ").title(),
            qs={
                "all verbs": tense_q,
            },
        )

        print(f"Added quiz: /{tense}/ - {tense.title()} Tense")


def main():
    """Main entry point."""
    print("Spanish Verb Conjugation Quiz Server")
    print("=" * 50)
    print(f"Verbs: {', '.join(ALL_VERBS)}")
    print(f"Persons: {', '.join(PERSONS)}")
    print(f"Tenses: {', '.join(TENSES)}")
    print("=" * 50)
    print()

    # Create the game server
    game = APIGame()

    # Add all tense quizzes
    create_all_tense_quizzes(game)

    print()
    print("Starting server on http://localhost:8000/")
    print("Visit the lobby to select a tense quiz!")
    print()

    # Start the server
    game.start(host="localhost", port=8000)


if __name__ == "__main__":
    main()
