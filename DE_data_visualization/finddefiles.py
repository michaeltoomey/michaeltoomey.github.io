import sys, os, copy

class DifferentialExpressionFiles():

	def __init__(self, data_dir):
		self.data_dir = data_dir

	def buildDirectoryMap(self):
		self.dir_map = {}
		for file in os.listdir(self.data_dir):
			f = file.replace('[', '').replace('.txt', '').split(']')
			const_cond = f[0].split('-')
			var_cond = f[1].split('_')[-1].split('-')

			const_cond_formatted = []
			for cond in const_cond:
				const_cond_formatted += [cond.split('_')[-1]]

			cond = const_cond_formatted + var_cond

			self.recursiveBuild(self.dir_map, cond, self.data_dir + file)

	def recursiveBuild(self, dir_map, paths_to_add, file):
		if len(paths_to_add) == 1:
			dir_map[paths_to_add[0]] = file
		else:
			for item in paths_to_add:
				paths_temp = copy.deepcopy(paths_to_add)
				if not item in dir_map.keys():
					dir_map[item] = {}
				paths_temp.remove(item)
				self.recursiveBuild(dir_map[item], paths_temp, file)

	def getFilePath(self, condition_list):
		dir_map_temp = self.dir_map
		for i, item in enumerate(condition_list):
			if item in dir_map_temp.keys():
				if i + 1 == len(condition_list):
					return dir_map_temp[item]
				else:
					dir_map_temp = dir_map_temp[item]
			else:
				print item + ' is not a condition in the directory map'
				return None