from .vizualizations.QlikAppObject import QlikSenseAppObject


class QlikSenseSheet:
    def __init__(self, engine_sheet: dict, app):
        self.id = engine_sheet['qInfo']['qId']
        self.title = engine_sheet['qMeta']['title']
        self.cells = engine_sheet['cells'] if 'cells' in engine_sheet else engine_sheet['qData']['cells']
        self.app = app

    @staticmethod
    def __build_child(obj: QlikSenseAppObject):
        return {"qChildren": [], "qProperty": obj.full_def, "qEmbeddedSnapshotRef": None}

    def add_object(self, obj, col: int, row: int, colspan: int, rowspan: int):

        child_obj = self.__build_child(obj)
        coordinates = {
            "col": col,
            "row": row,
            "colspan": colspan,
            "rowspan": rowspan
        }
        return self.app.host_server.qs_engine.add_obj_to_sheet(self.app.id, self.id, child_obj, coordinates)

    def add_objects(self, *objects_and_coordinates: list[dict]):
        """
        :param objects_and_coordinates: [
                        { "obj": KPI(...), "coordinates": {"col": 0, "row": 0, "colspan": 1, "rowspan": 1}},
                        ...
                    ]
        :return:
        """

        objects_and_coordinates = [
            {**o,  "obj": self.__build_child(o['obj'])} for o in objects_and_coordinates
        ]

        return self.app.host_server.qs_engine.add_obj_to_sheet_many(self.app.id, self.id, objects_and_coordinates)
