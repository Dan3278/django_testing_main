from .base_test import (
    TestBase,
    URL_NOTES_LIST,
    URL_NOTES_ADD,
    URL_NOTES_EDIT,
)
from notes.forms import NoteForm


class TestPages(TestBase):

    def test_note_not_displayed_for_non_author(self):
        response = self.client_reader.get(URL_NOTES_LIST)
        displayed_notes = response.context['object_list']
        self.assertNotIn(self.note1, displayed_notes)

    def test_displaying_note_in_list(self):
        response = self.client_author.get(URL_NOTES_LIST)
        displayed_notes = response.context['object_list']
        self.assertIn(self.note1, displayed_notes)
        displayed_note = displayed_notes.get(pk=self.note1.pk)
        self.assertEqual(self.note1.title, displayed_note.title)
        self.assertEqual(self.note1.text, displayed_note.text)
        self.assertEqual(self.note1.slug, displayed_note.slug)
        self.assertEqual(self.note1.author, displayed_note.author)

    def test_transfer_form_for_adding_editing_notes(self):
        for url in (URL_NOTES_ADD, URL_NOTES_EDIT):
            with self.subTest(url=url):
                form = self.client_author.get(url).context.get('form')
                self.assertIsInstance(form, NoteForm)
