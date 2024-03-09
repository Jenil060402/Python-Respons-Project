#all the imports necessary
import logging
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from pymongo import MongoClient
import pymongo

# Configure logging
logging.basicConfig(filename='address_book.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class AddressBook(App):
    def build(self):
        try:
            # MongoDB connection
            uri = 'mongodb+srv://jenil060402:Je10514912nil%40@project1.agjazpp.mongodb.net/?retryWrites=true&w=majority&appName=Project1'
            self.client = pymongo.MongoClient(uri)
            #database connection
            self.db = self.client['address_book']
            #collection check
            self.collection = self.db['contacts']
            # enforce a unique constraint
            # Ensures  that each email address can only be associated with one record
            # in the collection. If an attempt is made to insert a new record with an 
            # email address that already exists, MongoDB will raise a duplicate key error.
            self.collection.create_index([('email', pymongo.ASCENDING)], unique=True)
            
            # UI layout
            layout = GridLayout(cols=2, spacing=10, padding=10)

            # Input fields
            self.name_input = TextInput(hint_text='Enter Name', multiline=False)
            self.email_input = TextInput(hint_text='Enter Email', multiline=False, input_type='mail')
            self.phone_input = TextInput(hint_text='Enter Phone Number', multiline=False)
            self.address_input = TextInput(hint_text='Enter Address (House No, Street, Locality, City, Pincode)', multiline=True)

            # Buttons
            add_update_button = Button(text='Add/Update Record')
            delete_button = Button(text='Delete Address')
            
            # Binding buttons to functions
            add_update_button.bind(on_press=self.add_or_update_record)
            delete_button.bind(on_press=self.confirm_delete)

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
        except Exception as e:
            logging.error(f"An error occurred: {type(e).__name__} - {e}")
            raise

    def check_and_update_address(self, instance, value):
        try:
            name = self.name_input.text
            email = self.email_input.text.lower()
            phone = self.phone_input.text
            
            query = {'name': name, 'email': email, 'phone': phone}
            existing_contact = self.collection.find_one(query)
            
            if existing_contact:
                self.address_input.text = existing_contact.get('address', '')
        except Exception as e:
            logging.error(f"An error occurred: {type(e).__name__} - {e}")

    def add_or_update_record(self, instance):
        try:
            name = self.name_input.text
            email = self.email_input.text.lower()
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
        except Exception as e:
            logging.error(f"An error occurred: {type(e).__name__} - {e}")

    def confirm_delete(self, instance):
        try:
            # Define the content of the popup
            content = BoxLayout(orientation='vertical')
            content.add_widget(Label(text='Are you sure you want to delete the address?'))

            # Define the buttons of the popup
            confirm_button = Button(text='Confirm')
            cancel_button = Button(text='Cancel')

            # Define the actions for the buttons
            confirm_button.bind(on_press=self.delete_address)
            cancel_button.bind(on_press=self.dismiss_popup)

            # Add buttons to the content layout
            content.add_widget(confirm_button)
            content.add_widget(cancel_button)

            # Create and open the popup
            self.popup = Popup(title='Delete Confirmation', content=content, size_hint=(None, None), size=(300, 200))
            self.popup.open()
        except Exception as e:
            logging.error(f"An error occurred: {type(e).__name__} - {e}")

    def delete_address(self, instance):
        try:
            name = self.name_input.text
            email = self.email_input.text.lower()
            phone = self.phone_input.text
            
            # Clear address field
            new_values = {'$set': {'address': ''}}
            self.collection.update_one({'name': name, 'email': email, 'phone': phone}, new_values)
            
            # Clear address input field
            self.address_input.text = ''

            # Close the popup
            self.dismiss_popup()
        except Exception as e:
            logging.error(f"An error occurred: {type(e).__name__} - {e}")

    def dismiss_popup(self, instance):
        try:
            # Dismiss the popup
            self.popup.dismiss()
        except Exception as e:
            logging.error(f"An error occurred: {type(e).__name__} - {e}")

    def on_stop(self):
        try:
            self.client.close()
        except Exception as e:
            logging.error(f"An error occurred: {type(e).__name__} - {e}")

if __name__ == '__main__':
    AddressBook().run()
