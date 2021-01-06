import threading


def multiple_likes():
    import datetime
    now = datetime.datetime.now()
    print (f"Sending data at {now.hour}:{now.minute}:{now.second}")

def race_condition():
    threading.Thread(target = multiple_likes).start()
    threading.Thread(target = multiple_likes).start()
    threading.Thread(target = multiple_likes).start()
