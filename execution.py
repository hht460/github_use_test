import sys,os
import threading
import time
from subprocess import check_call
import logging
from logging import debug as _d, info as _i, error as _e

# remove it since we have configed the log in main.py
# FORMAT = "%(asctime)-15s [%(thread)-5s] %(levelname)s - %(message)s"
# logging.basicConfig(
# 		filename='server.log',
# 		format=FORMAT,
# 		level=logging.INFO)


class Execution():
	def __init__(self):
		pass
	def run(self):
		pass

class SingleExecution(Execution):
	def __init__(self, command_line, name=None):
		self.command_line = command_line
		if name:
			self.name = name
		else:
			self.name = command_line
	def run(self):
		logging.info('[Begin] %s' % self.name)
		_i('Cmd : {0}'.format(self.command_line))
		_d('sys.path = {0}'.format(sys.path))
		rc = check_call(self.command_line.split())
		logging.info('[ End ] %s ReturnCode=%d' % (self.name,rc))

class SerialExecutions(Execution):
	def __init__(self, executions):
		self.executions = executions
	def run(self):
		for e in self.executions:
			e.run()

class ParallelExecutions(Execution):
	def __init__(self, executions):
		self.executions = executions
		self.interval = 0.0
	def setInterval(self, interval):
		self.interval = interval
	def run(self):
		threads = []
		for e in self.executions:
			t = threading.Thread(target=e.run)
			t.start()
			time.sleep(self.interval)
			threads.append(t)
		for t in threads:
			t.join()
			

if __name__=="__main__":
	a1 = SingleExecution("ping 127.0.0.1 -n 2")
	a2 = SingleExecution("ping 127.0.0.2 -n 3")
	a3 = SingleExecution("ping 127.0.0.3 -n 6")
	s1 = SerialExecutions([a1,a2])
	s2 = ParallelExecutions([s1,a3])
	s2.run()
