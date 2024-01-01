from .QlikAppObject import QlikSenseAppObject
from .definitions.kpi import kpi_definition


class KPI(QlikSenseAppObject):
    def __init__(self, measure: str):
        self.full_def = kpi_definition(measure)
        self.id = self.full_def['qInfo']['qId']
        self.type = self.full_def['qInfo']['qType']
