from datetime import datetime


def add_pretty_published_at_to_note(note):
    note["published_at_pretty"] = datetime.fromisoformat(note["published_at"]).strftime(
        "%d %B %Y"
    )
    return note


def add_pretty_published_at_to_notes(notes):
    for note in notes:
        add_pretty_published_at_to_note(note)
    return notes
