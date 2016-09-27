from tkinter import Tk, Menu, Message, Button, filedialog, Toplevel, \
    Label, StringVar, OptionMenu, messagebox, ttk, Frame
from examsresult.control import lng_load, center_pos
from examsresult.dbhandler import DatabaseConnector


class View(object):

    database_file = None
    db_loaded = "disabled"
    dbc = None

    def __init__(self, language='english'):
        self.tk = Tk()
        self.lng = lng_load(language=language)
        lng = self.lng['filetypes']
        self.filetypes = [
            (lng['filetype_exf'], '*.exf'),
            (lng['filetype_all'], '*')
        ]

    def connect_db(self):
        if self.database_file:
            self.dbc = DatabaseConnector(self.database_file)

        if not self.dbc:
            self.db_loaded = "disabled"
            messagebox.showerror("", self.lng['window_openfile']['msg_open_err'] % self.database_file, parent=self.tk)
        else:
            self.db_loaded = "normal"
            old_db_version, db_version = self.dbc.db_updater()
            if old_db_version and old_db_version < db_version:
                messagebox.showinfo("", self.lng['window_openfile']['msg_db_updated'], parent=self.tk)
            elif old_db_version > db_version:
                self.db_loaded = "disabled"
                messagebox.showerror("", self.lng['window_openfile']['msg_db_to_new'], parent=self.tk)

        if self.db_loaded == 'normal':
            self.tk.title(string="%s - %s" % (self.lng['main']['title'], self.database_file))
        else:
            self.tk.title(string=self.lng['main']['title'])
            self.database_file = None

        self.toggle_menu(self.db_loaded)

    def toggle_menu(self, db_state):
        # Enable/Disable Menu Entries
        menutext = self.lng['menu']
        self.editmenu.entryconfig(menutext['schoolyear'], state=db_state)
        self.editmenu.entryconfig(menutext['schoolclass'], state=db_state)
        self.editmenu.entryconfig(menutext['subject'], state=db_state)

    def action_app_close(self):
        self.tk.quit()

    def action_subject_add(self, root_window):
        # TODO: Give me something to do
        messagebox.showinfo("", "Give me something to do!", parent=root_window)
    
    def action_subject_edit(self, root_window):
        # TODO: Give me something to do
        messagebox.showinfo("", "Give me something to do!", parent=root_window)
    
    def action_subject_remove(self, root_window):
        # TODO: Give me something to do
        messagebox.showinfo("", "Give me something to do!", parent=root_window)

    def action_schoolyear_add(self, root_window):
        # TODO: Give me something to do
        messagebox.showinfo("", "Give me something to do!", parent=root_window)

    def action_schoolyear_edit(self, root_window):
        # TODO: Give me something to do
        messagebox.showinfo("", "Give me something to do!", parent=root_window)
    
    def action_schoolyear_remove(self, root_window):
        # TODO: Give me something to do
        messagebox.showinfo("", "Give me something to do!", parent=root_window)

    def action_schoolclass_add(self, root_window):
        # TODO: Give me something to do
        messagebox.showinfo("", "Give me something to do!", parent=root_window)
    
    def action_schoolclass_edit(self, root_window):
        # TODO: Give me something to do
        messagebox.showinfo("", "Give me something to do!", parent=root_window)
    
    def action_schoolclass_remove(self, root_window):
        # TODO: Give me something to do
        messagebox.showinfo("", "Give me something to do!", parent=root_window)
    
    def window_newfile(self):
        lng = self.lng['window_newfile']
        database_file = filedialog.asksaveasfilename(title=lng['title'], filetypes=self.filetypes)
        if database_file:
            self.database_file = database_file
            self.connect_db()

    def window_openfile(self):
        lng = self.lng['window_openfile']
        database_file = filedialog.askopenfilename(title=lng['title'], filetypes=self.filetypes)
        if database_file:
            self.database_file = database_file
            self.connect_db()

    def window_schoolyear(self, root_window, width=400, height=150):
        lng = self.lng['window_schoolyear']
        tk_window = Toplevel(root_window)
        tk_window.transient(root_window)
        tk_window.title(string=lng['title'])
        tk_window.minsize(width=width, height=height)
        tk_window.maxsize(width=width, height=height)
        center_pos(window_object=tk_window, width=width, height=height)

        btn_add = Button(tk_window, text=self.lng['main']['add'], command=lambda: self.action_schoolyear_add(tk_window), width=10)
        btn_edit = Button(tk_window, text=self.lng['main']['edit'], command=lambda: self.action_schoolyear_edit(tk_window), width=10)
        btn_remove = Button(tk_window, text=self.lng['main']['remove'], command=lambda: self.action_schoolyear_remove(tk_window), width=10)
        btn_close = Button(tk_window, text=self.lng['main']['close'], command=tk_window.destroy, width=10)
        btn_add.focus()
        btn_add.pack()
        btn_edit.pack()
        btn_remove.pack()
        btn_close.pack()

    def window_schoolclass(self, root_window, width=400, height=150):
        lng = self.lng['window_schoolclass']
        tk_window = Toplevel(root_window)
        tk_window.transient(root_window)
        tk_window.title(string=lng['title'])
        tk_window.minsize(width=width, height=height)
        tk_window.maxsize(width=width, height=height)
        center_pos(window_object=tk_window, width=width, height=height)

        btn_add = Button(tk_window, text=self.lng['main']['add'], command=lambda: self.action_schoolclass_add(tk_window), width=10)
        btn_edit = Button(tk_window, text=self.lng['main']['edit'], command=lambda: self.action_schoolclass_edit(tk_window), width=10)
        btn_remove = Button(tk_window, text=self.lng['main']['remove'], command=lambda: self.action_schoolclass_remove(tk_window), width=10)
        btn_close = Button(tk_window, text=self.lng['main']['close'], command=tk_window.destroy, width=10)
        btn_add.focus()
        btn_add.pack()
        btn_edit.pack()
        btn_remove.pack()
        btn_close.pack()

    def window_subject(self, root_window, width=400, height=150):
        lng = self.lng['window_subject']
        tk_window = Toplevel(root_window)
        tk_window.transient(root_window)
        tk_window.title(string=lng['title'])
        tk_window.minsize(width=width, height=height)
        tk_window.maxsize(width=width, height=height)
        center_pos(window_object=tk_window, width=width, height=height)

        btn_add = Button(tk_window, text=self.lng['main']['add'], command=lambda: self.action_subject_add(tk_window), width=10)
        btn_edit = Button(tk_window, text=self.lng['main']['edit'], command=lambda: self.action_subject_edit(tk_window), width=10)
        btn_remove = Button(tk_window, text=self.lng['main']['remove'], command=lambda: self.action_subject_remove(tk_window), width=10)
        btn_close = Button(tk_window, text=self.lng['main']['close'], command=tk_window.destroy, width=10)
        btn_add.focus()
        btn_add.pack()
        btn_edit.pack()
        btn_remove.pack()
        btn_close.pack()

    def window_about(self, root_window, width=400, height=100):
        lng = self.lng['window_about']
        tk_window = Toplevel(root_window)
        tk_window.transient(root_window)
        tk_window.title(string=lng['title'])
        tk_window.minsize(width=width, height=height)
        tk_window.maxsize(width=width, height=height)
        center_pos(window_object=tk_window, width=width, height=height)

        Message(tk_window, text=self.lng['main']['title'], width=100).pack()
        Message(tk_window, text=lng['infotext'], width=2/3 * width).pack()
        button = Button(tk_window, text=self.lng['main']['ok'], command=tk_window.destroy, width=10)
        button.focus()
        button.pack()

    def main_window(self, width=800, height=600):
        self.tk.title(string=self.lng['main']['title'])
        self.tk.minsize(width=width, height=height)
        self.tk.maxsize(width=width, height=height)
        self.tk.protocol("WM_DELETE_WINDOW", self.action_app_close)
        center_pos(window_object=self.tk, width=width, height=height)

        menutext = self.lng['menu']

        # create a pulldown menu, and add it to the menu bar
        self.menubar = Menu(self.tk)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label=menutext['newfile'], command=self.window_newfile)
        self.filemenu.add_command(label=menutext['openfile'], command=self.window_openfile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label=menutext['quit'], command=self.action_app_close)
        self.menubar.add_cascade(label=menutext['mainmenufile'], menu=self.filemenu)

        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label=menutext['schoolyear'], command=lambda: self.window_schoolyear(self.tk))
        self.editmenu.add_command(label=menutext['schoolclass'], command=lambda: self.window_schoolclass(self.tk))
        self.editmenu.add_command(label=menutext['subject'], command=lambda: self.window_subject(self.tk))
        self.menubar.add_cascade(label=menutext['mainmenuedit'], menu=self.editmenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label=menutext['about'], command=lambda: self.window_about(self.tk))
        self.menubar.add_cascade(label=menutext['mainmenuhelp'], menu=self.helpmenu)

        # display the menu
        self.tk.config(menu=self.menubar)

        # # no File to open found, ask for ...
        # if not self.database_file:
        #     self.window_openfile()

        self.toggle_menu(self.db_loaded)
        self.tk.mainloop()
