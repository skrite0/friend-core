from datetime import datetime, timedelta

def read_file_to_list(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    # Strip newline characters from each line
    lines = [line.strip() for line in lines]
    return lines

bad_words = read_file_to_list('bad_words.txt')

cd_users = {}
message_log = {}

def process_message(message, user):
    if not message:
        return
    message_lower = message.lower()
    if user in message_log:
        message_log[user].append(message)
    else:
        message_log[user] = []
        message_log[user].append(message)
    for bad_word in bad_words:
        if bad_word in message_lower:
            user_exist = check_user(user)
            readable_date = datetime.strptime(str(cd_users[user]), '%Y-%m-%d %H:%M:%S.%f')
            readable_date = readable_date.strftime('%B %d, %Y %I:%M%p')
            if not user_exist:
                return f"You've said the {bad_word[0]}-word. You are on CD. Your CD will end {readable_date}"
            else:
                return f"**Repeat Offense** You've said the {bad_word[0]}-word. Your CD will be extended. Your CD will end {readable_date}"
    
def check_user(user):
    if user not in cd_users:
        cd_users[user] = datetime.now() + timedelta(hours=1)
        return None
    cd_users[user] = cd_users[user] + timedelta(hours=1)
    return True

def remove_cd(user):
    if user not in cd_users:
        return
    if datime.now() > cd_users[user]:
        del cd_users[user]

def get_user(user):
    return user in cd_users

def get_message_log(user):
    if user not in message_log:
        return 'You are not on CD.'
    response = ''
    for messages in message_log[user]:
        response += messages + '\n'
    return response