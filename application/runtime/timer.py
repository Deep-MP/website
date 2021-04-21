# -*- coding:utf-8 -*-
"""***************************************************************
******************************************************************
*........．．∵ ∴★．∴∵∴ ╭ ╯╭ ╯╭ ╯╭ ╯∴∵∴∵∴  .........................
*.........．☆．∵∴∵．∴∵∴▍▍ ▍▍ ▍▍ ▍▍☆ ★∵∴  .........................
*.......... ▍．∴∵∴∵．∴▅███████████☆ ★∵    ........................
*...........◥█▅▅▅▅███▅█▅█▅█▅█▅█▅█████████◤........@file timer.py 
*.............◥█████@author YangQi█████◤..........@time 2020/9/19
*...............◥████████████████████■◤............................
*******************************************************************
******************* ↓ ☆t☆ ↓ **************************************
******************* ↓ ☆i☆ ↓ **************************************
******************* ↓ ☆p☆ ↓ **************************************
计时器工具，用于时间统计
****************************************************************"""
import time


class Timer:

	def __init__(self):
		self.begin_time = None
		self.end_time = None
		self.progress_bar = ''
		for i in range(1, 101):
			self.progress_bar += '▉'
		for i in range(1, 101):
			self.progress_bar += '|'  # ░
		self.begin()

	def begin(self):
		# 强制刷新计时器的开始时间
		print('\n\n开始计时')
		self.begin_time = time.time()

	def end(self):
		self.end_time = time.time()

	# 输出耗费的时间
	def out_time_cost(self):
		self.end()
		cost = self.end_time - self.begin_time
		print(round(cost, 3))

	# 计算遍历耗时
	def out_ergodic_info(self, total_length: int, now_index: int, remark: str = ''):
		"""
		:param total_length:  总共要遍历的长度
		:param now_index: 当前的index，0开始计
		:param remark: 备注信息，打印的时候方便查看是在执行什么代码
		:return:直接打印到控制台
		"""
		percentage = (now_index + 1) / total_length  # 已走百分比
		has_cost_time = time.time() - self.begin_time  # 已花费时间
		remain_time = has_cost_time / percentage - has_cost_time  # 剩余时长

		if now_index > 0:
			speed = now_index / has_cost_time  # 每秒多少个
			# 如果每秒速度小于1 则计算多少秒一个
			if speed < 1:
				speed_info = f'{round(has_cost_time / now_index, 2)}秒/个'
			else:
				speed_info = f'{round(speed, 2)}个/每秒'
		else:
			speed_info = ''

		i = int(percentage * 100)
		print(f"\r运行 \"{remark}\" 中，"
		      f"当前进度：{self.progress_bar[101 - i:200 - i]}{round(percentage * 100, 3)}%，"
		      f"总长度为{total_length}，"
		      f"进行到第{now_index + 1}个，"
		      f"速度：{speed_info}，"
		      f"已耗费时间{round(has_cost_time, 2)}秒，"
		      f"预计还需要{round(remain_time, 2)}秒  "
		      , end='')

		# 运行结束后换行
		if now_index+1 == total_length:
			print('\n')
