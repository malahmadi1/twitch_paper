import random

import pandas as pd
from dateutil import parser
sys_random = random.SystemRandom()

def select_sample_numbers():
    pass

def check_if_all_passed(list1, list2):
    result = all(elem in list1 for elem in list2)
    if result:
        return True
    else:
        return False

#TODO: refactoring
def sample_msgs_users(messages, max_per_channel = 200):
    all_indices = []
    #1 1271180475, 1294656573
    for key, item in messages.groupby('VidID'):
        if not key == 1271180475:
            continue
        selected_rows = []
        print(key)
        #users_count = item.pivot_table(columns=['UserName'], aggfunc='size')
        item['Frequency'] = item.groupby('UserName')['UserName'].transform('count')
        item.sort_values('Frequency', inplace=True, ascending=False)
        group_username = item.groupby('UserName', sort=False)
        try:
            while not len(selected_rows) == max_per_channel:
                for key, item in group_username:
                    if len(selected_rows) == max_per_channel:
                        group_username=""
                        break
                    list_index = sorted(item['#'].tolist())
                    random_index = random.choice(list_index) #select random message per user
                    if check_if_all_passed(selected_rows,list_index):
                        break
                    while not random_index in selected_rows:#select only one message per user, then repeat the same process
                        selected_rows.append(random_index)
                        break
            all_indices.extend(selected_rows)
        except Exception as e:
            print(e)
        #break to test only the first video

    messages = messages.iloc[all_indices]    # return only those rows, unified sampling (choose the first
    messages['Frequency'] = messages.groupby('UserName')['UserName'].transform('count')
    messages.sort_values('Frequency', inplace=True, ascending=False)
    messages = messages.sort_values(by=['VidID'])
    return messages


def drop_unnamed_column(messages):
    return messages.loc[:, ~messages.columns.str.contains('^Unnamed')]

def add_index_column(messages):
    messages.insert(0, "#", range(0, len(messages)))
    return messages

def change_timestamp_format(messages):
    #TODO: maybe add them in the column after ChatTimestamp
    messages['sent_hour'] = messages['ChatTimestamp'].map(lambda ChatTimestamp: parser.parse(ChatTimestamp).hour)
    messages['sent_minute'] = messages['ChatTimestamp'].map(lambda ChatTimestamp: parser.parse(ChatTimestamp).minute)
    messages['sent_second'] = messages['ChatTimestamp'].map(lambda ChatTimestamp: parser.parse(ChatTimestamp).second)
    return messages

def preprocess_texts(messages):
    #TODO: talk to ahmad, what to filter out?
    pass

if __name__ == '__main__':
    #TODO: 1. collect data (videos, audios, transcription, and text messages), DONE!.
    chat_messages = pd.read_csv("input_data/chats_data_round2_newVideos.csv")
    chat_messages = drop_unnamed_column(chat_messages)
    chat_messages = add_index_column(chat_messages)
    chat_messages = change_timestamp_format(chat_messages)

    #TODO: 2.talk to ahmad what to preprocess/filter_out, non-english?
    #chat_messages = preprocess_texts(chat_messages)

    #TODO: 3. sample messages (e.g., per video, per user, per timeframe?)
    sampled_msgs = sample_msgs_users(messages=chat_messages, max_per_channel = 200)
    sampled_msgs.to_csv("sampled_chat_messages_2ndVIDEOS_2k.csv",index=False)
    print()
    #TODO: 3. manually label the data after getting the sample (categories?)

    #TODO: 4. perform qualitative study, similar to the one esteban did (e.g., based on the categories identified above)

    #TODO: 5. perform auto classification (e.g., bert?)
