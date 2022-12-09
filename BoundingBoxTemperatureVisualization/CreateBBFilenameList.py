import fnmatch
import os
import numpy as np
import pdb 

''' 
Function Name: filterErrors(video_names,bb_names,errors,video_temps_C,video_temps_F)

Input Argument(s):
    1. video_temps_C - list of temperatures in celcius (string)
    2. video_temps_F - list of temperatures in fahrenheit (string)
    3. video_names - list of filenames corresponding to the temperature lists
    4. bb_names - list of filenames of each bounding box
    5. errors - list of error tuples 

Output Argument(s): 
    1. video_temps_C2 - list of filtered temperatures in celcius (string)
    2. video_temps_F2 - list of filtered temperatures in fahrenheit (string)
    3. video_names2 - list of filtered filenames corresponding to the temperature lists
    4. bb_names2 - list of filtered filenames of each bounding box

This function iterates through each element in each input lists and filters out the values 
from our list of error tuples.
'''
def filterErrors(video_names,bb_names,errors,video_temps_C, video_temps_F):
    #Split Error Tuple list
    error_names = [error[0] for error in errors] #Creates list of error names by grabbing first element from each tuple in error tuple list
    error_indicies = [error[1] for error in errors] #Creates list of error indicies by grabbing second element

    #Initialize empty arrays to hold filtered lists 
    bb_names2 = []
    video_names2 = []
    video_temps_C2 = []
    video_temps_F2 = []

    for i in range(len(bb_names)): #Iterates through each name in list of Bounding Box names
        check = 0 
        for name in error_names: #Iterates through each name in list of error names
            if (bb_names[i] == name): #If current BB name matches any of the error names
                check = 1 #Set check to 1
        if (check == 0): #If check is still 0 after comparing current BB name with all error names
            bb_names2.append(bb_names[i]) #add BB name to filtered return list

    for i in range(len(video_names)):
        check = 0 
        for name in error_names:
            if (video_names[i] == name):
                check = 1
        if (check == 0):
            video_names2.append(video_names[i])
            video_temps_F2.append(video_temps_F[i])
            video_temps_C2.append(video_temps_C[i])
   # pdb.set_trace()
    return video_names2, bb_names2, video_temps_C2, video_temps_F2

''' 
Function Name: getTemperatures(video_names, bb_names, temperatures)

Input Argument(s):
    1. video_names - list of filenames corresponding to the temperature lists
    2. bb_names - list of filenames of each bounding box
    3. temperatures - temperatures

Output Argument(s): 
    bb_temperatures - list of temperatures that corresponds with the bb_names index positions

This function iterates through each element in the list of bounding box filenames and each element of the 
list of video filenames. If a match between two elements is found, the value at the index position in the temperature list
is added to the output list.
'''
def getTemperatures(video_names, bb_names, temperatures):
    #Initialize new list to return temperature values 
    bb_temperatures = []
    
    for i in range(len(bb_names)): #Iterates through each name in list of Bounding Box names
        for j in range(len(video_names)): #Iterates through each name in list of video names
            #Find the index position in video names list that matches BB name. Add the value at that index position in the temperature
            # list to return list.
            if ((bb_names[i]) == (video_names[j])): 
                bb_temperatures.append(temperatures[j])         
            
    return bb_temperatures


''' 
Function Name: makeBBlists(outputPath,bbFramePath)

Input Argument(s):
    1. outputPath - path to output folder
    2. bbFramePath - path to folder containing bounding boxes 
Output Argument(s): 
    1. video_temps_C_filt - list of filtered temperatures in celcius (string)
    2. video_temps_F_filt - list of filtered temperatures in fahrenheit (string)
    3. video_names - list of filtered filenames corresponding to the temperature lists
    4. bb_names_filt - list of filtered filenames of each bounding box
    5. bb_temps_F_filt - list of bounding box temperatures in fahrenheit
    6. bb_temps_C_filt - list of bounding box temperatures in celcius

This function calls the functions defined above to filter out errors from our lists and saves them as new files 
to the output folder. It also creates 2 new lists to store temperature values with index positions corresponding
with the list of bounding box filenames.
'''
def makeBBlists(outputPath,bbFramePath):
    #cam_name = "3JUIL_Extracted_Data/"

    errors = np.load(os.path.join(outputPath,"errors.npy"))
    video_temps_C = np.load(os.path.join(outputPath,"video_temps_C.npy"))
    video_temps_F = np.load(os.path.join(outputPath,"video_temps_F.npy"))
    video_names = np.load(os.path.join(outputPath,"video_names.npy"))

    paths = bbFramePath
    paths = fnmatch.filter(os.listdir(paths), "*.jpg")

    bb_names = []  # intialize empty list to bounding box filenames

    for path in paths:
        filename = path.split('_')[0]
        bb_names.append(filename)

    print(f"Number of errors: {len(errors)}")
    print(f"BB Names before filter: {len(bb_names)}")
    print(f"Celsius Temps before filter: {len(video_temps_C)}")
    print(f"Far Temps before filter: {len(video_temps_F)}")
    print(f"Vid Names before filter: {len(video_names)}")
    print()
        
    video_names2, bb_names2, video_temps_C2, video_temps_F2 = filterErrors(video_names, bb_names, errors, video_temps_C, video_temps_F)
    
    # print()
    print(f"BB Names after filter: {len(bb_names2)}")
    # print(f"Celsius Temps after filter: {len(video_temps_C2)}")
    print(f"Far Temps after filter: {len(video_temps_F2)}")
    # print(f"Vid Names after filter: {len(video_names2)}")

    bb_temperatures = []
    baboon_temperatures_F = getTemperatures(video_names2, bb_names2, video_temps_F2)
    baboon_temperatures_C = getTemperatures(video_names2, bb_names2, video_temps_C2)

    print(f"Found BB Cel values: {len(baboon_temperatures_C)}")
    print(f"Found BB Far values: {len(baboon_temperatures_F)}")

    np.save(os.path.join(outputPath,"baboon_temperatures_F_filt.npy"), baboon_temperatures_F)
    np.save(os.path.join(outputPath,"baboon_temperatures_C_filt.npy"), baboon_temperatures_C)
    np.save(os.path.join(outputPath,"video_names_filt.npy"), video_names2)
    np.save(os.path.join(outputPath,"video_temps_F_filt.npy"), video_temps_F2)
    np.save(os.path.join(outputPath,"video_temps_C_filt.npy"), video_temps_C2)
    np.save(os.path.join(outputPath,"baboon_names_filt.npy"), bb_names)

