from .QlikAppObject import QlikSenseAppObject
class KPI(QlikSenseAppObject):
    def __init__(self, id):
        self.id = id
        self.type = 'kpi'