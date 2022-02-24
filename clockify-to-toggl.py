import csv
from datetime import datetime
from toggl.TogglPy import Toggl
from toggl.TogglPy import Endpoints

API_TOKEN = ''

def createTimeEntry(toggl, duration, description=None, projectid=None, projectname=None,
                        taskid=None, clientname=None, year=None, month=None, day=None, hour=None, minute=None, hourdiff=-2):
        data = {
            "time_entry": {}
        }
        billable=False
        if not projectid:
            if projectname and clientname:
                projectid = (toggl.getClientProject(clientname, projectname))['data']['id']
            elif projectname:
                project = (toggl.searchClientProject(projectname))
                projectid = project['id']
                billable = project['billable']
            else:
                print('Too many missing parameters for query')
                exit(1)

        if description:
            data['time_entry']['description'] = description

        if taskid:
            data['time_entry']['tid'] = taskid

        year = datetime.now().year if not year else year
        month = datetime.now().month if not month else month
        day = datetime.now().day if not day else day
        hour = datetime.now().hour if not hour else hour

        timestruct = datetime(year, month, day, hour + hourdiff, minute).isoformat() + '.000Z'
        data['time_entry']['start'] = timestruct
        data['time_entry']['duration'] = duration
        data['time_entry']['pid'] = projectid
        data['time_entry']['created_with'] = 'NAME'
        data['time_entry']['billable'] = billable

        response = toggl.postRequest(Endpoints.TIME_ENTRIES, parameters=data)
        return toggl.decodeJSON(response)

def main():
    toggl = Toggl()
    toggl.setAPIKey(API_TOKEN) 

    with open('ClockifyCSV.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Columns: {", ".join(row)}')
                line_count += 1
            startDate = row["Start Date"].split("-")
            startTime = row["Start Time"].split(":")
            durationArray = row["Duration (h)"].split(":")
            duration = int(durationArray[0])*3600 + int(durationArray[1])*  3600 // 60 + int(durationArray[2]) % 60
            createTimeEntry(toggl=toggl,description=row["Description"],  duration=duration, projectname=row["Project"], year=int(startDate[0]), month=int(startDate[1]), day=int(startDate[2]), hour=int(startTime[0]), minute=int(startTime[1]), hourdiff=3)
            print(f'\t{row["Project"]} - {row["Description"]} - {row["Start Date"]} - {row["Start Time"]}.')
            line_count += 1
        print(f'Processed {line_count} lines.')

if __name__ == '__main__':
    main()