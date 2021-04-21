# -*- coding:utf-8 -*-
"""***************************************************************
******************************************************************
*........．．∵ ∴★．∴∵∴ ╭ ╯╭ ╯╭ ╯╭ ╯∴∵∴∵∴  .........................
*.........．☆．∵∴∵．∴∵∴▍▍ ▍▍ ▍▍ ▍▍☆ ★∵∴  .........................
*.......... ▍．∴∵∴∵．∴▅███████████☆ ★∵    ........................
*...........◥█▅▅▅▅███▅█▅█▅█▅█▅█▅█████████◤........@file run_me.py
*.............◥█████@author YangQi█████◤..........@time 2020/8/26
*...............◥████████████████████■◤............................
*******************************************************************
******************* ↓ ☆t☆ ↓ **************************************
******************* ↓ ☆i☆ ↓ **************************************
******************* ↓ ☆p☆ ↓ **************************************
自动化开启、关闭浏览器，进行netron的解析
****************************************************************"""
import os
import time
import netron_yq as netron
from datetime import datetime
from runtime.file import File
from runtime.timer import Timer

# 模型文件的路径
BASE_MODEL_FILE_PATH = 'input/'

# 解析好的模型信息路径
BASE_MODEL_INFO_PATH = 'output/'

TIME_OUT = 60  # 解析超时时间


# 第二代的netron解析器
# 间隔开启解析任务，浏览器的报错、关闭均由js进行
def handle_all_V_two(model_filename_list):
	begin = 0

	timer = Timer()
	timer.begin()

	total_models = len(os.listdir(BASE_MODEL_FILE_PATH))
	total_length = len(model_filename_list[begin:])

	for i, name in enumerate(model_filename_list[begin:]):
		timer.out_ergodic_info(total_length=total_length, now_index=i)
		try:
			print(f'\n\n启动时间：{datetime.now()},总编号：{i + begin},文件名{name},'
			      f'共计{total_models}个模型，'
			      f'已经解析了{len(os.listdir(BASE_MODEL_INFO_PATH))}个')
			full_path = BASE_MODEL_FILE_PATH + name
			# 如果已经解析过该模型，则跳过
			if File(BASE_MODEL_INFO_PATH + name + '.json').check_path_is_exist():
				print('文件已存在，跳过', BASE_MODEL_INFO_PATH + name + '.json')
				continue
			else:
				netron.start(file=full_path, browse=True, log=False)
				time.sleep(0.8)  # win速度较慢
		except:  # win下有浏览器线程报错
			print('error--->>', name)


if __name__ == '__main__':
	'''测试用'''
	# netron.start(browse=True, log=False)

	'''正式用'''
	model_filename_list = os.listdir(BASE_MODEL_FILE_PATH)
	handle_all_V_two(model_filename_list)
