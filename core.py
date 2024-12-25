from datetime import datetime, timedelta
import pytz


def read_file_to_list(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    # Strip newline characters from each line
    lines = [line.strip() for line in lines]
    return lines

bad_words = read_file_to_list('bad_words.txt')
ignore_words = read_file_to_list('ignore_words.txt')

est = pytz.timezone('US/Eastern')

cd_users = {}
message_log = {}

def set_response(code, response_message):
    return {
        'code': code,
        'message': response_message
    }

def process_message(message, user):

    code = 0
    content = 'None'

    if message == '!crime':
        code = 2
        content = get_message_log(user)

    elif message == '!info':
        code = 3
        content = get_info()

    elif message.startswith('!ult'):
        code = 4
        return

    cleaned_message = message.lower().replace(' ', '')

    ignore_characters = [ignore_word for ignore_word in ignore_words if ignore_word in cleaned_message]

    if ignore_characters:
        return

    # iterate through all bad_words    
    bw_characters = [bad_word[0] for bad_word in bad_words if bad_word in cleaned_message]

    if bw_characters:
        user_exist = get_user(user)
        if not user_exist:
            code = 5
        else:
            code = 1

        # log the time the user is on CD for
        log_user_cd_time(user, len(bw_characters))

        # get datetime and make it readable for user
        readable_date = cd_users[user].strftime('%B %d, %Y %I:%M %p %Z')

        # log the user messages that got them on CD
        log_user_messages(user, message, user_exist)
        
        # strip the bad word from offensive letters and spit back the response message based on if user is a repeat offender
        content = get_response_message(bw_characters, readable_date, user_exist)
    else:
        remove_cd(user)

    response = set_response(code, content)
    return response

    
    
def get_response_message(bw_characters, date, user_exist):

    formatted_string = ''

    # Format each element as "<letter>-word"
    if len(bw_characters) == 1:
        # Handle single element
        formatted_string = f"{bw_characters[0]}-word"
    elif len(bw_characters) == 2:
        # Handle exactly two elements
        formatted_string = f"{bw_characters[0]}-word and the {bw_characters[1]}-word"
    else:
        # Handle three or more elements
        formatted_string = ", ".join(f"{letter}-word" for letter in bw_characters[:-1])
        formatted_string += f", and the {bw_characters[-1]}-word"

    if not user_exist and len(bw_characters) == 1:
        return f"You've said the {formatted_string}. You are on CD. Your CD will end {date}"
    elif not user_exist and len(bw_characters) > 1:
        return f"You've used multiple abilities at once by saying the {formatted_string}. You are on a CD. Your CD will end {date}"
    elif user_exist and len(bw_characters) == 1:
        return f"**Repeat Offense** You've said the {formatted_string}. Your CD will be extended. Your CD will end {date}"
    elif user_exist and len(bw_characters) > 1:
        return f"**Repeat Offense** You've used multiple abilities at once by saying the {formatted_string}. Your CD will be extended. Your CD will end {date}"

def log_user_messages(user, message, user_exist):
    current_time = datetime.now(pytz.utc).astimezone(est)
    current_time = current_time.strftime('%B %d, %Y %I:%M %p %Z')

    if user_exist:
        message_log[user].append("[" + current_time + "] " + message)
        return
    message_log[user] = []
    message_log[user].append("[" + current_time + "] " + message)

def log_user_cd_time(user, char_len):
    if not get_user(user):
        current_time = datetime.now(pytz.utc)
        if char_len == 1:
            cd_users[user] = current_time.astimezone(est) + timedelta(minutes=30)
        else:
            cd_users[user] = current_time.astimezone(est) + timedelta(hours=1)
        return
    if char_len == 1:
        cd_users[user] = cd_users[user] + timedelta(minutes=30)
    else:
        cd_users[user] = cd_users[user] + timedelta(hours=1)

def remove_cd(user):
    if user not in cd_users:
        return
    current_time = datetime.now(pytz.utc)
    current_time = current_time.astimezone(est)
    if current_time > cd_users[user]:
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

def get_info():
    bad_words = get_bad_words()
    response = f'Hello, nice to meet you friend! I simply work by helping you remember to be kind. You can say a _bad word_ but you will be placed in a Cool Down (CD) state. If you are in CD the next time you try to saw a _bad word_ your CD state will be extended:\n* Standard one word CDs are 30 mins\n* More than one CDs in one message are 1 hour\nThe bad words are as follows:\n{bad_words}\nIf you want to bypass the bot you can use the `!ult` command.'
    return response

def get_bad_words():
    response = [bad_word + '\n' for bad_word in bad_words]
    response = ''.join(response)
    return '```' + response + '```'