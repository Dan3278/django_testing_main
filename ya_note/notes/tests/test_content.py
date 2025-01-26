from .base_test import (
    TestBase,
    URL_NOTES_LIST,
    URL_NOTES_ADD,
    URL_NOTES_EDIT,
)
from notes.forms import NoteForm


class TestPages(TestBase):
    def test_displaying_note_in_list(self):
        response = self.client_author.get(URL_NOTES_LIST)
        displayed_notes = list(response.context['object_list'])
        self.assertIn(self.note, displayed_notes)
        for field in ['title', 'text', 'slug', 'author']:
            self.assertEqual(getattr(self.note, field), getattr(
                displayed_notes[displayed_notes.index(self.note)],
                field))

    def test_transfer_form_for_adding_editing_notes(self):
        for url in (
            URL_NOTES_ADD,
            URL_NOTES_EDIT,
        ):
            with self.subTest(url=url):
                assert isinstance(
                    self.client_author.get(url).context.get('form'), NoteForm
                )
