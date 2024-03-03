import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import math


API_KEY = "0d69156b6965edea88597c02b524d56c"
image_label = None  # Declare the image_label as a global variable

def get_weather():
    city = city_entry.get() 
    language = selected_option.get()
    units = "imperial"
    if language == "Chinese":
        language = "zh_tw"
        units = "metric"
    elif language == "Vietnamese":
        language = "vi"
        units = "metric"
    elif language == "Korean":
        language = "kr"
        units = "metric"
    else:
        language = "en"
        units = "imperial"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&lang={language}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        display_image(data["weather"][0]["id"]) 
        city_name = data["name"]
        temperature = math.ceil(data["main"]["temp"])
        condition = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        city_label.config(text=f"{city_name}")
        temperature_label.config(text=f"{temperature}°")
        condition_label.config(text=f"{condition}")
        if language == "vi": 
            humidity_num.config(text=f"{humidity}%")
            wind_speed_num.config(text=f"{wind_speed} dặm/giờ")
            humidity_label.config(text=f"độ ẩm")
            wind_speed_label.config(text=f"tốc độ gió")
        elif language == "zh_tw": 
            humidity_num.config(text=f"{humidity}%")
            wind_speed_num.config(text=f"{wind_speed} 英里/小時")
            humidity_label.config(text=f"濕度")
            wind_speed_label.config(text=f"風速")
        elif language == "kr":
            humidity_num.config(text=f"{humidity}%")
            wind_speed_num.config(text=f"{wind_speed} 시속")
            humidity_label.config(text=f"습기")
            wind_speed_label.config(text=f"바람 속도")
        else: 
            humidity_num.config(text=f"{humidity}%")
            wind_speed_num.config(text=f"{wind_speed} km/h")
            humidity_label.config(text=f"Humidity")
            wind_speed_label.config(text=f"Wind Speed") 
    else:
        temperature_label.config(text="Invalid city")
        condition_label.config(text="")
        humidity_label.config(text="")
        wind_speed_label.config(text="")

def option_selected(option):
    messagebox.showinfo("Option Selected", f"You selected: {option}")

def display_image(id):
    global image_label  # Declare image_label as a global variable
    image_path = ""
    if image_label:
        image_label.destroy()  # Destroy the previous image label if it exists
    if id == 800:
        image_path = "images/clear_day.png"  # Replace with your image file pat
    elif id == 801:
        image_path = "images/few_clouds_day.png"
    elif id == 802:
        image_path = "images/scattered_clouds.png"
    elif id == 803 or id == 804:
        image_path = "images/broken_clouds.png"
    elif id >= 500 and id <= 504:
        image_path = "images/rain_day.png"
    elif id >= 511 and id <= 531:
        image_path = "images/rain_night.png"
    elif id >= 300 and id <= 321:
        image_path = "images/shower_rain.png"
    elif id >= 200 and id <= 232:
        image_path = "images/thunderstorm.png"
    elif id >= 600 and id <= 622:
        image_path = "images/snow.png"
    elif id == "mist":
        image_path = "images/clear_day.png"
    image = Image.open(image_path)
    image = image.resize((150,150))  # Adjust the size of the image as needed
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(root, image=photo)
    image_label.image = photo
    image_label.place(relx=0.5, rely=0.25,anchor=tk.CENTER)


#############################################################################################################

root = tk.Tk()
root.title("Weather App")
root.geometry("400x600")


city_entry = tk.Entry(root, font=("Helvetica", 14))
city_entry.config(width=40)
city_entry.place(relx=0.5, rely=0, anchor=tk.N)


canvas_width = 30
canvas_height = 30

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)

button_radius = 10
icon_path = "images/search.svg.png"  # Replace with the actual path to your icon image

# Load the icon image
icon_image = Image.open(icon_path)

# Resize the icon image to fit the button
icon_image = icon_image.resize((button_radius*2, button_radius*2), Image.LANCZOS)

button_icon = ImageTk.PhotoImage(icon_image)

# Calculate the position of the circular button
button_x = (canvas_width - button_radius*2) // 2
button_y = (canvas_height - button_radius*2) // 2

# Create a search icon image
search_image = tk.PhotoImage(file="images/search.svg.png")

button = canvas.create_oval(button_x, button_y, button_x + button_radius*2, button_y + button_radius*2, fill="white")
button_image = canvas.create_image(button_x + button_radius, button_y + button_radius, image=button_icon)

# Bind the click event to the button
canvas.tag_bind(button_image, "<Button-1>", lambda event: get_weather())
canvas.place(relx=0.9, rely=0.03,anchor=tk.CENTER)


city_label = tk.Label(root, font=("Helvetica", 30))
city_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

temperature_label = tk.Label(root, font=("Helvetica", 40))
temperature_label.place(relx=0.5, rely=0.53,anchor=tk.CENTER)

condition_label = tk.Label(root, font=("Helvetica", 20))
condition_label.place(relx=0.5, rely=0.6,anchor=tk.CENTER)

humidity_label = tk.Label(root, font=("Helvetica", 12))
humidity_label.place(relx=0.7, rely=0.8, anchor=tk.CENTER)

humidity_num = tk.Label(root, font=("Helvetica", 20))
humidity_num.place(relx=0.7, rely=0.75, anchor=tk.CENTER)

wind_speed_label = tk.Label(root, font=("Helvetica", 12))
wind_speed_label.place(relx=0.3, rely=0.8, anchor=tk.CENTER)

wind_speed_num = tk.Label(root, font=("Helvetica", 20))
wind_speed_num.place(relx=0.3, rely=0.75, anchor=tk.CENTER)

selected_option = tk.StringVar(root)
selected_option.set("Language")

options = ["English", "Chinese", "Vietnamese", "Korean"]

dropdown = tk.OptionMenu(root, selected_option, *options, command=option_selected)
dropdown.pack(side=tk.BOTTOM, anchor="s")

root.mainloop()