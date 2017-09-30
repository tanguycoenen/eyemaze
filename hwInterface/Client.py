# --------------------------------------------------------------------------------
#  Project    : AR/VR demonstrator
#  Filename   : Client.py
#  Content    : Demonstrator for the client side of the communication interface 
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

class GameInterfaceClient:

	fileName = 'Interface.bin'
	version = 1
	
	def __init__(self):
		# define interface file order
		self.indices = {'version': 0, 'up': 1, 'down': 2, 'left': 3, 'right': 4, 'blink': 5, 'CalibrationStimulus': 6, 'ProgramState': 7}
		self.events = {k: self.indices[k] for k in ('up', 'down', 'left', 'right', 'blink')}
			
	def __enter__(self):
		try:
			# open the interface file
			self.f = open(self.fileName, 'r+b')
			# memory-map the file, size 0 means whole file
			self.mm = mmap.mmap(self.f.fileno(), 0)
		except FileNotFoundError as e:
			raise Exception('Ensure that both client and server are in the same folder and that the server is running first') from e
			
		if self.mm[self.indices['version']] == self.version:
			return self
		else:
			raise ValueError('Incompatible interface version')
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.mm.close()		
		self.f.close()
		
	def SetProgramState(self, state):
		self.mm[self.indices['ProgramState']] = state
		
	def GetEvents(self):
		state = bytearray(self.mm)
		eventDict = {k: state[self.events[k]] for k in self.events}
		activeEvents = []
		for key,val in eventDict.items():
			if val:
				activeEvents.append(key)
		
		self.ClearEvents(activeEvents)
		return activeEvents
		
	def ClearEvents(self, events):
		for event in events:
			self.mm[self.events[event]] = False
		

with GameInterfaceClient() as C:
	state = 0
	
	while True:
		events = C.GetEvents()
		if events:
			print(events)
			state = (state + len(events)) % 256 # increment by number of events and contain within the range [0, 255]
			C.SetProgramState(state)

