from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from pymongo import MongoClient
import pymongo


class AddressBook(App):
    def build(self):
        uri = 'mongodb+srv://jenil060402:Je10514912nil%40@project1.agjazpp.mongodb.net/?retryWrites=true&w=majority&appName=Project1'
    
        #trying to connect to the databse using idp
        try:
            self.client = pymongo.MongoClient(uri)
        except  pymongo.errors.ConfigurationError:
            print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
        try:
            self.db = self.client['address_book']  # Selecting the databse
        except pymongo.errors.ConnectionFailure:
            print('No db found')
        try:
            self.collection = self.db['contacts']  # Selecting the collectn
        except pymongo.errors.ConnectionInvalid:
            print('No such collection found')

        # layout = BoxLayout(orientation='vertical')
        layout = GridLayout(cols=2, spacing=10, padding=10)


        self.name_input = TextInput(hint_text='Enter Name', multiline=False)
        self.email_input= TextInput(hint_text='Enter Email', multiline=False)
        self.phone_input = TextInput(hint_text='Enter Phone Number', multiline=False)
        self.address_input = TextInput(hint_text='Enter Address', multiline=False)
        add_button = Button(text='Add Contact')
        
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
        layout.add_widget(add_button)

        
        add_button.bind(on_press=self.add_contact)
        
        return layout

    def check_and_update_address(self, instance, value):
        name = self.name_input.text
        email = self.email_input.text
        phone = self.phone_input.text
        
        query = {'name': name, 'email': email, 'phone': phone}
        existing_contact = self.collection.find_one(query)
        
        if existing_contact:
            self.address_input.text = existing_contact.get('address', '')

    def add_contact(self, instance):
        name = self.name_input.text
        email = self.email_input.text
        phone = self.phone_input.text
        address = self.address_input.text
        
        query = {'name': name, 'email': email, 'phone': phone}
        new_values = {'$set': {'address': address}}
        
        self.collection.update_one(query, new_values)
        
        self.name_input.text = ''
        self.email_input.text = ''
        self.phone_input.text = ''
        self.address_input.text = ''

    def on_stop(self):
        self.client.close()

if __name__ == '__main__':
    AddressBook().run()
