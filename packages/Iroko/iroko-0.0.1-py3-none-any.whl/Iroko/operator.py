import click



class Operator:


	@staticmethod
	def Print(instance, *args, **kwargs):
		try:
			fn = instance.__print__
		except AttributeError:
			return print(instance)

		output = fn(*args, **kwargs)
		if output is None:
			return

		click.echo(output)


	@staticmethod
	def Inspect(instance, *args, **kwargs):
		try:
			fn = instance.__inspect__
		except AttributeError:
			print(instance)
			return

		output = fn(*args, **kwargs)
		if output is None:
			return

		click.echo(output)
