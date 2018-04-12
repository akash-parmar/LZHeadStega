class CoverGenerator(object):
	def __init__(self, domain_mapping):
		if domain_mapping is None:
			return

		try:
			with open(domain_mapping, 'r') as infile:
				content = infile.readlines()
			self.domain_map = {x.split("->")[0]:int(x.split("->")[1]) for x in content}

		except Exception as e:
			print("Exception Found: ", str(e))


if __name__ == "__main__":
	generator = CoverGenerator("domain_mapping.txt")