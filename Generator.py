import random
import os
from pathlib import Path
import customtkinter as ctk
from PIL import Image
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to center the window
def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    win.geometry(f'{width}x{height}+{x}+{y}')

# Function to handle the generate button click and show a popup
def generate_card():
    card_type = card_type_menu.get()
    card_holder_name = card_holder_name_entry.get().strip()  # Remove leading/trailing spaces
    if not card_holder_name or card_type not in ["Visa", "MasterCard"]:
        show_invalid_popup("Please enter a valid name and select a card type.")
        return  # Exit the function if input is invalid

    Digits = "001234567891"
    Card_Length = 12
    VBIN = "4677"
    MBIN = "5448"
    
    # Generate card number
    cn = "".join(random.sample(Digits, Card_Length))
    
    if card_type == "Visa":
        card_number = VBIN + cn
    elif card_type == "MasterCard":
        card_number = MBIN + cn
    else:
        card_number = "Invalid Card Type"
        
    cvv_length = 3
    CVV = "".join(random.sample(Digits, cvv_length))
    
    days = [f"{str(i).zfill(2)}" for i in range(1, 32)]  # Days from 01 to 31
    months = [f"{str(i).zfill(2)}" for i in range(1, 13)]  # Months from 01 to 12
    
    # Get the current year and create a list for the next 5 years
    current_year = datetime.now().year
    years = [str(current_year + i) for i in range(6)]  # Next 5 years including the current year
    
    day = "".join(random.sample(days, 1))
    month = "".join(random.sample(months, 1))
    year = "".join(random.sample(years, 1))
    divider = "/"    
    expiry_date = day + divider + month + divider + year

    # Create the popup window
    popup = ctk.CTkToplevel()
    popup.title("Generated Card Info")
    
    # Set popup window size and center it
    popup_width = 400
    popup_height = 250
    center_window(popup, popup_width, popup_height)

    # Make the popup modal
    popup.grab_set()

    # Disable main window interactions
    root.attributes('-disabled', True)

    # Add Name field in the popup
    name_label = ctk.CTkLabel(popup, text="Name", font=ctk.CTkFont(size=14))
    name_label.place(x=30, y=30)

    name_entry = ctk.CTkEntry(popup, width=150)
    name_entry.insert(0, card_holder_name)  # Pre-fill the name
    name_entry.place(x=30, y=60)

    # Add Card Number field in the popup (right of the Name field)
    card_number_label = ctk.CTkLabel(popup, text="Card Number", font=ctk.CTkFont(size=14))
    card_number_label.place(x=220, y=30)

    card_number_entry = ctk.CTkEntry(popup, width=150)
    card_number_entry.insert(0, card_number) 
    card_number_entry.place(x=220, y=60)

    # Add CVV field below the Name field
    cvv_label = ctk.CTkLabel(popup, text="CVV", font=ctk.CTkFont(size=14))
    cvv_label.place(x=30, y=100)

    cvv_entry = ctk.CTkEntry(popup, width=150)
    cvv_entry.insert(0, CVV) 
    cvv_entry.place(x=30, y=130)

    # Add Expiry Date field below the Card Number field
    expiry_date_label = ctk.CTkLabel(popup, text="Expiry Date", font=ctk.CTkFont(size=14))
    expiry_date_label.place(x=220, y=100)

    expiry_date_entry = ctk.CTkEntry(popup, width=150)
    expiry_date_entry.insert(0, expiry_date)  
    expiry_date_entry.place(x=220, y=130)

    # Function to handle save button click
    def save_card_info():
        # Create PDF
        pdf_path = Path(os.path.join(os.path.expanduser("~"), "Desktop", "Generated Cards"))
        pdf_file = pdf_path.joinpath('Generated_Card_Info.pdf')
        
        # Ensure the directory exists
        if not pdf_path.is_dir():
            os.mkdir(pdf_path)
        
        # Generate PDF
        c = canvas.Canvas(str(pdf_file), pagesize=letter)
        c.drawString(100, 750, 'Generated Card Details:')
        c.drawString(100, 700, f'Name: {card_holder_name}')
        c.drawString(100, 650, f'Card Number: {card_number}')
        c.drawString(100, 600, f'CVV: {CVV}')
        c.drawString(100, 550, f'Expiry Date: {expiry_date}')
        c.save()

        # Show success message popup
        success_popup = ctk.CTkToplevel()
        success_popup.title("Success")
        
        # Set popup window size and center it
        success_width = 300
        success_height = 100
        center_window(success_popup, success_width, success_height)

        # Show success message
        success_label = ctk.CTkLabel(success_popup, text="Card info has been saved as PDF!", font=ctk.CTkFont(size=12))
        success_label.pack(pady=20)

        # Make sure the success popup is modal
        success_popup.grab_set()
        
        # Disable main window interactions
        root.attributes('-disabled', True)

        # Make sure the success popup closes and releases the grab when the user closes it
        success_popup.protocol("WM_DELETE_WINDOW", lambda: (success_popup.grab_release(), root.attributes('-disabled', False), success_popup.destroy()))

    # Add Save button at the middle bottom of the popup
    save_button = ctk.CTkButton(popup, text="Save as PDF", command=save_card_info, fg_color="black")
    save_button.place(relx=0.5, rely=0.85, anchor="center")  # Centered at the bottom

    # Make sure the popup closes and releases the grab when the user closes it
    popup.protocol("WM_DELETE_WINDOW", lambda: (popup.grab_release(), root.attributes('-disabled', False), popup.destroy()))

# Function to show an invalid input popup
def show_invalid_popup(message):
    invalid_popup = ctk.CTkToplevel()
    invalid_popup.title("Invalid Input")
    
    # Set popup window size and center it
    invalid_width = 300
    invalid_height = 100
    center_window(invalid_popup, invalid_width, invalid_height)

    # Show invalid message
    invalid_label = ctk.CTkLabel(invalid_popup, text=message, font=ctk.CTkFont(size=12))
    invalid_label.pack(pady=20)

    # Make sure the popup is modal
    invalid_popup.grab_set()
    
    # Disable main window interactions
    root.attributes('-disabled', True)

    # Make sure the invalid popup closes and releases the grab when the user closes it
    invalid_popup.protocol("WM_DELETE_WINDOW", lambda: (invalid_popup.grab_release(), root.attributes('-disabled', False), invalid_popup.destroy()))

# Create the main window
root = ctk.CTk()
root.title("Credit Card Generator")
root.iconbitmap('app.ico')  # Change 'path_to_your_logo.ico' to your logo file's path


# Set window size and center it
window_width = 700
window_height = 500
center_window(root, window_width, window_height)

# Create a tabbed view (using CTkTabview)
tabview = ctk.CTkTabview(root, width=800, height=400)
tabview.pack(expand=True, fill="both")

# Add two tabs: "Generate Cards" and "Developer Info"
tabview.add("Generate Cards")
tabview.add("Developer Info")

# Tab 1: Generate Cards
tab1_frame = tabview.tab("Generate Cards")

# Add Card Type Label and Dropdown menu on the left
card_type_label = ctk.CTkLabel(tab1_frame, text="Card Type", font=ctk.CTkFont(size=14))
card_type_label.place(x=50, y=50)

# Limit the options to only "Visa" and "MasterCard", make it readonly
card_type_menu = ctk.CTkComboBox(tab1_frame, values=["Visa", "MasterCard"], width=250, state="readonly")
card_type_menu.place(x=50, y=80)

# Add Card Holder Name Label and Entry on the right
name_label = ctk.CTkLabel(tab1_frame, text="Card Holder Name", font=ctk.CTkFont(size=14))
name_label.place(x=400, y=50)

card_holder_name_entry = ctk.CTkEntry(tab1_frame, width=250)
card_holder_name_entry.place(x=400, y=80)

# Add Generate Button below the dropdown and name entry
generate_button = ctk.CTkButton(tab1_frame, text="Generate", command=generate_card, fg_color="black")
generate_button.place(relx=0.5, rely=0.9, anchor="center")

# Tab 2: Developer Info
tab2_frame = tabview.tab("Developer Info")
# Load the developer's photo
image_path = "developer.jpg"  # Ensure this image is in the same directory or provide full path
passport_photo = ctk.CTkImage(light_image=Image.open(image_path), size=(100, 100))

# Display the image in the top-middle of the Developer Info tab
image_label = ctk.CTkLabel(tab2_frame, image=passport_photo, text="")
image_label.pack(pady=10)

# Developer Information
developer_info = [
    "Developer Name: Mohammad Mahfuz Rahman",
    "Software Name: Credit Card Generator",
    "Company Name: Dexcorp Softwares Limited",
    "Email: mahfuzrahman0712@gmail.com",
    "Contact: 01876891680",
    "Facebook: fb.com/mahfuzrahman0712",
    "GitHub:  github.com/mahfuz0712",
    "Version: 1.0.0",
]

for i, info in enumerate(developer_info):
    info_label = ctk.CTkLabel(tab2_frame, text=info, font=ctk.CTkFont(size=12))
    info_label.pack(pady=2)



# Start the main loop
root.mainloop()
