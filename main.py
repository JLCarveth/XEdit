# Text Editor
# Version 0.01
# 2016/12/06
# (c) John Carveth
from tkinter import *

class TextEditor:
    def __init__(self, master):
        self.master = master
        master.title('Text Editor')

        # File path of currently open file
        self.open_now = ''

        self.text = Text(master)
        self.menubar = Menu(master)
        self.scrollbar = Scrollbar(master, command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)

        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label='Open', command=self.open_file, accelerator='Ctrl+O')
        self.file_menu.insert_separator(1)
        self.file_menu.add_command(label='Save As', command=self.save_as, accelerator='Ctrl+Shift+S')
        self.file_menu.add_command(label='Save', command=self.save_as, accelerator='Ctrl+S')

        self.editor_menu = Menu(self.menubar, tearoff=0)
        self.editor_menu.add_command(label='Clear Writing Area', command=self.erase)
        self.editor_menu.add_command(label='Options')
        
        self.menubar.add_cascade(label='File', menu=self.file_menu)
        self.menubar.add_cascade(label='Editor', menu=self.editor_menu)

        # Keybinds
        master.bind("<Control-KeyPress-S>", self.save_as)
        master.bind("<Control-o>", self.open_file)
        master.bind("<Control-s>", self.save)
        master.bind("<Control-KeyPress-Q>", self.quit_instance)

        # Grid
        self.text.grid(row=0, column=0, sticky=N+S+E+W)
        self.scrollbar.grid(row=0, column=1, sticky=N+S+E+W)
        
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.config(menu=self.menubar)

        #Brings window to top of screen
        self.text.focus_set()
        master.lift()
        master.mainloop()


    def open_file(self, *event):
        '''
        Opens a "Choose a File" dialog, prompting the user to choose a file.
        This file's content is then inserted into the text widget and the
        open_now variable is given the file path.
        '''
        content = ''
        chosen_file = filedialog.askopenfilename(title="Choose a file to open.")
        self.open_now = chosen_file
        with open(chosen_file) as file:
            for line in file:
                content = content + line
            self.text.insert(INSERT, content)
            self.master.title(chosen_file)

    def save_as(self, *event):
        '''
        Similar to open_file, asks where user wants to save their work. Creates
        an entirely new file.
        '''
        directory = filedialog.asksaveasfilename(defaultextension=".txt",title="Where do you wish to save the file?")
        content = self.get_text()
        with open(directory, 'w') as file:
            file.write(content)
        self.open_now = directory

    def save(self, *event):
        '''
        Only difference from save_as is this ovberwrites the currently opened
        file instead of saving it as a new file.
        '''
        print(self.get_text())
        if(self.open_now == ''):
            self.save_as()
        else:
            with open(self.open_now, 'w') as file:
                file.write(self.get_text())

    def get_text(self):
        '''(TextEditor)->Str
        Returns the current text in the Text Widget.
        '''
        content = self.text.get('1.0', 'end-1c')
        return content

    def quit_instance(self, event):
        '''
        Destroys the window.
        '''
        self.master.destroy()

    def erase(self):
        '''
        Clears the content from the Text widget.
        '''
        if messagebox.askokcancel(message="Are you sure you want to erase the writing area? This will erase what you have written."):
            self.text.delete("1.0", END)
        else:
            pass

if __name__ == '__main__':
    TextEditor(Tk())
