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


def add_pretty_tags_to_note(note):
    if note["tags"]:
        note["pretty_tags"] = list(
            filter(None, [tag.strip() for tag in note["tags"].split(",")])
        )
    else:
        note["pretty_tags"] = []
    return note


def add_pretty_tags_to_notes(notes):
    for note in notes:
        add_pretty_tags_to_note(note)
    return notes


def get_all_tags_from_notes(notes):
    all_tags = set()
    for note in notes:
        if note["tags"]:
            tags = [tag.strip() for tag in note["tags"].split(",")]
            all_tags.update(filter(None, tags))
    return sorted(all_tags)
