import tkinter
from tkinter import messagebox
from dag import *

_DISABLE_SCROLLING = True
NODE = "node"
ARC = "arc"
TEXT = "text"
IN = 1
OUT = 0


class CanvasObject:

    def __init__(self, objectID, canvas):
        self.objectID = objectID
        self.canvas = canvas
        self.tags = set()

    def __str__(self):
        return "(objectID:%s, tags:%s)" % (str(self.objectID), str(self.tags))

    def __repr__(self):
        return "(objectID:%s, tags:%s)" % (str(self.objectID), str(self.tags))

    def get_coords(self):
        return self.canvas.coords(self.objectID)

    def set_coords(self, coords):
        self.canvas.coords(self.objectID, coords)

    def get_x(self):
        return self.canvas.coords(self.objectID)[0]

    def get_y(self):
        return self.canvas.coords(self.objectID)[1]

    def get_centre(self):
        coords = self.get_coords()
        return (((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2))

    def get_type(self):
        return self.canvas.type(self.objectID)

    def add_tag(self, tag):
        # self.canvas.addtag_closest(tag, self.get_x(), self.get_y())
        self.tags.add(tag)

    def remove_tag(self, tag):
        # self.canvas.dtag(self.objectID, tag)
        self.tags.remove(tag)

    def get_tags(self):
        return self.tags
        # return self.canvas.gettags(self.objectID)

    def delete(self):
        del self.canvas.canvas_objects[self.objectID]
        self.canvas.delete(self.objectID)
        del self


class Arc(CanvasObject):

    def __init__(self, objectID, canvas):
        self.objectID = objectID
        self.canvas = canvas
        self.tags = set()
        self.vertex = Vertex(objectID)
        self.parents = ()

    def add_parents(self, from_, to):
        if self.parents:
            notify_error("Arc Error", "Arc already has parents")
            return
        self.parents = (from_, to)

    def delete(self):
        try:
            if self.parents:
                self.canvas.network.remove_edge(parents[0], parents[1])
        except KeyError:
            notify_error("Delete error", "Arc's parent(s) not in graph.")
        except ValueError:
            notify_error("Delete error", "Specified arc does not exist.")
        del self.canvas.canvas_objects[self.objectID]
        self.canvas.delete(self.objectID)
        del self

    def move(self, mode):  # TODO (cosmetic) fix flickering of the arrow when nodes above one another
        x1, y1 = self.parents[0].get_centre()
        x2, y2 = self.parents[1].get_centre()
        coords = [x1, y1, x2, y2]

        (xo, yo) = self.parents[1].get_arc_offsets()
        (xd1, yd1) = self.get_direction(xmagnitude=xo, ymagnitude=yo)
        (xo, yo) = self.parents[0].get_arc_offsets()
        (xd0, yd0) = self.get_direction(xmagnitude=xo, ymagnitude=yo)
        coords = [coords[0] + xd0, coords[1] + yd0,
                  coords[2] - xd1, coords[3] - yd1]
        self.set_coords(coords)

    def get_direction(self, xmagnitude=1, ymagnitude=1):
        x1, y1, x2, y2 = self.get_coords()
        xdir = (x1 - x2)
        ydir = (y1 - y2)
        if xdir > 0:
            xdir = xmagnitude
        elif xdir < 0:
            xdir = -xmagnitude
        else:
            xdir = 0
        if ydir > 0:
            ydir = ymagnitude
        elif ydir < 0:
            ydir = -ymagnitude
        else:
            ydir = 0
        return (xdir, ydir)


class Node(CanvasObject):
    """ ### """

    def __init__(self, objectID, name, canvas):
        self.objectID = objectID
        self.canvas = canvas
        self.tags = set()
        self.name = name
        self.vertex = Vertex(objectID)
        self.arcs_in = set()
        self.arcs_out = set()
        self.label = None

    def __str__(self):
        return "(name:%s, objectID:%s, tags:%s)" % (str(self.name), str(self.objectID), str(self.tags))

    def __repr__(self):
        return "(name:%s, objectID:%s, tags:%s)" % (str(self.name), str(self.objectID), str(self.tags))

    def delete(self):
        if self.arcs_out and False:
            # TODO: test if that is actually the case. Maybe there is a better
            # way of handling this
            # P.S. actually better to allow this but check that graph is
            # contiguous before starting demo
            notify_error("Delete Error",
                         "Cannot remove node with outgoing connections")
            return
        for arc in self.arcs_in:
            arc.delete()
        self.canvas.network.remove_vertex(self.vertex)
        self.canvas.delete(self.objectID)
        self.arcs_in
        self.label.delete()
        del self.canvas.canvas_objects[self.objectID]
        del self

    def add_arc_inc(self, arc):
        """ add incoming arc to node """
        self.arcs_in.add(arc)

    def add_arc_out(self, arc):
        """ add outgoing arc to node """
        self.arcs_out.add(arc)

    def move(self, event):
        coords = self.canvas.coords(self.objectID)
        xsize = (coords[0] - coords[2]) / 2
        ysize = (coords[1] - coords[3]) / 2
        self.canvas.coords(self.objectID,
                           event.x - xsize, event.y - ysize,
                           event.x + xsize, event.y + ysize)
        self.canvas.coords(self.label.objectID,
                           event.x, event.y)
        for arc in self.arcs_in:
            arc.move(IN)
        for arc in self.arcs_out:
            arc.move(OUT)

    def get_arc_offsets(self):
        coords = self.get_coords()
        x = (coords[0] - coords[2]) / 2
        y = (coords[1] - coords[3]) / 2
        return (x, y)


class NetworkManager(tkinter.Canvas):

    """docstring for NetworkManager"""

    def __init__(self, master=None, cnf={}, **kwargs):
        tkinter.Canvas.__init__(self, master, cnf, **kwargs)

        # init variables
        self.menuevent = None
        self.motionevent = None
        self.canvas_objects = {}
        self._node_name = None
        self._adding_node = False
        self._connecting_nodes = False
        self._selected_arc = None
        self._selected_node = None
        self._dragged_node = None
        self.network = DAG()

        # create context menu and bind it to RMB
        self.bind("<ButtonRelease-3>", self.menuHandler)
        self.nodeMenu = tkinter.Menu(self, tearoff=0)
        self.canvasMenu = tkinter.Menu(self, tearoff=0)
        self.canvasMenu.add_command(label="Add node",
                                    command=self.add_node)
        # self.nodeMenu.add_command(label="Select node",
        #                           command=self.get_node)
        self.nodeMenu.add_command(label="Connect node",
                                  command=self.connect_node)
        self.nodeMenu.add_command(label="Remove node",
                                  command=self.remove_node)

        # bind dragging to LMB
        self.bind("<Button-1>", self.clickHandler)
        self.bind("<B1-Motion>", self.dragHandler)
        self.bind("<Motion>", self.motionHandler)

    def notify(self, title, message):
        messagebox.showinfo(title, message)

    def notify_error(self, title, message):
        messagebox.showerror(title, message)
        # raise Exception(title, message)

    def text_dialog(self):
        input_box = tkinter.Toplevel()
        input_field = tkinter.Entry(master=input_box)
        input_label = tkinter.Label(
            master=input_box, text="Enter node name please ")
        ok_button = tkinter.Button(input_box)
        ok_button["text"] = "OK"
        cancel_button = tkinter.Button(input_box)
        cancel_button["text"] = "Cancel"

        def _text_dialog_ok(self=self, input_field=input_field, input_box=input_box):
            self._node_name = input_field.get()
            input_box.destroy()

        def _text_dialog_cancel(self=self, input_box=input_box):
            input_box.destroy()
            self._node_name = None

        ok_button["command"] = _text_dialog_ok
        cancel_button["command"] = _text_dialog_cancel

        input_box.grid()
        input_label.grid()
        input_field.grid()
        ok_button.grid()
        cancel_button.grid()
        return input_box

    # def reconfigure_on_resize(self, event):
    #     # self.configure(width=event.width)
    #     pass

    def add_node(self):
        "add node to the system and draw it at mouse position"
        self._adding_node = True
        td = self.text_dialog()
        self.wait_window(td)
        if self._node_name == "":
            self.notify_error("Node Error", "Node name cannot be blank.")
        if not self._node_name:
            self._node_name = None
            self._adding_node = False
            return
        try:
            if any([self._node_name == obj.name for obj in self.canvas_objects.values()]):
                self.notify_error(
                    "Node Error", "Node with that name already exists.")
                self._node_name = None
                self._adding_node = False
                return
        except AttributeError:
            pass

        label = self.create_text(
            self.menuevent.x, self.menuevent.y,
            text=str(self._node_name), tags=(TEXT),
            font=('Calibri', '24'))
        boxheight = 32 + 8
        boxlength = (len(str(self._node_name)) * 16) + 16
        new_node = self.create_rectangle(
            self.menuevent.x - boxlength / 2, self.menuevent.y - boxheight / 2,
            self.menuevent.x + boxlength / 2, self.menuevent.y + boxheight / 2,
            fill="#efefef", activewidth=2, width=1.5, tags=(NODE))
        self.canvas_objects[label] = CanvasObject(label, self)
        self.canvas_objects[label].add_tag(TEXT)
        self.canvas_objects[new_node] = Node(new_node, self._node_name, self)
        self.canvas_objects[new_node].add_tag(NODE)
        self.canvas_objects[new_node].label = self.canvas_objects[label]
        self.tag_raise(label, new_node)
        self._node_name = None
        try:
            self.network.add_vertex(self.canvas_objects[new_node].vertex)
        except KeyError:
            del self.canvas_objects[new_node]
            self.delete(new_node)
            self.notify_error("Node Error", "Node already exists.")
        self._adding_node = False

    def remove_node(self):
        """ remove node from canvas and network """
        self._selected_node.delete()
        self._selected_node = None

    def connect_node(self):
        node1 = self._selected_node
        node_centre = node1.get_centre()
        new_line = self.create_line(node_centre[0], node_centre[1],
                                    self.motionevent.x, self.motionevent.y,
                                    tags=(ARC), arrow=tkinter.LAST, arrowshape=(
                                        15, 18, 10),
                                    smooth=True, width=2)
        self._selected_arc = Arc(new_line, self)
        self._selected_arc.add_tag(ARC)
        self.canvas_objects[new_line] = self._selected_arc
        # self.tag_raise(self._selected_node.objectID,
        #                self._selected_arc.objectID)
        self._connecting_nodes = True

    def _finalise_connection(self, node):
        cleanup = False
        try:
            if not self.network.test_edge(self._selected_node.vertex, node.vertex):
                self.network.add_edge(self._selected_node.vertex, node.vertex)
            else:
                cleanup = True
                self.notify_error("Connection Error", "An arc from %s to %s already exists." % (
                    self._selected_node.name, node.name))
        except ValueError:
            cleanup = True
            self.notify_error("Connection Error",
                              "Connection would cause a cycle, aborting.")
        except KeyError:
            cleanup = True
            self.notify_error("Connection Error",
                              "One of the nodes is not in the graph.")
        if cleanup:
            self._selected_arc.delete()
        else:
            self._selected_arc.add_parents(self._selected_node, node)
            self._selected_node.add_arc_out(self._selected_arc)
            node.add_arc_inc(self._selected_arc)
            # self._selected_arc.move(IN)

        self._selected_node = None
        self._selected_arc = None
        self._connecting_nodes = False

    def _cancel_connection(self):
        self._selected_arc.delete()
        self._connecting_nodes = False
        self._selected_node = None
        self._selected_arc = None
        self._selected_node = None

    def get_node(self, x, y):
        nodes = self.get_objects_with_tag(x, y, NODE)
        if nodes:
            for node in nodes:
                try:
                    return self.canvas_objects[node.objectID]
                except KeyError:
                    pass
        return None

    def configure_node(self, objectID):
        pass

    def menuHandler(self, event):
        "bring up the context menu"
        if self._adding_node:
            return
        if self._connecting_nodes:
            self._cancel_connection()
            return
        self.menuevent = event
        self._selected_node = self.get_node(event.x, event.y)
        if self._selected_node:
            self.nodeMenu.post(event.x_root, event.y_root)
        else:
            self.canvasMenu.post(event.x_root, event.y_root)

    def motionHandler(self, event):
        self.motionevent = event
        if self._connecting_nodes:
            if self._selected_arc:
                coords = self._selected_arc.get_coords()
                coords = [coords[0], coords[1], event.x, event.y]
                self._selected_arc.set_coords(coords)

    def clickHandler(self, event):
        "on LMB drag nodes or reposition canvas"
        if self._adding_node:
            return
        if self._connecting_nodes:
            node = self.get_node(event.x, event.y)
            if node:
                self._finalise_connection(node)
            else:
                self._cancel_connection()
        else:
            self._dragged_node = self.get_node(event.x, event.y)
            self.tag_raise(self._dragged_node.objectID)
            self.tag_raise(self._dragged_node.label.objectID,
                           self._dragged_node.objectID)

    def dragHandler(self, event):
        if self._connecting_nodes:
            return

        if self._dragged_node:
            self._dragged_node.move(event)

    def _get_object_ids(self, x, y, cursorsize=0):
        """ returns object found on canvas at (x,y) """
        return self.find_overlapping(
            x - cursorsize / 2, y - cursorsize / 2,
            x + cursorsize / 2, y + cursorsize / 2)

    def get_objects(self, x, y, cursorsize=0):
        """ returns object found on canvas at (x,y) """
        object_ids = self._get_object_ids(x, y, cursorsize)
        return self._objects_from_ids(object_ids)

    def _objects_from_ids(self, object_ids):
        out = []
        for id_ in object_ids:
            try:
                # Maybe aborts creating list after exception, check
                out.append(self.canvas_objects[id_])
            except KeyError:
                pass
        if out:
            return out
        return None

    def get_objects_with_tag(self, x, y, tag, cursorsize=0):
        """ returns object found on canvas at (x,y) with specified tag"""
        objects = self._objects_from_ids(
            self._get_object_ids(x, y, cursorsize))
        out = []
        if objects:
            for obj in objects:
                if tag in obj.get_tags():
                    out.append(obj)
        if out:
            return out
        return None


class GUI(tkinter.Frame):

    """docstring for GUI"""

    def __init__(self, master=None, cnf={}, **kw):
        tkinter.Frame.__init__(self, master, cnf, **kw)

        self.grid(sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self.top = self.master.winfo_toplevel()
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.buttonContainer = tkinter.Frame(self)
        self.buttonContainer.configure(
            background="red", borderwidth=2.5)
        self.buttonContainer.grid(
            column=3, row=0, rowspan=3, sticky=tkinter.N + tkinter.S)

        self.printButton = tkinter.Button(self.buttonContainer)
        self.printButton["text"] = "print test"
        self.printButton["fg"] = "blue"
        self.printButton["command"] = self.testfunc
        self.printButton.grid()
        self.quitButton = tkinter.Button(self.buttonContainer)
        self.quitButton["text"] = "Quit"
        self.quitButton["fg"] = "red"
        self.quitButton["command"] = self.master.destroy
        self.quitButton.grid()

        # create a canvas, set its dimentions, put it in the window
        self.network_manager = NetworkManager(self)
        self.network_manager.configure(  # relief="raised",
            bg="white",  width=500, height=500,
            # scrollregion=(0, 0, 1000, 1000),
            scrollregion=(self.network_manager.grid_bbox()),
            confine=True)
        self.network_manager.grid(
            row=1, column=0,
            sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W)  # , sticky=tkinter.N + tkinter.W)

        line_colour = "gray"
        canvas_size = 2000
        line_interval = 50
        for x in range(0, canvas_size, line_interval):
            self.network_manager.create_line(
                0, x, canvas_size, x, fill=line_colour)
            self.network_manager.create_line(
                x, 0, x, canvas_size, fill=line_colour)

        # TODO: (extra) fix locating objects if canvas was scrolled,
        #       probably need to scroll or get objects differently
        if not _DISABLE_SCROLLING:
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

        # create a toolbar for editing a node
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
        print("DAG:")
        print(self.network_manager.network)
        print("Canvas:")
        print(self.network_manager.canvas_objects)
        print()


if __name__ == '__main__':
    # tk.minsize(400, 400)
    gui = GUI()
    gui.title("Network Creation")
    gui.mainloop()
