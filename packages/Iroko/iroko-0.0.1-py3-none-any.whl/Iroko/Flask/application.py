import flask



class Application(flask.Flask):

	def __init__(self, *args, **kwargs):
		super().__init__(__name__, *args, **kwargs)

	def mount(self, component):
		self.register_blueprint(component)
