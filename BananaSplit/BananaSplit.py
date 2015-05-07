import os
import sys
import shutil
import math
import subprocess
import time
# import antigravity

print("****************************************")
print("Banana Split by Sleepydragn1")
print("https://github.com/Sleepydragn1/BananaSplit")
print("Type 'exit' in any of the inputs to exit the script!")
print("****************************************")
print("")

class InvalidInputError(Exception):
    pass

def inputE(question):
    inputStr = input(question)
    if inputStr == 'exit':
        print("Exiting script.")
        sys.exit()
    return inputStr

path = inputE("File path: " )
if path[len(path) - 1] != "/" and path[len(path) - 1] != "\\":
    path = os.path.join(path, "")
while not os.path.exists(path):
    print("Invalid or inaccessible file path!")
    path = inputE("File path: " )

validFlag = False
while not validFlag:
    project = inputE("Project name: ")
    if not project:
        print("No project specified. After Effects will render your currently open project.")
        validFlag = True
    else:
        if project.endswith(".aep"):
            if not os.path.exists(path + project):
                print("Invalid or inaccessible project!")
            else:
                path = path[0:len(path) - 4]
                validFlag = True
        else:
            if not os.path.exists(path + project + ".aep"):
                print("Invalid or inaccessible project!")
            else:
                validFlag = True

composition = inputE("Composition name: ")
if not composition:
    print("Defaulting to 'Main'")
    composition = "Main"

validFlag = False
while not validFlag:
    framerate = inputE("Composition framerate: ")
    if framerate == "":
        print("Defaulting to 60fps.")
        framerate = 60.0
        validFlag = True
    else:
        try:
            framerate = float(framerate)
            if framerate <= 0:
                raise InvalidInputError("")
            validFlag = True
        except ValueError:
            print("Invalid framerate!")
        except InvalidInputError:
            print("Framerate cannot be less than or equal to zero!")

validFlag = False
while not validFlag:
    rFramerate = inputE("Re-encode framerate: ")
    if rFramerate == "":
        print("Defaulting to composition framerate (" + str(framerate) + ")")
        rFramerate = framerate
        validFlag = True
    else:
        try:
            rFramerate = float(rFramerate)
            if rFramerate <= 0:
                raise InvalidInputError("")
            validFlag = True
        except ValueError:
            print("Invalid framerate!")
        except InvalidInputError:
            print("Framerate cannot be less than or equal to zero!")
        
validFlag = False
while not validFlag:
    audio = inputE("Include audio? (y/n): ")
    if not audio:
        print("Defaulting to enabled audio.")
        audio = True
        validFlag = True
    elif audio == "y" or audio == "Y":
        audio = True
        validFlag = True
    elif audio == "n" or audio == "N":
        audio = False
        validFlag = True
    else:
        print("Invalid answer!")

durationFlag = False
while not durationFlag:
    validFlag = False
    while not validFlag:
        durationHours = inputE("Composition hour duration: ")
        if not durationHours:
            print("Defaulting to 0.")
            durationHours = 0
            validFlag = True
        else:
            try:
                durationHours = int(durationHours)
                if durationHours < 0:
                    print("Duration cannot be negative.")
                else: 
                    validFlag = True
            except ValueError:
                print("Invalid duration!")
    
    validFlag = False
    while not validFlag:
        durationMinutes = inputE("Composition minute duration: ")
        if not durationMinutes:
            print("Defaulting to 0.")
            durationMinutes = 0
            validFlag = True
        else:
            try:
                durationMinutes = int(durationMinutes)
                if durationMinutes < 0:
                    print("Duration cannot be negative.")
                elif durationMinutes > 60:
                    print("Minute duration cannot exceed 60.")
                else: 
                    validFlag = True
            except ValueError:
                print("Invalid duration!")
                
    validFlag = False
    while not validFlag:
        durationSeconds = inputE("Composition second duration: ")
        if not durationSeconds:
            print("Defaulting to 0.")
            durationSeconds = 0
            validFlag = True
        else:
            try:
                durationSeconds = int(durationSeconds)
                if durationSeconds < 0:
                    print("Duration cannot be negative.")
                elif durationSeconds > 60:
                    print("Second duration cannot exceed 60.")
                else: 
                    validFlag = True
            except ValueError:
                print("Invalid duration!")
                
    validFlag = False
    while not validFlag:
        durationFrames = inputE("Composition frame duration: ")
        if not durationFrames:
            print("Defaulting to 0.")
            durationFrames = 0
            validFlag = True
        else:
            try:
                durationFrames = int(durationFrames)
                if durationFrames < 0:
                    print("Duration cannot be negative.")
                elif durationFrames > framerate:
                    print("Frame duration cannot exceed framerate.")
                else:
                    validFlag = True
            except ValueError:
                print("Invalid duration!")
    
    print("The selected composition duration is " + "%02d" % (durationHours) + ":" + "%02d" % (durationMinutes) + ":" + "%02d" % (durationSeconds) + ":" + "%02d" % (durationFrames) + ".")
    
    validFlag = False
    while not validFlag:
        correct = inputE("Is this correct? (y/n): ")
        
        if correct == "y" or correct == "Y" or correct == "n" or correct == "N":
            validFlag = True
        else:
            print("Invalid answer!")
            
    if correct == "y" or correct == "Y":
        durationFlag = True

validFlag = False
while not validFlag:
    segmentSize = inputE("Max duration of segments in minutes: ")
    if not segmentSize:
        print("Defaulting to 3 minutes.")
        segmentSize = 3.0
        validFlag = True
    else:
        try:
            segmentSize = float(segmentSize)
            validFlag = True
        except ValueError:
            print("Invalid segment size!")
        
validFlag = False
while not validFlag:
    reviewToggle = inputE("Pause before final concatenation to allow for review? (y/n): ")
    if not reviewToggle:
        print("Defaulting to enabled.")
        reviewToggle = True
        validFlag = True
    elif reviewToggle == "y" or reviewToggle == "Y":
        reviewToggle = True
        validFlag = True
    elif reviewToggle == "n" or reviewToggle == "N":
        reviewToggle = False
        validFlag = True
    else:
        print("Invalid answer!")
        
validFlag = False
while not validFlag:
    phase = inputE("Would you like to skip to the review/re-rendering phase? (y/n): ")
    if not phase:
        print("Defaulting to no.")
        phase = False
        validFlag = True
    elif phase == "y" or phase == "Y":
        phase = True
        validFlag = True
    elif phase == "n" or phase == "N":
        phase = False
        validFlag = True
    else:
        print("Invalid answer!")

firstTime = True

frames = math.ceil((float(durationMinutes) * 60.0 * framerate) + (float(durationSeconds) * framerate) + float(durationFrames))
segmentSize = 0.25
framerate = 15.0
segmentSizeFrames = math.ceil(segmentSize * 60.0 * framerate)
numSegments = math.ceil(frames / segmentSizeFrames)
        
def configCreate():
    f = open(path + 'bsConfig.txt', 'w+')
    f.write("# Substitution tokens:\n" 
                + "# @n: The fragment's file name\n" 
                + "# @f: Framerate\n" 
                + "#\n" 
                + "Main re-encoding parameters:\n" 
                + "-i\n" 
                + "@n.avi\n" 
                + "-c:v\n" 
                + "libx264\n" 
                + "-crf\n" 
                + "18\n" 
                + "-r\n" 
                + "@f\n" 
                + "-y\n" 
                + "@n.mp4\n" 
                + "#\n" 
                + "Audio parameters:\n" 
                + "-c:a\n" 
                + "ac3\n" 
                + "-b:a\n" 
                + "128k\n")
    f.close()
    return
        
def renderCommand(audio, outputFile):
    if not os.path.exists(path + "bsConfig.txt"):
        configCreate()
    f = open(path + 'bsConfig.txt', 'r+')
    
    command = ["ffmpeg"]
    
    for l in f:
        if not l.startswith("#"):
            if not audio and l.startswith("Audio parameters:"):
                break
            elif not l.startswith("Main re-encoding parameters:"):
                command.append(l.replace("@n", path + outputFile).replace("@f", str(rFramerate)).replace("\n", ""))
            
    print(command)
    return command

def render(i, s, e, fLModify):
    print("")
    print("****************************************")
    print("Now rendering fragment " + str(i))
    print("****************************************")
    print("")
    time.sleep(5)
    
    startTime = time.time()
    
    if project:
        outputFile = project + '_' + composition + "_fragment" + "_" + str(i)
        subprocess.call(['aerender', '-project', path + str(project) + ".aep", '-comp', composition, '-s', str(s), '-e', str(e), '-output', path + outputFile + '.avi'])
    else:
        outputFile = composition + "_fragment" + str(i)
        subprocess.call(['aerender', '-comp', composition, '-s', str(s), '-e', str(e), '-output', path + outputFile + '.avi'])
    
    print("")
    print("****************************************")
    print("Re-encoding fragment " + str(i))
    print("****************************************")
    print("")
    time.sleep(5)

    if audio:
        #os.system('ffmpeg' + " " + '-i' + " " + '"' + path + outputFile + '.avi' + '"' + " " + '-c:v' + " " + 'libx264' + " " + '-crf' + " " + '18' + " " + '-r' + " " + str(framerate) + " " + '-c:a' + " " + 'ac3' + " " + '-b:a' + " " + '128k' + " -y " + '"' + path + outputFile + '.mp4' + '"')
        subprocess.call(renderCommand(True, outputFile))
    else:
        #os.system('ffmpeg' + ' ' + '-i' + ' ' + '"' + path + outputFile + '.avi' + '"' + ' ' + '-c:v' + ' ' + 'libx264' + ' ' + '-crf' + ' ' + '18' + ' ' + '-r' + ' ' + str(framerate) + ' ' + '-an' + ' -y ' + '"' + path + outputFile + '.mp4' + '"')
        subprocess.call(renderCommand(False, outputFile))

    print("")
    print("****************************************")
    print("Done processing fragment " + str(i))
    print("Total fragment processing time: " + renderTime(startTime))
    print("****************************************")
    print("")
    
    print("Deleting the uncompressed video file...")
    os.remove(path + outputFile + '.avi')
    print("Done!")
    #subprocess.call(['del', '"' + path + outputFile + '.avi' + '"'])
    
    if fLModify:
        print("Adding fragment entry to fragmentList.txt...")
        global firstTime
        if not os.path.exists(path + 'fragmentList.txt'):
            open(path + 'fragmentList.txt', 'w+').close()
        elif firstTime:
            print("Existing fragmentList.txt detected. Backing it up to fragmentList.bak...")
            shutil.copyfile(path + 'fragmentList.txt', path + 'fragmentList.bak')
            os.remove(path + 'fragmentList.txt')
            open(path + 'fragmentList.txt', 'w+').close()
            print("Done!")
            firstTime = False
        
        f = open(path + 'fragmentList.txt', 'r+')
        f.read(-1)
        
        if i == numSegments - 1: 
            f.write("file '" + path + outputFile + ".mp4'")
        else:
            f.write("file '" + path + outputFile + ".mp4'\n")
        
        f.flush()
        f.close()
        
        print("Done!")

    return

def renderTime(startTime):
    rend = round(time.time() - startTime, 4)
    rendDays = math.trunc(rend / 86400)
    rend -= rendDays * 86400
    rendHours = math.trunc(rend / 3600)
    rend -= rendHours * 3600
    rendMinutes = math.trunc(rend / 60)
    rend -= rendMinutes * 60
    rendSeconds = rend
    
    rendString = ""
    if (rendDays > 0):
        rendString += str(rendDays) + " Days"
    if (rendHours > 0):
        rendString += str(rendHours) + " Hours" 
    if (rendMinutes > 0):
        rendString += str(rendMinutes) + " Minutes"
    if (rendSeconds > 0):
        rendString += str(rendSeconds) + " Seconds"
        
    return rendString

def renderLoop():
    startTime = time.time()
    
    start = 0
    end = segmentSizeFrames - 1

    i = 0
    while i < numSegments:
        render(i, start, end, True)
        i += 1
        start = i * segmentSizeFrames
        end = ((i + 1) * segmentSizeFrames) - 1
        if end > frames:
            end = frames
    
    print("")
    print("Total render time: " + renderTime(startTime) + ".")
    
    return

def review():
    if reviewToggle:
        print("")
        print("Please review the fragments at this time.")
        
        while True:
            try:
                rr = inputE("What fragment(s) would you like to re-render (separate with spaces)? ")
                
                if not rr:
                    break
                else:
                    rr = rr.split(" ")
                    i = 0
                    while i < len(rr):
                        rr[i] = int(rr[i])
                        if rr[i] < 0 or rr[i] >= numSegments:
                            raise InvalidInputError
                        i+=1
                    i = 0
                    while i < len(rr):
                        start = rr[i] * segmentSizeFrames
                        end = ((rr[i] + 1) * segmentSizeFrames) - 1
                        render(rr[i], start, end, False)
                        i+=1
            except ValueError:
                print("Invalid entry. Please enter only integer values.")
            except InvalidInputError:
                print(str(i) + " is not a valid fragment number. Fragments must be within the range 0 -" + str(numSegments - 1) + ".")

    print("")
    print("****************************************")
    print("Combining fragments...")
    print("****************************************")
    print("")
    
    startTime = time.time()
    
    if project:
        subprocess.call(['ffmpeg', '-f', 'concat', '-i', path + 'fragmentList.txt', '-c', 'copy', '-y', path + project + '_' + composition + '.mp4'])
    else:
        subprocess.call(['ffmpeg', '-f', 'concat', '-i', path + 'fragmentList.txt', '-c', 'copy', '-y', path + '_' + composition + '.mp4'])
    
    print("")
    print("****************************************")
    print("Done combining fragments.")
    print("Total concatenation time: " + renderTime(startTime))
    print("****************************************")
    print("")
    
    validFlag = False
    while not validFlag:
        delF = inputE("Delete fragmentList.txt? Only do this if this is the final production version. (y/n): ")
        if not delF:
            print("Not deleting fragmentList.txt by default.")
            delF = False
            validFlag = True
        elif delF == "y" or delF == "Y":
            delF = True
            validFlag = True
        elif delF == "n" or delF == "N":
            delF = False
            validFlag = True
        else:
            print("Invalid answer!")
    
    if delF:
        print("Deleting fragmentList.txt...")
        os.remove(path + 'fragmentList.txt')
        print("Done!")
        
    if os.path.exists(path + "fragmentList.bak"):
        validFlag = False
        while not validFlag:
            delF = inputE("Delete fragmentList.bak? Only do this if this is the final production version. (y/n): ")
            if not delF:
                print("Not deleting fragmentList.bak by default.")
                delF = False
                validFlag = True
            elif delF == "y" or delF == "Y":
                delF = True
                validFlag = True
            elif delF == "n" or delF == "N":
                delF = False
                validFlag = True
            else:
                print("Invalid answer!")
        
        if delF:
            print("Deleting fragmentList.bak...")
            os.remove(path + 'fragmentList.bak')
            print("Done!")
    
    validFlag = False
    while not validFlag:
        delF = inputE("Delete video fragments? Only do this if this is the final production version. (y/n): ")
        if not delF:
            print("Not deleting fragments by default.")
            delF = False
            validFlag = True
        elif delF == "y" or delF == "Y":
            delF = True
            validFlag = True
        elif delF == "n" or delF == "N":
            delF = False
            validFlag = True
        else:
            print("Invalid answer!")
    
    if delF:
        print("Deleting fragments...")
        i = 0
        while i < numSegments:
            if project:
                outputFile = project + '_' + composition + "_fragment" + "_" + str(i) + '.mp4'
            else:
                outputFile = composition + "_fragment" + str(i) + '.mp4'
            print("Deleting fragment " + str(i) + "...")
            os.remove(path + outputFile)
            print("Done!")
            i += 1
    
    return
    
if phase:
    review()
else:
    renderLoop()
    review()