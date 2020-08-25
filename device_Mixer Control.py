# name=nanoKontrol2 - Mixer V1.2 (Lonz)
# url=https://forum.image-line.com/viewtopic.php?f=1994&t=236400


import transport
import mixer
import ui
import midi
import time
from nK2.nK2_FL import *
from nK2.userPara import *

Tog_TP=True #toggel TP-Button rewind and fastforward

lsChan = [20,30,40,50,60,70,80,90] #idx-Channel-Zuweisungen
lsKnob = [21,31,41,51,61,71,81,91] #idx-Knobs
lsSld = [22,32,42,52,62,72,82,92] #idx-Slider
lsSoloB = [23,33,43,53,63,73,83,93] #idx-Solo-Button
lsMuteB = [24,34,44,54,64,74,84,94] #idx-Mute-Button
lsRecB = [25,35,45,55,65,75,85,95] #idx-Rec-Button
lsSelTrackNames = ["[1]= ","[2]= ","[3]= ","[4]= ","[5]= ","[6]= ","[7]= ","[8]= "] #Name addition for selected tracks. Will be added at the front
ST_HintMsg=1.0 #Time to show Hint-Msg
FL_TR_COUNT_MAX=126 #max numbers of Mixer-Tracks

NK_CC_SLider_First = 36 # CC-Number first Slider
NK_CC_Slider_Last = 43 # CC-Number Slider 8 (last)
NK_CC_Knob_First = 4 # CC-Number first Knob
NK_CC_Knob_Last = 11 # CC-Number Knob 8 (last)
NK_Solo_But_First = 0 # CC-Number first Slider
NK_Solo_But_Last = 7 # CC-Number Slider 8 (last)
NK_Mute_But_First = 36 # CC-Number first Slider
NK_Mute_But_Last = 43 # CC-Number Slider 8 (last)
NK_Rec_But_First = 72 # CC-Number first Slider
NK_Rec_But_Last = 79 # CC-Number Slider 8 (last)

StepsPerTick=1
#lsSPT_Values is defined in nK2.userPara.py.
SPT_IDX=0#Index for lsSPT_Values
Tog_Steps=True #toggel Step-Ticker between Up(+1) and Down(-1) 
goTo=0

#Selection function in FL-Mixer

def selectActivMixTrack(MixTrackNr):
#Select only MixTrackNr
	mixer.setTrackNumber(MixTrackNr,1)
		
def selectActivArea(goTo):
#mark the 8 tracks that are controlled
	if Flag_No_Sel_Names: return
	x=NK_NrOf_ControlGr#8
	if goTo+NK_NrOf_ControlGr>FL_TR_COUNT_MAX:
		goL_Delta=(goTo+NK_NrOf_ControlGr-FL_TR_COUNT_MAX)
		x=x-goL_Delta
	for i in range(goTo,goTo+x):
		orgName= mixer.getTrackName(i)
		mixer.setTrackNumber(i,1)
		if isSelName(orgName)==False: mixer.setTrackName(i,lsSelTrackNames[i-goTo]+orgName[0:])
		
#reset selection function
def isSelName(lastName):
#check is it my SelectionName
	if lastName[0]=='[' and lastName[2]==']': return True
	else: return False

#reset last selction Tracknames (namePrefix)
def resetTrackName(event,lastIdx):
	if Flag_No_Sel_Names: return
	for i in range(lastIdx,lastIdx+8):
		lastName= mixer.getTrackName(i)
		if isSelName(lastName): mixer.setTrackName(i,lastName[5:])
	
#reset all Track-namePrefix
def resetAllName():
	if Flag_No_Sel_Names: return
	ui.setHintMsg("reset namePrefix")
	time.sleep(ST_HintMsg)
	for i in range(0,FL_TR_COUNT_MAX):
		lastName= mixer.getTrackName(i)
		if isSelName(lastName): mixer.setTrackName(i,lastName[5:])



#Main class NK-Control	
class TNKaction():
#Script/NK-Control: given function =========
	def OnInit(self):
		#resetAllName()
		goTo=0
		selectActivArea(goTo)	
		ui.showWindow(midi.widMixer)
		Tog_TP=True
		Tog_Steps=True
		StepsPerTick=1

	def OnDeInit(self):
		ui.showWindow(midi.widMixer)
		resetAllName()
		
	def OnMidiIn(self, event):
		pass
		
	def OnMidiMsg(self, event):
		FoundButton=[False,"",0,0,0]	#[Gefunden?,Name,idx,event.data1,event.data2]
		Last_Data=[0,""]
		FoundButton = getButton(event, FoundButton)
		
		if FoundButton[0]:
			if not (Last_Data[0]==event.data2 and Last_Data[1]==FoundButton[1]):
				self.actionButton(event, FoundButton)
				Last_Data=event.data2,FoundButton[1]
		
		
			



# my NK-Control-function =========
	def actionButton(self, event, FoundButton):	
	#Action to Button (wiht my Index FoundButton[2])
		global goTo
		global Tog_TP
		global Tog_Steps
		global StepsPerTick
		global lsSPT_Values
		global SPT_IDX
		snapVal=7
		
		def goRight(steps):
		#Selection go steps to the rigeht sight of Mixer
			sEnd=" "
			global goTo #Warum hier global und in goSteps nicht?
			lastgoTo=goTo
			if goTo+NK_NrOf_ControlGr+steps < FL_TR_COUNT_MAX: goTo=goTo+steps #print("right")
			else: 
				goTo=FL_TR_COUNT_MAX-NK_NrOf_ControlGr
				sEnd="END of Mixer (right)! - "	#wird mir goTo nie überschritten
			sHi_MixTR_Range=sEnd+"Mix-Tracks "+str(goTo)+"-"+str(NK_NrOf_ControlGr+goTo-1) #activ HintMsg Track area
			ui.setHintMsg(sHi_MixTR_Range)
			if lastgoTo!=goTo: resetTrackName(event,lastgoTo)
			selectActivArea(goTo)
			event.handled = True

		def goLeft(steps):
			#Selection go steps to the left sight of Mixer
			sEnd=" "
			global goTo 
			lastgoTo=goTo
			if goTo > steps-1: goTo=goTo-steps #print("left")
			else: 
				goTo=0
				sEnd="END of Mixer (left)! - "
			sHi_MixTR_Range=sEnd+"Mix-Tracks "+str(goTo)+"-"+str(NK_NrOf_ControlGr+goTo-1) #activ HintMsg Track area
			ui.setHintMsg(sHi_MixTR_Range)
			if lastgoTo!=goTo: resetTrackName(event,lastgoTo)
			selectActivArea(goTo)

		if FoundButton[2]==2: #8 to left
			goLeft(NK_NrOf_ControlGr)
			
		elif FoundButton[2]==3: #8 to right 
			goRight(NK_NrOf_ControlGr)
			
		elif FoundButton[2]==4: #reset
			ui.showWindow(midi.widMixer)
			resetAllName()
			event.handled = True #sonst knallt es
			
		elif FoundButton[2]==5: #set stepswide
		### Könnte ich dazu verwenden um einen Track fest zu zu ordnen
			if Tog_Steps and SPT_IDX<len(lsSPT_Values): 
				SPT_IDX+=1
				if SPT_IDX==(len(lsSPT_Values)-1): Tog_Steps = not Tog_Steps#max 7 per Ticker, Toggel betwenn Up/down
			elif SPT_IDX>0:
				SPT_IDX-=1
				if SPT_IDX==0: Tog_Steps = not Tog_Steps#max 7 per Ticker
			else: print("Error: Step-Counter")
			StepsPerTick=lsSPT_Values[SPT_IDX]
			ui.setHintMsg("set "+str(lsSPT_Values[SPT_IDX])+" steps")
			event.handled = True
			time.sleep(ST_HintMsg)
			
		elif FoundButton[2]==6: #StepsPerTick) to left
			goLeft(StepsPerTick)

		elif FoundButton[2]==7: #StepsPerTick) to right
			goRight(StepsPerTick)
			
		elif FoundButton[2]==8: #TP Rew
			if Tog_TP: transport.rewind(2)
			else: transport.rewind(0)
			Tog_TP= not Tog_TP
			event.handled = True
			
		elif FoundButton[2]==9: #TP FF
			if Tog_TP: transport.fastForward(2)
			else: transport.fastForward(0)
			Tog_TP= not Tog_TP
			event.handled = True
			
		elif FoundButton[2]==10: #TP stop 
			if Tog_TP: transport.fastForward(2)
			transport.stop()
			event.handled = True
			
		elif FoundButton[2]==11: #TP play
			transport.start()
			event.handled = True
			
		elif FoundButton[2]==12: #TP rec
			if bPrintAction: print("TP rec ",FoundButton[1]," Wert: ",FoundButton[4])
			transport.record()
			event.handled = True
			
		elif FoundButton[2] in lsKnob: #Paning
			nMixTrIndex=FoundButton[3]-(NK_CC_Knob_First) #36to43-35=MixTrackIdx in FL
			nMixTrPan=(1/64)*(FoundButton[4]-63) # max Pan. FL=-1.0 - 1.0 (0-127 steps)
			FL_Pan=int(mixer.getTrackPan(nMixTrIndex+goTo)*64)
			
			#Only change the value if the position of the controller matches the FL value. To avoid jumps
			if FoundButton[4]-63 in range(FL_Pan-snapVal,FL_Pan+snapVal) and Reg_Snap: 	mixer.setTrackPan(nMixTrIndex+goTo, nMixTrPan) #Set Paning
			if Reg_Snap==False: mixer.setTrackPan(nMixTrIndex+goTo, nMixTrPan) #Set Paning
			selectActivMixTrack(nMixTrIndex+goTo)
			event.handled = True

		elif FoundButton[2] in lsSld: #Volume
			nMixTrIndex=FoundButton[3]-(NK_CC_SLider_First) #36to43-35=MixTrackIdx in FL
			nMixTrVolu=(1/127)*FoundButton[4] # max Vol. FL=1.0 / max Vol. nK2=127, event.data2=Value from nK2-Slider
			FL_Vol=int(mixer.getTrackVolume(nMixTrIndex+goTo)*127)
			#Only change the value if the position of the controller matches the FL value. To avoid jumps
			if FoundButton[4] in range(FL_Vol-snapVal,FL_Vol+snapVal) and Reg_Snap: mixer.setTrackVolume(nMixTrIndex+goTo, nMixTrVolu) #Set Vol
			if Reg_Snap==False: mixer.setTrackVolume(nMixTrIndex+goTo, nMixTrVolu) #Set Vol
			selectActivMixTrack(nMixTrIndex+goTo)
			event.handled = True
		
		elif FoundButton[2] in lsSoloB: #Solo-Button
			nMixTrIndex=FoundButton[3]+NK_Solo_But_First 
			selectActivMixTrack(nMixTrIndex+goTo)
			mixer.soloTrack(nMixTrIndex+goTo) #
			event.handled = True
			
		elif FoundButton[2] in lsMuteB: #Mute-Button
			nMixTrIndex=FoundButton[3]-(NK_Mute_But_First) #36to43-35=MixTrackIdx in FL
			mixer.muteTrack(nMixTrIndex+goTo) #
			selectActivMixTrack(nMixTrIndex+goTo)
			event.handled = True

		elif FoundButton[2] in lsRecB: #Rec-Button
			nMixTrIndex=FoundButton[3]-(NK_Rec_But_First) #72to73-71=MixTrackIdx in FL
			mixer.armTrack(nMixTrIndex+goTo) #
			selectActivMixTrack(nMixTrIndex+goTo)
			event.handled = True
	
		
TNKaction = TNKaction()


def OnInit():
	TNKaction.OnInit()

def OnDeInit():
	TNKaction.OnDeInit()

def OnMidiIn(event):
	TNKaction.OnMidiIn(event)

def OnMidiMsg(event):
	TNKaction.OnMidiMsg(event)

