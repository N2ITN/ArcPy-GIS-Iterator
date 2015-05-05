#Overview: 
#This process will map one-to-many labels (for example one station, many analytes + results) 
#This is feature which ArcGIS is generally missing. 
#It will do so for a list of analyte/matrix combinations referred to in this document as 'keys'.

#This process uses the following inputs:
	#a template MXD - the template for your map, should have all auxilluary data and formatting set up already
	#a template layer - holds the label expression and label style preferences
	#a 'Key' list of analyte/matrix combos 
	#a flat file arranged around the data keys and projected into arc as a shapefile

#This process generates the following outputs for each 'key' combo in the list, based on your data:
	#a layer file with a unique definition query
	#a close-to-production-ready MXD with a unique layer file with labels turned on and a custimized title block
	#a pdf of the mxd with the date of export and correct name
	#the process may require converting labels to annotation, then rearranging the lables and re-publishing to pdf

#It requires some auxillliary scripts:
	#GIS_LabelExpression.py - this goes in the label expression of the template file (python, advanced)
	#GIS_PrintMXDs.py - this iterates through your newly created MXDs and prints pdfs to a new folder



import arcpy, os
#get library dependencies



#*****************************************Set Environment*********************************************

mxd_path = r"C:\data\2015_sampling_locs_simple.mxd"
#The template MXD's path
mxd = arcpy.mapping.MapDocument(mxd_path)
#The template MXD arcpy object

df =arcpy.mapping.ListDataFrames(mxd,"Layers")[0]
#The dataframe in which the iterated layers will be found

layers = arcpy.mapping.ListLayers(mxd, "*", df)
#The layers in the template MXD

arcpy.MakeFeatureLayer_management(r"C:\data\layers\XYFOR_MAP2.shp","test_lyr")
#Generate a layer that is a copy of the template shapefile

lyr = arcpy.mapping.Layer("test_lyr")
#Name the layer for Python




#******************************************Set Map Gen Data Keys********************************************

maplist = ["GW_Metals" , "GW_SVOC" , "GW_TPH" , "GW_VOC" , "Soil_Metals" , "Soil_Moisture" , "Soil_PAHs&PCBs" , "Soil_TPH" , "Soil_VOC" 
]
#This list of 'Keys' contains every combination of two media types and several chemical groups

#The list of 'Keys' that will be used to generate: 
	#each layer's definition query
	#name of each MXD
	#text in each map's Title Block
	#name of each pdf export


layernames = []
#Declare this list so we can append to it in the next for loop




#***************************************Generate Unique Layers***********************************************

for MAP in maplist:
#Iterate through the list of 'keys' in order to generate the customized layers
#the customized layers each have a unique definition query that filters the desired sub-set for display 

	lyr.name = "2015" + MAP + ".lyr"
	#generate a name for the layer

	layernames.append(lyr.name)
	#add the name to a list we can use later to iterate through the layers

	newlayer = r"C:/data/layers/" + lyr.name
	#declare a file path for the layer

	KeepName = lyr.name
	#remember the layers name

	if os.path.exists(newlayer) == False:

		arcpy.SaveToLayerFile_management (lyr, newlayer)
		print "created new layer at: %s" % newlayer

	# addLayer = arcpy.mapping.Layer(newlayer)
	# arcpy.mapping.AddLayer(df, addLayer,"BOTTOM")
	# mxd.save()
	## This is supposed to add the new layer to the mxd but its not working. I just run it once to make the layers then drag them
	##	into the mxd template the first time.
	

	updateLayer = arcpy.mapping.ListLayers(mxd,lyr.name,df)[0] 
	#now we will update the layer with the settings from our 'template' layer

	#the template layer is where you set your label style and placement
	#as well as the label script
	#this way you only have to adjust the template once and the results are copied to all the layers

	sourceLayer = arcpy.mapping.Layer(r"C:\Data\layers\TEMPLATE.lyr")
	#layer to copy settings (label expression, formatting, symbology etc.) from


	arcpy.mapping.UpdateLayer(df, updateLayer, sourceLayer, False)
	#copy the settings

	updateLayer2 = arcpy.mapping.ListLayers(mxd, "TEMPLATE.lyr", df)[0]  
	#give the new layer object a name

	updateLayer2.name = KeepName
	#rename layer object to original name

	updateLayer2.definitionQuery = '"Map"' +" = " + "'"+ MAP + "'"
	#set the definition query. 
	#the names of the maps in the maplist are derived from a field in the data table
	#the table has 1 row for each MAP combo / sample loc combination
	#that row contains all analytes and their qualifiers and results


	updateLayer2.saveACopy(r"C:\data\layers\\" + lyr.name)
	#save the updated layer

	
del lyr
#deleting temporary variables supposedly helps with processing resources





#*************************************Generate Unique MXDs*************************************************

newMxdList = []
#delcare a new list we will append to soon
n=0
#counter for "figure #"
for L in layernames:
	if "Moisture" in L:
		continue
	#skip moisture

#iterate through all of the layer names
	n+=1
	newMxd = r"C:/data/mxds/"+"Figure_"+str(n)+"_"+L[:-4]+".mxd"
	#save a copy of the template MXD 
	#for each separate item in our 'key' list
	mxd.saveACopy (newMxd)

	newMxdList.append(newMxd)
	#keep a list of the new MXD paths

	mxd2 =  arcpy.mapping.MapDocument(newMxd)
	#the name of the current MXD we are iterating on

	df2 =arcpy.mapping.ListDataFrames(mxd2,"Layers")[0]
	#...and its data frame	


	for layer in arcpy.mapping.ListLayers(mxd2, "", df2):
	#iterate through the layers in the current mxd
		if layer.name == L:
		#if the layer matches the one layer file we are going to display
	  		layer.visible = True
	  		layer.showLabels = True
	  		#turn on the labels and make the layer visible
	  	elif layer.name in layernames or layer.name == "TEMPLATE.lyr":
	  	#if the layer is in our list of layers, but is not the one we are going to display	
	  		arcpy.mapping.RemoveLayer(df2, layer)
	  		#remove it from the data frame




#****************************************Update Title Block in Each MXD**********************************************

	info_ = L[4:-4]
	#strip out 2015- and  -.lyr from the layer's name

	Matrix = info_.split("_").pop(0)
	Chem = info_.split("_").pop(1)
	Chem = Chem.replace("&"," and ")
	
	Matrix = Matrix.replace("Soil2","Soil (Lower Depth)")
	Matrix = Matrix.replace("Soil1","Soil (Upper Depth)")

	#Separate the first and second parts of the layer in to two variables, format them

	Units = ''
	#declare a string 

	if 'Soil' in L:
		if 'TPH' in L or 'Metals' in L:
			Units = "mg/kg dry wt"
			
		else: Units = "ug/kg dry wt"
	if 'GW' in L:
		Units = "ug/L"
	if 'Moisture' in L:
		continue
	#decision tree to infer units from analysis/matrix combo
	#(derived from pivoting the flat file in excel)
		

	for elm in arcpy.mapping.ListLayoutElements(mxd2, "TEXT_ELEMENT"):
	# iterate through each text element in the current mxd
		Line1 = "Sample Concentrations for %s in %s" %(Chem, Matrix)
		elm.text = elm.text.replace("Figure 1", "Figure %s" %n) 
		elm.text = elm.text.replace("XY", Units)
		elm.text = elm.text.replace("Sample Locations", Line1) 		

		#replace the template text with the string variables  
		#from the 'keys'

	mxd2.save()
	#save the new mxd




#***************************************Call the Print Iterator to Print All Maps***********************************************

import GIS_PrintMXDs 
#call the function that prints a pdf of each mxd



