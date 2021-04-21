# -*- coding:utf-8 -*-
import json
import os
import shutil
from time import time

from lib.easy_async import async_func
import aiofiles


class File:
	def __init__(self, path):
		self.path = path

	# 获取文件的格式
	def get_filetype(self):
		filetype = self.path.split('.')[-1]
		return filetype

	def read_json(self):
		s = time()
		# 检测文件的格式
		filetype = self.get_filetype()
		if filetype != 'json':
			raise TypeError(f'文件格式不正确,{self.path}')
		# print(f'读取json,{self.get_filesize()}mb,{self.path}')
		with open(self.path, 'r', encoding='utf8')as f:
			json_data = json.load(f)
			# print('读取耗时 ', round(time() - s, 4), '秒')
			return json_data

	@async_func
	def write_json(self, data):
		with open(self.path, 'w', encoding='utf8')as f:
			json.dump(data, f)

	# print(f'写入json,{round(self.get_filesize(max_acc_mode=True) / 1024)} kb,{self.path}')

	def read_txt(self):
		s = time()
		with open(self.path, 'r', encoding='utf8')as f:
			data = f.read()
			print('读取耗时 ', round(time() - s, 4), '秒')
			return data

	@async_func
	def write_txt(self, data):
		with open(self.path, 'w', encoding='utf8')as f:
			f.write(str(data))

	def make_dir(self):
		path = self.path.strip()  # 去除首位空格
		path = path.rstrip("\\")  # 去除尾部 \ 符号
		is_exists = os.path.exists(path)
		# 判断结果
		if not is_exists:
			os.makedirs(path)
			return True
		else:
			return False

	def move_file(self, to_path):
		if not os.path.isfile(self.path):
			print("%s not exist!" % (self.path))
		else:
			fpath, fname = os.path.split(to_path)  # 分离文件名和路径
			if fpath != '' and os.path.exists(fpath) == False:
				os.makedirs(fpath)  # 创建路径
			shutil.move(self.path, to_path)  # 移动文件
			print(f"移动 {self.path} -> {to_path}")

	def copy_file(self, to_path):
		if not os.path.isfile(self.path):
			print(f"{self.path}不存在!")
		else:
			fpath, fname = os.path.split(to_path)  # 分离文件名和路径
			# fpath 可能为空，即相对路径没有前缀时出现
			if fpath != '' and os.path.exists(fpath) == False:
				os.makedirs(fpath)  # 创建路径
			shutil.copyfile(self.path, to_path)  # 复制文件
			print(f"复制 {self.path} -> {to_path}")

	def get_filesize(self, acc: int = 2, max_acc_mode=False):
		size = os.path.getsize(self.path)
		if max_acc_mode:
			return size
		else:
			size = size / float(1024 * 1024)
			return round(size, acc)  # 精度

	# 检测路径是否存在
	def check_path_is_exist(self) -> bool:
		return os.path.exists(self.path)

	# 检测路径是个文件，还是文件夹
	def check_is_file_or_folder(self) -> str:
		# 先检测路径是否存在
		if not self.check_path_is_exist():
			return 'not exist'
		if os.path.isfile(self.path):
			return 'file'
		else:
			return 'folder'

	# 列出目录文件列表
	def listdir_pro(self):
		filename_list = []
		for i in os.listdir(self.path):
			if i != '.DS_Store':
				filename_list.append(i)
		return filename_list

	# 异步读取json
	async def quick_read_json(self):
		s = time()
		async with aiofiles.open(self.path, mode='r', encoding='utf8') as f:
			contents = await f.read()
			json_data = json.load(contents)
			print('读取耗时 ', time() - s)
			return json_data

	"""删除文件"""

	def delete(self):
		os.remove(self.path)
