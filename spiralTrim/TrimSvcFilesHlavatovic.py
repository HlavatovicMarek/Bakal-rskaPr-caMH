
import os
import pandas as pd
import json
import datetime
from datetime import datetime, timezone


db_path = 'C:\BDALab\spiralTrim'

#get all directories in the db_path ID 1, ID 2...
dirs = os.listdir(db_path)

#iterate over them
for dir in dirs:
    iDir = os.path.join(db_path, dir)
    if os.path.isdir(iDir):

        #TSK1.svc filepath
        svc_file_path = os.path.join(iDir, "TSK1.svc") 
        
        #Open the timestamps json file, load it as a dictionary
        timestamps_path = os.path.join(iDir, 'fileTimeStampTasks.json')
        timestamps = {}

        #check file exists
        if not os.path.isfile(timestamps_path):
            continue
        with open(timestamps_path) as f:
            timestamps = json.load(f)

        #the spiral is exercise number three, get the time it starts and ends
        spiral_exercise_start_time = datetime.strptime(timestamps.get("three"), "%H:%M:%S%f").replace(tzinfo=timezone.utc).replace(year=1970)
        spiral_exercise_end_time = datetime.strptime(timestamps.get("four"), "%H:%M:%S%f").replace(tzinfo=timezone.utc).replace(year=1970)

        #convert the UTC timestamps to miliseconds since epoch (same as the timestamp in .svc)
        epoch = datetime.fromtimestamp(0, tz= timezone.utc)
        spiral_exercise_timestamp = (spiral_exercise_start_time - epoch).total_seconds() * 1000
        spiral_exercise_end_timestamp = (spiral_exercise_end_time - epoch).total_seconds() * 1000

        #open the handwriting .svc file
        handwriting_df = pd.read_table(svc_file_path, skiprows=1, delimiter=' ', names=['X', 'Y', 'timestamp', 'on_surface', 'irelevant1', 'irelevant2', 'irelevant3'])

        #filter the lines by timestamp to only get the spiral exercise
        spiral_exercise = handwriting_df[handwriting_df['timestamp']>spiral_exercise_timestamp]
        spiral_exercise = spiral_exercise[spiral_exercise['timestamp']<spiral_exercise_end_timestamp]

        #save to a new file
        svc_file_path = os.path.join(iDir, "spiral.svc")
        spiral_exercise.to_csv(svc_file_path, ' ', index=False, header=False)

        


