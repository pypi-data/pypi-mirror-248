
import json
from ...core.serialization import json_io as jsonIoHelp


class FromJsonMixin():

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		outObj = cls()
		optionsObj = jsonIoHelp.createInstanceFromJSON(useDict["payload"]["options"])
		commandObjs = [ jsonIoHelp.createInstanceFromJSON(x) for x in useDict["payload"]["commands"] ]

		outObj._options = optionsObj
		outObj._commands = commandObjs
		return outObj


class FromPlotterMixin():

	@classmethod
	def fromPlotter(cls, inpPlotter):
		""" Create the plotter using options from inpPlotter.
		
		Args:
			inpPlotter: (PlotterInter) Should generally be the same type as the target, though doesnt have to be (see Notes for behaviour details).
		
		Returns:
			outPlotter: (PlotterInter)


		Notes:
			a) We dont explicitly copy anything by default. So a SimpleNamespace option-value on outPlotter will point to the same object as on inpPlotter. You may wish to use copy.deepcopy(outPlotter) for safety.
			b) outPlotter will set every relevant option it finds on inpPlotter. If an option is ONLY on inpPlotter, it will be ignored. If an option is ONLY on outPlotter, the default value will be used.
			c) w.r.t. point b); note that some options with the same name (e.g. "plotData") may mean different things on different plotters. Thus, care should be exercised if type(inpPlotter) does not match type(outPlotter)

		 
		"""
		outPlotter = cls()
		sharedOptNames = set(inpPlotter.optionNames).intersection(outPlotter.optionNames)

		optDict = dict()
		for optName in sharedOptNames:
			currVal = getattr(inpPlotter.opts,optName).value
			optDict[optName] = currVal

		outPlotter.setOptionVals(optDict)

		return outPlotter


def _getAxisEdges(inpAx):
	startX, startY, xLength, yLength = inpAx.get_position().bounds
	endX, endY = startX+xLength, startY+yLength
	return startX, startY, endX, endY



#Refactored/Extracted from bar_plotter; also usable in boxPlotter (and likely other similar plotters in the future)
def _getIndividAndGroupCentresBarLikePlot(nGroups, nSeries, widthBar, widthIntraSpacing,
                                          widthInterSpacing, startPos=0, skipSeries=None):
	outCentres = [ list() for x in range(nSeries) ]
	currPos = startPos

	if skipSeries is None:
		skipSeries = [False for x in range(nSeries)]

	#Figure out where to plot the individual bars/similar
	for gIdx in range(nGroups):
		for skipShift,sIdx in zip(skipSeries, range(nSeries)):
			outCentres[sIdx].append(currPos)
			if skipShift is False:
				currPos += widthIntraSpacing
				currPos += widthBar

		#Not 100% sure why this if statement had to be added
		if any(skipSeries):
			currPos += widthInterSpacing + widthBar
		else:
			currPos += widthInterSpacing


	#Figure out the centre of each group
	groupCentres = list()
	for idx in range(nGroups):
		currCentres = [ x[idx] for x in outCentres ]
		currAverage = sum(currCentres)/len(currCentres)
		groupCentres.append(currAverage)
	
	return outCentres, groupCentres

