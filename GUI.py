import tkinter


global tk
tk = tkinter.Tk()


class NodeCreator:

    """docstring for NodeCreator"""

    def __init__(self):
        self.window = tkinter.Toplevel()
        self.window.overrideredirect(1)
        self.border = tkinter.Frame(self.window)
        self.border.configure(background="black", padx=2, pady=2)

        self.frame = tkinter.Frame(self.border)
        # self.frame.pack()
        self.frame.configure(padx=5, pady=2.5)

        self.input_ = tkinter.StringVar()
        self.entry = tkinter.Entry(self.frame, textvariable=self.input_)
        self.node_name = self.input_.get()

        create = createButton(
            master=self.frame, text="Create", command=self.create_node)
        cancel = createButton(
            master=self.frame, text="Cancel", command=self.quit)
        self.window.bind("<FocusOut>", quit)
        self.reset()

    def open_window(self, menuevent):

        self.border.pack()
        self.entry.pack()
        self.window.geometry("+%s+%s" %
                             (menuevent.x_root, menuevent.y_root))
        self.window.focus_set()

    def create_node(self, event=None):
        self.node_name = input_.get()
        self.window.pack_forget()

    def quit(self, event=None):
        self.window.pack_forget()

    def reset(self):
        self.node_name = ""
        self.input_.set("")


class NetworkDrawer(tkinter.Canvas):

    """docstring for NetworkDrawer"""

    def __init__(self, master=None):
        super(NetworkDrawer, self).__init__(master)
        self.nodeCreator = NodeCreator()
        self.pack(fill="both", expand=1)
        self.bind("<Button-3>", self.menupopup)
        self.menu = tkinter.Menu(self, tearoff=0)
        self.menu.add_command(label="node",
                              command=self.add_node)

    def add_node(self):
        self.nodeCreator.open_window(self.menuevent)

    def menupopup(self, event):
        self.menuevent = event
        self.menu.post(event.x_root, event.y_root)


class GUI:

    """docstring for GUI"""

    def __init__(self, master=None):
        self.frame = tkinter.Frame(master)
        self.frame.pack(anchor="center", expand=1, fill="both")

        self.right = tkinter.Frame(self.frame)
        self.right.pack(side="right", fill="both", expand=0, anchor="e")
        self.right.configure(background="red", padx=5, pady=2.5)

        self.left = tkinter.Frame(self.frame)
        self.left.pack(side="left", fill="both", expand=1, anchor="w")
        self.left.configure(borderwidth=10)

        self.buttons = []
        self.buttons.append(createButton(
            master=self.right, text="1. print test",
            color="blue", command=self.testfunc))

        self.buttons.append(createButton(
            master=self.right, text="2. quit",
            color="red", command=tk.destroy))

        self.drawer = NetworkDrawer(self.left)

    def mainloop(self):
        self.frame.mainloop()

    def testfunc(self):
        print("test test")

    def testdraw(self):
        self.drawer.create_oval(
            self.menuevent.x-10, self.menuevent.y-10,
            self.menuevent.x+10, self.menuevent.y+10)


def createButton(master=None, text=None, color=None, command=None):
    button = tkinter.Button(master)
    if text is not None:
        button["text"] = text
    if color is not None:
        button["fg"] = color
    if command is not None:
        button["command"] = command
    button.pack(
        anchor="n", fill="x", expand=0, pady=2.5)
    return button


def main():

    tk.title("Menu")
    tk.minsize(200, 200)
    gui = GUI(master=tk)
    gui.mainloop()

if __name__ == '__main__':
    main()
