import os
import re
import uuid

from datetime import datetime


def parse_convos(file, user, export_path, remove=None, include_user=False):
    """
    Function that removes your entries and anonymizes the conversation. Also,
    removes emoji and URLs which don't add much to the conversation.

    Parameters
    ----------
    file [str]:             Path to the text file containing the entire 
                            conversation history.
    username [str]:         Your user's full name as it appears in the 
                            conversation file.
    export_path [str]:      Path where you want to export the JSON Lines file.
    remove_user [str]:      Name of the user for whom you want to remove the
                            dialogue. Useful if you want to remove your entries 
                            and only leave your user's.
    include_user [bool]:    Whether you want to have the user's anonymized ID
                            in the prompt. 

    Returns
    -------
    Text file without your dialogue and anonymized user entries.
    """
    text = ""
    user_id = ""

    with open(file) as f:
        text = f.read()

        # Remove header
        header = r'1?\d{1}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s[AP]M\s-\sMessages\sand\scalls\sare\send-to-end\sencrypted.+'
        text = re.sub(header, '', text)

        # Remove emoji
        emoji = r'[^a-zA-Z0-9\s\*\(\)!\.,:-áéíúó\-\+\/\'ñ"]'
        text = re.sub(emoji, ' ', text)
        text = re.sub(r'\s{2,}', ' ', text)

        # Remove URLs
        text = re.sub(r'https?:\/\/.+', '', text)

        ## Remove newlines in a user's message.
        text = re.sub(r'\n', '', text)
        ## Flatten a user's conversation into a single line
        timestamp = r'(1?\d{1}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s[AP]M\s-\s)'
        text = re.sub(timestamp, r'\n\1', text)
        ## Remove your dialogues
        you = rf'1?\d{1}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s[AP]M\s-\s{remove}.+'
        text = re.sub(you, '', text)
        text = re.sub(r'\n{2,}', r'\n', text)

        # Anonymize user
        user_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, user))

        # Include user's name in prompt
        if add_user:
            text = re.sub(re.compile(user), user_id, text)
        else:
            text = re.sub(re.compile(user), "", text)

        # Transform date strings into ISO format
        date = r'1?\d{1}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s[AP]M'
        ugly_dates = list(set(re.findall(date, text)))

        for d in ugly_dates:
            nice_date = datetime.strptime(d, '%m/%d/%y, %I:%M %p').isoformat()
            text = re.sub(re.compile(d), nice_date, text)

        # Encapsulate into OpenAI's format for fine-tuning
        text = re.sub(r'(.+)\n', r'{"prompt": "\1\\n\\n###\\n\\n", "completion": " END"}\n', text)

    path = os.path.join(export_path, user_id + '.jsonl')
    with open(path, 'w') as f:
        f.write(text)
