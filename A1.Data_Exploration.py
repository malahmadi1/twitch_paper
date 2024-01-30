from collections import Counter

import pandas as pd
from scipy.stats import ttest_ind
from spellchecker import SpellChecker
import seaborn as sns
import matplotlib.pyplot as plt
import statistics
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')


def cloud_words(file_name):
    data = pd.read_csv(file_name)
    # Split data by category
    relevance_messages = data[data['label'] == 'Relevant to Streamer']
    irrelevance_messages = data[data['label'] == 'Irrelevant to Streamer']
    messages_rev = relevance_messages['message'].tolist()
    messages_rev = [str(msg) for msg in messages_rev if not isinstance(msg, float)]  # convert float to string
    messages_irr = irrelevance_messages['message'].tolist()
    messages_irr = [str(msg) for msg in messages_irr if not isinstance(msg, float)]
    #df_results = df.loc[df['label'] == cat, 'message'].tolist()
    # Generate word clouds for each category
    relevance_wordcloud = WordCloud(width=400, height=400,
                                    background_color='white',
                                    stopwords=None,
                                    min_font_size=5).generate(' '.join(messages_rev))

    # messages_rev_list =  [word for sentence in messages_rev for word in sentence.split()]
    # filtered_words = [word for word in messages_rev_list if word.lower() not in stopwords.words('english')]
    #
    # word_count = Counter([word for sentence in filtered_words for word in sentence.split()])
    word_count = Counter(relevance_wordcloud.words_)

    print("most common in relevance")
    for word, count in word_count.most_common(10):
        print(word, count)


    irrelevance_wordcloud = WordCloud(width=400, height=400,
                                      background_color='white',
                                      stopwords=None,
                                      min_font_size=5).generate(' '.join(messages_irr))

    word_count = Counter(irrelevance_wordcloud.words_)
    print("most common in irrelevance")
    for word, count in word_count.most_common(10):
        print(word, count)
    # Plot the word clouds
    plt.figure(figsize=(4, 4), facecolor=None)
    plt.imshow(relevance_wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.figure(figsize=(4, 4), facecolor=None)
    plt.imshow(irrelevance_wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.show()


def compute_spell_errors(file_name):
    # Read CSV file
    df = pd.read_csv(file_name)
    # initialize spellchecker
    spell = SpellChecker()

    # compute spelling errors for each message
    df['spelling_errors'] = df['message'].apply(lambda x: len(spell.unknown(x.split())))

    # compute stats for each label
    stats = df.groupby('label')['spelling_errors'].describe()

    # print results
    print(stats)

    # generate boxplot for each label
    for label in df['label'].unique():
        sns.boxplot(x='label', y='spelling_errors', data=df[df['label'] == label])
        plt.title(f'Spelling errors for {label} messages')
        plt.show()

def simple_compute_spell_errors(file_name):
    spell = SpellChecker()
    # Read CSV file
    df = pd.read_csv(file_name)
    list_of_cat = [ "Relevant to Streamer", "Irrelevant to Streamer"]
    data_rows = []
    #MIN, MAX, Median, Mean, are # of erros per message
    columns_errors = ["Category", "Total # of words","Min # of words", "Max # of words", "Median # of words", "Mean # of words", "Total # of Spelling Errors", "Average # of Spelling Errors","Min # of Errors", "Max # of Errors", "Median # of Errors", "Mean # of errors"]

    for cat in list_of_cat:
        df_results = df.loc[df['label'] == cat, 'message'].tolist()
        label_counts = df['label'].value_counts()
        print(label_counts)
        error_counts = []
        total_words = []
        duplicate_words = []
        punc_counts = []
        punctuations = string.punctuation

        for message in df_results:
            message_list = str(message).split()
            duplicate_words.append(len(message_list) - len(set(message_list)))
            punc_counts.append(sum(str(message).count(char) for char in punctuations))

            #remove mention and hashtag
            message_list = [x for x in message_list if not x.startswith("#") and not x.startswith("@")]
            #remove punctation
            message_list = [s.translate(str.maketrans("", "", string.punctuation)) for s in message_list]
            #remove empty strings
            message_list = [s for s in message_list if s.strip()]

            total_words.append(len(message_list))

            count_current = 0
            for msg in message_list:

                count_current  = count_current + len(spell.unknown([msg]))

            # print(message_list, count_current)
            error_counts.append(count_current)

        print(f"Total # of words in {cat} category: {sum(total_words)}")
        print("Total # of spelling errors in {0} category: {1}".format(cat, sum(error_counts)))
        print("Average # of words in {0} category: {1}".format(cat, statistics.mean(total_words)))
        print("Average # of spelling errors in all words in {0} category: {1}".format(cat,  sum(error_counts)/sum(total_words)))

        print("Min. # of spelling errors in a message that belongs to {0} category: {1}".format(cat, min(error_counts)))
        print("Max. # of spelling errors in a message that belongs to {0} category: {1}".format(cat, max(error_counts)))
        print("Median # of spelling errors in a message that belongs to {0} category: {1}".format(cat, statistics.median(error_counts)))
        print("Mean # of spelling errors in a message that belongs to {0} category: {1}".format(cat, statistics.mean(error_counts)))

        print("="*50)
        print("Min. # of duplicate words in a message that belongs to {0} category: {1}".format(cat, min(duplicate_words)))
        print("Max. # of duplicate words in a message that belongs to {0} category: {1}".format(cat, max(duplicate_words)))
        print("Mean # of duplicate words in a message that belongs to {0} category: {1}".format(cat, statistics.mean(duplicate_words)))
        print("Median # of duplicate words in a message that belongs to {0} category: {1}".format(cat, statistics.median(duplicate_words)))

        print("Average # of duplicate words in all messages that belongs to {0} category: {1}".format(cat, sum(duplicate_words)/sum(total_words)))
        print("=" * 50)

        print("="*50)
        print("Min. # of punctuation in a message that belongs to {0} category: {1}".format(cat, min(punc_counts)))
        print("Max. # of punctuation in a message that belongs to {0} category: {1}".format(cat, max(punc_counts)))
        print("Mean # of punctuation in a message that belongs to {0} category: {1}".format(cat, statistics.mean(punc_counts)))
        print("Median # of punctuation in a message that belongs to {0} category: {1}".format(cat, statistics.median(punc_counts)))

        print("Average # of punctuation in all messages that belongs to {0} category: {1}".format(cat, sum(punc_counts)/sum(total_words)))
        print("Total # of punctuation in all messages that belongs to {0} category: {1}".format(cat, sum(punc_counts)))

        print("=" * 50)




        data_rows.append((cat, sum(total_words), min(total_words), max(total_words),  statistics.median(total_words), statistics.mean(total_words), sum(error_counts),  sum(error_counts)/sum(total_words),  min(error_counts), max(error_counts), statistics.median(error_counts), statistics.mean(error_counts)))

    dev_df = pd.DataFrame(data_rows, columns = columns_errors)
    dev_df.to_csv("stat_spelling_errors.csv", index = None)

    relevance_mean_errors = data_rows[0][11]
    irrelevance_mean_errors = data_rows[1][11]
    # Perform a t-test to determine if there is a significant difference in the means
    t_statistic, p_value = ttest_ind(relevance_mean_errors, irrelevance_mean_errors)
    if p_value < 0.05:
        print("There is a significant difference in the mean number of spelling errors between the two categories.")
    else:
        print("There is no significant difference in the mean number of spelling errors between the two categories.")

    t_statistic, p_value = ttest_ind(relevance_mean_errors, irrelevance_mean_errors)
    if p_value < 0.05:
        print("There is a significant difference in the mean number of spelling errors between the two categories.")
    else:
        print(
            "There is no significant difference in the mean number of spelling errors between the two categories.")


if __name__ == '__main__':
    #simple_compute_spell_errors("twitch_messages.csv")
    cloud_words("twitch_messages.csv")
