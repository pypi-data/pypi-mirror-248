class QlikSenseHyperCube:
	def __init__(
			self,
			dimensions: list[str] = None,
			measures: list[str] = None,
			context_set_analysis: str = ""
	):
		self.dimensions = [{"qDef": {"qFieldDefs": [field]}} for field in dimensions]
		self.measures = [{"qDef": {"qDef": measure}} for measure in measures]
		self.context_set_analysis = context_set_analysis

	def __dict__(self):
		return self.get_cube_def()

	def get_cube_def(self):
		return {
			"qInfo": {"qType": "qlik_generic_obj"},
			"qHyperCubeDef": {
				"qContextSetExpression": self.context_set_analysis,
				"qDimensions": self.dimensions,
				"qMeasures": self.measures
			}
		}
