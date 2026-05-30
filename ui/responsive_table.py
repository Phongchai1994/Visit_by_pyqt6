from PyQt6.QtWidgets import QTableView

class ResponsiveTableView(QTableView):
    def __init__(self, proportions, parent=None):
        super().__init__(parent)
        self.proportions = proportions
        self.setObjectName('Qtable_View')

    def apply_column_widths(self):
        model = self.model()
        if model is None:
            return

        total_width = self.viewport().width()
        if total_width <= 0:
            return

        for i, proportion in enumerate(self.proportions):
            self.setColumnWidth(i, max(20, int(total_width * proportion)))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.apply_column_widths()
