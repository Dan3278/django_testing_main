from http import HTTPStatus

from .base_test import (
    TestBase,
    URL_NOTES_ADD,
    URL_NOTES_SUCCESS,
    URL_NOTES_EDIT,
    URL_NOTES_DELETE,
    EXPECTED_URL
)
from notes.models import Note


class TestLogic(TestBase):
    def posting_and_checking(self):
        Note.objects.all().delete()
        response = self.client_author.post(URL_NOTES_ADD, data=self.form_data)
        self.assertRedirects(response, URL_NOTES_SUCCESS)
        self.assertEqual(Note.objects.count(), 1)
        note_new = Note.objects.get(title=self.form_data['title'],
                                    slug=self.form_data['slug'])
        self.assertEqual(note_new.title, self.form_data['title'])
        self.assertEqual(note_new.text, self.form_data['text'])
        self.assertEqual(note_new.slug, self.form_data['slug'])
        self.assertEqual(note_new.author, self.client_author)

    def test_not_unique_slug(self):
        initial_notes = list(Note.objects.all().order_by('pk'))
        self.form_data['slug'] = self.note.slug
        self.client_author.post(URL_NOTES_ADD, data=self.form_data)
        final_notes = list(Note.objects.all().order_by('pk'))
        self.assertEqual(initial_notes, final_notes)

    def test_anon_user_cant_create_note(self):
        initial_notes = list(Note.objects.all())
        response = self.client.post(URL_NOTES_ADD, data=self.form_data)
        expected_url = EXPECTED_URL
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), len(initial_notes))

        final_notes = list(Note.objects.all())
        self.assertListEqual(initial_notes, final_notes)

    def test_author_can_edit_note(self):
        self.client_author.post(URL_NOTES_EDIT, self.form_data)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.author, self.note.author)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])

    def test_reader_cant_edit_note(self):
        response = self.client_reader.post(URL_NOTES_EDIT, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.author, self.note.author)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)

    def test_author_can_delete_note(self):
        response = self.client_author.post(URL_NOTES_DELETE)
        self.assertRedirects(response, URL_NOTES_SUCCESS)
        self.assertEqual(Note.objects.count(), 0)

    def test_reader_cant_delete_note(self):
        note_count = Note.objects.count()
        response = self.client_reader.post(URL_NOTES_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), note_count)
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)
