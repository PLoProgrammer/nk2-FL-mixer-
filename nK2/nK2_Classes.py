# Elements of nanoKontrol2 as Classes
#
import midi
import utils
from nK2.testing import *
"""
Rebuild the Korg nanoKontrol2 as software classes
==================================================

Replica of the Button \ Knobs \ Sliders of the nanoKontrol2 as software classes. To facilitate the assignment and, if necessary, to expand the range of functions.
"""

TP_Common=14 #Transport Button Midi Channel=14 optional [1-16, Global]
Glob_Midi_CH = 1 #Control_Groups can have Midi-Channel (1-16) or global, ist set in Common-LED (defaul: 1)
Midi_Not = 0 #Button is not enabel, No Assign (Button-State[No Assign, Control Change, Note])
B_Enable = True #Regulator is enable
B_Disable = False
Typ_But = 1
Typ_Knob = 2 #Regulator is a Knob
Typ_Slider= 3 #Regulator is a Slider
Reg_Typ = [Typ_Knob, Typ_Slider]
LED_Int = 0 #Internal LED-Mode
LED_Ext = 1 #External LED-Mode
LED_Mode = [LED_Int, LED_Ext]
ButtonBehavior = ['Momentary','Toggle'] #Momentary On and Off Note-Event acure, Toggle only Note On
ControlMode =['CC','Cubase','Digital Performer','Live','Pro Tools','SONAR']
TP_OffValue = 0 # Off Value Transport-Button
TP_OnValue= 127 # On Value Transport-Button
Knob_LeftValue = 0 # Low Value of Knob
Knob_RightValue = 127 # High Value of Knob
Slider_LowerValue = 0 # Low Value of Slider
Slider_UpperValue = 127 # High Value of Slider

#Count_OMM = 0#Counter for OnMidiMsg
Last_Data = [0,""]

# Transport Section
class TNK_Button:
# Class for Transport, Solo, Mute and Rec-Button 
#	Transport-Button CC-Events and Note-Events
#	Solo, Mute and Rec-Button normaly Note-Events
	def __init__(self,idx,name,assignType,buttonBehavior,CC_Note_Nummber,offValue,onValue):
		self.idx = idx #intern Identifyer
		self.name = name
		self.Type = Typ_But
		self.AT =assignType #Note, CC or not enable
		self.BB = buttonBehavior #Momentary or Toggle
		self.CC_NN = CC_Note_Nummber
		self.offV= offValue
		self.onV = onValue
		print__init(self.name)
		
	#Check Note or CC -event and CC/Note-Nr
	def identifyMe(self):
		list = [self.AT,self.CC_NN,self.onV] #in some casse checkt OnValue
		return list
		
class  TNK_Regulator:
# Class for Knob and Slider
#	Always CC-Events
	def __init__(self,idx,name,regulatorType,enable,CC_Nummber,lowValue,highValue):
		self.idx = idx #intern Identifyer
		self.name = name
		self.Type =regulatorType #Knob or Slider
		self.enable = enable
		self.CC = CC_Nummber
		self.lowV= lowValue
		self.highV = highValue
		print__init(self.name)

	#Check Note or CC -event and CC/Note-Nr
	def identifyMe(self):
		list = [midi.MIDI_CONTROLCHANGE,self.CC,self.highV]
		return list

#Control group
class TTNK_Control_group:
# Group of 3 Buttons (Solo,Mute,Rec), a Knob and a Slider.
#	Have a name, Index and a Midi-Channel
	def __init__(self,idx,name,nr,midiChannel,soloButton,muteButton,recButton,knob,slider):
		self.idx = idx #intern Identifyer
		self.name = name
		self.Nr = nr
		self.midiChannel = midiChannel #is Glob_Midi_CH set form TCommon_LED
		self.sBut = soloButton
		self.mBut = muteButton
		self.rBut = recButton
		self.knob = knob
		self.slider = slider
		print__init(self.name)


class TCommon_LED:
# Global Control, LED
	def setGlobMidiChannel(self, globMidiCH):
		Glob_Midi_CH = self.globMidiCH
		return Glob_Midi_CH
		
	def __init__(self,idx,name,globalMidiChannel,controlMode,modeLED):
		self.idx = idx #intern Identifyer
		self.name = name
		self.globChannel = globalMidiChannel # set the global-Midi-Channel 
		self.controlMode =controlMode
		self.LED= modeLED
		print__init(self.name)
		
	def getGlobMidiChannel(self):
		return self.globChannel
		
class TNK_Control:
# And now the nanoKontrol
	def __init__(self,idx,name, LED, TP_Common, TP_But01, TP_But02, TP_But03, TP_But04, TP_But05, TP_But06, TP_But07, TP_But08, TP_But09, TP_But10, TP_But11, ConGroup01, ConGroup02, ConGroup03, ConGroup04, ConGroup05, ConGroup06, ConGroup07, ConGroup08):
		self.idx = idx #intern Identifyer
		self.name = name #"for FL Studio"
		self.LED = LED 
		self.TP_Common = TP_Common
		self.leftTR = TP_But01
		self.rightTR = TP_But02
		self.cycle = TP_But03
		self.set = TP_But04
		self.leftMarker = TP_But05
		self.rightMarker = TP_But06
		self.trRew = TP_But07
		self.trFF = TP_But08
		self.trStop = TP_But09
		self.trPlay = TP_But10
		self.tr_Rec = TP_But11
		self.ConGroup01 = ConGroup01
		self.ConGroup02 = ConGroup02
		self.ConGroup03 = ConGroup03
		self.ConGroup04 = ConGroup04
		self.ConGroup05 = ConGroup05
		self.ConGroup06 = ConGroup06
		self.ConGroup07 = ConGroup07
		self.ConGroup08 = ConGroup08
		print__init(self.name)

		#Count_OMM = 0 #Counter for OnMidiMsg
		#Last_EV2_Value = 0
		Last_Data = [0,""]
#=========== END of Class def ===========

#=========== Funktionen ===========
	def getGlobMidiChannel(self):
			return self.LED.getGlobMidiChannel()
		
	def identifyObj(self,FoundButton,event,obj):
	#Determine which button / knob / slider was pressed and assign it to the corresponding class
	#Warning: I cannot differentiate whether Knob 01 was operated with the values ​​63-65 or Track rew or Track FF because they have the same values.: 	
		global Last_Data
		print__funClass(obj.name+".identifyObj(...)")

		if FoundButton[0]==False:
			#Marker Rew & FF
			if event.midiId == midi.MIDI_CONTROLCHANGE and (event.data1 == 35):
				if event.midiId == obj.identifyMe()[0] and event.data1 == obj.identifyMe()[1] and event.data2 == obj.identifyMe()[2]: #Rew or FF
					FoundButton=[True,obj.name,obj.idx,event.data1,event.data2]
					Last_Data=event.data2,FoundButton[1]
					return FoundButton
				else: #if not first (Rew or FF) Break and try next
					FoundButton = [False,"",0,0,0]
					return FoundButton
			
			#Track Rew & FF or Knob 1
			if event.midiId == midi.MIDI_CONTROLCHANGE and (event.data1 == 0):
				if event.midiId == obj.identifyMe()[0] and event.data1 == obj.identifyMe()[1] and (event.data2<63 or event.data2>65): #Knob 1
					if (obj.name=="TP Track Rew" or obj.name=="TP Track FF"):
						FoundButton = [False,"",0,0,0]
						return FoundButton
					else:
						#print("Knob 01 <63 or >65",event.data2)
						FoundButton=[True,obj.name,obj.idx,event.data1,event.data2]
						Last_Data=event.data2,FoundButton[1]
						return FoundButton
				else:
					#Track Rew & FF data2=63-65
					if event.midiId == obj.identifyMe()[0] and event.data1 == obj.identifyMe()[1] and event.data2 == obj.identifyMe()[2] and Last_Data[1]!="TNK_Regulator: Knob 01" and (obj.name=="TP Track Rew" or obj.name=="TP Track FF"): 
						FoundButton=[True,obj.name,obj.idx,event.data1,event.data2]
						Last_Data=event.data2-Last_Data[0],FoundButton[1]
						return FoundButton
					elif event.midiId == obj.identifyMe()[0] and event.data1 == obj.identifyMe()[1] and Last_Data[1]=="TNK_Regulator: Knob 01" and (obj.name!="TP Track Rew" and obj.name!="TP Track FF") and abs(event.data2-Last_Data[0])==1: #event.data2!=Last_Data[0]: #Knob 1 data2=63-65
						#print("Wohl doch Knob 01",event.data2)
						FoundButton=[True,obj.name,event.data1,event.data2] #"TNK_Regulator: Knob 01"
						Last_Data=event.data2,FoundButton[1]
						return FoundButton
					else:
						FoundButton = [False,"",0,0,0]
						return FoundButton

			if event.midiId == obj.identifyMe()[0] and event.data1 == obj.identifyMe()[1] and event.data1 != 35:
				FoundButton=[True,obj.name,obj.idx,event.data1,event.data2]
				Last_Data=event.data2,FoundButton[1]
		
			if FoundButton[0]: 
				Last_Data=event.data2,FoundButton[1]
			
		return FoundButton

		
	