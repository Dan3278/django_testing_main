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
        self.assertIn(self.note, list(response.context['object_list']))

    def test_notes_do_not_mix_for_author(self):
        self.assertNotIn(
            self.note,
            self.client_reader.get(URL_NOTES_LIST).context['object_list']
        )

    def test_transfer_form_for_adding_editing_notes(self):
        for url in (
            URL_NOTES_ADD,
            URL_NOTES_EDIT,
        ):
            with self.subTest(url=url):
                assert isinstance(
                    self.client_author.get(url).context.get('form'), NoteForm
                )
