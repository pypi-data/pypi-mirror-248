from .QlikAppObject import QlikSenseAppObject
from .definitions.linechart import linechart_definition


class LineChart(QlikSenseAppObject):
    def __init__(self, dimensions: list[str] = None,  measures: list[str] = None):
        self.full_def = linechart_definition(dimensions=dimensions, measures=measures)
        self.id = self.full_def['qInfo']['qId']
        self.type = self.full_def['qInfo']['qType']
