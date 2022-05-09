import random
import tkinter.messagebox
import winsound
from tkinter import *
import string
from time import sleep
import numpy as np
import pandas as pd


class hangman:
    """This class has been defined to create hangman game and includes  steps"""

    # Step1 :
    def __init__(self):
        """ This function includes three steps:
         Step 1_a: Creates the tkinter window and set properties
         Step 1_b: Sets some variables to use in the game
         Step 1_c: Calls needed functions to start program for the first time"""

        # Step 1_a:
        self.root = Tk()  # The main window
        self.root.geometry('600x400')  # Size of the main window
        self.root.resizable(width=False, height=False)  # Disable the size of it
        self.root.title('Hangman game')  # Title of it

        # Step 1_b:
        self.level_of_the_game = 0
        self.initial_score = 100
        self.win_score = 500
        self.lose_score = 0
        self.input_letters_by_client = []  # To store entered letters by client
        self.index_of_input_letters_by_client = []  # To store index of the entered letters by client
        self.entry_section_list = []  # To store and make boxes with appropriate numbers
        self.input_section_list = []  # To store string values in the boxes
        self.list_of_labels_of_text = []  # To store labels, including texts to show to client to be removed one by one
        winsound.PlaySound('music.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)  # Play a music in the background

        # Step 1_c:
        self.insert_pictures()
        self.read_hangman_words()
        self.read_word()
        self.separate_word_into_letters()
        self.create_entry_sections()
        self.fill_entry_sections_with_chosen_letters_as_help()
        self.buttons()
        self.create_player_score_label()
        self.root.mainloop()

    # Step 2:
    def insert_pictures(self):
        """"This function inserts all pictures needed for the game and set background label"""

        self.background_picture = PhotoImage(file='background_pic.png')
        self.score_picture = PhotoImage(file='background_score_pic.png')
        self.detail_picture = PhotoImage(file='detail.png')
        self.next_button_picture = PhotoImage(file='next_pic.png')
        self.exit_button_picture = PhotoImage(file='exit.png')
        self.question_button_picture = PhotoImage(file='question.png')
        self.music_button_picture = PhotoImage(file='music_pic.png')
        self.mute_music_button_picture = PhotoImage(file='mute_music_pic.png')
        self.repeat_button_picture = PhotoImage(file='repeat_pic.png')

        # Instead of inserting pictures of 26 letters(list of alphabets) one by one, I used a loop to insert all of them
        self.alphabet_string = string.ascii_lowercase
        self.alphabet_list = list(self.alphabet_string)
        self.alphabet_list_copy = self.alphabet_list.copy()
        for i in range(len(self.alphabet_list)):
            self.alphabet_list[i] = PhotoImage(file=f'{self.alphabet_list[i]}.png')
        # Set background label
        self.background_label = Label(master=self.root, image=self.background_picture)  # Set background picture
        self.background_label.place(x=0, y=0)

    # Step 3:
    def read_hangman_words(self):
        """This function reads words of hangman data with more than 200 words
        then chose 100 of them randomly and lists them"""

        filepath = 'hangman_data.csv'
        data = pd.read_csv(filepath)  # Read words from data
        index_of_random_words = np.random.randint(0, data.shape[0], 100)  # Chose 100 of them randomly
        self.list_of_words = data.iloc[index_of_random_words].values
        print('All words in the list that you can guess their letters are :\n', data.iloc[index_of_random_words].reset_index())

    # Step 4:
    def read_word(self):
        """ This function reads just one word of the variable 'list_words' for each level of the game"""

        self.word = self.list_of_words[self.level_of_the_game][0]
        print(f'In this level ({self.level_of_the_game} level) of the game you must guess : [{self.word}]')

    # Step 5:
    def separate_word_into_letters(self):
        """This function separates letters of the word, then with the help of 'random. sample' and based on below conditions
        shows some letters to the client as help and keep others to guess. Finally, This function gives
         us self.letters_to_show, self.index_of_letters_to_show, self.letters_to_show, self.index_of_letters_to_show """

        self.word_separated_by_letters = list(self.word)
        length_word = len(self.word)
        if length_word <= 3:
            chosen_letters_plus_indexes = random.sample(list(enumerate(self.word_separated_by_letters)), 2)
        elif 8 < length_word <= 12:
            chosen_letters_plus_indexes = random.sample(list(enumerate(self.word_separated_by_letters)), 5)

        elif 3 < length_word <= 5:
            chosen_letters_plus_indexes = random.sample(list(enumerate(self.word_separated_by_letters)), 3)

        elif 5 < length_word <= 8:
            chosen_letters_plus_indexes = random.sample(list(enumerate(self.word_separated_by_letters)), 4)

        else:
            chosen_letters_plus_indexes = random.sample(list(enumerate(self.word_separated_by_letters)), 6)

        # Command enumerate includes the random letters with their indexes
        # So for better understand I separate chosen_letter from their indexes:
        length_chosen_letters = len(chosen_letters_plus_indexes)
        self.letters_to_show = []  # To store chosen letters by random.sample
        self.index_of_letters_to_show = []  # To store index of chosen letters by random.sample
        for i in range(length_chosen_letters):
            self.letters_to_show.append(chosen_letters_plus_indexes[i][1])
            self.index_of_letters_to_show.append(chosen_letters_plus_indexes[i][0])

    # Step 6:
    def create_entry_sections(self):
        """ This function creates enough boxes(entry sections) based of length word."""

        self.x_position = 100  # The starting x_point of the first box
        self.y_position = 65  # The starting y_point of the first box

        for i in range(len(self.word)):
            self.entry_section_list.append(StringVar())
            self.input_section_list.append(
                Entry(self.root, textvariable=self.entry_section_list[i], font=("Calibri", 25),
                      disabledforeground='black', disabledbackground='lightblue', state='disabled'))
            self.input_section_list[i].place(x=self.x_position, y=self.y_position, width=40, height=40)
            self.x_position += 45

    # Step 7:
    def fill_entry_sections_with_chosen_letters_as_help(self):
        """This function fills boxes(entry_sections) with chosen letters by 'random. sample' discussed before"""

        for j in range(len(self.word)):
            if j in self.index_of_letters_to_show:
                self.entry_section_list[j].set(self.word[j])

    # Step 8:
    def buttons(self):
        """"This function set all buttons needed in the game"""

        self.button_a = Button(self.root, image=self.alphabet_list[0],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('a'))

        self.button_a.place(x=12, y=203)
        self.button_b = Button(self.root, image=self.alphabet_list[1],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('b'))
        self.button_b.place(x=92, y=203)
        self.button_c = Button(self.root, image=self.alphabet_list[2],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('c'))
        self.button_c.place(x=172, y=203)
        self.button_d = Button(self.root, image=self.alphabet_list[3],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('d'))
        self.button_d.place(x=252, y=203)
        self.button_e = Button(self.root, image=self.alphabet_list[4],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('e'))
        self.button_e.place(x=332, y=203)
        self.button_f = Button(self.root, image=self.alphabet_list[5],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('f'))
        self.button_f.place(x=412, y=203)
        self.button_g = Button(self.root, image=self.alphabet_list[6],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('g'))
        self.button_g.place(x=492, y=203)
        self.button_h = Button(self.root, image=self.alphabet_list[7],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('h'))
        self.button_h.place(x=12, y=243)
        self.button_i = Button(self.root, image=self.alphabet_list[8],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('i'))
        self.button_i.place(x=92, y=243)
        self.button_j = Button(self.root, image=self.alphabet_list[9],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('j'))
        self.button_j.place(x=172, y=243)
        self.button_k = Button(self.root, image=self.alphabet_list[10],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('k'))
        self.button_k.place(x=252, y=243)
        self.button_l = Button(self.root, image=self.alphabet_list[11],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('l'))
        self.button_l.place(x=332, y=243)
        self.button_m = Button(self.root, image=self.alphabet_list[12],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('m'))
        self.button_m.place(x=412, y=243)
        self.button_n = Button(self.root, image=self.alphabet_list[13],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('n'))
        self.button_n.place(x=492, y=243)
        self.button_o = Button(self.root, image=self.alphabet_list[14],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('o'))
        self.button_o.place(x=12, y=283)
        self.button_p = Button(self.root, image=self.alphabet_list[15],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('p'))
        self.button_p.place(x=92, y=283)
        self.button_q = Button(self.root, image=self.alphabet_list[16],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('q'))
        self.button_q.place(x=172, y=283)
        self.button_r = Button(self.root, image=self.alphabet_list[17],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('r'))
        self.button_r.place(x=252, y=283)
        self.button_s = Button(self.root, image=self.alphabet_list[18],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('s'))
        self.button_s.place(x=332, y=283)
        self.button_t = Button(self.root, image=self.alphabet_list[19],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('t'))
        self.button_t.place(x=412, y=283)
        self.button_u = Button(self.root, image=self.alphabet_list[20],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('u'))
        self.button_u.place(x=492, y=283)
        self.button_v = Button(self.root, image=self.alphabet_list[21],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('v'))
        self.button_v.place(x=92, y=323)
        self.button_w = Button(self.root, image=self.alphabet_list[22],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('w'))
        self.button_w.place(x=172, y=323)
        self.button_x = Button(self.root, image=self.alphabet_list[23],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('x'))
        self.button_x.place(x=252, y=323)
        self.button_y = Button(self.root, image=self.alphabet_list[24],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('y'))
        self.button_y.place(x=332, y=323)
        self.button_z = Button(self.root, image=self.alphabet_list[25],
                               command=lambda: self.fill_entry_sections_with_guessed_letters_by_client('z'))
        self.button_z.place(x=412, y=323)

        self.button_next = Button(self.root, borderwidth=0, height=43, background='lightblue',
                                  image=self.next_button_picture, command=lambda: self.next_level())
        self.button_next.place(x=478, y=153)

        self.button_repeat = Button(self.root, borderwidth=0, image=self.repeat_button_picture,
                                    command=lambda: self.repeat())
        self.button_repeat.place(x=494, y=346)

        self.button_help = Button(self.root, image=self.question_button_picture,
                                  command=lambda: self.detail())
        self.button_help.place(x=108, y=0)

        self.button_music = Button(self.root, image=self.music_button_picture, command=lambda: self.play_music_in_background())
        self.button_music.place(x=36, y=0)

        self.button_mute_music = Button(self.root, image=self.mute_music_button_picture, command=lambda: self.mute_music_in_background())
        self.button_mute_music.place(x=72, y=0)

        self.button_exit = Button(self.root, image=self.exit_button_picture, command=lambda: self.exit())
        self.button_exit.place(x=0, y=0)

    # Step 9:
    def fill_entry_sections_with_guessed_letters_by_client(self, letter):
        """ This function firstly checks if the box is empty or not, if so , fills it out with entered letters by client
        """
        for i in range(len(self.word)):
            if i in self.index_of_letters_to_show:
                pass

            else:
                self.index_of_letters_to_show.append(i)
                self.entry_section_list[i].set(letter)
                a = self.entry_section_list[i].get()
                self.input_letters_by_client.append(a)
                self.index_of_input_letters_by_client.append(i)
                break

    # Step 10:
    def check_if_the_guess_is_correct_or_not(self):
        """This function includes step a and step b:
        Step 10_a: Checks whether all entered letters by client are correct or not, if so, return correctness_of_all_letters with 1 value.
        Step 10_b: Creates a label and show a suitable text to the client"""

        # Step 10_a:
        count = 0  # Used in below loop
        self.correctness_of_all_letters = 0
        try:
            for i in self.index_of_input_letters_by_client:
                if self.word[i] == self.input_letters_by_client[count]:
                    count += 1
                    self.correctness_of_all_letters = 1
                else:
                    self.correctness_of_all_letters = 0

        except:
            self.correctness_of_all_letters = 0

        # Step 10_b:
        self.text = Label(self.root, text='', background='#1ff05a', font=("Arial", 10), height=1, width=62)
        self.text.place(x=100, y=40)
        if self.correctness_of_all_letters == 1:
            self.text['text'] = f'Congratulations. Your previous guess was correct and the word was: {self.word}'
            self.list_of_labels_of_text.append(self.text)
            self.update_player_score()
        else:
            self.text['text'] = f'Sorry.Your previous guess was not correct.The correct word was: {self.word}'
            self.text['background'] = '#f31c26'
            self.list_of_labels_of_text.append(self.text)
            self.update_player_score()

    # Step 11:
    def create_player_score_label(self):
        """" This function creates player_score_label"""

        self.player_score_label = Label(self.root, text=self.initial_score, background='#42210b',
                                        font=("Arial Black", 13), width=12, height=1, foreground='green',
                                        relief="flat",
                                        borderwidth=0, cursor="heart man")
        self.player_score_label.place(x=229, y=378)

    # Step 12:
    def update_player_score(self):
        """ This function updates the player_score and set it to player_score_label"""

        if self.correctness_of_all_letters == 1:
            self.initial_score += 20
        else:
            self.initial_score -= 20

        if self.initial_score == 1000:
            tkinter.messagebox.showinfo('Congratulations', f'You won. Your score is : {self.initial_score} \nAfter clicking Ok, the game will be closed in 3 seconds')
            sleep(3)
            self.exit()
        elif self.initial_score == 0:
            tkinter.messagebox.showerror('Game over', f'Sorry. You lost. Your score is : {self.initial_score} \nAfter clicking Ok, the game will be closed in 3 seconds')
            sleep(3)
            self.exit()

        self.create_player_score_label()

    # Step 13:
    def make_entry_sections_invisible(self):
        """This function makes entry sections(boxes) invisible, since when we click on the next_button or repeat_button, we need to see new boxes, not old ones"""

        for j in range(len(self.word)):  # We need to remove all boxes in input_section_list
            self.input_section_list[j].place_forget()

    # Step 14:
    def make_text_labels_invisible(self):
        """This function makes text_labels invisible, since when we click on the repeat_button, we do not like to see old messages"""

        for i in range(len(self.list_of_labels_of_text)):
            self.list_of_labels_of_text[i].place_forget()

    # Step 15:
    def next_level(self):
        """This function calls other functions and goes to the next step, since you clicked the next_button"""

        self.level_of_the_game += 1
        self.check_if_the_guess_is_correct_or_not()
        self.make_entry_sections_invisible()
        self.input_letters_by_client = []
        self.index_of_input_letters_by_client = []
        self.input_section_list = []
        self.entry_section_list = []
        self.read_word()
        self.separate_word_into_letters()
        self.create_entry_sections()
        self.fill_entry_sections_with_chosen_letters_as_help()
        self.buttons()

    # Step 16:
    def repeat(self):
        """This function restarts the program and goes to first step, since you clicked on the repeat_button"""
        tkinter.messagebox.showinfo('Repeat', 'This action helps you to restart the game from the first level')
        self.initial_score = 100
        self.level_of_the_game = 0
        self.make_entry_sections_invisible()
        self.make_text_labels_invisible()
        self.input_letters_by_client = []
        self.index_of_input_letters_by_client = []
        self.input_section_list = []
        self.entry_section_list = []
        self.create_player_score_label()
        self.read_hangman_words()
        self.read_word()
        self.separate_word_into_letters()
        self.create_entry_sections()
        self.fill_entry_sections_with_chosen_letters_as_help()
        self.buttons()

    # Step 17:
    def play_music_in_background(self):
        winsound.PlaySound('music.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)

    # Step 18:
    def mute_music_in_background(self):
        winsound.PlaySound(None, winsound.SND_PURGE)

    # Step 19:
    def detail(self):
        """This function gives you useful information about the performance of the game"""

        self.root1 = Toplevel()  # Set a window to show information
        self.root1.title('Detail of the game')  # Set title
        Label(self.root1, image=self.detail_picture).pack()  # Set the image, including information
        self.root1.mainloop()

    # Step 20:
    def exit(self):
        """This function closes the tkinter window and ends the game"""
        self.root.destroy()


run_game = hangman()  # Create an object of the defined class
