from tkinter import *
import requests
import json
import datetime
from PIL import ImageTk, Image
import urllib.parse



# Put your OpenWeatherMap API key here
api_key = '9cf4f8f31e7c3bcaa6021d05556ccb61'



# Main window setup
root = Tk()
root.title("Weather App")
root.geometry("450x700")
background_image = Image.open("back_ground.jpg") 
background_image = background_image.resize((2000, 800),Image.Resampling.LANCZOS)# Make sure the image is in the same folder
bg = ImageTk.PhotoImage(background_image)

# Create a label with the background image
background_label = Label(root, image=bg)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Now add widgets *after* placing the background
label = Label(root, text="Weather App \n Author: Given Ikaneng", font=("Helvetica", 20), bg='lightblue')
label.place(relx=0.5, y=20, anchor="n")




try:
    background_img = ImageTk.PhotoImage(Image.open('logo.png'))
    panel = Label(root, image=background_img)
    panel.place(x=0, y=520)
except:
    print("myimage.jpeg not found. Replace or remove this part.")


# Date & Time
dt = datetime.datetime.now()

date = Label(root, text=dt.strftime('%A --'), bg='lightblue', font=("bold", 15))
date.place(x=5, y=130)

month = Label(root, text=dt.strftime('%m %B'), bg='lightblue', font=("bold", 15))
month.place(x=100, y=130)

hour = Label(root, text=dt.strftime('%I : %M %p'), bg='lightblue', font=("bold", 15))
hour.place(x=10, y=160)

# Time-based icon
hour_now = int(dt.strftime('%H'))

#  Ensure these images exist (sun.png and moon.png)
try:
    if hour_now >= 20 or hour_now <= 5:
        img = ImageTk.PhotoImage(Image.open('moon.png'))  # Night
    else:
        img = ImageTk.PhotoImage(Image.open('sun.png'))   # Day
    panel_theme = Label(root, image=img)
    panel_theme.place(x=210, y=200)
except:
    print("sun.png or moon.png not found. Add them or remove this part.")

# City input
city_var = StringVar()
city_entry = Entry(root, textvariable=city_var, width=45)
city_entry.grid(row=1, column=0, ipady=10, sticky=W+E+N+S)

# Labels for output
lable_citi = Label(root, text="...", bg='lightblue', font=("bold", 15))
lable_citi.place(x=10, y=63)

lable_country = Label(root, text="...", bg='lightblue', font=("bold", 15))
lable_country.place(x=135, y=63)

lable_lon = Label(root, text="...", bg='lightblue', font=("Helvetica", 15))
lable_lon.place(x=25, y=95)

lable_lat = Label(root, text="...", bg='lightblue', font=("Helvetica", 15))
lable_lat.place(x=95, y=95)

lable_temp = Label(root, text="...", bg='lightblue', font=("Helvetica", 110), fg='black')
lable_temp.place(x=18, y=220)

humi = Label(root, text="Humidity: ", bg='lightblue', font=("bold", 15))
humi.place(x=3, y=400)

lable_humidity = Label(root, text="...", bg='lightblue', font=("bold", 15))
lable_humidity.place(x=107, y=400)

maxi = Label(root, text="Max. Temp.: ", bg='lightblue', font=("bold", 15))
maxi.place(x=3, y=430)

max_temp = Label(root, text="...", bg='lightblue', font=("bold", 15))
max_temp.place(x=128, y=430)

mini = Label(root, text="Min. Temp.: ", bg='lightblue', font=("bold", 15))
mini.place(x=3, y=460)

min_temp = Label(root, text="...", bg='lightblue', font=("bold", 15))
min_temp.place(x=128, y=460)

note = Label(root, text="All temperatures in degree celsius", bg='white', font=("italic", 10))
note.place(x=95, y=495)

# Function to get weather data
def get_weather():
   
    
    city = city_var.get().strip()
    if city == "":
      lable_citi.config(text="Enter city name")
      return
    city = urllib.parse.quote(city)


    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

# Check for valid city
        if data.get("cod") != 200:
          lable_citi.config(text="City not found")
          return


        # Extracting values
        current_temp = data['main']['temp']
        humidity = data['main']['humidity']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        lon = data['coord']['lon']
        lat = data['coord']['lat']
        country = data['sys']['country']
        city_name = data['name']

        # Update GUI labels
        lable_temp.config(text=f"{current_temp:.1f}")
        lable_humidity.config(text=f"{humidity}%")
        max_temp.config(text=f"{temp_max}°C")
        min_temp.config(text=f"{temp_min}°C")
        lable_lon.config(text=f"Lon: {lon}")
        lable_lat.config(text=f"Lat: {lat}")
        lable_country.config(text=country)
        lable_citi.config(text=city_name)

    except Exception as e:
        lable_citi.config(text="Error")
        print("Error fetching weather data:", e)

# Search button
city_nameButton = Button(root, text="Search", command=get_weather)
city_nameButton.grid(row=1, column=1, padx=5, sticky=W+E+N+S)

# Run the app
root.mainloop()
