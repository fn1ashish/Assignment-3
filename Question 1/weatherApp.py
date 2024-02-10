import tkinter as tk
import requests

class APIConfig:
    def __init__(self):
        self.api_key = "3873434422c7ee8b6b11f81ef2a87393"  # API key

    def api_url(self, city):
        return f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"

class WeatherApp(tk.Tk, APIConfig):  
    def __init__(self):
        tk.Tk.__init__(self)  # (Multiple Inheritance) Initialize tk.Tk
        APIConfig.__init__(self)  # (Multiple Inheritance) Initialize APIConfig
        self.title("Weather App")  # Set the title of the window
        self.geometry("400x200")  # Set the dimensions of the window

        self.city_var = tk.StringVar()  # Variable to hold city name entered by user
        self.weather_info_var = tk.StringVar()  # Variable to hold weather information
        self.weather_info_var.set("")  # Initialize weather info to an empty string

        self.create_widgets()  # Call method to create GUI widgets

    def create_widgets(self):
        label_city = tk.Label(self, text="Enter City:")  # Label prompting user to enter city
        label_city.pack()  # Add label to window

        entry_city = tk.Entry(self, textvariable=self.city_var)  # Entry field to input city name
        entry_city.pack()  # Add entry field to window

        button_get_weather = tk.Button(self, text="Get Weather", command=self.get_weather)  # Button to fetch weather
        button_get_weather.pack()  # Add button to window

        label_weather_info = tk.Label(self, textvariable=self.weather_info_var)  # Label to display weather info
        label_weather_info.pack()  # Add label to window

    @staticmethod  
    def handle_response_errors(func):  # (Multiple Decorators) Decorator to handle request errors
        def wrapper(*args, **kwargs):  # Wrapper function to handle errors
            try:
                return func(*args, **kwargs)  # Call the original function
            except requests.exceptions.RequestException as e:  # Handle request errors
                print("Request Error:", e)  # Print error message
                return None  # Return None in case of error
        return wrapper  # Return the wrapper function

    def get_weather(self):
        city = self.city_var.get()  # Get city name entered by user
        weather_data = self.fetch_weather_data(city)  # Fetch weather data for the city
        if weather_data:  # If weather data is retrieved successfully
            self.update_weather_info(weather_data)  # Update weather info display
        else:  # If failed to fetch weather data
            self.weather_info_var.set("Failed to fetch weather information.")  # Update display with error message

    @handle_response_errors  
    def fetch_weather_data(self, city):  # Method to fetch weather data from API
        api_url = self.api_url(city)  # Generate API URL for the given city
        response = requests.get(api_url)  # Send GET request to API
        response.raise_for_status()  # Raise exception if response status is not 200
        return response.json()  # Return JSON data from the response

    def update_weather_info(self, weather_data):
        temperature = weather_data.get("main", {}).get("temp", "N/A")  # Extract temperature from weather data
        description = weather_data.get("weather", [{}])[0].get("description", "N/A")  # Extract weather description
        self.weather_info_var.set(f"Weather: {description}, Temperature: {temperature}°C")  # Update weather info display

if __name__ == "__main__":
    app = WeatherApp()  # Create instance of WeatherApp class
    app.mainloop()  # Start the Tkinter event loop



# Github Link --------( https://github.com/fn1ashish/Assignment-3.git )----------------