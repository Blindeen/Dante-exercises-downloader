import requests

subjects = {
    'Dante1': '25',
    'Dante2': '27',
    'SO2': '29'
}

urls = {
    'units_url': 'https://dante.iis.p.lodz.pl/api/student/topicbrowser/getTopics?subjectid=',
    'tasks_url': 'https://dante.iis.p.lodz.pl/api/student/taskbrowser/getTasks?subjectid=',
    'reply_url': 'https://dante.iis.p.lodz.pl/api/student/reply/getReplyHistory?subjectid='
}


def fetch(*args):
    args_len = len(args)
    fetch_url = ''

    if args_len == 3:
        fetch_url = args[1] + args[2]
    else:
        for i in range(1, 5):
            fetch_url += args[i]

    rq = requests.get(fetch_url, cookies=args[0])
    response = rq.json()

    return response['Entries']


def concat_path(path, unit_number, task_number):
    if int(unit_number) < 10:
        path += '0' + unit_number + '.'
    else:
        path += unit_number + '.'

    if int(task_number) < 10:
        path += '0' + task_number
    else:
        path += task_number

    path += '.zip'

    return path
