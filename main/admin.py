from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from pymongo import MongoClient
import pymongo

class DatabaseViewer(App):
    def __init__(self, collection, sortable_fields, **kwargs):
        super().__init__(**kwargs)
        self.collection = collection
        self.sortable_fields = sortable_fields

    def build(self):
        self.root_layout = GridLayout(cols=1, spacing=10, padding=10)

        self.search_layout = GridLayout(cols=2, spacing=10)
        self.search_label = Label(text="Search:")
        self.search_input = TextInput(hint_text="Enter search term")
        self.search_button = Button(text="Search", on_press=self.search_entries)
        self.search_layout.add_widget(self.search_label)
        self.search_layout.add_widget(self.search_input)
        self.search_layout.add_widget(self.search_button)

        self.sort_layout = GridLayout(cols=3, spacing=10)
        self.sort_label = Label(text="Sort by:")
        self.sort_spinner = Spinner(text=self.sortable_fields[0], values=self.sortable_fields)
        self.sort_button = Button(text="Sort", on_press=self.sort_entries)
        self.sort_layout.add_widget(self.sort_label)
        self.sort_layout.add_widget(self.sort_spinner)
        self.sort_layout.add_widget(self.sort_button)

        self.entries_layout = GridLayout(cols=1, spacing=10)
        self.display_entries()

        self.root_layout.add_widget(self.search_layout)
        self.root_layout.add_widget(self.sort_layout)
        self.root_layout.add_widget(self.entries_layout)

        return self.root_layout

    def display_entries(self):
        self.entries_layout.clear_widgets()
        entries = self.collection.find()
        for entry in entries:
            entry.pop('_id', None)  # Remove the ObjectID
            entry_label = Label(text=str(entry))
            self.entries_layout.add_widget(entry_label)

    def search_entries(self, instance):
        search_term = self.search_input.text
        search_results = self.collection.find({'$or': [{'name': {'$regex': search_term, '$options': 'i'}},
                                                      {'email': {'$regex': search_term, '$options': 'i'}},
                                                      {'phone': {'$regex': search_term, '$options': 'i'}},
                                                      {'address': {'$regex': search_term, '$options': 'i'}}]})
        self.entries_layout.clear_widgets()
        for result in search_results:
            result.pop('_id', None)  # Remove the ObjectID
            result_label = Label(text=str(result))
            self.entries_layout.add_widget(result_label)

    def sort_entries(self, instance):
        sort_field = self.sort_spinner.text
        sorted_entries = self.collection.find().sort(sort_field)
        self.entries_layout.clear_widgets()
        for entry in sorted_entries:
            entry.pop('_id', None)  # Remove the ObjectID
            entry_label = Label(text=str(entry))
            self.entries_layout.add_widget(entry_label)

if __name__ == "__main__":
    client = pymongo.MongoClient('mongodb+srv://jenil060402:Je10514912nil%40@project1.agjazpp.mongodb.net/?retryWrites=true&w=majority&appName=Project1')  # Assuming MongoDB is running locally
    db = client['address_book']  # Change to your database name
    collection = db['contacts']  # Change to your collection name
    sortable_fields = ['name', 'email', 'phone', 'address']  # Define sortable fields

    DatabaseViewer(collection, sortable_fields).run()
