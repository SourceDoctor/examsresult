
class CoreView(object):

    changed_mark = "! "
    changed_mark_enabled = True

    lng = {}
    # {name, type, unique, editable}
    column_title = []
    row_title = ()

    table_left = 0
    table_top = 0
    table_height = 200
    table_width = 200

    cell_editable = False
    full_row_select = True
    full_column_select = False

    sorting = True
    header_horizontal = True
    header_vertical = False
    float_precision = 2

    def set_filetypes(self, lng):
        filetype = []
        for desc in [(lng['filetype_exf'], '*.exf'), (lng['filetype_all'], '*')]:
            filetype.append("%s (%s)" % (desc[0], desc[1]))
        self.filetypes = ";;".join(filetype)

    def _define_column_title(self):
        return []

    def _set_changed(self, status):
        return True

    def set_changed(self, status):
        if not self._set_changed(status):
            return False

        # (un)mark tab title
        if self.changed_mark_enabled:
            index = 0
            while index <= self.tab_window.count():
                title = self.tab_window.tabText(index)
                if status:
                    search_title = "%s" % self.lng['title']
                    new_title = "%s%s" % (self.changed_mark, title)
                else:
                    search_title = "%s%s" % (self.changed_mark, self.lng['title'])
                    new_title = title.replace(self.changed_mark, '')

                if title == search_title:
                    break
                index += 1
            self.tab_window.setTabText(index, new_title)

        self.button_save.setEnabled(status)
        return True
