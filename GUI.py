import tkinter
import time


global tk


class Node:

    def __init__(self, obejectID):
        self.obejectID = obejectID


class NetworkManager(tkinter.Canvas):

    """docstring for NetworkManager"""

    def __init__(self, master=None, cnf={}, **kwargs):
        tkinter.Canvas.__init__(self, master, cnf, **kwargs)
        # init variables
        self.dragevent = None
        self.menuevent = None

        # reconfigure on resize
        self.bind("<Configure>", self.reconfigure_on_resize)

        # create context menu and bind it to RMB
        self.bind("<Button-3>", self.menupopup)
        self.nodeMenu = tkinter.Menu(self, tearoff=0)
        self.canvasMenu = tkinter.Menu(self, tearoff=0)
        self.canvasMenu.add_command(label="Add node",
                                    command=self.add_node)
        self.nodeMenu.add_command(label="Select node",
                                  command=self.select_node)
        self.nodeMenu.add_command(label="Remove node",
                                  command=self.remove_node)
        self.nodeMenu.add_command(label="Connect node",
                                  command=self.conenct_node)

        # bind dragging to LMB NOTE: WIP
        self.bind("<Button-1>", self.initialise_drag)
        self.bind("<B1-Motion>", self.dragHandler)

    def reconfigure_on_resize(self, event):
        # self.configure(width=event.width)
        pass

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

    def dragHandler(self, event):  # add scrollbars to be able to scroll
        objType = self.type(self.selectedObject)
        # if objType is None:
        #     print("dragging")
        #     self.scan_dragto(event.x_root, event.y_root, gain=0)
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

        self.grid(sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self.top = self.master.winfo_toplevel()
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.buttonContainer = tkinter.Frame(master)
        self.buttonContainer.configure(
            background="red", borderwidth=2.5)
        self.buttonContainer.grid(
            column=3, row=0, sticky=tkinter.N + tkinter.S)

        self.printButton = tkinter.Button(self.buttonContainer)
        self.printButton["text"] = "print test"
        self.printButton["fg"] = "blue"
        self.printButton["command"] = self.testfunc
        self.printButton.grid()
        self.quitButton = tkinter.Button(self.buttonContainer)
        self.quitButton["text"] = "Quit"
        self.quitButton["fg"] = "red"
        self.quitButton["command"] = tkinter.Tk().destroy
        self.quitButton.grid()

        # create a canvas, set its dimentions, put it in the window
        self.network_manager = NetworkManager(self)
        self.network_manager.configure(  # relief="raised",
            bg="white",  width=600, height=400,
            # scrollregion=(0, 0, 500, 500),
            scrollregion=(self.network_manager.grid_bbox()),
            confine=True)

        self.network_manager.grid(
            row=1, column=0,
            sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W)  # , sticky=tkinter.N + tkinter.W)
        for x in range(0, 500, 10):
            self.network_manager.create_line(0, x, 500, x)
            self.network_manager.create_line(x, 0, x, 500)

        # create scrollbars for canvas
        self.scrollbarX = tkinter.Scrollbar(
            self, orient=tkinter.HORIZONTAL, command=self.network_manager.xview)
        self.scrollbarY = tkinter.Scrollbar(
            self, orient=tkinter.VERTICAL, command=self.network_manager.yview)
        # set canvas scroll commands to the scrollbars
        self.network_manager["xscrollcommand"] = self.scrollbarX.set
        self.network_manager["yscrollcommand"] = self.scrollbarY.set
        # stick scrollbars to the sides of the canvas
        self.scrollbarX.grid(row=2, column=0, sticky=tkinter.E + tkinter.W)
        self.scrollbarY.grid(row=1, column=1, sticky=tkinter.N + tkinter.S)

        # create a toolbar for editing a node NOTE: learn grid options
        # self.toolbar = tkinter.Frame(self)
        # self.toolbar = tkinter.Frame(master,
        #                              bg="red", borderwidth=2.5)
        # self.toolbar.grid(row=0, column=0, sticky=tkinter.E + tkinter.W)
        # self.testButton = tkinter.Button(self.toolbar)
        # self.testButton["text"] = "blank"
        # self.testButton.grid()

    def title(self, title):
        self.master.title(title)

    def testfunc(self):
        print("test test")


if __name__ == '__main__':
    # tk.minsize(400, 400)
    root = tkinter.Tk()
    gui = GUI(root)
    gui.title("Network Creation")
    gui.mainloop()
