#Testing.Function
bPrint__init = False
def print__init(name):
	if bPrint__init : print(name+".__init__")

bPrint__func = False
def print__func(name):
	if bPrint__func : print("function: "+name)

bPrint__funClass = False
def print__funClass(name):
	if bPrint__funClass : print("Class.function: "+name)

bPrintAction = False
def print__action(name):
	if bPrintAction : print("action: "+name)


#Testing END
