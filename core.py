bad_words = [
    'faggot',
    'bitch',
    'pussy'
]

def process_message(message):
    if not message:
        return
    message = message.lower()
    for bad_word in bad_words:
        if bad_word in message:
            return f"You've said the {bad_word[0]}-word. You are on CD."
    