def stopWatch(value):
	# A stopwatch to track time
	
	valueMinutes = value/60
	minutes = int(valueMinutes)

	valueSeconds = (valueMinutes - minutes)*60
	seconds = int(valueSeconds)

	valueMiliSeconds = (valueSeconds - seconds)*1000
	miliSeconds = int(valueMiliSeconds)


	if(minutes>0): return "(Time: "+str(minutes)+" minutes and "+str(seconds)+" seconds)"
	if(seconds>0): return "(Time: "+str(seconds)+" seconds and "+str(miliSeconds)+" milliseconds)"
	else: return "(Time: "+str(miliSeconds)+" milliseconds)"

