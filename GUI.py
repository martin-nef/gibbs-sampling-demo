import tkinter
import time

global tk
tk = tkinter.Tk()


# class NodeCreator:

#     """docstring for NodeCreator"""

#     def __init__(self, master=None):
#         # self.window = tkinter.Toplevel()
#         # self.window.overrideredirect(1)
#         self.window = tkinter.Toplevel()
#         self.border = tkinter.Frame(self.window)
#         self.border.configure(background="black", padx=2, pady=2)

#         self.frame = tkinter.Frame(self.border)
#         # self.frame.pack()
#         self.frame.configure(padx=5, pady=2.5)

#         self.input_ = tkinter.StringVar()
#         self.entry = tkinter.Entry(self.frame, textvariable=self.input_)
#         self.node_name = self.input_.get()

#         # create = createButton(
#         #     master=self.frame, text="Create", command=self.create_node)
#         # cancel = createButton(
#         #     master=self.frame, text="Cancel", command=self.quit)

#         # self.window.bind("<FocusOut>", quit) NOTE: makes program quit since it is out of focus at launch.
#         self.reset()

#     def open_window(self, menuevent):
#         # if True: return

#         if menuevent is None:
#             print("menuevent is None")
#             return

#         self.border.pack()
#         self.entry.pack()
#         self.window.geometry("100x100")
#         # self.window.geometry("+%s+%s" %
#         #                      (menuevent.x_root, menuevent.y_root))


#         # self.window.focus_set() # NOTE: unnecessary, focus behaves better as is

#     def create_node(self, event=None):
#         self.node_name = input_.get()
#         self.window.pack_forget()

#     def quit(self, event=None):
#         self.window.pack_forget()

#     def reset(self):
#         self.node_name = ""
#         self.input_.set("")


class Node:

    def __init__(self, obejectID):
        self.obejectID = obejectID


class NetworkManager(tkinter.Canvas):

    """docstring for NetworkManager"""

    def __init__(self, master=None):
        super(NetworkManager, self).__init__(master)
        # init variables
        self.dragevent = None
        self.menuevent = None

        # create context menu and bind it to RMB
        self.bind("<Button-3>", self.menupopup)
        self.nodeMenu = tkinter.Menu(self, tearoff=0)
        self.canvasMenu = tkinter.Menu(self, tearoff=0)
        self.toolbar = tkinter.Menu(self, tearoff=0)
        self.canvasMenu.add_command(label="Add node",
                                    command=self.add_node)
        self.nodeMenu.add_command(label="Select node",
                                  command=self.select_node)
        self.nodeMenu.add_command(label="Remove node",
                                  command=self.remove_node)
        self.nodeMenu.add_command(label="Connect node",
                                  command=self.conenct_node)

        # bind dragging to LMB
        self.bind("<Button-1>", self.initialise_drag)
        self.bind("<B1-Motion>", self.dragHandler)

        # TODO: configure the canvas
        self.toolbar = tkinter.Frame(master,
                                     bg="red", borderwidth=2.5)
        # self.toolbar.pack(fill="x")
        self.toolbar.grid()
        self.configure(bg="white",
                       scrollregion=(-10000, -10000, 10000, 10000),
                       relief="raised")
        # self.pack(fill="both", expand=1)
        self.grid()

        # create canvas on the toplevel window
        # self.window = tkinter.Toplevel()
        # self.border = tkinter.Frame(self.window)
        # self.border.configure(background="red", padx=2, pady=2)
        # self.frame = tkinter.Frame(self.border)
        # self.frame.configure(background="green", padx=5, pady=2.5)

        # self.input_ = tkinter.StringVar()
        # self.entry = tkinter.Entry(self.frame, textvariable=self.input_)
        # self.node_name = self.input_.get()

    def add_node(self):
        "add node to the system and draw it at mouse position"
        self.create_oval(
            self.menuevent.x - 30, self.menuevent.y - 15,
            self.menuevent.x + 30, self.menuevent.y + 15,
            fill="#efefef", activewidth=1.5, width=1)

    def remove_node(self):
        self.delete(self.selectedObject)
        self.selectedObject = None

    def conenct_node(self):
        pass

    def select_node(self):
        self.configure_node(self.selectedObject)

    def configure_node(self, objectID):
        pass

    def menupopup(self, event):
        "bring up the context menu"
        self.menuevent = event
        self.selectedObject = self.get_canvas_object_at_position(
            event.x, event.y)
        objType = self.type(self.selectedObject)
        if objType is None:
            self.canvasMenu.post(event.x_root, event.y_root)
        if objType == "oval":
            self.nodeMenu.post(event.x_root, event.y_root)

    def initialise_drag(self, event):
        "on LMB drag nodes or reposition canvas"
        self.selectedObject = self.get_canvas_object_at_position(
            event.x, event.y)
        objType = self.type(self.selectedObject)
        if objType is None:
            self.scan_mark(event.x, event.y)

    def dragHandler(self, event): # add scrollbars to be able to scroll
        objType = self.type(self.selectedObject)
        if objType is None:
            print("dragging")
            self.scan_dragto(event.x_root, event.y_root, gain=0)
        if objType == "oval":
            coords = self.coords(self.selectedObject)
            xsize = (coords[0] - coords[2]) / 2
            ysize = (coords[1] - coords[3]) / 2
            self.coords(self.selectedObject, event.x - xsize,
                        event.y - ysize, event.x + xsize, event.y + ysize)

    def get_canvas_object_at_position(self, x, y, cursorsize=0):
        return self.find_overlapping(
            x - cursorsize / 2, y - cursorsize / 2,
            x + cursorsize / 2, y + cursorsize / 2)

    def quit(self, event=None):
        self.window.pack_forget()

    def reset(self):
        self.node_name = ""
        self.input_.set("")


class GUI(tkinter.Frame):

    """docstring for GUI"""

    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        # self.frame = tkinter.Frame(master)
        # # self.frame.pack(anchor="center", expand=1, fill="both")

        self.grid()

        self.right = tkinter.Frame(master)
        # self.right.pack(side="right", fill="both", expand=0, anchor="e")
        self.right.grid(column=1, row=0)
        self.right.configure(background="red", borderwidth=2.5)

        self.left = tkinter.Frame(master)
        # self.left.pack(side="left", fill="both", expand=1, anchor="w")
        self.left.grid(column=0, row=0)
        self.left.configure(borderwidth=0)

        self.buttons = []
        self.buttons.append(createButton(
            master=self.right, text="1. print test",
            color="blue", command=self.testfunc))

        self.buttons.append(createButton(
            master=self.right, text="2. quit",
            color="red", command=tk.destroy))

        self.buttons.append(createButton(
            master=self.right, text="3. scroll test",
            color="blue", command=self.scrolltest))

        self.network_manager = NetworkManager(self.left, )

    def title(self, title):
        self.master.title(title)

    def scrolltest(self):
        self.network_manager.xview_moveto(0.1)
        time.sleep(1)
        self.network_manager.xview_moveto(0.9)
        time.sleep(1)
        self.network_manager.xview_moveto(0.5)

    def testfunc(self):
        print("test test")


def createButton(master=None, text=None, color=None, command=None):
    button = tkinter.Button(master)
    if text is not None:
        button["text"] = text
    if color is not None:
        button["fg"] = color
    if command is not None:
        button["command"] = command
    # button.pack(
        # anchor="n", fill="x", expand=0, pady=2.5 / 2)
    button.grid()
    return button


if __name__ == '__main__':
    tk.minsize(400, 400)
    gui = GUI()
    gui.title("Network Creation")
    gui.mainloop()
