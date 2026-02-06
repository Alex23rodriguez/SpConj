"""Conjugation utilities for Spanish verbs.

This module provides functions to conjugate Spanish verbs using:
1. Irregular overrides from verb_data.py
2. Regular -er conjugation rules as fallback
"""

from verb_data import (ALL_VERBS, IRREGULAR_OVERRIDES, IRREGULAR_VERBS,
                       PERSONS, REGULAR_ENDINGS_ER, REGULAR_VERBS, TENSES)


def get_infinitive_ending(verb: str) -> str:
    """Get the infinitive ending of a verb.

    All verbs in this project are -er verbs.

    Args:
        verb: The infinitive verb (e.g., "deber")

    Returns:
        The ending (e.g., "er")
    """
    return verb[-2:]


def get_stem(verb: str) -> str:
    """Get the stem (root) of a verb by removing the infinitive ending.

    Args:
        verb: The infinitive verb (e.g., "deber")

    Returns:
        The stem (e.g., "deb")
    """
    return verb[:-2]


def is_irregular(verb: str) -> bool:
    """Check if a verb is in the irregular list.

    Args:
        verb: The infinitive verb

    Returns:
        True if irregular, False if regular
    """
    return verb in IRREGULAR_VERBS


def conjugate_regular(verb: str, tense: str, person: str) -> str:
    """Conjugate a regular -er verb.

    Args:
        verb: The infinitive verb (e.g., "deber")
        tense: The tense (e.g., "present", "future")
        person: The grammatical person (e.g., "Yo", "Tú")

    Returns:
        The conjugated form (e.g., "debo")

    Raises:
        ValueError: If the tense or person is invalid
    """
    if tense not in TENSES:
        raise ValueError(f"Unknown tense: {tense}. Must be one of {TENSES}")

    if person not in PERSONS:
        raise ValueError(f"Unknown person: {person}. Must be one of {PERSONS}")

    stem = get_stem(verb)
    ending = REGULAR_ENDINGS_ER[tense][person]
    return stem + ending


def conjugate(verb: str, tense: str, person: str) -> str:
    """Conjugate a verb, checking for irregular overrides first.

    This is the main conjugation function. It checks if the verb has an
    irregular conjugation for the given tense and person. If not, it
    falls back to regular conjugation rules.

    Args:
        verb: The infinitive verb (e.g., "ir", "deber")
        tense: The tense (e.g., "present", "preterite")
        person: The grammatical person (e.g., "Yo", "Tú")

    Returns:
        The conjugated form

    Raises:
        ValueError: If the verb is not in the known list

    Example:
        >>> conjugate("ir", "present", "Yo")
        'voy'
        >>> conjugate("deber", "present", "Yo")
        'debo'
        >>> conjugate("tener", "future", "Nosotros")
        'tendremos'
    """
    if verb not in ALL_VERBS:
        raise ValueError(f"Unknown verb: {verb}. Must be one of {ALL_VERBS}")

    # Check for irregular override
    if verb in IRREGULAR_OVERRIDES:
        if tense in IRREGULAR_OVERRIDES[verb]:
            if person in IRREGULAR_OVERRIDES[verb][tense]:
                return IRREGULAR_OVERRIDES[verb][tense][person]

    # Fall back to regular conjugation
    return conjugate_regular(verb, tense, person)


def get_conjugation_table(verb: str, tense: str) -> dict[str, str]:
    """Get the full conjugation table for a verb in a specific tense.

    Args:
        verb: The infinitive verb
        tense: The tense

    Returns:
        Dictionary mapping persons to conjugated forms
    """
    return {person: conjugate(verb, tense, person) for person in PERSONS}


def format_question_text(person: str, verb: str) -> str:
    """Format the question text for a fill-in-the-blank question.

    Args:
        person: The grammatical person
        verb: The infinitive verb

    Returns:
        Formatted question text (e.g., "Yo [...] (ir)")
    """
    return f"{person} [...] ({verb})"


def format_context(person: str, verb: str, tense: str) -> str:
    """Format the context/instruction text for a question.

    Args:
        person: The grammatical person
        verb: The infinitive verb
        tense: The tense name

    Returns:
        Formatted context text
    """
    return f"Conjugate '{verb}' in the {tense} tense for '{person}'"
