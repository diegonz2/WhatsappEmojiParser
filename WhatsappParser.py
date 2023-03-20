import pandas as pd
import re
from collections import Counter
import plotly.graph_objs as go

# Regular expression for timestamps in WhatsApp chat
timestamp_regex = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s-\s'

# Regular expression for emojis
emoji_regex = r'[\U0001F600-\U0001F64F\U0001F900-\U0001F9FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]'

def extract_messages(chat_file_path):
    """Extracts messages from a WhatsApp chat file."""
    with open(chat_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        messages = []
        current_message = ''
        for line in lines:
            if re.match(timestamp_regex, line):
                if current_message:
                    messages.append(current_message)
                    current_message = ''
                current_message += line
            else:
                current_message += ' ' + line.strip()
        if current_message:
            messages.append(current_message)
        return messages

# Path to the WhatsApp chat file
chat_file_path = 'Argentina2018.txt'

# Extract the messages from the chat file
messages = extract_messages(chat_file_path)

# Create a pandas DataFrame from the messages
df = pd.DataFrame({'message': messages})

# Count the frequency of each emoji in the chat
emoji_counts = Counter(re.findall(emoji_regex, ' '.join(df['message'])))

# Get the top 15 most frequent emojis in the chat
top_emojis = dict(emoji_counts.most_common(15))
print(top_emojis)

# Create a bar graph of the top emojis using plotly
fig = go.Figure([go.Bar(x=list(top_emojis.keys()), y=list(top_emojis.values()))])
fig.update_layout(title_text=f'Top 15 most frequent emojis in '+ str(chat_file_path)[:-4], xaxis_title='Emoji', yaxis_title='Frequency')

# Save the bar graph as an HTML file
fig.write_html("top_emojis_"+str(chat_file_path)[:-4]+".html")