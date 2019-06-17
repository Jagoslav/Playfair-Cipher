"""
Created on Tue March 17 19:14:50 2018

@author: Jakub Grzeszczak
"""

from tkinter import filedialog
from tkinter import messagebox
from tkinter import *

alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
cipher_matrix = []
pairs_before = []
pairs_after = []
pairs_iterator = 0


def fix_phrase_to_match_alphabet(phrase):
    fixed_phrase = ""
    for letter in phrase.upper():
        if letter in alphabet:
            fixed_phrase = fixed_phrase + letter
        else:
            if letter == 'J':
                fixed_phrase = fixed_phrase + 'I'
            if letter == 'Ą':
                fixed_phrase = fixed_phrase + 'A'
            if letter == 'Ć':
                fixed_phrase = fixed_phrase + 'C'
            if letter == 'Ę':
                fixed_phrase = fixed_phrase + 'E'
            if letter == 'Ł':
                fixed_phrase = fixed_phrase + 'L'
            if letter == 'Ó':
                fixed_phrase = fixed_phrase + 'O'
            if letter == 'Ś':
                fixed_phrase = fixed_phrase + 'S'
            if letter == 'Ź':
                fixed_phrase = fixed_phrase + 'Z'
            if letter == 'Ż':
                fixed_phrase = fixed_phrase + 'Z'
    return fixed_phrase


def remove_doubles(msg):
    message = msg[0]
    for i in range(1, len(msg)):
        if message[-1] != msg[i]:
            message += msg[i]
        elif message[-1] == 'X':
            message += 'Y'
            message += msg[i]
        else:
            message += 'X'
            message += msg[i]
    if len(message) % 2 == 1:
        if message[-1] == 'X':
            message += 'Y'
        else:
            message += 'X'
    return message



def create_cipher_matrix():
    key = fix_phrase_to_match_alphabet(entry_key.get())
    matrix = []
    for i in key:
        if i in alphabet and i not in matrix:
            matrix.append(i)
    for i in alphabet:
        if i not in matrix:
            matrix.append(i)
    global cipher_matrix
    cipher_matrix = [matrix[5 * i: 5 * i + 5] for i in range(0, 5)]
    global labels_cipher_matrix
    for i in range(0, 5):
        for j in range(0, 5):
            labels_cipher_matrix[str(i) + str(j)]['text'] = cipher_matrix[i][j]


def clear_message():
    entry_input.delete(0, END)
    entry_fixed_input['state'] = 'normal'
    entry_fixed_input.delete(0, END)
    entry_fixed_input['state'] = 'readonly'
    entry_input_as_pairs['state'] = 'normal'
    entry_input_as_pairs.delete(0, END)
    entry_input_as_pairs['state'] = 'readonly'
    entry_output_as_pairs['state'] = 'normal'
    entry_output_as_pairs.delete(0, END)
    entry_output_as_pairs['state'] = 'readonly'
    entry_output['state'] = 'normal'
    entry_output.delete(0, END)
    entry_output['state'] = 'readonly'


def split_into_pairs(message):
    message = fix_phrase_to_match_alphabet(message)
    if len(message) %2 != 0:
        message = message + ('Y' if message[-1] == 'X' else 'X')
    return [message[x]+message[x+1] for x in range(0,len(message), 2)]


def encode_pair(pair, direction):
    xa, ya = None, None
    xb, yb = None, None
    for row_id in range(0, len(cipher_matrix)):
        if pair[0] in cipher_matrix[row_id]:
            xa, ya = cipher_matrix[row_id].index(pair[0]), row_id
        if pair[1] in cipher_matrix[row_id]:
            xb, yb = cipher_matrix[row_id].index(pair[1]), row_id
    if xa == xb:
        ya = (5 + ya + direction) % 5
        yb = (5 + yb + direction) % 5
    elif ya == yb:
        xa = (5 + xa + direction) % 5
        xb = (5 + xb + direction) % 5
    else:
        xa, xb = xb, xa
    return cipher_matrix[ya][xa] + cipher_matrix[yb][xb]


def encode(shift_direction):
    global cipher_matrix
    for field in labels_cipher_matrix:
        labels_cipher_matrix[field]['relief'] = 'groove'
        labels_cipher_matrix[field]['bg'] = 'SystemButtonFace'
    msg = entry_input.get()
    if msg == "":
        return
    global pairs_before
    global pairs_after
    global pairs_iterator
    msg = fix_phrase_to_match_alphabet(msg)
    if shift_direction == 1:
        msg = remove_doubles(msg)
    entry_fixed_input['state'] = 'normal'
    entry_fixed_input.delete(0, END)
    entry_fixed_input.insert(END, msg)
    entry_fixed_input['state'] = 'readonly'
    pairs_before = msg = split_into_pairs(msg)
    entry_input_as_pairs['state'] = 'normal'
    entry_input_as_pairs.delete(0, END)
    entry_input_as_pairs.insert(END, " ".join(msg))
    entry_input_as_pairs['state'] = 'readonly'
    pairs_after = msg = [encode_pair(pair, shift_direction) for pair in msg]
    pairs_iterator = len(pairs_after)
    entry_output_as_pairs['state'] = 'normal'
    entry_output_as_pairs.delete(0, END)
    entry_output_as_pairs.insert(END, " ".join(msg))
    entry_output_as_pairs['state'] = 'readonly'
    entry_output['state'] = 'normal'
    entry_output.delete(0, END)
    for pair in msg:
        entry_output.insert(END, pair)
    entry_output['state'] = 'readonly'
    if len(pairs_after) == 1:
        button_first['state'] = 'disabled'
        button_previous['state'] = 'disabled'
        button_next['state'] = 'disabled'
        button_last['state'] = 'disabled'
    else:
        button_first['state'] = 'normal'
        button_previous['state'] = 'normal'
        button_next['state'] = 'normal'
        button_last['state'] = 'normal'


def shift_pair(shift):
    global pairs_iterator
    global pairs_before
    global pairs_after
    global entry_input_as_pairs
    global label_input_pair
    global entry_output_as_pairs
    global label_output_pair
    global entry_output
    if not entry_input.get():
        return
    if shift == 'first':
        pairs_iterator = 1
    elif shift == 'prev':
        pairs_iterator = max(1, pairs_iterator - 1)
    elif shift == 'next':
        pairs_iterator = min(len(pairs_after), pairs_iterator + 1)
    elif shift == 'last':
        pairs_iterator = len(pairs_after)
    entry_output_as_pairs['state'] = 'normal'
    entry_output_as_pairs.delete(0, END)
    entry_output_as_pairs.insert(END, " ".join(pairs_after[0:pairs_iterator]))
    entry_output_as_pairs['state'] = 'readonly'
    entry_output['state'] = 'normal'
    entry_output.delete(0, END)
    entry_output.insert(END, "".join(pairs_after[0:pairs_iterator]))
    entry_output['state'] = 'readonly'
    label_input_pair['text'] = pairs_before[pairs_iterator - 1]
    label_output_pair['text'] = pairs_after[pairs_iterator - 1]
    mark_on_matrix(pairs_before[pairs_iterator - 1], pairs_after[pairs_iterator - 1])


def mark_on_matrix(to_sunk, to_raise):
    global cipher_matrix
    for field in labels_cipher_matrix:
        labels_cipher_matrix[field]['relief'] = 'groove'
        labels_cipher_matrix[field]['bg'] = 'SystemButtonFace'
    xa, ya = None, None
    xb, yb = None, None
    xc, yc = None, None
    xd, yd = None, None
    for row_id in range(0, len(cipher_matrix)):
        if to_sunk[0] in cipher_matrix[row_id]:
            xa, ya = cipher_matrix[row_id].index(to_sunk[0]), row_id
        if to_sunk[1] in cipher_matrix[row_id]:
            xb, yb = cipher_matrix[row_id].index(to_sunk[1]), row_id
        if to_raise[0] in cipher_matrix[row_id]:
            xc, yc = cipher_matrix[row_id].index(to_raise[0]), row_id
        if to_raise[1] in cipher_matrix[row_id]:
            xd, yd = cipher_matrix[row_id].index(to_raise[1]), row_id
    labels_cipher_matrix[str(ya)+str(xa)]['relief'] = 'sunken'
    labels_cipher_matrix[str(ya)+str(xa)]['bg'] = 'lightgreen'
    labels_cipher_matrix[str(yb)+str(xb)]['relief'] = 'sunken'
    labels_cipher_matrix[str(yb)+str(xb)]['bg'] = 'tomato'
    labels_cipher_matrix[str(yc)+str(xc)]['relief'] = 'raised'
    labels_cipher_matrix[str(yc)+str(xc)]['bg'] = 'lightgreen'
    labels_cipher_matrix[str(yd)+str(xd)]['relief'] = 'raised'
    labels_cipher_matrix[str(yd)+str(xd)]['bg'] = 'tomato'


def save_to_file():
    if not entry_output.get():
        messagebox.showerror("Error",
                             "Nothing to save")
        return
    filename = filedialog.asksaveasfilename(initialdir="/",
                                            title="Save file",
                                            filetypes=(("Playfair Encrypted Files", "*.pef"),
                                                       ("All files", "*.*")))
    if filename:
        try:
            if filename[-4:] == ".pef":
                file = open(filename, 'w')
            else:
                file = open(filename + '.pef', 'w')
            file.write(entry_output.get())
            messagebox.showinfo("Succes",
                                "File Saved")
            file.close()
        except IOError:
            messagebox.showerror("Error",
                                 "Failed to save a file")


def load_from_file():
    filename = filedialog.askopenfilename(title="Load file",
                                          filetypes=(("Playfair Encrypted Files", "*.pef"),
                                                     ("All files", "*.*")))
    if filename:
        try:
            file = open(filename)
            text = file.readlines()
            file.close()
            entry_input.delete(0, END)
            entry_input.insert(END, "".join(text))
        except:
            messagebox.showerror("Error",
                                 "Loading failed")


if __name__ == "__main__":
    window = Tk()
    window.title('Playfair')
    window.resizable(width=False, height=False)
    window.geometry('%dx%d+%d+%d' % (714, 320, window.winfo_screenwidth() / 2 - 357, window.winfo_screenheight() / 2 - 160))
    window.protocol('WM_DELETE_WINDOW', window.destroy)

    for i in range(0, 72):
        window.columnconfigure(i, minsize=10)
    for i in range(0, 43):
        window.rowconfigure(i, minsize=10)
    label_cipher_matrix_background = Label(window, borderwidth=10, relief='ridge')
    label_cipher_matrix_background.grid(row=0, column=0, rowspan=22, columnspan=22, stick=N+E+S+W)
    labels_cipher_matrix = {}
    for i in range(0, 5):
        for j in range(0, 5):
            labels_cipher_matrix[str(i) + str(j)] = Label(window, text=alphabet[5 * i + j], borderwidth=2, relief='groove')
            labels_cipher_matrix[str(i) + str(j)].grid(row=str(1 + i * 4),
                                                       column=str(1 + j * 4),
                                                       rowspan=4,
                                                       columnspan=4,
                                                       stick=N+E+S+W)

    #  cipher matrix related content
    label_key = Label(window, text='Key:')
    label_key.grid(row=22, column=1, rowspan=3, columnspan=3, sticky=N+E+S+W)
    entry_key = Entry(window, justify='right')
    entry_key.grid(row=22, column=4, rowspan=3, columnspan=12, sticky=E+W)

    button_set_matrix = Button(text='Set', command=lambda: create_cipher_matrix()) 
    button_set_matrix.grid(row=22, column=17, rowspan=3, columnspan=5, sticky=E+W)

    # Load'n'Save

    save_button = Button(window, text='Save\nOutput', command=save_to_file)
    save_button.grid(row=26, column=1, rowspan=4, columnspan=9, sticky=N+E+S+W)
    load_button = Button(window, text='Load\nMessage', command=load_from_file)
    load_button.grid(row=26, column=12, rowspan=4, columnspan=9, sticky=N+E+S+W)

    #  translation related content
    label_fixed_input = Label(window, text='Fixed:')
    label_fixed_input.grid(row=1, column=22, rowspan=3, columnspan=6, sticky=N+E+S)
    entry_fixed_input = Entry(window, state='readonly', justify='right')
    entry_fixed_input.grid(row=1, column=28, rowspan=3, columnspan=42, sticky=E+W)

    label_input_as_pairs = Label(window, text='Pairs:')
    label_input_as_pairs.grid(row=5, column=22, rowspan=3, columnspan=6, sticky=N+E+S)
    entry_input_as_pairs = Entry(window, state='readonly', justify='right')
    entry_input_as_pairs.grid(row=5, column=28, rowspan=3, columnspan=42, sticky=E+W)

    label_pair_text = Label(window, text='Pair:')
    label_pair_text.grid(row=9, column=37, rowspan=3, columnspan=6, sticky=N+E+S)
    label_input_pair = Label(window, borderwidth=2, relief='ridge')
    label_input_pair.grid(row=9, column=43, rowspan=3, columnspan=3, sticky=N+E+S+W)
    label_arrow = Label(window, text='->')
    label_arrow.grid(row=9, column=46, rowspan=3, columnspan=3, sticky=N+E+S+W)
    label_output_pair = Label(window, borderwidth=2, relief='ridge')
    label_output_pair.grid(row=9, column=49, rowspan=3, columnspan=3, sticky=N+E+S+W)

    label_output_as_pairs = Label(window, text='Pairs:')
    label_output_as_pairs.grid(row=13, column=22, rowspan=3, columnspan=6, sticky=N+E+S)
    entry_output_as_pairs = Entry(window, state='readonly', justify='right')
    entry_output_as_pairs.grid(row=13, column=28, rowspan=3, columnspan=42, sticky=E+W)

    label_output = Label(window, text='Output:')
    label_output.grid(row=17, column=22, rowspan=3, columnspan=6, sticky=N+E+S)
    entry_output = Entry(window, state='readonly', justify='right')
    entry_output.grid(row=17, column=28, rowspan=3, columnspan=42, sticky=E+W)

    label_input = Label(window, text='Message:')
    label_input.grid(row=21, column=21, rowspan=3, columnspan=7, sticky=N+E+S)
    entry_input = Entry(window, justify='right')
    entry_input.grid(row=21, column=28, rowspan=3, columnspan=42, sticky=E+W)

    button_encode = Button(window, text='Encode', command=lambda: encode(1))
    button_encode.grid(row=25, column=23, rowspan=3, columnspan=23, sticky=E+W)

    button_decode = Button(window, text='Decode', command=lambda: encode(-1))
    button_decode.grid(row=25, column=47, rowspan=3, columnspan=23, sticky=E+W)

    button_first = Button(window, text='first', command=lambda: shift_pair('first'), state=DISABLED)
    button_first.grid(row=28, column=23, rowspan=3, columnspan=11, sticky=E+W)
    button_previous = Button(window, text='previous', command=lambda: shift_pair('prev'), state=DISABLED)
    button_previous.grid(row=28, column=35, rowspan=3, columnspan=11, sticky=E+W)
    button_next = Button(window, text='next', command=lambda: shift_pair('next'), state=DISABLED)
    button_next.grid(row=28, column=47, rowspan=3, columnspan=11, sticky=E+W)
    button_last = Button(window, text='last', command=lambda: shift_pair('last'), state=DISABLED)
    button_last.grid(row=28, column=59, rowspan=3, columnspan=11, sticky=E+W)
    create_cipher_matrix()
    window.mainloop()
