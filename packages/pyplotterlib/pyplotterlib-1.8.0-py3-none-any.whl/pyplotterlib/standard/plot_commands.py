
import itertools as it
import json
import matplotlib.ticker
import matplotlib.pyplot as plt


import numpy as np

from ..core import plot_command as plotCommCoreHelp
from ..core.serialization import register as serializationReg


#Generic commands should work for all
@serializationReg.registerForSerialization()
class AddPlotterToOutput(plotCommCoreHelp.PlotCommand):
	""" Adds the plotter instance to the output of createPlot()

	"""
	def __init__(self):
		self._name = "add-plotter-instance-to-output"
		self._description = "Adds the plotter instance used to create a plot to the output generated"

	def execute(self, plotterInstance):
		plotterInstance._scratchSpace["outDict"]["plotter"] = plotterInstance

#These are the multi-plotter class ones

#Below ALL refer to single-plotter cases
@serializationReg.registerForSerialization()
class AddColorBar(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "add-color-bar"
		self._description = "Adds a color bar to the plot"
		self._showAttr = "colorBarShow"

	def execute(self, plotterInstance):
		toShow = _getValueFromOptName(plotterInstance, self._showAttr)
		label = _getValueFromOptName(plotterInstance, "colorBarLabel")
		location = _getValueFromOptName(plotterInstance, "colorBarLocation")
		labelRotation = _getValueFromOptName(plotterInstance, "colorBarLabelRotation")

		if toShow is True:
			cbar = plt.colorbar(label=label,location=location)
			plotterInstance._scratchSpace["cbar"] = cbar			

			if labelRotation is not None:
				cbar.ax.xaxis.label.set_rotation(labelRotation)
				cbar.ax.yaxis.label.set_rotation(labelRotation)


@serializationReg.registerForSerialization()
class CopyNumpyArrayPlotDataToScratchSpace(plotCommCoreHelp.PlotCommand):

	def __init__(self, plotDataName="plotData"):
		""" Initializer
		
		Args:
			plotDataName: (str) The name of the attribute holding plot data. This may vary between plotters (e.g. at time of writing its plotData1D for BarPlotter)
				 
		"""
		self._name = "copy-plot-data-to-scratch-space"
		self._description = "Copies the basic plot data to the scratch space; this can be useful if data-processing is being carried out before plotting the data"
		self.plotDataName = plotDataName

	#Need to overwrite these classes to include the attr name for plotData
	def toJSON(self):
		outDict = {"class": str(self.__class__), "payload": {"plotDataName":self.plotDataName} }
		return json.dumps(outDict)

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		return cls( plotDataName=useDict["payload"]["plotDataName"] ) #Should almost ALWAYS be called without any values passed

	def execute(self, plotterInstance):
		plotData = _getValueFromOptName(plotterInstance, self.plotDataName)
		if plotData is None:
			plotterInstance._scratchSpace["usePlotData"] = None
		else:
			plotterInstance._scratchSpace["usePlotData"] = np.array(plotData,copy=True)


@serializationReg.registerForSerialization()
class CreateFigureIfNoAxHandle(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "create-figure"
		self._description = "If no ax-handle is present, create a figure"
		self._axHandleKey = "axHandle"

	def execute(self, plotterInstance):
		try:
			currAxHandle = plotterInstance._scratchSpace["axHandle"]
		except KeyError:
			self._createFigure(plotterInstance)

	def _createFigure(self, plotterInstance):
		try:
			figSize = getattr(plotterInstance.opts,"figSizeOnCreation").value
		except AttributeError:
			figSize = None

		currFigHandle = plt.figure(figsize=figSize)
		currFigHandle.add_subplot(111)
		plotterInstance._scratchSpace["axHandle"] = plt.gca()

@serializationReg.registerForSerialization()
class DrawShadedAnnotationsGeneric(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "drawGenericShadedAnnotations"
		self._description = "Adds shaded area annotations to the plot"
		self._optName = "annotationsShadedGeneric"

	def execute(self, plotterInstance):
		vals = _getValueFromOptName(plotterInstance, self._optName)
		if vals is None:
			return None

		for annotation in vals:
			self._addSingleAnnotation(plotterInstance, annotation)


	def _addSingleAnnotation(self, plotterInstance, annotation):
		#Figure out the command to use
		useComm = self._getUseComm(annotation)		

		#Figure out the keyword arguments
		kwargDict = {"alpha":annotation.opacity}

		if annotation.color is not None:
			kwargDict["color"] = annotation.color

		if annotation.polygonHooks is not None:
			kwargDict.update(annotation.polygonHooks)

		useComm(*annotation.shadeRange, **kwargDict)



	def _getUseComm(self, annotation):
		if annotation.direction.lower() == "vertical":
			return plt.axvspan
		elif annotation.direction.lower() == "horizontal":
			return plt.axhspan
		else:
			raise ValueError("{} is an invalid value for annotation.direction".format(annotation.direction))


@serializationReg.registerForSerialization()
class DrawTextAnnotationsGeneric(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "drawGenericAnnotations"
		self._description = "Adds Text annotations to the plot"
		self._optName = "annotationsTextGeneric"

	def execute(self, plotterInstance):
		vals = _getValueFromOptName(plotterInstance, self._optName)
		if vals is None:
			return None

		for annotation in vals:
			self._addSingleAnnotation(plotterInstance, annotation)

	def _addSingleAnnotation(self, plotterInstance, annotation):
		annotatePos = annotation.arrowPos if annotation.arrowPos is not None else annotation.textPos
		posArgs = [annotation.textVal, annotatePos]
		useDict = {"xytext":annotation.textPos}

		#Deal with fontsize; Note this can still be overwritten with "annotateMplHooks"
		fontSize = _getValueFromOptName(plotterInstance, "fontSizeDefault")
		fontSize = fontSize if annotation.fontSize is None else annotation.fontSize
		useDict["fontsize"] = fontSize

		#Update various fields
		if annotation.arrowPos is not None:
			useDict["arrowprops"] = dict()
			if annotation.arrowPropHooks is not None:
				useDict.update({"arrowprops":annotation.arrowPropHooks})

		if annotation.annotateMplHooks is not None:
			useDict.update(annotation.annotateMplHooks)

		if annotation.arrowCoordSys is not None:
			useDict.update({"xycoords":annotation.arrowCoordSys})

		if annotation.textCoordSys is not None:
			useDict.update({"textcoords":annotation.textCoordSys})

		#Actually add the annotation
		plt.annotate(*posArgs, **useDict)


@serializationReg.registerForSerialization()
class GridLinesCreate(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "create-grid-lines"
		self._description = "Creates grid lines if required" 
		self._settingsComms = [_GridLinesSetVisibilityOption(),
		                       _GridLinesSetLineStyles(),
		                       _GridLinesSetLineWidths()]

	def execute(self, plotterInstance):
		#Run all the commands to set kwarg dict
		for command in self._settingsComms:
			command.execute(plotterInstance)

		#Get kwarg dicts
		genDict = plotterInstance._scratchSpace.get("grid_line_opts", None)
		xDict = plotterInstance._scratchSpace.get("grid_line_opts_x", None)
		yDict = plotterInstance._scratchSpace.get("grid_line_opts_y", None)

		#Figure out if we need to do anything; return if not
		allDicts = [genDict, xDict, yDict]
		if all([x is None for x in allDicts]):
			return None

		#Figure out the visibility of the axis in general
		if genDict is None:
			genVis = False

		#We need to set x and y visibility to global if its not specifically set
		if xDict is not None:
			xVis = xDict.get("visible", None)
			if xVis is None:
				xDict["visible"] = genVis

		if yDict is not None:
			yVis = yDict.get("visible", None)
			if yVis is None:
				yDict["visible"] = genVis

		#Apply any options to grid lines (including turning on/off)
#		self._applyGeneralGridLineOpts(genDict)
		self._applyAxisGridLineOpts(genDict, axis="both")
		self._applyAxisGridLineOpts(xDict, axis="x")
		self._applyAxisGridLineOpts(yDict, axis="y")

#		raise ValueError("TODO: Want to set linewidth/color on GENERAL only")

	def _applyAxisGridLineOpts(self, genDict, axis="both"):
		if genDict is None:
			return None

		plt.gca().grid(**genDict, axis=axis)


@serializationReg.registerForSerialization()
class _GridLinesSetVisibilityOption(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "grid-lines-set-visibility"
		self._description = "Sets option for grid-lines visibility"
		self._optNameGen = "gridLinesShow"
		self._optNameX = "gridLinesShowX"
		self._optNameY = "gridLinesShowY"

		self._dictNameGen = "grid_line_opts"
		self._dictNameX = "grid_line_opts_x"
		self._dictNameY = "grid_line_opts_y"
		self._dictKey = "visible"

	def execute(self, plotterInstance):
		#General settings
		genVal = _getValueFromOptName(plotterInstance, self._optNameGen)
		if genVal is not None:
			_setScratchSpaceDictKey(plotterInstance, self._dictNameGen, self._dictKey, genVal)

		#x-specific settings
		xVal = _getValueFromOptName(plotterInstance, self._optNameX)
		if xVal is not None:
			_setScratchSpaceDictKey(plotterInstance, self._dictNameX, self._dictKey, xVal)

		#y-specific settings
		yVal = _getValueFromOptName(plotterInstance, self._optNameY)
		if yVal is not None:
			_setScratchSpaceDictKey(plotterInstance, self._dictNameY, self._dictKey, yVal)

@serializationReg.registerForSerialization()
class _GridLinesSetLineStyles(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "grid-lines-set-styles"
		self._description = "Sets option for grid line styles"

		self._dictNameGen = "grid_line_opts"
		self._genOptName = "gridLinesStyle"
		self._dictKey = "linestyle"

	def execute(self, plotterInstance):
		genVal = _getValueFromOptName(plotterInstance, self._genOptName)
		if genVal is not None:
			_setScratchSpaceDictKey(plotterInstance, self._dictNameGen, self._dictKey, genVal)

@serializationReg.registerForSerialization()
class _GridLinesSetLineWidths(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "grid-lines-set-widths"
		self._description = "Sets the width of grid lines"

		self._dictNameGen = "grid_line_opts"
		self._genOptName = "gridLinesWidth"
		self._dictKey = "linewidth"

	def execute(self, plotterInstance):
		genVal = _getValueFromOptName(plotterInstance, self._genOptName)
		if genVal is not None:
			_setScratchSpaceDictKey(plotterInstance, self._dictNameGen, self._dictKey, genVal)


#Will likely need to factor most out + inherit
@serializationReg.registerForSerialization()
class PlotDataAsLines(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "plot-line-data"
		self._description = "Plots available data using standard line-plot mode (matplotlibs plot)"
		self._optName = "plotData"

	def execute(self, plotterInstance):
		#Get the data; exit if none present
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None
		elif len(targVal)==0:
			return None

		#Look for any error bars present
		_errorBarDefVal = [None for x in targVal]
		errorBarsY = _getValueFromOptName(plotterInstance, "errorBarDataY", _errorBarDefVal)
		errorBarsX = _getValueFromOptName(plotterInstance, "errorBarDataX", _errorBarDefVal)
		errorBarMplHooks = _getValueFromOptName(plotterInstance, "errorBarLineMplHooks", _errorBarDefVal)

		errorBarMplHooks = [hooks for hooks,unused in zip( it.cycle(errorBarMplHooks), targVal)]

		#Plot the data; may want to return handles to scratch space later
		lineHandles = list()
		errorLineHandles, errorCapHandles = list(), list()
		capsizeVals = self._getCapsizeVals(plotterInstance)
		for idx,(currData, xErrBars, yErrBars, hooks) in enumerate(it.zip_longest(targVal,errorBarsX,errorBarsY, errorBarMplHooks)):
			xData, yData = np.array(currData)[:,0], np.array(currData)[:,1]
			if (xErrBars is not None) or (yErrBars is not None):
				_xBars, _yBars = [self._reshapeErrorBarData(bars) for bars in [xErrBars,yErrBars]]
				hooks = dict() if hooks is None else hooks
				if capsizeVals[idx] is not None:
					hooks["capsize"] = capsizeVals[idx]
				_allLines = plt.errorbar( xData, yData, yerr=_yBars, xerr=_xBars, **hooks ).lines
				currLines = _allLines[0]
				errorCapHandles.append(_allLines[1])
				errorLineHandles.append(_allLines[2])
			else:
				currLines = plt.plot( xData, yData )[0]
			lineHandles.append(currLines)

		#Add plotted lines to scratch space
		_setScratchSpaceDictKey(plotterInstance, "plotLineHandles", "value", lineHandles)
		if len(errorLineHandles) > 0:
			_setScratchSpaceDictKey(plotterInstance, "errorBars", "lineHandles", errorLineHandles)
			_setScratchSpaceDictKey(plotterInstance, "errorBars", "capHandles", errorCapHandles)

		return

	def _reshapeErrorBarData(self, errorBarData):
		if errorBarData is None:
			return None

		useData = np.array(errorBarData)

		if useData.shape[-1] == 2:
			return useData.transpose()
		else:
			return useData

	def _getCapsizeVals(self, plotterInstance):
		#Figure out how many vals we need to know
		plotData = _getValueFromOptName(plotterInstance, self._optName, retIfNone=list())

		#Figure out what capsizes to use
		errorCapsizes = _getValueFromOptName(plotterInstance, "errorBarCapsize", retIfNone=None)
		if errorCapsizes is None:
			return [None for x in plotData]

		useCapsizes = it.cycle(errorCapsizes)
		outVals = [capsize for data,capsize in zip(plotData, useCapsizes)]

		return outVals


@serializationReg.registerForSerialization()
class PlotHozAndVertLines(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "plot-hoz-and-vert-lines"
		self._description = "Plots horizontal and vertical lines; generally should be AFTER the main plotting (and x/y limit setting)"

	def execute(self, plotterInstance):
		self._plotHozLines(plotterInstance)
		self._plotVertLines(plotterInstance)

	def _plotHozLines(self, plotterInstance):
		#1) Get the positions
		linePositions = self._getLinePositionsFromKwarg(plotterInstance, "plotHozLinePositions")
		if linePositions is None:
			return None

		kwargDicts = self._getKwargDictsForHozLines(plotterInstance, len(linePositions))

		for currPos,kwargDict in it.zip_longest(linePositions, kwargDicts):
			plt.gca().axhline(y=currPos, **kwargDict)


	def _plotVertLines(self, plotterInstance):
		#1) Get the positions
		linePositions = self._getLinePositionsFromKwarg(plotterInstance, "plotVertLinePositions")
		if linePositions is None:
			return None

		kwargDicts = self._getKwargDictsForVertLines(plotterInstance, len(linePositions))

		for currPos,kwargDict in it.zip_longest(linePositions,kwargDicts):
			plt.gca().axvline(x=currPos,**kwargDict)


	def _getKwargDictsForHozLines(self, plotterInstance, nLines):
		#
		lineColors = _getValueFromOptName(plotterInstance, "plotHozLineColorStrs")
		lineColors = self._getCycledStrListFromStrOrStrIter(lineColors, nLines)

		#
		lineStyles = _getValueFromOptName(plotterInstance, "plotHozLineStyleStrs")
		lineStyles = self._getCycledStrListFromStrOrStrIter(lineStyles, nLines)

		outDicts = list()
		for idx,unused in enumerate(lineColors):
			_currDict = {"color": lineColors[idx], "linestyle":lineStyles[idx]}
			_currDict = {k:v for k,v in _currDict.items() if v is not None}
			outDicts.append(_currDict)
		return outDicts

	def _getKwargDictsForVertLines(self, plotterInstance, nLines):
		#
		lineColors = _getValueFromOptName(plotterInstance, "plotVertLineColorStrs")
		lineColors = self._getCycledStrListFromStrOrStrIter(lineColors, nLines)

		#
		lineStyles = _getValueFromOptName(plotterInstance, "plotVertLineStyleStrs")
		lineStyles = self._getCycledStrListFromStrOrStrIter(lineStyles, nLines)

		outDicts = list()
		for idx,unused in enumerate(lineColors):
			_currDict = {"color": lineColors[idx], "linestyle":lineStyles[idx]}
			_currDict = {k:v for k,v in _currDict.items() if v is not None}
			outDicts.append(_currDict)
		return outDicts

	def _getCycledStrListFromStrOrStrIter(self, strOrStrIter, nLines):
		if strOrStrIter is None:
			return [None for x in range(nLines)]

		if isinstance(strOrStrIter, str):
			useVals = [x[1] for x in zip( range(nLines), it.cycle([strOrStrIter]) ) ]
		else:
			useVals = [x[1] for x in zip( range(nLines), it.cycle(strOrStrIter) ) ]
		
		return useVals

	def _getLinePositionsFromKwarg(self, plotterInstance, kwarg):
		linePositions = _getValueFromOptName(plotterInstance, kwarg)
		if linePositions is None:
			return None

		try:
			iter(linePositions)
		except TypeError:
			linePositions = [linePositions]
		else:
			pass

		return linePositions


@serializationReg.registerForSerialization()
class SetAspectStr(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-aspect-str"
		self._description = "Sets the aspect string for the axis"
		self._optName = "aspectStr"

	def execute(self, plotterInstance):
		aspectStr = _getValueFromOptName(plotterInstance, self._optName)
		if aspectStr is None:
			return None
		else:
			_setScratchSpaceDictKey(plotterInstance, "plotKwargs", "aspect", aspectStr)


@serializationReg.registerForSerialization()
class SetAxisBorderInvisible(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetAxisBorderVisibility"
		self._description = "Sets the border visibility for various axes (top/bottom/left/right)"
		self._optName = "axisBorderMakeInvisible"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		attrKeys = ["top", "bottom", "left", "right"]
		if targVal is None:
			return None

		attrVals = [getattr(targVal,attr) for attr in attrKeys]
		if all([x is False for x in attrVals]):
			return None

		for attrKey, attrVal in it.zip_longest(attrKeys, attrVals):
			if attrVal is True:
				plt.gca().spines[attrKey].set_visible(False)
				if attrKey == "left":
#					plt.gca().get_yaxis().set_ticks([])
					plt.gca().tick_params(which="both", left=False, labelleft=False)
				if attrKey == "bottom":
#					plt.gca().get_xaxis().set_ticks([])
					plt.gca().tick_params(which="both", bottom=False, labelbottom=False)
				if attrKey == "right":
					plt.gca().tick_params(which="both", right=False, labelright=False)
				if attrKey == "top":
					plt.gca().tick_params(which="both", top=False, labeltop=False)

#				if attrKey == "right":

		#NOTE: Possibly some better commands here
		# hide the spines between ax and ax2
#		ax1.spines.bottom.set_visible(False)
#		ax2.spines.top.set_visible(False)
#		ax1.xaxis.tick_top()
#		ax1.tick_params(labeltop=False)  # don't put tick labels at the top
#		ax2.xaxis.tick_bottom()


@serializationReg.registerForSerialization()
class SetAxisColorX(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetAxisColorX"
		self._description = "Sets the base color for the x-axis"
		self._optName = "axisColorX"
		self._inclSpinesOptName = "axisColorX_exclSpines"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		#Set options
		currAx = plt.gca()
		currAx.xaxis.label.set_color(targVal)
		currAx.tick_params(axis='x', colors=targVal)

		exclSpines = getattr(plotterInstance.opts, self._inclSpinesOptName).value
		if exclSpines is not True:
			currAx.spines["bottom"].set_color(targVal)
			currAx.spines["top"].set_color(targVal)

@serializationReg.registerForSerialization()
class SetAxisColorY(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetAxisColorY"
		self._description = "Sets the base color for the y-axis"
		self._optName = "axisColorY"
		self._inclSpinesOptName = "axisColorY_exclSpines"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		#Set options
		currAx = plt.gca()
		currAx.yaxis.label.set_color(targVal)
		currAx.tick_params(axis='y', colors=targVal)

		exclSpines = getattr(plotterInstance.opts, self._inclSpinesOptName).value
		if exclSpines is not True:
			currAx.spines["left"].set_color(targVal)
			currAx.spines["right"].set_color(targVal)

@serializationReg.registerForSerialization()
class SetAxisScaleX(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-axis-scale-x"
		self._description = "Sets the type of scale for the x-axis; uses matplotlib set_xscale"

	def execute(self, plotterInstance):
		scaleVal = _getValueFromOptName(plotterInstance, "axisScaleX")
		if scaleVal is None:
			return None

		plt.gca().set_xscale(scaleVal)


@serializationReg.registerForSerialization()
class SetAxisScaleY(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-axis-scale-y"
		self._description = "Sets the type of scale for the y-axis; uses matplotlib set_yscale"

	def execute(self, plotterInstance):
		scaleVal = _getValueFromOptName(plotterInstance, "axisScaleY")
		if scaleVal is None:
			return None

		plt.gca().set_yscale(scaleVal)


@serializationReg.registerForSerialization()
class SetAxisTickAndLabelVisibilitiesEachSide(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetAxisTickAndLabelVisiblityEachSide"
		self._description = "Sets which sides of the plot to show/hide tick markers and labels"
		self._optName = "showTicksAndLabelsOnSides"

	def execute(self, plotterInstance):
		#
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None
		
		#
		useDict = {}
		attrs = ["bottom", "top", "left", "right"]
		for attr in attrs:
			currVal = getattr(targVal, attr)
			currLabelOpt, currTickOpt = "label" + attr, attr
			if currVal is True:
				useDict[currLabelOpt], useDict[currTickOpt] = True, True
			elif currVal is False:
				useDict[currLabelOpt], useDict[currTickOpt] = False, False
			else:
				pass #To catch None. Though will also catch other values

		plt.gca().tick_params(**useDict)
		plt.gca().tick_params(which="minor",**useDict)

@serializationReg.registerForSerialization()
class SetBarDataLabels(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-data-labels-for-bars"
		self._description = "Sets the data labels (to use in a legend) for a bar chart; this is different to the line plotter version since theres no safe equivalent to ax.get_lines()"
		self._optName = "dataLabels"

	def execute(self, plotterInstance):
		dataLabels = getattr(plotterInstance.opts, self._optName).value
		if dataLabels is None:
			return None

		plottedBars = plotterInstance._scratchSpace.get("barHandles", None)

		if plottedBars is None:
			return None

		if len(plottedBars) == 0:
			return None

		for barHandle, dataLabel in zip(plottedBars, dataLabels):
			if dataLabel is not None:
				barHandle.set_label(dataLabel)


@serializationReg.registerForSerialization()
class SetBarColors(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-colors-for-bars"
		self._description = "Sets the colors for series of bars"
		self._optName = "barColors"

	def execute(self, plotterInstance):
		colors = getattr(plotterInstance.opts, self._optName).value
		if colors is None:
			colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

		plottedBars = plotterInstance._scratchSpace.get("barHandles", None)
		if plottedBars is None:
			return None
		useColors = it.cycle(colors)

		for color,barSet in zip(useColors,plottedBars):
			_children = barSet.get_children()
			for child in _children:
				child.set_color(color)

@serializationReg.registerForSerialization()
class SetBarOpacities(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-opacities-for-bars"
		self._description = "Sets the opacities for a series of bars"
		self._optName = "barOpacities"

	def execute(self, plotterInstance):
		opacities = getattr(plotterInstance.opts, self._optName).value
		plottedBars = plotterInstance._scratchSpace.get("barHandles", None)

		if (plottedBars is None) or (opacities is None):
			return None

		useOpacities = it.cycle(opacities)
		for opacity, barSet in zip(useOpacities, plottedBars):
			_children = barSet.get_children()
			for child in _children:
				child.set_alpha(opacity)


@serializationReg.registerForSerialization()
class SetColorbarFontSizes(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-color-bar-fonts"
		self._description = "Sets the font sizes on the color bar (if its present)"
		self._dictKey = "cbar"

	def execute(self, plotterInstance):
		cbar = plotterInstance._scratchSpace.get("cbar",None)
		if cbar is None:
			return None
		
		#		
		globDefFont = _getValueFromOptName(plotterInstance, "fontSizeDefault")
		cbarDefFont = _getValueFromOptName(plotterInstance, "colorBarFontSize", retIfNone=globDefFont)
		labelFont = _getValueFromOptName(plotterInstance, "colorBarLabelFontSize", retIfNone=cbarDefFont)
		tickFont =  _getValueFromOptName(plotterInstance, "colorBarTickLabelFontSize", retIfNone=cbarDefFont)

		#
		self._setLabelFont(cbar, labelFont)
		self._setTickFont(cbar, tickFont)

	def _setLabelFont(self, cbar, labelFont):
		if labelFont is not None:
			cbar.ax.xaxis.label.set_fontsize(labelFont)
			cbar.ax.yaxis.label.set_fontsize(labelFont)

	def _setTickFont(self, cbar, tickFont):
		if tickFont is not None:
			cbar.ax.tick_params(labelsize=tickFont)


@serializationReg.registerForSerialization()
class SetColormapInPlotKwargs(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-color-map"
		self._description = "Sets the color map to use (just sets in a scratch-space dict though)"
		self._optName = "colorMapStr"

	def execute(self, plotterInstance):
		colorMapStr = _getValueFromOptName(plotterInstance, self._optName)
		if colorMapStr is None:
			return None
		else:
			_setScratchSpaceDictKey(plotterInstance, "plotKwargs", "cmap", colorMapStr) 

@serializationReg.registerForSerialization()
class SetColormapMaxValInPlotKwargs(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-max-colormap-val"
		self._description = "Sets the maximum value to use when mapping data to colors (sets a value in a scratchSpace dict)"
		self._optName = "colorMapMaxVal"

	def execute(self, plotterInstance):
		colorMapMaxVal = _getValueFromOptName(plotterInstance, self._optName)
		if colorMapMaxVal is None:
			return None
		else:
			_setScratchSpaceDictKey(plotterInstance, "plotKwargs", "vmax", colorMapMaxVal)

@serializationReg.registerForSerialization()
class SetColormapMinValInPlotKwargs(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-min-colormap-val"
		self._description = "Sets the minimum value to use when mapping data to colors (sets a value in a scratchSpace dict)"
		self._optName = "colorMapMinVal"

	def execute(self, plotterInstance):
		colorMapMinVal = _getValueFromOptName(plotterInstance, self._optName)
		if colorMapMinVal is None:
			return None
		else:
			_setScratchSpaceDictKey(plotterInstance, "plotKwargs", "vmin", colorMapMinVal)


@serializationReg.registerForSerialization()
class SetDataLabels(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetDataLabels"
		self._description = "Sets the data labels for lines currently plotted; this is needed to show a legend"
		self._optName = "dataLabels"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		_defVal = list()
		plottedLineHandles = _getScratchSpaceValueIfPresent(plotterInstance, "plotLineHandles", "value", retValIfNone=_defVal)

		for lineHandle, dataLabel in zip(plottedLineHandles, targVal):
			if dataLabel is not None:
				lineHandle.set_label(dataLabel)


@serializationReg.registerForSerialization()
class SetLineErrorBarColors(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLineErrorBarColors"
		self._description = "Sets the color of the error bars"

	def execute(self, plotterInstance):
		#Get error bar handles (exit if not present)
		errorHandles = _getScratchSpaceValueIfPresent(plotterInstance, "errorBars", "lineHandles", retValIfNone=None)
		errorCapHandles = _getScratchSpaceValueIfPresent(plotterInstance, "errorBars", "capHandles", retValIfNone=None)
		if errorHandles is None:
			return None

		#Figure out what colors to use; if empty then exit without doing anything
		colorCycle = self._getColorCycle(plotterInstance)
		if colorCycle is None:
			return None

		useColors = it.cycle(colorCycle)

		for capHandles,barHandles,color in zip(errorCapHandles,errorHandles,useColors):
			[handle.set_color(color) for handle in barHandles]
			[handle.set_color(color) for handle in capHandles]

	def _getColorCycle(self, plotterInstance):
		outCycles = None #The output variable

		#Set default values to the data line colors if their present
		useLineColors = _getValueFromOptName(plotterInstance, "errorBarColorsMatchLinesByDefault", retIfNone=False)
		lineColors = _getValueFromOptName(plotterInstance, "lineColors", retIfNone=None)
		if (lineColors is not None) and (useLineColors is True):
			outCycles = lineColors

		#TODO: Overwrite this with a more specific option if present
		overwriteColors = _getValueFromOptName(plotterInstance, "errorBarColors", retIfNone=None)
		if overwriteColors is not None:
			outCycles = overwriteColors

		return outCycles


@serializationReg.registerForSerialization()
class SetLegendFontSize(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLegendFontSize"
		self._description = "Sets the font size to use in the legend"

	def execute(self, plotterInstance):
		defFont = _getDefaultFontSizeFromPlotter(plotterInstance)
		useFont = defFont #No more specific way to overide yet
		if useFont is None:
			return None

		_setScratchSpaceDictKey(plotterInstance, "legendKwargDict", "fontsize", useFont)


@serializationReg.registerForSerialization()
class SetLegendNumberColumns(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLegendNumbColumns"
		self._description = "Sets the number of columns to use in the legend"
		self._optName = "legendNumbCols"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		_setScratchSpaceDictKey(plotterInstance, "legendKwargDict", "ncol", targVal)


@serializationReg.registerForSerialization()
class SetLegendLocStr(plotCommCoreHelp.PlotCommand):
	
	def __init__(self):
		self._name = "setLegendLocStr"
		self._description = "Sets the 'loc' option for matplotlibs legend() function; as far as i understand, this either tells mpl where to draw the legend or where to START drawing from"
		self._optName = "legendLocStr"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		#We REALLY want to avoid setting to something that isnt a string (such as the loc tuple)
		#or things will get confusing when setting fractional position
		assert isinstance(targVal, str)
		_setScratchSpaceDictKey(plotterInstance, "legendKwargDict", "loc", targVal)


#Note: This should generally be called AFTER SetLegendLocStr
@serializationReg.registerForSerialization()
class SetLegendFractPosStart(plotCommCoreHelp.PlotCommand):
	
	def __init__(self):
		self._name = "setLegendFractPosStart"
		self._description = "Sets either the 'loc' or 'bbox_to_anchor' values in mpl. Regardless, this tells it where to start drawing the legend"
		self._optName = "legendFractPosStart"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		try:
			locStr = plotterInstance._scratchSpace["legendKwargDict"]["loc"] = targVal
		except KeyError:
			plotterInstance._scratchSpace["legendKwargDict"]["loc"] = targVal
		else:
			plotterInstance._scratchSpace["legendKwargDict"]["bbox_to_anchor"] = targVal

#
@serializationReg.registerForSerialization()
class SetLegendHandlesToPlottedLinesDefault(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLegendHandlesToPlottedLines"
		self._description = "If they are present in the scratch space, the legend handles are set to plotLineHandles; this is to avoid errorbars interfering with the legend"

	def execute(self, plotterInstance):
		lineHandles = _getScratchSpaceValueIfPresent(plotterInstance, "plotLineHandles", "value")
		if lineHandles is None:
			return None
		_setScratchSpaceDictKey(plotterInstance, "legendKwargDict", "handles", lineHandles)
		

@serializationReg.registerForSerialization()
class SetLineAlpha(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLineThickness"
		self._description = "Sets the line thicknesses for lines currently plotted"
		self._optName = "lineAlpha"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		#
		try:
			iter(targVal)
		except TypeError:
			useVal = it.cycle([targVal])
		else:
			useVal = it.cycle(targVal)

		#
		lineHandles = _getScratchSpaceValueIfPresent(plotterInstance, "plotLineHandles", "value", retValIfNone=list())

		for line, alpha in zip(lineHandles, useVal):
			line.set_alpha(alpha)



@serializationReg.registerForSerialization()
class SetLineColors(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLineColors"
		self._description = "Sets the line colors for lines currently plotted"
		self._optName = "lineColors"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None



		_defVal = list()
		dataLines = _getScratchSpaceValueIfPresent(plotterInstance, "plotLineHandles", "value", retValIfNone=_defVal)
		colors = it.cycle(targVal)
		for dataLine, color in zip(dataLines, colors):
			dataLine.set_color(color)

@serializationReg.registerForSerialization()
class SetLineMarkerSizes(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLineMarkerSizes"
		self._description = "Sets the sizes for line markers"
		self._optName = "lineMarkerSizes"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		dataLines = _getScratchSpaceValueIfPresent(plotterInstance, "plotLineHandles", "value", retValIfNone=list())
		try:
			iter(targVal)
		except TypeError:
			useVal = it.cycle([targVal])
		else:
			useVal = it.cycle(targVal)

		for dataLine, markerSize in zip(dataLines, useVal):
			dataLine.set_markersize(markerSize)


@serializationReg.registerForSerialization()
class SetLineMarkerStyles(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLineMarkerStyles"
		self._description = "Sets the line markers for lines currently plotted"
		self._optName = "lineMarkerStyles"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		dataLines = _getScratchSpaceValueIfPresent(plotterInstance, "plotLineHandles", "value", retValIfNone=list())
		markerStyles = it.cycle(targVal)
		for dataLine, markerStyle in zip(dataLines, markerStyles):
			dataLine.set_marker(markerStyle)

@serializationReg.registerForSerialization()
class SetLineStyles(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLineStyles"
		self._description = "Sets the line styles for lines currently plotted"
		self._optName = "lineStyles"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		#
		_defLinesVal = list()
		dataLines = _getScratchSpaceValueIfPresent(plotterInstance, "plotLineHandles", "value", retValIfNone=_defLinesVal)


		lineStyles = it.cycle(targVal)
		for dataLine, lineStyle in zip(dataLines, lineStyles):
			dataLine.set_linestyle(lineStyle)


@serializationReg.registerForSerialization()
class SetLineThickness(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLineThickness"
		self._description = "Sets the line thicknesses for lines currently plotted"
		self._optName = "lineThickness"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		#
		try:
			iter(targVal)
		except TypeError:
			useVal = it.cycle([targVal])
		else:
			useVal = it.cycle(targVal)

		#
		lineHandles = _getScratchSpaceValueIfPresent(plotterInstance, "plotLineHandles", "value", retValIfNone=list())

		for line, thickness in zip(lineHandles, useVal):
			line.set_linewidth(thickness)



@serializationReg.registerForSerialization()
class SetTickLabelFontSize(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setTickLabelFontSize"
		self._description = "Sets the size of the font for axis tick labels"
		self._optName = "setTickLabelFontSize"

	def execute(self, plotterInstance):
		defVal = _getDefaultFontSizeFromPlotter(plotterInstance)
		if defVal is None:
			return None

		plt.gca().xaxis.set_tick_params(labelsize=defVal)
		plt.gca().yaxis.set_tick_params(labelsize=defVal)


@serializationReg.registerForSerialization()
class SetTickLabelValues(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetTickLabelValues"
		self._description = "Sets the values for the tick labels on x/y axes"
		self._optNameX = "tickMarkerLabelsX"
		self._optNameY = "tickMarkerLabelsY"

	def execute(self, plotterInstance):
		xLabelVals = _getValueFromOptName(plotterInstance, self._optNameX)
		yLabelVals = _getValueFromOptName(plotterInstance, self._optNameY)

		if xLabelVals is not None:
			plt.gca().set_xticklabels(xLabelVals)
			
		if yLabelVals is not None:
			plt.gca().set_yticklabels(yLabelVals)

@serializationReg.registerForSerialization()
class SetTickMarkerValues(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setTickMarkerValues"
		self._description = "Sets the values for the (major) tick marker positions on x/y axes"
		self._optNameX = "tickMarkerValsX"
		self._optNameY = "tickMarkerValsY"

	def execute(self, plotterInstance):
		xTickVals = _getValueFromOptName(plotterInstance, self._optNameX)
		yTickVals = _getValueFromOptName(plotterInstance, self._optNameY)

		if xTickVals is not None:
			plt.gca().set_xticks(xTickVals)

		if yTickVals is not None:
			plt.gca().set_yticks(yTickVals)

@serializationReg.registerForSerialization()
class SetTickMinorMarkersOn(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setTickMinorMarkersOn"
		self._description = "Optionally turns the minor tick markers on/off"
		self._optNameX = "showMinorTickMarkersX"
		self._optNameY = "showMinorTickMarkersY"

	def execute(self, plotterInstance):
		showMinorTicksX = _getValueFromOptName(plotterInstance, self._optNameX)
		showMinorTicksY = _getValueFromOptName(plotterInstance, self._optNameY)

		if showMinorTicksX is not None:
			if showMinorTicksX is False:
				plt.gca().xaxis.set_minor_locator( matplotlib.ticker.AutoMinorLocator(n=1) )
			elif showMinorTicksX is True:
				plt.gca().xaxis.set_minor_locator( matplotlib.ticker.AutoMinorLocator()   )

		if showMinorTicksY is not None:
			if showMinorTicksY is False:
				plt.gca().yaxis.grid(visible=False, which="minor")
			elif showMinorTicksY is True:
				plt.gca().yaxis.set_minor_locator( matplotlib.ticker.AutoMinorLocator()   )


@serializationReg.registerForSerialization()
class SetGroupTickValsToPosKey(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-tick-vals-to-values-in-scratchspace"
		self._description = "Sets the tick markers to groups of values found in the scratchspace. More general than setting to group Centres (original goal was to allow labels to be on left/right of bars)"
		self.defaultKey = "groupCentres"
		self.groupLabelPosKey = "groupLabelTickPosKey"

	def execute(self, plotterInstance):
		#
		plotHoz = plotterInstance.opts.plotHorizontally.value
		useKey = _getValueFromOptName(plotterInstance, self.groupLabelPosKey, retIfNone=self.defaultKey)
		useVals = plotterInstance._scratchSpace.get(useKey,None)

		if useVals is None:
			return None

		#
		everyN = _getValueFromOptName(plotterInstance, "groupLabelTicksEveryN", retIfNone=1)
		useCentres = [x for idx,x in enumerate(useVals) if idx%everyN==0]

		if plotHoz:
			plt.gca().set_yticks(useCentres)
		else:
			plt.gca().set_xticks(useCentres)


@serializationReg.registerForSerialization()
class SetTickValsToGroupCentres(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-tick-val-to-group-centres"
		self._description = "Sets the tick markers to the centre of each group of bars"
		
	def execute(self, plotterInstance):
		#Check if we have any data; exit if not
#		if not( _doesPlotterInstanceHaveData(plotterInstance) ):
#			return None

		plotHoz = plotterInstance.opts.plotHorizontally.value
		groupCentres = plotterInstance._scratchSpace.get("groupCentres",None)
		if groupCentres is None:
			return None

		#
		everyN = _getValueFromOptName(plotterInstance, "groupLabelTicksEveryN", retIfNone=1)
		useCentres = [x for idx,x in enumerate(groupCentres) if idx%everyN==0]

		if plotHoz:
			plt.gca().set_yticks(useCentres)
		else:
			plt.gca().set_xticks(useCentres)

@serializationReg.registerForSerialization()
class SetTickLabelsToGroupLabels(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-tick-labels-to-group-names"
		self._description = "Sets the axis tick labels to group names"

	def execute(self, plotterInstance):

		groupLabels = plotterInstance.opts.groupLabels.value
		if groupLabels is None:
			return None

		groupCentres = plotterInstance._scratchSpace.get("groupCentres",None)
		if groupCentres is None:
			return None

		#Basically same code i used to figure out where the ticks should go if every N
		everyN = _getValueFromOptName(plotterInstance, "groupLabelTicksEveryN", retIfNone=1)
		groupCentres = [x for idx,x in enumerate(groupCentres) if idx%everyN==0]

		#
		groupLabels = [x for idx,x in enumerate(groupLabels) if idx%everyN==0]

		#
		nGroups = len(groupCentres)
		useLabels = [ label for label,unused in it.zip_longest(groupLabels, range(nGroups)) ]
		useLabels = useLabels[:nGroups] if len(groupLabels)>nGroups else useLabels

		rotation = _getValueFromOptName(plotterInstance, "groupLabelRotation")

		#
		plotHoz = plotterInstance.opts.plotHorizontally.value
		if plotHoz:
			plt.gca().set_yticklabels(useLabels, rotation=rotation)
		else:
			plt.gca().set_xticklabels(useLabels, rotation=rotation)


@serializationReg.registerForSerialization()
class SetTickLabelRotations(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-tick-label-rotation"
		self._description = "Sets the rotation angle (in degrees) for labels on the x/y axis"

	def execute(self, plotterInstance):
		rotationX = _getValueFromOptName(plotterInstance, "tickLabelRotationX")
		rotationY = _getValueFromOptName(plotterInstance, "tickLabelRotationY")

		if rotationX is not None:
			plt.gca().xaxis.set_tick_params(rotation=rotationX)

		if rotationY is not None:
			plt.gca().yaxis.set_tick_params(rotation=rotationY)


@serializationReg.registerForSerialization()
class SetTitleStr(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setTitleString"
		self._description = "Sets the axis title string"
		self._optName = "titleStr"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		defFontSize = _getDefaultFontSizeFromPlotter(plotterInstance)
		xPosVal = _getValueFromOptName(plotterInstance, "titleFractPosX")
		yPosVal = _getValueFromOptName(plotterInstance, "titleFractPosY")

		kwargDict = {"fontsize":defFontSize, "x":xPosVal, "y":yPosVal}
		kwargDict = {k:v for k,v in kwargDict.items() if v is not None}
		plt.title(targVal, **kwargDict)

@serializationReg.registerForSerialization()
class SetXLabelStr(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetXLabelStr"
		self._description = "Set the string value for the x-label" 
		self._optName = "xLabelStr"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		defFontSize = _getDefaultFontSizeFromPlotter(plotterInstance)
		plt.xlabel(targVal, fontsize=defFontSize)

@serializationReg.registerForSerialization()
class SetXLabelFractPos(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetXLabelFractPos"
		self._description = "Set the fractional position for the x-label"
		self._optName = "xLabelFractPos"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None
		plt.gca().xaxis.set_label_coords(targVal[0], targVal[1])


@serializationReg.registerForSerialization()
class SetXLimit(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetXLimit"
		self._description = "Set the x-axis limits"
		self._optName = "xLimit"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None
		plt.xlim(targVal)

@serializationReg.registerForSerialization()
class SetYLimit(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetYLimit"
		self._description = "Set the y-axis limits"
		self._optName = "yLimit"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None
		plt.ylim(targVal)


@serializationReg.registerForSerialization()
class SetYLabelStr(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetYLabelStr"
		self._description = "Set the string value for the y-label"
		self._optName = "yLabelStr"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		defFontSize = _getDefaultFontSizeFromPlotter(plotterInstance)
		plt.ylabel(targVal, fontsize=defFontSize)


@serializationReg.registerForSerialization()
class SetYLabelFractPos(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetYLabelFractPos"
		self._description = "Set the fractional position for the y-label"
		self._optName = "yLabelFractPos"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None
		plt.gca().yaxis.set_label_coords(targVal[0], targVal[1])

@serializationReg.registerForSerialization()
class TurnLegendOnIfRequested(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "TurnLegendOnIfRequested"
		self._description = "Turn the legend on if requested"
		self._optName = "showLegend"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		legendKwargDict = plotterInstance._scratchSpace["legendKwargDict"]

		#Need to pass data line handles explicitly if present, otherwise error bars can interfere
		_defLinesVal = list()
		dataLines = _getScratchSpaceValueIfPresent(plotterInstance, "plotLineHandles", "value")


		if targVal is True:
#			if dataLines is not None:
#				plt.legend(dataLines,**legendKwargDict)
#			else:
			plt.legend(**legendKwargDict)



#Some shared helper functions
def _getDefaultFontSizeFromPlotter(plotterInstance):
	try:
		outVal = getattr(plotterInstance.opts, "fontSizeDefault").value
	except AttributeError:
		outVal = None
	return outVal


def _getValueFromOptName(plotterInstance, optName, retIfNone=None):
	try:
		outVal = getattr(plotterInstance.opts, optName).value
	except AttributeError:
		outVal = None

	if outVal is None:
		outVal = retIfNone

	return outVal

def _setAttributeIfPresent(plotterInstance, optName, value):
	try:
		getattr(plotterInstance.opts, optName).value = value
	except AttributeError:
		pass

def _setScratchSpaceDictKey(plotterInstance, dictName, key, value):
	#
	try:
		useDict = plotterInstance._scratchSpace[dictName]
	except KeyError:
		useDict = dict()
		plotterInstance._scratchSpace[dictName] = useDict

	#
	useDict[key] = value


def _getScratchSpaceValueIfPresent(plotterInstance, dictName, key, retValIfNone=None):
	#Check for dictionary, and get key if present
	try:
		useDict = plotterInstance._scratchSpace[dictName]
	except KeyError:
		return retValIfNone

	#Check for key in dictionary + return it if present
	try:
		outVal = useDict[key]
	except KeyError:
		return retValIfNone

	return outVal

