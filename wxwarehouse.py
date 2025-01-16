#!/usr/bin/env python
"""
Warehouse.
"""

import wx
import whListLeft
import whListRight
#import whToolbar

data = [
    ['склад', '1110001', 'RBY8021', 'Радіостанція Motorola DP4400', '1'],
    ['склад', '1110001', 'RBY8022', 'Радіостанція Motorola DP4400', '1'],
    ['склад', '1110001', 'RBY8023', 'Радіостанція Motorola DP4400', '1'],
    ['склад', '1110001', 'RBY8024', 'Радіостанція Motorola DP4400', '1'],
    ['склад', '1110001',  '', 'Радіостанція Motorola DP4400', '10'],
    ['взв 1 дшб', '1110001', '', 'Радіостанція Motorola DP4400', '3'],
    ['взв 2 дшб', '1110001', '', 'Радіостанція Motorola DP4400', '4'],
    ['взв 3 дшб', '1110001', '', 'Радіостанція Motorola DP4400', '6']
    ]

class PageOne(wx.SplitterWindow):
    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent, -1)

        # and create a sizer to manage the layout of child widgets

        #splitter = wx.SplitterWindow(parent, -1)
        self.SetMinimumPaneSize(400)

        listleft = whListLeft.whListLeft(self, data)
        listleft.SetBackgroundColour(wx.LIGHT_GREY)

        listright = whListRight.whListRight(self, [])
        listright.SetBackgroundColour(wx.LIGHT_GREY)

        self.SplitVertically(listleft, listright)
        #self.Add(splitter)


class PageTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        wx.StaticText(self, -1, "This is a PageTwo object", (40, 40))


class PageThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        wx.StaticText(self, -1, "This is a PageThree object", (60, 60))

class WarehouseFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(WarehouseFrame, self).__init__(*args, **kw)

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("./res/warehouse.png", wx.BITMAP_TYPE_PNG))
        self.SetIcon(icon)

        # create a menu bar
        self.makeMenuBar()

        # put some text with a larger bold font on it
        toolbar = self.CreateToolBar()
        toolbar.AddTool(1, "Open", wx.Image('./res/open.png',
                        wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
                        wx.NullBitmap, wx.ITEM_NORMAL, 'Open', "Long help for 'Open'.", None)
        toolbar.AddTool(2, "Settigns", wx.Image('./res/settings.png',
                        wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
                        wx.NullBitmap, wx.ITEM_NORMAL, 'Settings', "Long help for 'Settings'.", None)
        toolbar.AddTool(3, "Report", wx.Image('./res/report.png',
                        wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
                        wx.NullBitmap, wx.ITEM_NORMAL, 'Report', "Long help for 'Report'.", None)
        textctrl = wx.TextCtrl(toolbar)
        toolbar.AddControl(textctrl)
        toolbar.AddTool(4, "Search", wx.Image('./res/search.png',
                        wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
                        wx.NullBitmap, wx.ITEM_NORMAL, 'Search', "Long help for 'Search'.", None)
        toolbar.AddSeparator()
        toolbar.AddTool(5, "Move", wx.Image('./res/move.png',
                        wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
                        wx.NullBitmap, wx.ITEM_NORMAL, 'Move', "Long help for 'Move'.", None)
        toolbar.AddStretchableSpace()

        toolbar.AddTool(6, "Save", wx.Image('./res/save.png',
                        wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
                        wx.NullBitmap, wx.ITEM_NORMAL, 'Save', "Long help for 'Save'.", None)
        toolbar.AddTool(7, "Delete", wx.Image('./res/trash.png',
                        wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
                        wx.NullBitmap, wx.ITEM_NORMAL, 'Delete', "Long help for 'Delete'.", None)
        toolbar.AddSeparator()
        combo = wx.ComboBox(toolbar, choices=["склад","взв 1 дшб","взв 2 дшб","взв 3 дшб","взв аемб"])
        toolbar.AddControl(combo)
        toolbar.Realize()

        p = wx.Panel(self)
        self.nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        page1 = PageOne(self.nb)
        page2 = PageTwo(self.nb)
        page3 = PageThree(self.nb)

        # add the pages to the notebook with the label to show on the tab
        self.nb.AddPage(page1, "Operations")
        self.nb.AddPage(page2, "Catalog")
        self.nb.AddPage(page3, "Units")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Warehouse on wxPython!")


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a Warehouse project About",
                      "About Warehouse",
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = WarehouseFrame(None, title='Warehouse')
    frm.Show()
    app.MainLoop()

