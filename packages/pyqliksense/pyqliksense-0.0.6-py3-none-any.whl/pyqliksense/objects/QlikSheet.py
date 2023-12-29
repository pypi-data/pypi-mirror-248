class QlikSenseSheet:
    def __init__(self, engine_sheet: dict):
        self.id = engine_sheet['qInfo']['qId']
        self.title = engine_sheet['qMeta']['title']
        self.cells = engine_sheet['cells'] if 'cells' in engine_sheet else engine_sheet['qData']['cells']
