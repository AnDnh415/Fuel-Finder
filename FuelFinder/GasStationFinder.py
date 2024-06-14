from tkinter import *
import tkintermapview
from googleplaces import GooglePlaces, types
import geocoder

#get your location
#my location has to be pulled by IP so its not as accurate. If I was using a phone, the location would be a lot more accurate
location = geocoder.ip('me')
holder = location.latlng
my_lat = holder[0]
my_lon = holder[1]

#get gas station location
#Zaim's code
api_key = 'AIzaSyB7Mbim_exyAoQKpkho325JUWpbtD72GQY'
google_places = GooglePlaces('AIzaSyB7Mbim_exyAoQKpkho325JUWpbtD72GQY')
query_result = google_places.nearby_search(lat_lng={'lat': my_lat, 'lng': my_lon}, radius=2000,types=[types.TYPE_GAS_STATION])

if query_result.has_attributions:
    print(query_result.html_attributions)

#gui window basics
#Tommy's code
root = Tk()
root.title('Fuel Finder')
root.geometry('1200x700')
root.resizable(False, False)

#getting map onto the gui
map_widget = tkintermapview.TkinterMapView(root, width=800, height=600, corner_radius=0)
map_widget.grid(row=1, column=0, padx=20, pady=20)

#map default settings
#Christian's code
map_widget.set_position(my_lat, my_lon)
my_pin = map_widget.set_marker(my_lat, my_lon, text='You', marker_color_circle='blue', marker_color_outside='black')
map_widget.set_zoom(16)

#low gas button code
#An's code
def myClick():
    popup = Tk()
    popup.title('Low Fuel!')
    popup.geometry('300x200')

    window=LabelFrame(popup)
    window.pack()

    Word_part = Label(popup, text='Your car has 25% fuel left!\n Please find a nearby gas station!', font=20, pady=20)
    Word_part.pack()

    def go_back():
        popup.destroy()

    go_back_button = Button(popup, text='Okay!', width=20, height=5, font=30, command=go_back)
    go_back_button.pack()

#gas is low stimulation (Press the button to stimulate your car being low on gas)
low_gas_stimulation = Button(root, text='Stimulate Low Gas', font=20, command=myClick)
low_gas_stimulation.grid(row=2, column=0)

#making gas station list box
gas_station_box = Listbox(root, height=38, width=50)
gas_station_box.grid(row=1, column=1, padx=15)

#adding the gas stations into the list box
#Alex's code
gas_lat_list = []
gas_lon_list = []
for place in query_result.places:
    gas_station_box.insert(END, place.name)
    gas_lat_list.append(str(place.geo_location['lat']))
    gas_lon_list.append(str(place.geo_location['lng']))

#Confirm command
def Confirm():
    global gas_pin
    global reset_button
    global route
    holding_var = gas_station_box.curselection()
    res = int(''.join(map(str, holding_var)))
    gas_lat = gas_lat_list[res]
    gas_lon = gas_lon_list[res]
    gas_pin = map_widget.set_marker((float(gas_lat)), float(gas_lon), text='Selected Gas Station', marker_color_circle='red', marker_color_outside='black')
    reset_button = Button(root, text='Deselect', font=20, command=del_pins)
    reset_button.grid(row=2, column=1)
    route = map_widget.set_path([my_pin.position, gas_pin.position], width=5)


#delete all pins command
def del_pins():
    global gas_pin
    global reset_button
    global route
    gas_pin.delete()
    reset_button.destroy()
    route.delete()

#button to confirm what gas station you want to go to
Confirm_button = Button(root, text='Confirm', font=20, command=Confirm)
Confirm_button.grid(row=2, column=1)


root.mainloop()