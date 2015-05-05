


 

 def FindLabel ( [sample_id], [Res_1], [Res_2], [Res_3], [Res_4], [Res_5], [Res_6], [Res_7], [Res_8], [Res_9], [Res_10], [Res_11], [Res_12] ):
  mylist = [Res_1], [Res_2], [Res_3], [Res_4], [Res_5], [Res_6], [Res_7], [Res_8], [Res_9], [Res_10], [Res_11], [Res_12]
  labName = "<BOL>" + [sample_id] + "</BOL> \r"
  for x in mylist:
    if len(x)>1:
     labName = labName + x + "\r"
  return labName


 #for each column that could contain data in the current row (data = analyte + result + qualifier for current map+sample point combination)
 # add sample ID to label in bold
 #if the data field not blank:
	 #add the data to the label, make a line break
	 #next data
 #when the row is done return the label name to the function
 