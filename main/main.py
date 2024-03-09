from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from pymongo import MongoClient
import pymongo

class AddressBook(App):
    def build(self):
        # MongoDB connection
        uri = 'mongodb+srv://jenil060402:Je10514912nil%40@project1.agjazpp.mongodb.net/?retryWrites=true&w=majority&appName=Project1'
        self.client = pymongo.MongoClient(uri)
        self.db = self.client['address_book']
        self.collection = self.db['contacts']
        
        # UI layout
        layout = GridLayout(cols=2, spacing=10, padding=10)

        # Input fields
        self.name_input = TextInput(hint_text='Enter Name', multiline=False)
        self.email_input = TextInput(hint_text='Enter Email', multiline=False)
        self.phone_input = TextInput(hint_text='Enter Phone Number', multiline=False)
        self.address_input = TextInput(hint_text='Enter Address', multiline=False)

        # Buttons
        add_update_button = Button(text='Add/Update Record')
        delete_button = Button(text='Delete Address')
        
        # Binding buttons to functions
        add_update_button.bind(on_press=self.add_or_update_record)
        delete_button.bind(on_press=self.delete_address)

        self.name_input.bind(text=self.check_and_update_address)
        self.email_input.bind(text=self.check_and_update_address)
        self.phone_input.bind(text=self.check_and_update_address)
        
        # Adding widgets to layout
        layout.add_widget(Label(text='Name:')) 
        layout.add_widget(self.name_input)
        layout.add_widget(Label(text='Email:'))
        layout.add_widget(self.email_input)
        layout.add_widget(Label(text='Phone Number:'))
        layout.add_widget(self.phone_input)
        layout.add_widget(Label(text='Address:'))
        layout.add_widget(self.address_input)
        layout.add_widget(add_update_button)
        layout.add_widget(delete_button)

        return layout

    def check_and_update_address(self, instance, value):
        name = self.name_input.text
        email = self.email_input.text
        phone = self.phone_input.text
        
        query = {'name': name, 'email': email, 'phone': phone}
        existing_contact = self.collection.find_one(query)
        
        if existing_contact:
            self.address_input.text = existing_contact.get('address', '')

    def add_or_update_record(self, instance):
        name = self.name_input.text
        email = self.email_input.text
        phone = self.phone_input.text
        address = self.address_input.text
        
        # Check if record exists
        existing_record = self.collection.find_one({'name': name, 'email': email, 'phone': phone})
        if existing_record:
            # Update existing record
            new_values = {'$set': {'address': address}}
            self.collection.update_one({'name': name, 'email': email, 'phone': phone}, new_values)
        else:
            # Insert new record
            self.collection.insert_one({'name': name, 'email': email, 'phone': phone, 'address': address})
        
        # Clear input fields
        self.name_input.text = ''
        self.email_input.text = ''
        self.phone_input.text = ''
        self.address_input.text = ''
    
    

    def delete_address(self, instance):
        name = self.name_input.text
        email = self.email_input.text
        phone = self.phone_input.text
        
        # Clear address field
        new_values = {'$set': {'address': ''}}
        self.collection.update_one({'name': name, 'email': email, 'phone': phone}, new_values)
        
        # Clear address input field
        self.address_input.text = ''

    def on_stop(self):
        self.client.close()

if __name__ == '__main__':
    AddressBook().run()
