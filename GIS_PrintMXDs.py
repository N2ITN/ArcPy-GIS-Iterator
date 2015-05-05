import os, arcpy, time

def printMaps(mxd):
	mxd_literal = mxd
	#string of mxd path
	mxd = arcpy.mapping.MapDocument(mxd)
	#mxd Object
	print "starting..."
	path = mxd_literal.split("\\").pop()[:-4]
	print path
	#format path and print to console
	fold = r'C:\data\prints\\'
	#destination folder for pdfs

	pdf = ".pdf"
	date = (time.strftime("_%Y.%d.%m"))
	#get date and time in YYYY.DD.MM format
	newPdf = fold  + path + date + pdf
	#construct full path of output pdf
	if os.access(fold,os.F_OK) == False:
	    os.mkdir(fold)
	#make the destination folder if it isn't already there
	arcpy.mapping.ExportToPDF(mxd, newPdf)
	#export the target mxd to the destination folder


for x, y, z in os.walk(r"C:\data\mxds"):
#for main folder, subdirs, files in mxd folder 
	for file in z:
	#for each file
		mxd= x+"\\"+file
		#construct full filepath of mxd
		print mxd
		#print name of mxd to console


		printMaps(mxd)
		#send mxd to printMaps function