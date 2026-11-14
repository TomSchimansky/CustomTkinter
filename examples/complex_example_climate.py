"""
Complex example: climate overview of European capitals, with a map (TkinterMapView) and a chart (matplotlib).

This example needs two more packages:

    pip install matplotlib tkintermapview
"""

import os
import tkinter
import customtkinter

try:
    from PIL import Image
    import tkintermapview
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError as error:
    raise SystemExit(f"{error.name} is missing, install the packages for this example with: pip install matplotlib tkintermapview")

customtkinter.set_appearance_mode("system")  # Modes: "system" (standard), "dark", "light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# approximate monthly averages of 1991-2020: temperature in °C, precipitation in mm, sunshine in hours
CITIES = {
    "Amsterdam": {"country": "Netherlands", "position": (52.370, 4.895),
                  "temperature": [3.9, 4.2, 6.6, 9.7, 13.3, 15.9, 18.0, 17.9, 15.2, 11.3, 7.5, 4.6],
                  "precipitation": [68, 56, 55, 39, 53, 66, 79, 87, 82, 84, 82, 76],
                  "sunshine": [63, 85, 141, 199, 233, 222, 225, 208, 155, 115, 64, 52]},
    "Athens": {"country": "Greece", "position": (37.984, 23.728),
               "temperature": [9.9, 10.6, 12.8, 16.3, 21.0, 25.9, 28.6, 28.6, 24.6, 19.9, 15.4, 11.5],
               "precipitation": [51, 44, 43, 27, 17, 9, 6, 5, 18, 39, 64, 70],
               "sunshine": [130, 134, 183, 231, 291, 336, 363, 343, 270, 210, 155, 120]},
    "Berlin": {"country": "Germany", "position": (52.520, 13.405),
               "temperature": [0.9, 1.9, 5.0, 10.0, 14.5, 17.8, 20.0, 19.6, 15.3, 10.3, 5.3, 1.9],
               "precipitation": [42, 36, 37, 30, 55, 60, 59, 63, 47, 37, 43, 47],
               "sunshine": [51, 76, 127, 207, 245, 245, 249, 230, 172, 116, 56, 40]},
    "Budapest": {"country": "Hungary", "position": (47.498, 19.040),
                 "temperature": [0.6, 2.6, 7.1, 12.6, 17.2, 20.9, 23.0, 22.8, 17.6, 12.0, 6.4, 1.6],
                 "precipitation": [37, 34, 32, 40, 64, 68, 56, 59, 50, 39, 52, 43],
                 "sunshine": [64, 96, 148, 197, 245, 262, 290, 274, 202, 156, 79, 54]},
    "Copenhagen": {"country": "Denmark", "position": (55.676, 12.568),
                   "temperature": [1.4, 1.3, 3.3, 7.3, 11.6, 15.1, 17.6, 17.5, 14.1, 9.9, 5.8, 2.9],
                   "precipitation": [46, 31, 35, 31, 46, 63, 63, 72, 61, 60, 56, 54],
                   "sunshine": [44, 66, 130, 199, 255, 248, 244, 214, 156, 102, 53, 35]},
    "Dublin": {"country": "Ireland", "position": (53.350, -6.260),
               "temperature": [5.5, 5.6, 6.8, 8.6, 11.0, 13.8, 15.6, 15.3, 13.4, 10.6, 7.6, 5.9],
               "precipitation": [63, 48, 51, 50, 56, 63, 63, 73, 59, 76, 76, 74],
               "sunshine": [59, 75, 109, 160, 195, 174, 158, 154, 128, 97, 71, 53]},
    "Helsinki": {"country": "Finland", "position": (60.170, 24.938),
                 "temperature": [-3.6, -4.4, -1.1, 4.2, 10.3, 14.8, 17.9, 16.5, 11.7, 6.4, 2.0, -1.4],
                 "precipitation": [52, 38, 36, 32, 37, 59, 69, 80, 59, 77, 73, 61],
                 "sunshine": [33, 64, 136, 206, 283, 290, 302, 232, 152, 84, 33, 21]},
    "Lisbon": {"country": "Portugal", "position": (38.722, -9.139),
               "temperature": [11.6, 12.6, 14.9, 16.2, 18.6, 21.6, 23.5, 23.9, 22.4, 19.3, 15.1, 12.4],
               "precipitation": [100, 81, 60, 63, 46, 13, 4, 6, 33, 88, 108, 117],
               "sunshine": [142, 156, 202, 238, 292, 313, 351, 341, 268, 207, 152, 141]},
    "London": {"country": "United Kingdom", "position": (51.507, -0.128),
               "temperature": [5.8, 6.2, 8.1, 10.6, 13.9, 17.1, 19.3, 18.9, 16.2, 12.6, 8.9, 6.3],
               "precipitation": [56, 41, 37, 42, 47, 47, 47, 53, 49, 66, 60, 56],
               "sunshine": [61, 78, 115, 168, 199, 204, 212, 199, 151, 112, 70, 52]},
    "Madrid": {"country": "Spain", "position": (40.417, -3.704),
               "temperature": [6.6, 8.1, 11.2, 13.6, 17.5, 23.0, 26.2, 25.8, 21.4, 15.8, 10.3, 7.1],
               "precipitation": [32, 35, 34, 47, 48, 21, 11, 10, 25, 67, 57, 47],
               "sunshine": [149, 158, 211, 230, 286, 333, 362, 337, 250, 194, 155, 128]},
    "Oslo": {"country": "Norway", "position": (59.914, 10.752),
             "temperature": [-2.3, -2.1, 0.9, 5.6, 10.8, 14.8, 17.3, 16.1, 11.7, 6.4, 2.0, -1.6],
             "precipitation": [54, 42, 41, 44, 59, 75, 83, 98, 82, 95, 84, 54],
             "sunshine": [41, 79, 143, 190, 247, 255, 254, 207, 141, 87, 49, 33]},
    "Paris": {"country": "France", "position": (48.857, 2.352),
              "temperature": [5.4, 6.2, 9.0, 11.8, 15.2, 18.6, 20.9, 20.6, 17.2, 13.3, 8.8, 5.9],
              "precipitation": [51, 41, 42, 45, 66, 50, 62, 57, 48, 56, 56, 58],
              "sunshine": [59, 84, 136, 179, 199, 222, 231, 218, 172, 120, 69, 52]},
    "Prague": {"country": "Czechia", "position": (50.076, 14.438),
               "temperature": [-0.5, 0.8, 4.3, 9.3, 14.0, 17.4, 19.4, 19.0, 14.4, 9.2, 4.2, 0.6],
               "precipitation": [24, 23, 28, 28, 61, 70, 73, 64, 41, 30, 30, 27],
               "sunshine": [52, 77, 131, 191, 231, 237, 252, 238, 172, 115, 54, 41]},
    "Rome": {"country": "Italy", "position": (41.903, 12.496),
             "temperature": [7.9, 8.7, 11.2, 14.0, 18.2, 22.4, 25.2, 25.4, 21.6, 17.5, 12.6, 9.0],
             "precipitation": [67, 73, 58, 81, 53, 34, 19, 33, 68, 113, 111, 91],
             "sunshine": [121, 132, 167, 201, 264, 285, 332, 298, 237, 195, 129, 112]},
    "Stockholm": {"country": "Sweden", "position": (59.329, 18.069),
                  "temperature": [-0.7, -1.2, 1.6, 6.3, 11.4, 15.7, 18.4, 17.4, 12.9, 7.6, 3.6, 0.6],
                  "precipitation": [40, 30, 27, 30, 36, 59, 61, 72, 51, 52, 49, 45],
                  "sunshine": [40, 74, 155, 218, 293, 286, 295, 239, 165, 101, 51, 30]},
    "Vienna": {"country": "Austria", "position": (48.208, 16.374),
               "temperature": [0.9, 2.5, 6.6, 11.6, 16.2, 19.8, 21.9, 21.4, 16.6, 11.1, 5.8, 1.7],
               "precipitation": [39, 44, 51, 46, 72, 70, 69, 72, 64, 40, 49, 45],
               "sunshine": [63, 94, 141, 203, 248, 261, 285, 270, 192, 136, 69, 51]},
    "Warsaw": {"country": "Poland", "position": (52.230, 21.012),
               "temperature": [-1.5, -0.5, 3.0, 9.0, 14.3, 17.6, 19.6, 18.9, 13.9, 8.6, 3.9, 0.0],
               "precipitation": [33, 29, 34, 33, 60, 66, 77, 62, 51, 37, 36, 35],
               "sunshine": [43, 64, 121, 189, 253, 250, 259, 247, 172, 112, 44, 30]},
}

NOTES = {
    "Amsterdam": "Mild and wet all year, a light rain jacket is never wrong. Cycling along the canals is best from May to September.",
    "Athens": "Very hot and dry in July and August. Spring and autumn are much better for walking up to the Acropolis.",
    "Berlin": "Warm summers and grey winters. Swimming in the lakes from June to August, Christmas markets in December.",
    "Budapest": "Hot summers and cold winters. The thermal baths are worth a visit in every season.",
    "Copenhagen": "Windy and cool most of the year. Long summer evenings, but very short days in December.",
    "Dublin": "Mild winters and cool summers, the rain is spread over the whole year.",
    "Helsinki": "The coldest capital in this list. Snow from December to March, white nights in June.",
    "Lisbon": "Warm and sunny, the winters are mild but rainy. The Atlantic is cold even in summer.",
    "London": "Mild and changeable weather, it rarely gets really hot or really cold.",
    "Madrid": "Hot and dry summers, cold nights in winter because of the altitude.",
    "Oslo": "Cold winters with snow and pleasant summers. August and October are the wettest months.",
    "Paris": "Mild climate with rain in every month. Spring and early autumn are the best time to visit.",
    "Prague": "Rather dry, most of the rain falls in summer thunderstorms. Cold winters.",
    "Rome": "Hot summers and mild winters, October and November are the wettest months.",
    "Stockholm": "Cold winters, but sunny summers with very long days.",
    "Vienna": "Warm summers and cold winters, often windy.",
    "Warsaw": "Continental climate with cold winters and warm summers.",
}

MAP_STYLES = {
    "Google Satellite": ("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", 22),
    "Google Maps": ("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", 22),
    "OpenStreetMap": ("https://tile.openstreetmap.org/{z}/{x}/{y}.png", 19),
}

LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_images", "CustomTkinter_logo_single.png")

THEME = customtkinter.ThemeManager.theme
ACCENT_COLOR = THEME["CTkButton"]["fg_color"]  # (light, dark) color of the current theme
GRAY_TEXT_COLOR = ("gray40", "gray60")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("CustomTkinter complex_example_climate.py")
        self.iconphoto(True, tkinter.PhotoImage(file=LOGO_PATH))  # window icon on Linux, Dock icon on macOS
        self.geometry("1240x780")
        self.minsize(1000, 660)

        # CTkFont objects can be changed later, all widgets that use them are updated
        self.title_font = customtkinter.CTkFont(size=26, weight="bold")
        self.value_font = customtkinter.CTkFont(size=20, weight="bold")

        self.city = None
        self.notes = {}

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.create_sidebar()
        self.create_main_view()

        self.select_city("Berlin")
        # matplotlib doesn't know the appearance mode, the chart is drawn again when it changes, also when the system changes it
        customtkinter.AppearanceModeTracker.add(self.appearance_mode_changed)

    # ------------------------------------------------------------------ layout

    def create_sidebar(self):
        sidebar = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(2, weight=1)

        logo = customtkinter.CTkImage(Image.open(LOGO_PATH), size=(30, 30))
        customtkinter.CTkLabel(sidebar, text="  CustomTkinter", image=logo, compound="left",
                               font=self.value_font).grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        customtkinter.CTkLabel(sidebar, text="Complex Example", text_color=GRAY_TEXT_COLOR).grid(row=1, column=0, padx=20, sticky="w")

        city_list = customtkinter.CTkScrollableFrame(sidebar, width=160, fg_color="transparent")
        city_list.grid(row=2, column=0, padx=(10, 5), pady=(15, 10), sticky="nsew")
        city_list.grid_columnconfigure(0, weight=1)
        self.city_buttons = {}
        for row, name in enumerate(CITIES):
            button = customtkinter.CTkButton(city_list, text=name, anchor="w", height=32, fg_color="transparent",
                                             text_color=("gray10", "gray90"), hover_color=("gray75", "gray25"),
                                             command=lambda name=name: self.select_city(name))
            button.grid(row=row, column=0, padx=(0, 5), pady=2, sticky="ew")
            self.city_buttons[name] = button

        customtkinter.CTkLabel(sidebar, text="Appearance mode:", anchor="w").grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        appearance_menu = customtkinter.CTkOptionMenu(sidebar, values=["System", "Light", "Dark"], command=self.change_appearance_mode)
        appearance_menu.grid(row=4, column=0, padx=20, pady=(5, 10), sticky="ew")
        customtkinter.CTkLabel(sidebar, text="UI scaling:", anchor="w").grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        scaling_menu = customtkinter.CTkOptionMenu(sidebar, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling)
        scaling_menu.grid(row=6, column=0, padx=20, pady=(5, 20), sticky="ew")
        scaling_menu.set("100%")

    def create_main_view(self):
        main = customtkinter.CTkFrame(self, fg_color="transparent")
        main.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        # uniform: the columns and rows keep their proportions, also when the content of the tabview changes
        main.grid_columnconfigure(0, weight=3, uniform="columns")
        main.grid_columnconfigure(1, weight=2, uniform="columns")
        main.grid_rowconfigure((2, 3), weight=1, uniform="rows")

        # header with the name of the selected city
        header = customtkinter.CTkFrame(main, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        self.city_label = customtkinter.CTkLabel(header, font=self.title_font)
        self.city_label.grid(row=0, column=0, sticky="w")
        self.location_label = customtkinter.CTkLabel(header, text_color=GRAY_TEXT_COLOR)
        self.location_label.grid(row=0, column=1, padx=15, pady=(6, 0), sticky="w")

        self.create_value_cards(main)
        self.create_map(main)
        self.create_chart(main)
        self.create_options(main)
        self.create_notes(main)

    def create_value_cards(self, master):
        cards = customtkinter.CTkFrame(master, fg_color="transparent")
        cards.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        cards.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="cards")

        self.mean_card = self.create_value_card(cards, "Yearly mean", column=0)
        self.warmest_card = self.create_value_card(cards, "Warmest month", column=1)
        self.precipitation_card = self.create_value_card(cards, "Precipitation", column=2)
        self.sunshine_card = self.create_value_card(cards, "Sunshine", column=3)
        self.sunshine_bar = customtkinter.CTkProgressBar(self.sunshine_card["frame"], height=6)
        self.sunshine_bar.grid(row=3, column=0, padx=15, pady=(0, 12), sticky="ew")

    def create_value_card(self, master, title, column):
        frame = customtkinter.CTkFrame(master)
        frame.grid(row=0, column=column, padx=(0, 20) if column < 3 else 0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        customtkinter.CTkLabel(frame, text=title, text_color=GRAY_TEXT_COLOR).grid(row=0, column=0, padx=15, pady=(10, 0), sticky="w")
        value = customtkinter.CTkLabel(frame, font=self.value_font)
        value.grid(row=1, column=0, padx=15, sticky="w")
        detail = customtkinter.CTkLabel(frame, text_color=GRAY_TEXT_COLOR)
        detail.grid(row=2, column=0, padx=15, pady=(0, 8), sticky="w")
        return {"frame": frame, "value": value, "detail": detail}

    def create_map(self, master):
        card = customtkinter.CTkFrame(master)
        card.grid(row=2, column=0, padx=(0, 20), pady=(0, 20), sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)

        self.search_entry = customtkinter.CTkEntry(card, placeholder_text="Search a place on the map")
        self.search_entry.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="ew")
        self.search_entry.bind("<Return>", lambda event: self.search_place())
        customtkinter.CTkButton(card, text="Search", width=90, command=self.search_place).grid(row=0, column=1, padx=10, pady=10)
        self.map_style_menu = customtkinter.CTkOptionMenu(card, values=list(MAP_STYLES), width=150, command=self.change_map_style)
        self.map_style_menu.grid(row=0, column=2, padx=(0, 10), pady=10)

        self.map = tkintermapview.TkinterMapView(card, corner_radius=14)
        self.map.grid(row=1, column=0, columnspan=3, padx=10, sticky="nsew")
        self.map.set_position(50.5, 10.0)
        self.map.set_zoom(4)
        self.markers = {}
        for name, city in CITIES.items():
            self.markers[name] = self.map.set_marker(*city["position"], data=name, command=lambda marker: self.select_city(marker.data))
        self.map_style_menu.set("Google Satellite")
        self.change_map_style("Google Satellite")

        controls = customtkinter.CTkFrame(card, fg_color="transparent")
        controls.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        controls.grid_columnconfigure(1, weight=1)
        customtkinter.CTkLabel(controls, text="Zoom").grid(row=0, column=0, padx=(5, 10))
        self.zoom_slider = customtkinter.CTkSlider(controls, from_=2, to=19, number_of_steps=17,
                                                   command=lambda value: self.map.set_zoom(round(value)))
        self.zoom_slider.grid(row=0, column=1, sticky="ew")
        self.zoom_slider.set(4)
        self.after(250, self.update_zoom_slider)
        self.follow_switch = customtkinter.CTkSwitch(controls, text="Follow selection")
        self.follow_switch.grid(row=0, column=2, padx=(20, 0))
        self.follow_switch.select()

    def create_chart(self, master):
        self.chart_card = customtkinter.CTkFrame(master)
        self.chart_card.grid(row=3, column=0, padx=(0, 20), sticky="nsew")
        self.chart_card.grid_columnconfigure(0, weight=1)
        self.chart_card.grid_rowconfigure(1, weight=1)

        customtkinter.CTkLabel(self.chart_card, text="Monthly averages", anchor="w").grid(row=0, column=0, padx=15, pady=10, sticky="ew")
        self.quantity_button = customtkinter.CTkSegmentedButton(self.chart_card, values=["Temperature", "Precipitation", "Sunshine"],
                                                                command=lambda value: self.draw_chart())
        self.quantity_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        self.quantity_button.set("Temperature")

        self.figure = Figure(figsize=(4, 2.4), layout="constrained")
        self.chart = self.figure.add_subplot()
        self.chart_canvas = FigureCanvasTkAgg(self.figure, master=self.chart_card)
        self.chart_canvas.get_tk_widget().configure(highlightthickness=0)
        self.chart_canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")
        self.chart_canvas.get_tk_widget().bind("<Configure>", self.chart_resized, add="+")
        self.short_month_names = False
        self.update_chart_dpi()

    def create_options(self, master):
        tabview = customtkinter.CTkTabview(master, height=250)
        tabview.grid(row=2, column=1, pady=(0, 20), sticky="nsew")
        chart_tab = tabview.add("Chart")
        about_tab = tabview.add("About")

        chart_tab.grid_columnconfigure(1, weight=1)
        customtkinter.CTkLabel(chart_tab, text="Units").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.unit = tkinter.StringVar(value="°C")
        unit_frame = customtkinter.CTkFrame(chart_tab, fg_color="transparent")
        unit_frame.grid(row=0, column=1, padx=10, sticky="w")
        for column, unit in enumerate(("°C", "°F")):
            customtkinter.CTkRadioButton(unit_frame, text=unit, value=unit, variable=self.unit, width=60,
                                         command=self.update_city_view).grid(row=0, column=column)

        customtkinter.CTkLabel(chart_tab, text="Compare with").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.compare_box = customtkinter.CTkComboBox(chart_tab, values=["Nothing"] + list(CITIES), state="readonly",
                                                     command=lambda value: self.draw_chart())
        self.compare_box.grid(row=1, column=1, padx=10, sticky="ew")
        self.compare_box.set("Nothing")

        self.average_checkbox = customtkinter.CTkCheckBox(chart_tab, text="Show yearly mean", command=self.draw_chart)
        self.average_checkbox.grid(row=2, column=0, columnspan=2, padx=10, pady=8, sticky="w")
        self.average_checkbox.select()
        customtkinter.CTkButton(chart_tab, text="Save chart as PNG", fg_color="transparent", border_width=2,
                                text_color=("gray10", "#DCE4EE"), command=self.save_chart).grid(row=3, column=0, columnspan=2, padx=10, pady=8, sticky="ew")

        about_tab.grid_columnconfigure(0, weight=1)
        customtkinter.CTkLabel(about_tab, justify="left", anchor="w", wraplength=280,
                               text="The values are approximate monthly averages of the years 1991 to 2020. "
                                    "Click on a city in the list or on the map to see its climate.").grid(row=0, column=0, padx=10, pady=8, sticky="ew")

    def create_notes(self, master):
        card = customtkinter.CTkFrame(master)
        card.grid(row=3, column=1, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)
        self.notes_label = customtkinter.CTkLabel(card, anchor="w")
        self.notes_label.grid(row=0, column=0, padx=15, pady=10, sticky="ew")
        self.notes_textbox = customtkinter.CTkTextbox(card, wrap="word", height=100)
        self.notes_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

    # ------------------------------------------------------------------ city selection

    def select_city(self, name):
        if self.city is not None:
            self.notes[self.city] = self.notes_textbox.get("1.0", "end-1c")
            self.city_buttons[self.city].configure(fg_color="transparent", text_color=("gray10", "gray90"))
            self.markers[self.city].set_text(None)

        self.city = name
        self.city_buttons[name].configure(fg_color=ACCENT_COLOR, text_color=THEME["CTkButton"]["text_color"])
        self.markers[name].set_text(name)
        self.notes_label.configure(text=f"Notes about {name}")
        self.notes_textbox.delete("1.0", "end")
        self.notes_textbox.insert("1.0", self.notes.get(name, NOTES[name]))
        if self.follow_switch.get():
            self.map.set_position(*CITIES[name]["position"])

        self.update_city_view()

    def update_city_view(self):
        city = CITIES[self.city]
        latitude, longitude = city["position"]
        self.city_label.configure(text=self.city)
        self.location_label.configure(text=f"{city['country']}  ·  {latitude:.2f}° N, {abs(longitude):.2f}° {'E' if longitude >= 0 else 'W'}")

        temperatures = self.temperatures(self.city)
        warmest = temperatures.index(max(temperatures))
        coldest = temperatures.index(min(temperatures))
        self.mean_card["value"].configure(text=f"{sum(temperatures) / 12:.1f} {self.unit.get()}")
        self.mean_card["detail"].configure(text=f"Coldest: {MONTHS[coldest]}, {temperatures[coldest]:.1f} {self.unit.get()}")
        self.warmest_card["value"].configure(text=f"{temperatures[warmest]:.1f} {self.unit.get()}")
        self.warmest_card["detail"].configure(text=f"in {MONTHS[warmest]}")
        self.precipitation_card["value"].configure(text=f"{sum(city['precipitation'])} mm")
        self.precipitation_card["detail"].configure(text="per year")

        sunniest = max(CITIES, key=lambda name: sum(CITIES[name]["sunshine"]))
        sunshine = sum(city["sunshine"])
        self.sunshine_card["value"].configure(text=f"{sunshine:,} h".replace(",", " "))
        self.sunshine_card["detail"].configure(text="per year" if self.city == sunniest else f"{sunshine / sum(CITIES[sunniest]['sunshine']):.0%} of {sunniest}")
        self.sunshine_bar.set(sunshine / sum(CITIES[sunniest]["sunshine"]))

        self.draw_chart()

    def temperatures(self, name):
        if self.unit.get() == "°F":
            return [value * 9 / 5 + 32 for value in CITIES[name]["temperature"]]
        return CITIES[name]["temperature"]

    # ------------------------------------------------------------------ chart

    def color(self, color):
        """ hex value of a CustomTkinter color for matplotlib, colors are names like "gray20" or tuples for light and dark mode """
        if isinstance(color, (tuple, list)):
            color = color[0] if customtkinter.get_appearance_mode() == "Light" else color[1]
        red, green, blue = (value // 257 for value in self.winfo_rgb(color))
        return f"#{red:02x}{green:02x}{blue:02x}"

    def draw_chart(self):
        quantity = self.quantity_button.get()
        if quantity == "Temperature":
            values, unit = self.temperatures(self.city), self.unit.get()
        elif quantity == "Precipitation":
            values, unit = CITIES[self.city]["precipitation"], "mm"
        else:
            values, unit = CITIES[self.city]["sunshine"], "h"

        background = self.color(self.chart_card.cget("fg_color"))
        text_color = self.color(THEME["CTkLabel"]["text_color"])
        grid_color = self.color(("gray78", "gray28"))
        accent = self.color(ACCENT_COLOR)
        compare_color = self.color(("gray55", "gray55"))

        chart = self.chart
        chart.clear()
        self.figure.set_facecolor(background)
        chart.set_facecolor(background)

        months = range(12)
        if quantity == "Temperature":
            chart.fill_between(months, values, min(values) - 2, color=accent, alpha=0.12, linewidth=0)
            plot = chart.plot(months, values, color=accent, linewidth=2.5, marker="o", markersize=5, label=self.city, zorder=3)[0]
        else:
            plot = chart.bar(months, values, width=0.6, color=accent, label=self.city, zorder=3)

        handles = [plot]
        compare = self.compare_box.get()
        if compare in CITIES and compare != self.city:
            if quantity == "Temperature":
                compare_values = self.temperatures(compare)
            else:
                compare_values = CITIES[compare][quantity.lower()]
            handles += chart.plot(months, compare_values, color=compare_color, linewidth=2, linestyle="--", label=compare, zorder=4)

        if self.average_checkbox.get():
            mean = sum(values) / 12
            handles.append(chart.axhline(mean, color=text_color, linewidth=1, linestyle=":", alpha=0.7, zorder=2,
                                         label=f"Yearly mean {mean:.0f} {unit}"))

        if len(handles) > 1:
            chart.legend(handles=handles, frameon=False, labelcolor=text_color, fontsize=9, loc="best")

        chart.set_xticks(months, [month[0] for month in MONTHS] if self.short_month_names else MONTHS)
        chart.tick_params(colors=text_color, labelsize=9, length=0)
        chart.set_ylabel(unit, color=text_color, fontsize=9)
        chart.grid(axis="y", color=grid_color, linewidth=0.8)
        chart.set_axisbelow(True)
        for side, spine in chart.spines.items():
            spine.set_visible(side == "bottom")
            spine.set_color(grid_color)

        self.chart_canvas.get_tk_widget().configure(bg=background)  # can be visible for a moment when the window is resized
        self.chart_canvas.draw_idle()

    def appearance_mode_changed(self, mode):
        self.draw_chart()

    def chart_resized(self, event):
        self.update_month_names(event.width)

    def update_month_names(self, chart_width):
        """ the month names are shortened to one letter if there is not enough space for them """
        short_month_names = chart_width / 12 < 3 * self.figure.get_dpi() / 10
        if short_month_names != self.short_month_names and self.city is not None:
            self.short_month_names = short_month_names
            self.draw_chart()

    def update_chart_dpi(self):
        """ the chart has to be scaled like the widgets, for example on HighDPI displays or with set_widget_scaling() """
        dpi = 100 * customtkinter.ScalingTracker.get_widget_scaling(self)
        if self.figure.get_dpi() != dpi:
            self.figure.set_dpi(dpi)
            widget = self.chart_canvas.get_tk_widget()
            if widget.winfo_width() > 1:
                self.figure.set_size_inches(widget.winfo_width() / dpi, widget.winfo_height() / dpi)
                self.update_month_names(widget.winfo_width())
            self.chart_canvas.draw_idle()

    def save_chart(self):
        path = customtkinter.filedialog.asksaveasfilename(defaultextension=".png", initialfile=f"{self.city} {self.quantity_button.get()}.png",
                                                          filetypes=[("PNG image", "*.png")])
        if path:
            self.figure.savefig(path, dpi=200)

    # ------------------------------------------------------------------ map

    def search_place(self):
        address = self.search_entry.get().strip()
        if address:
            marker = self.map.set_address(address, marker=True, text=address)
            if marker is False:
                self.search_entry.delete(0, "end")
                self.search_entry.configure(placeholder_text=f"Nothing found for '{address}'")
                self.focus()  # shows the placeholder text again

    def change_map_style(self, style):
        url, max_zoom = MAP_STYLES[style]
        self.map.set_tile_server(url, max_zoom=max_zoom)
        for marker in self.markers.values():  # marker names have to be readable on the dark satellite images
            marker.text_color = "white" if style == "Google Satellite" else "#652A22"
            marker.draw()

    def update_zoom_slider(self):
        """ the map can also be zoomed with the mouse wheel and its buttons, the slider follows it """
        if round(self.zoom_slider.get()) != round(self.map.zoom):
            self.zoom_slider.set(round(self.map.zoom))
        self.after(250, self.update_zoom_slider)

    # ------------------------------------------------------------------ appearance mode and scaling

    def change_appearance_mode(self, mode):
        customtkinter.set_appearance_mode(mode)

    def change_scaling(self, scaling):
        customtkinter.set_widget_scaling(int(scaling.replace("%", "")) / 100)
        self.after(50, self.update_chart_dpi)


    def destroy(self):
        customtkinter.AppearanceModeTracker.remove(self.appearance_mode_changed)
        super().destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
