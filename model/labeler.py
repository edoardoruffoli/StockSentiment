import json
import joblib
import numpy as np


def ask_label(text):
    print("--------------- Text --------------- \n" + text + "\n")
    clf = joblib.load('../model/sentiment_classifier.pkl')

    my_list = [text]
    arr = np.asarray(my_list)
    arr.reshape(-1, 1)
    # Use model to make predictions
    y_pred = clf.predict(arr)
    print("Model predicts: ", y_pred)

    label = input("Select label: (pos, neg, neu, stop)\n")
    if label == "pos":
        label = "positive"
    elif label == "neg":
        label = "negative"
    elif label == "neu":
        label = "neutral"
    elif label != "stop":
        ask_label(text)
    return label


if __name__ == "__main__":
    while True:
        command = input("Select command: (first time? type help)\n >")
        if command == "help":
            print("Possible function:\n"
                  "\t- tweets\n"
                  "\t- news\n"
                  "\t- quit\n")
        elif command == "tweets":
            with open("../data/train/tweets_with_label.json") as feedsjson:
                feeds = json.load(feedsjson)
                skip = len(feeds)
                with open("../data/tweets/tweets_AMZN.json") as file:
                    for line in file:
                        if skip > 0:
                            skip = skip - 1
                            continue
                        data = json.loads(line)
                        label = ask_label(data["Text"])
                        if label == "stop":
                            break
                        row = {
                            "datetime": data['Datetime'],
                            "username": data['Account_Name'],
                            "text": data['Text'],
                            "target": label,
                            "number_follower": data['Number_Follower'],
                            "number_retweets": data['Number_Retweets'],
                            "number_likes": data['Number_Likes'],
                            "number_comments": data['Number_Comments']
                        }
                        feeds.append(row)
            with open("../data/train/tweets_with_label.json", mode='w') as f:
                f.write(json.dumps(feeds, indent=2))
        elif command == "news":
            with open("../data/train/news_with_label.json") as feedsjson:
                feeds = json.load(feedsjson)
                skip = len(feeds)
                with open("../data/news/news_AMZN_2020-12-06_2021-12-04.json") as file:
                    for line in file:
                        if skip > 0:
                            skip = skip -1
                            continue
                        data = json.loads(line)
                        text = data["headline"] + data["summary"]
                        label = ask_label(text)
                        if label == "stop":
                            break
                        row = {"text": text, "target": label}
                        feeds.append(row)
            with open("../data/train/news_with_label.json", mode='w') as f:
                f.write(json.dumps(feeds, indent=2))
        elif command == "quit":
            break
        else:
            print("Not valid command.\n")