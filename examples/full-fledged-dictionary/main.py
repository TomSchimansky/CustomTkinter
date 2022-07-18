from tkinter import ANCHOR, BOTH, END, HORIZONTAL, LEFT, TOP, X
from ttkwidgets.autocomplete import AutocompleteEntry
import customtkinter as ctk
import tkinter as tk
import pyperclip as clip
import dictionarymethods as dt


class App(ctk.CTk):

    def __init__(self):
        
        #--------------------Main root Window--------------------#
        self.main = ctk.CTk()
        self.main.geometry('500x400')
        self.main.title("VocabiPy")
        self.selected_font = ('Fixedsys', 12)



        #--------------------Settings Frame--------------------#

        #settings frame for app settings
        self.settings_frame = ctk.CTkFrame(self.main, width=50)
        self.settings_frame.pack(fill=X, side=tk.TOP, padx=2, pady=2)
        self.settings_frame.grid_columnconfigure(3, weight=1)
        self.settings_frame.grid_rowconfigure(1, weight=1)


        #--------------------Entry Frame--------------------#

        #entry frame containing the queryinput and search button
        self.entry_frame = ctk.CTkFrame(self.main, corner_radius=10)
        self.entry_frame.pack(pady=20)


        #--------------------Inside settings_frame--------------------#

        #button for copying the meaning to clipboard
        self.copy_meaning_button = ctk.CTkButton(self.settings_frame, text="Copy Meaning", text_font=self.selected_font, width=40, command=self.CopyMeaning)
        self.copy_meaning_button.grid(row=0, column=1, padx=5, pady=5, sticky='nswe')


        #change font option menu
        self.change_font_button = ctk.CTkButton(self.settings_frame, text="Change Font", text_font=self.selected_font, command=self.ChangeFont)
        self.change_font_button.grid(row=0, column=2, padx=5, pady=5, sticky='nswe')



        #change theme option menu
        self.theme_menu = ctk.CTkOptionMenu(self.settings_frame, values=['Dark','Light','System'], text_font=self.selected_font, command=self.ChangeTheme)
        self.theme_menu.grid(row=0, column=3, padx=5, pady=5, sticky='nswe')



        #--------------------Inside entry_frame--------------------#

        #taking the query input
        self.query_entry = ctk.CTkEntry(self.entry_frame, width=180, border_width=1, placeholder_text="Search word...", text_font=('fixedsys',12))
        self.query_entry.grid(row=0, column=0, pady=5, padx=5)

        #preferred language
        self.language_entry = ctk.CTkEntry(self.entry_frame, text_font=self.selected_font, width=80, placeholder_text="language")
        self.language_entry.grid(row=0, column=1, pady=5, padx=5)
        self.language_entry.insert(0, 'english')

    
    
        #search for the meaning button
        self.search_button = ctk.CTkButton(self.entry_frame, text="Search", width=50, text_font=self.selected_font, command=self.SearchMeaning)
        self.search_button.grid(row=0, column=2, pady=5, padx=5)




        #--------------------TextBox for displaying the meanings--------------------#
        self.search_results = tk.Text(self.main, font=self.selected_font, fg='white', bg='#303031', border=0, relief='flat')
        self.search_results.pack(fill=BOTH, expand=True, pady=10, padx=10, ipadx=10, ipady=10)
        self.search_results.config(state='disabled')



        #running the app
        self.main.mainloop()




    #--------------------class App Attributes/Functions--------------------#

    #inserting the found meaning in the text box
    def SearchMeaning(self):
        language_selected = self.language_entry.get()
        self.search_results.config(state='normal')
        self.search_results.delete('1.0',END)
        entry = self.query_entry.get()
        meaning_list = dt.meaning(entry)

        if len(meaning_list) != 1:
            for meanings in meaning_list:
                final_meaning = dt.translate(meanings, language_selected)
                if final_meaning == "Couldn't translate that!":
                    self.search_results.insert(END, final_meaning)
                    return

                else:
                    self.search_results.insert(END, f"■  {final_meaning}\n\n")

        else:
            tips = "Possible causes for error :- \n    Check for Typos\n    The word might not be available in the API"
            self.search_results.insert(END, "{}\n\n{}".format(meaning_list[0], tips))

        self.search_results.config(state='disabled')


    #change theme command
    def ChangeTheme(self, mode):
        ctk.set_appearance_mode(mode)
        if mode == 'Light':
            self.search_results.config(fg='#202020', bg='#dadada')

        else:
            self.search_results.config(fg='white', bg='#303031')


    #change font command
    def ChangeFont(self):
        #getting the name of the font
        font_name_input = ctk.CTkInputDialog(master=None, text="Enter font name...", title="Change Font")
        font = font_name_input.get_input()

        #trying to change the font
        try:
            #Unfortunately there is no way to configure the font of the ctk widgets yet :(

            # self.copy_meaning_button.config(text_font=(font, 12))
            # self.change_font_button.config(text_font=(font, 12))
            # self.theme_menu.config(text_font=(font, 12))
            # self.query_entry.config(text_font=(font, 12))
            # self.search_button.config(text_font=(font, 12))
            self.selected_font = (font, 12)
            self.search_results.config(font=self.selected_font)
            
        except:
            error_message = "Couldn't change the font!"
            self.search_results.config(state='normal')
            self.search_results.insert(END, error_message)
            self.search_results.config(state='disabled')
            

    #copy the meaning
    def CopyMeaning(self):
        meaning = self.search_results.get('1.0','end')
        clip.copy(meaning)

        
        

    





    

app = App()




