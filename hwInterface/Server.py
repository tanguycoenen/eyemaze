# --------------------------------------------------------------------------------
#  Project    : AR/VR demonstrator
#  Filename   : Server.py
#  Content    : Demonstrator for the server side of the communication interface 
#				between the signal processing algorithm and the game
#  Version    : 1.0
#  Created by : B. Tiemersma
#  Date       : 12-9-2017
#  Modification and Version History: 
#  | Developer     | Version |    Date   |       Comments       | 
#  | B. Tiemersma  |   1.0   | 12-9-2017 | Initial demonstrator |
#  Copyright : Stichting imec Nederland (http://www.imec-nl.nl)
# --------------------------------------------------------------------------------
import mmap

class GameInterfaceServer:

	fileName = 'Interface.bin'
	version = 1
	
	def __init__(self):
		# define interface file order
		self.indices = {'version': 0, 'up': 1, 'down': 2, 'left': 3, 'right': 4, 'blink': 5, 'CalibrationStimulus': 6, 'ProgramState': 7}
		self.events = {k: self.indices[k] for k in ('up', 'down', 'left', 'right', 'blink')}
	
		# initialize the interface file
		with open(self.fileName, 'wb') as f:
			# initial interface state
			version = self.version	# RO, [0,255]
			up = False 				# RW
			down = False 			# RW
			left = False 			# RW
			right = False 			# RW
			blink = False 			# RW
			CalibrationStimulus = 0 # RO, [0,255]
			ProgramState = 0 		# RW, [0,255]
			
			# pack state in list
			ar = [None] * 8
			ar[self.indices['version']] = version
			ar[self.indices['up']] = up
			ar[self.indices['down']] = down
			ar[self.indices['left']] = left
			ar[self.indices['right']] = right
			ar[self.indices['blink']] = blink
			ar[self.indices['CalibrationStimulus']] = CalibrationStimulus
			ar[self.indices['ProgramState']] = ProgramState
		
			# store list as bytes in the interface file
			f.write(bytearray(ar))
			
	def __enter__(self):
		# open the interface file
		self.f = open(self.fileName, 'r+b')
		# memory-map the file, size 0 means whole file
		self.mm = mmap.mmap(self.f.fileno(), 0)
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.mm.close()		
		self.f.close()
		
	def Send(self, event):
		if event in self.events:
			self.mm[self.indices[event]] = True
	
	def ListState(self):
		return [int(b) for b in bytearray(self.mm)]
		
	def GetProgramState(self):
		return self.mm[self.indices['ProgramState']]
		

with GameInterfaceServer() as S:
	while True:
		try:
			str = input('Send a command to the client: ')
			command = str[0].lower()
		except:
			continue
			
		if command == 'u': 		# Up
			S.Send('up')
		elif command == 'd': 	# Down
			S.Send('down')
		elif command == 'l': 	# Left
			S.Send('left')
		elif command == 'r': 	# Right
			S.Send('right')
		elif command == 'b': 	# Blink
			S.Send('blink')
		elif command == 'p': 	# ProgramState
			print(S.GetProgramState())
		elif command == 's': 	# List the full state
			print(S.ListState())
		elif command == 'q': 	# Quit
			break
		else:
			print('Invalid command')

