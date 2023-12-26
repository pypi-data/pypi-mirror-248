from typing import Any


class kdict(dict):
	r"""Like dict but accessible with x.key and x["key"]

	A class that creates a dict that is also accessible by using x.key, not just by using x["key"]

	How To Use
	----------
	x = kdict({"key": value, ...}); y = x.key
	print(y) # Output: value

	OR

	d = {"key": value, ...}; x = kdict(d); y = x.key
	print(y) # Output: value
	"""
	def __getattr__(self, name):
		if name in self:
			return self[name]
		raise KeyError(f"'{name}'")
	
	def __setattr__(self, name, value) -> None:
		self[name] = value