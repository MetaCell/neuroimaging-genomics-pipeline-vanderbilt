import os


def create_path_if_not_exists(path):
	if not os.path.exists(path):
		try:
			os.makedirs(path)
		except:
			raise OSError("Can't create destination directory (%s)!" % (path))