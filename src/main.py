import time
import wget

from functions import *

objects = load_objects('objects.json')
subjects = objects['subjects']
urls = objects['urls']
conn_error = objects['conn_error']
cookies = objects['cookies']
directory = objects['directory']

choice = input('Choose between PP1, PP2 or SO2 (type PP1, PP2 or SO2): ')
if choice not in subjects:
    print('Incorrect input')
    exit()

subject_id = subjects[choice]

print('----------START----------')

try:
    units = fetch(cookies, urls['units_url'], subject_id)

    for i in range(len(units)):
        print('------Unit%d------' % (i + 1))
        time.sleep(10)

        unit = units[i]
        unit_number = unit['Number']

        tasks = fetch(cookies, urls['tasks_url'], subject_id, '&topicid=', str(unit['TopicID']))

        for j in range(len(tasks)):
            save_path = directory
            task = tasks[j]
            task_number = task['TaskNumber']
            machine_status = task['MachineStatus']

            if machine_status is not None:
                taskID = task['TaskID']
                replies = fetch(cookies, urls['reply_url'], subject_id, '&taskid=', str(taskID))

                if (replies[0])['MachineMessage'] == 'Ok' or (replies[0])['MachineMessage'] == 'Ok.':
                    download_url = (replies[0])['MachineReport']
                    download_url = download_url.replace('index.html', 'source.zip', 1)

                    save_path = concat_path(save_path, unit_number, task_number)
                    output_mess = save_path[-1:-10:-1]

                    print('\033[92m' + 'Success ' + output_mess[::-1] + '\033[0m')

                    time.sleep(1)
                    wget.download(download_url, save_path)

except requests.RequestException:
    print('\033[91m' + '\033[1m' + conn_error['title'] + '\033[0m', conn_error['message'], sep='\n')

print('----------END----------')
