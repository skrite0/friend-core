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
    if not message or not user:
        return

    # iterate through all bad_words    
    for bad_word in bad_words:
        if bad_word in message.lower():

            user_exist = get_user(user)

            # log the time the user is on CD for
            log_user_cd_time(user)

            # get datetime and make it readable for user
            readable_date = datetime.strptime(str(cd_users[user]), '%Y-%m-%d %H:%M:%S.%f')
            readable_date = readable_date.strftime('%B %d, %Y %I:%M%p')

            # log the user messages that got them on CD
            log_user_messages(user, message, readable_date, user_exist)
            
            # strip the bad word from offensive letters and spit back the response message based on if user is a repeat offender
            return get_response_message(bad_word[0], readable_date, user_exist)
    
def get_response_message(letter, date, user_exist):
    if not user_exist:
        return f"You've said the {letter}-word. You are on CD. Your CD will end {date}"
    
    return f"**Repeat Offense** You've said the {letter}-word. Your CD will be extended. Your CD will end {date}"

def log_user_messages(user, message, date, user_exist):
    if user_exist:
        message_log[user].append("[" + date + "] " + message)
        return
    message_log[user] = []
    message_log[user].append("[" + date + "] " + message)

def log_user_cd_time(user):
    if not get_user(user):
        cd_users[user] = datetime.now() + timedelta(minutes=30)
        return
    cd_users[user] = cd_users[user] + timedelta(minutes=30)

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