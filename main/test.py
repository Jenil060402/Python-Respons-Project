from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from pymongo import MongoClient

class AddressBook(App):
    def build(self):
        self.client = MongoClient('mongodb://localhost:27017/')  # Connect to MongoDB
        self.db = self.client['address_book']  # Select database
        self.collection = self.db['contacts']  # Select collection

        layout = BoxLayout(orientation='vertical')
        
        self.name_input = TextInput(hint_text='Enter Name', multiline=False)
        self.email_input = TextInput(hint_text='Enter Email', multiline=False)
        self.phone_input = TextInput(hint_text='Enter Phone Number', multiline=False)
        self.address_input = TextInput(hint_text='Enter Address', multiline=False)
        
        self.name_input.bind(text=self.check_and_update_address)
        self.email_input.bind(text=self.check_and_update_address)
        self.phone_input.bind(text=self.check_and_update_address)
        
        layout.add_widget(Label(text='Name:'))
        layout.add_widget(self.name_input)
        layout.add_widget(Label(text='Email:'))
        layout.add_widget(self.email_input)
        layout.add_widget(Label(text='Phone Number:'))
        layout.add_widget(self.phone_input)
        layout.add_widget(Label(text='Address:'))
        layout.add_widget(self.address_input)
        
        return layout

    def check_and_update_address(self, instance, value):
        name = self.name_input.text
        email = self.email_input.text
        phone = self.phone_input.text
        
        query = {'name': name, 'email': email, 'phone': phone}
        existing_contact = self.collection.find_one(query)
        
        if existing_contact:
            self.address_input.text = existing_contact.get('address', '')
        
    def on_stop(self):
        self.client.close()

if __name__ == '__main__':
    AddressBook().run()
