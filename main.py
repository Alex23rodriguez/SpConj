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
from verb_data import IRREGULAR_VERBS, PERSONS, REGULAR_VERBS, TENSES


def create_tense_question_regular(tense: str) -> Q:
    """Create a Q object for regular verbs in a specific tense."""

    def get_seed():
        """Randomly select a regular verb and person."""
        verb = choice(REGULAR_VERBS)
        person = choice(PERSONS)
        return (verb, person)

    def ask(seed):
        """Create the question prompt."""
        verb, person = seed
        return {
            "text": format_question_text(person, verb, tense),
            "type": "fill",
        }

    def correct(seed):
        """Return the correct conjugation."""
        verb, person = seed
        return conjugate(verb, tense, person)

    def check(correct_ans: str, submitted_ans: str) -> bool:
        """Check if submitted answer matches correct answer (case-insensitive)."""
        return correct_ans.lower().strip() == submitted_ans.lower().strip()  # type: ignore

    return Q[tuple](
        get_seed=get_seed,
        ask=ask,
        correct=correct,
        check=check,  # type: ignore
    )


def create_tense_question_irregular(tense: str) -> Q:
    """Create a Q object for irregular verbs in a specific tense."""

    def get_seed():
        """Randomly select an irregular verb and person."""
        verb = choice(IRREGULAR_VERBS)
        person = choice(PERSONS)
        return (verb, person)

    def ask(seed):
        """Create the question prompt."""
        verb, person = seed
        return {
            "text": format_question_text(person, verb, tense),
            "type": "fill",
        }

    def correct(seed):
        """Return the correct conjugation."""
        verb, person = seed
        return conjugate(verb, tense, person)

    def check(correct_ans: str, submitted_ans: str) -> bool:
        """Check if submitted answer matches correct answer (case-insensitive)."""
        return correct_ans.lower().strip() == submitted_ans.lower().strip()  # type: ignore

    return Q[tuple](
        get_seed=get_seed,
        ask=ask,
        correct=correct,
        check=check,  # type: ignore
    )


def create_all_tense_quizzes(game: APIGame) -> None:
    """Create a separate quiz for each tense with regular and irregular categories.

    Args:
        game: The APIGame instance to add quizzes to
    """
    for tense in TENSES:
        # Create separate Q objects for regular and irregular verbs
        regular_q = create_tense_question_regular(tense)
        irregular_q = create_tense_question_irregular(tense)

        # Add quiz with two categories
        game.add_quiz(
            subpath=tense,
            title=tense.replace("_", " ").title(),
            qs={
                "regular verbs": regular_q,
                "irregular verbs": irregular_q,
            },
        )

        print(f"Added quiz: /{tense}/ - {tense.title()} Tense")


def main():
    """Main entry point."""
    print("Spanish Verb Conjugation Quiz Server")
    print("=" * 50)
    print(f"Regular verbs ({len(REGULAR_VERBS)}): {', '.join(REGULAR_VERBS)}")
    print(f"Irregular verbs ({len(IRREGULAR_VERBS)}): {', '.join(IRREGULAR_VERBS)}")
    print(f"Persons: {', '.join(PERSONS)}")
    print(f"Tenses: {', '.join(TENSES)}")
    print("=" * 50)
    print()

    # Create the game server
    game = APIGame()

    # Add all tense quizzes
    create_all_tense_quizzes(game)

    print()
    host = "0.0.0.0"
    print(f"Starting server on http://{host}:8000/")
    print("Visit the lobby to select a tense quiz!")
    print()

    # Start the server
    game.start(host=host, port=8000)


if __name__ == "__main__":
    main()
