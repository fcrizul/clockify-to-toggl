import csv
from datetime import datetime, timedelta
from toggl.TogglPy import Toggl
from toggl.TogglPy import Endpoints
import sys
import time

def createTimeEntry(toggl, duration, description=None,
                    projectid=None, projectname=None, taskid=None, clientname=None, 
                    year=None, month=None, day=None, hour=None, minute=None, 
                    hourdiff=-3):
        data = {
            "time_entry": {}
        }
        billable=False
        if not projectid:
            if projectname and clientname:
                project = (toggl.getClientProject(clientname, projectname))['data']
                projectid = project['id']
                billable = project['billable']
            elif projectname:                
                project = toggl.searchClientProject(projectname)
                if project is not None:   
                    projectid = project['id']
                    billable = project['billable']
            else:
                print('Too many missing parameters for query')
                exit(1)

        time.sleep(1) # safe window
        if description:
            data['time_entry']['description'] = description

        if taskid:
            data['time_entry']['tid'] = taskid

        year = datetime.now().year if not year else year
        month = datetime.now().month if not month else month
        day = datetime.now().day if not day else day
        hour = datetime.now().hour if not hour else hour

        date = datetime(year, month, day, hour, minute)


        timestruct = (date + timedelta(hours=hourdiff)).isoformat() + '.000Z'
        data['time_entry']['start'] = timestruct
        data['time_entry']['duration'] = duration
        data['time_entry']['pid'] = projectid
        data['time_entry']['created_with'] = 'NAME'
        data['time_entry']['billable'] = billable

        response = toggl.postRequest(Endpoints.TIME_ENTRIES, parameters=data)
        time.sleep(1) # safe window
        return toggl.decodeJSON(response)

def main():
    if len(sys.argv) < 2:
        print("You must set argument!!!")
        sys.exit()
    toggl = Toggl()
    
    toggl.setAPIKey(sys.argv[1]) 

    with open(sys.argv[2], mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Columns: {", ".join(row)}')
                line_count += 1
            startDate = row["Start Date"].split("-")
            startTime = row["Start Time"].split(":")
            durationArray = row["Duration (h)"].split(":")
            duration = (int(durationArray[0]) * 3600) + (int(durationArray[1]) * 3600 // 60) + (int(durationArray[2]) % 60)
            print(createTimeEntry(toggl=toggl,description=row["Description"],  duration=duration, projectname=row["Project"], year=int(startDate[0]), month=int(startDate[1]), day=int(startDate[2]), hour=int(startTime[0]), minute=int(startTime[1]), hourdiff=3))
            print(f'\t{row["Project"]} - {row["Description"]} - {row["Start Date"]} - {row["Start Time"]}.')
            line_count += 1
        print(f'Processed {line_count} lines.')

if __name__ == '__main__':
    main()