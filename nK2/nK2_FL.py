# Instanzierung for FL Studio
#
import midi
import utils
from nK2.nK2_Classes import *
"""
An instance with the values ​​for FL Studio
==================================================

create a nanoKontrol2 -Instanz from class TNK_Control, with the Mapping-Values for FL. i take the values from Krog mapping file: FL Studio - nanoKONTROL2.nktrl2_data
"""

#interne Identifizierungs-Liste der Elemente des nanoKontrol2
idList=[[20,21,22,23,24,25,26],[30,31,32,33,34,35,36],[40,41,42,43,44,45,46],[50,51,52,53,54,55,56],[60,61,62,63,64,65,66],[70,71,72,73,74,75,76],[80,81,82,83,84,85,86],[90,91,92,93,94,95,96],[1,2,3,4,5,6,100],[7,8,9,10,11,12,101]]			
#Transport-Buttons instanzieren
TP_TrackRew=TNK_Button(idList[8][1],"TP_Button: Track Rew",midi.MIDI_CONTROLCHANGE,ButtonBehavior[0],0,64,63)
TP_TrackFF=TNK_Button(idList[8][2],"TP_Button: Track FF",midi.MIDI_CONTROLCHANGE,ButtonBehavior[0],1,64,65)
TP_Cycle=TNK_Button(idList[8][3],"TP_Button: Cycle",midi.MIDI_NOTEON,ButtonBehavior[0],15,0,2)
TP_Set=TNK_Button(idList[8][4],"TP_Button: set",midi.MIDI_NOTEON,ButtonBehavior[0],33,0,2)
TP_MarkerRew=TNK_Button(idList[8][5],"TP_Button: Marker Rew",midi.MIDI_CONTROLCHANGE,ButtonBehavior[0],2,64,63)
TP_MarkerFF=TNK_Button(idList[9][0],"TP_Button: Marker FF",midi.MIDI_CONTROLCHANGE,ButtonBehavior[0],3,64,65)
TP_Rew=TNK_Button(idList[9][1],"TP_Button: Rew",midi.MIDI_NOTEON,ButtonBehavior[0],13,0,2)
TP_FF=TNK_Button(idList[9][2],"TP_Button: FF",midi.MIDI_NOTEON,ButtonBehavior[0],14,0,2)
TP_Stop=TNK_Button(idList[9][3],"TP_Button: stop",midi.MIDI_NOTEON,ButtonBehavior[0],11,0,2)
TP_Play=TNK_Button(idList[9][4],"TP_Button: play",midi.MIDI_NOTEON,ButtonBehavior[0],10,0,2)
TP_Rec=TNK_Button(idList[9][5],"TP_Button: Rec",midi.MIDI_NOTEON,ButtonBehavior[0],12,0,2)

#create the 8 Control-Groups
NK_NrOf_ControlGr=8
listTNK_ControlGr = []
#mostly every Group use the Channel, set in Common-LED=Glob_Midi_CH
groupsMidiChannels = [Glob_Midi_CH,Glob_Midi_CH,Glob_Midi_CH,Glob_Midi_CH,Glob_Midi_CH,Glob_Midi_CH,Glob_Midi_CH,Glob_Midi_CH]
for i in range(NK_NrOf_ControlGr):
	listTNK_ControlGr.append(TNK_Control_group(idList[i][0],"Control_group 0"+str(i+1),i,groupsMidiChannels[i],TNK_Button(idList[i][3],"CG_Button: Solo 0"+str(i+1),midi.MIDI_NOTEON,ButtonBehavior[0],i,TP_OffValue,TP_OnValue),TNK_Button(idList[i][4],"CG_Button: Mute 0"+str(i+1),midi.MIDI_NOTEON,ButtonBehavior[0],i+36,TP_OffValue,TP_OnValue),TNK_Button(idList[i][5],"CG_Button: Rec 0"+str(i+1),midi.MIDI_NOTEON,ButtonBehavior[0],i+72,TP_OffValue,TP_OnValue),TNK_Regulator(idList[i][1],"CG_Regulator: Knob 0"+str(i+1),Typ_Knob,B_Enable,i+4,Knob_LeftValue,Knob_RightValue),TNK_Regulator(idList[i][2],"CG_Regulator: Slider 0"+str(i+1),Typ_Slider,B_Enable,i+36,Slider_LowerValue,Slider_UpperValue)))
	

#========= create a nanoKontrol2 -Instanz with the Mapping-Values for FL ========= 
#Attention: set gl. Midi-Channel in TCommon_LED Para2 mostly 1  
NK_FL = TNK_Control(idList[8][6],"TNK_Control_FL", TCommon_LED(idList[8][0],"TCommon_LED",1,ControlMode[0],LED_Mode[1]), TP_Common, TP_TrackRew, TP_TrackFF, TP_Cycle, TP_Set, TP_MarkerRew, TP_MarkerFF, TP_Rew, TP_FF, TP_Stop, TP_Play, TP_Rec, listTNK_ControlGr[0],listTNK_ControlGr[1],listTNK_ControlGr[2],listTNK_ControlGr[3],listTNK_ControlGr[4],listTNK_ControlGr[5],listTNK_ControlGr[6],listTNK_ControlGr[7])

def getButton(event, FoundButton): #Last_Data=[Name,data2]
#Which Button was used? return FoundButton=[Gefunden?,Name,idx,event.data1]
	if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,NK_FL.leftTR)
	if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,NK_FL.rightTR)
	if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,NK_FL.leftMarker)
	if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,NK_FL.rightMarker)
	if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,NK_FL.cycle)
	if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,NK_FL.set)
	if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,NK_FL.trRew)
	if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,NK_FL.trFF)
	if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,NK_FL.trStop)
	if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,NK_FL.trPlay)
	if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,NK_FL.tr_Rec)
	#8 Control-Groups
	listNK_CG = [NK_FL.ConGroup01,NK_FL.ConGroup02,NK_FL.ConGroup03,NK_FL.ConGroup04,NK_FL.ConGroup05,NK_FL.ConGroup06,NK_FL.ConGroup07,NK_FL.ConGroup08]
	for i in range(NK_NrOf_ControlGr):
		if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,listNK_CG[i].sBut)
		if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,listNK_CG[i].mBut)
		if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,listNK_CG[i].rBut)
		if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,listNK_CG[i].knob)
		if FoundButton[0]==False: FoundButton=NK_FL.identifyObj(FoundButton,event,listNK_CG[i].slider)

	if FoundButton[0]==True: print(FoundButton[1]+": Id="+str(FoundButton[2])+" CC_Note_Nr="+str(FoundButton[3])+" Value="+str(FoundButton[4]))
	return FoundButton

