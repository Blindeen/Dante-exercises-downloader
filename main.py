import time
import requests
import wget

from functions import fetch_units, fetch_tasks, subjects

choice = input('Choose between Dante1, Dante2 or SO2 (type Dante1, Dante2 or SO2): ')
if choice not in subjects:
    print('Incorrect input')
    exit()

subject_id = subjects[choice]

print('----------START----------')

try:
    cookies = {'hwsid': '', 'hwtoken': ''}
    save_path_src = ''

    units_url = 'https://dante.iis.p.lodz.pl/api/student/topicbrowser/getTopics?subjectid='
    units = fetch_units(cookies, units_url, subject_id)
    units = units['Entries']

    for i in range(len(units)):
        print('------Unit%d------' % (i+1))
        time.sleep(10)
        task_number = 1

        unit = units[i]
        unit_number = unit['Number']

        tasks_url = 'https://dante.iis.p.lodz.pl/api/student/taskbrowser/getTasks?subjectid='
        tasks = fetch_tasks(cookies, tasks_url, subject_id, str(unit['TopicID']))
        tasks = tasks['Entries']

        for j in range(len(tasks)):
            save_path = save_path_src
            task = tasks[j]
            machine_status = task['MachineStatus']

            if machine_status is not None:
                taskID = task['TaskID']
                req = requests.get('https://dante.iis.p.lodz.pl/api/student/reply/getReplyHistory?subjectid=' + subject_id + '&taskid=' + str(taskID), cookies=cookies)

                replies = req.json()
                replies = replies['Entries']

                if (replies[0])['MachineMessage'] == 'Ok' or (replies[0])['MachineMessage'] == 'Ok.':
                    download_url = (replies[0])['MachineReport']
                    download_url = download_url.replace('index.html', 'source.zip', 1)

                    if int(unit_number) < 10:
                        save_path += '0' + unit_number + '.'
                    else:
                        save_path += unit_number + '.'

                    if task_number < 10:
                        save_path += '0' + str(task_number)
                    else:
                        save_path += str(task_number)

                    save_path += '.zip'
                    output_mess = save_path[-1:-10:-1]

                    print('\033[92m' + 'Success ' + output_mess[::-1] + '\033[0m')

                    time.sleep(1)
                    response = wget.download(download_url, save_path)

            task_number += 1

except requests.RequestException:
    print('\033[91m' + '\033[1m' + 'CONNECTION ERROR' + '\033[0m')
    print('If it\'s later than 10PM on weekdays or 9PM on weekends, remember to turn on VPN or check if you have set hwsid and hwtoken')

print('----------END----------')
