import wx
import wx.lib.mixins.listctrl as listmix


class whListLeft(wx.ListCtrl,
                 listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, data):
        wx.ListCtrl.__init__(self, parent, -1,
                             style=wx.LC_REPORT |
                                   wx.LC_VIRTUAL |
                                   wx.LC_HRULES |
                                   wx.LC_VRULES)

        #------------

        # Initialize the listCtrl auto width.
        listmix.ListCtrlAutoWidthMixin.__init__(self)

        #------------

        self.SetBackgroundColour("pink")

        #------------

        self.items = data
        print("Items :",  self.items)

        #------------

        self.InsertColumn(0, "Unit")
        self.InsertColumn(1, "CatalogID")
        self.InsertColumn(2, "SerialNumber")
        self.InsertColumn(3, "Name")
        self.InsertColumn(4, "Qty")

        self.SetColumnWidth(0, 100)
        self.SetColumnWidth(1, 100)
        self.SetColumnWidth(2, 100)
        self.SetColumnWidth(3, 200)
        self.SetColumnWidth(4, 30)

        #------------

        self.SetItemCount(len(data))

    #-----------------------------------------------------------------------

    def OnGetItemText(self, item, col):
        """
        ...
        """

        return self.items[item][col]

