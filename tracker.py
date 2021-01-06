



def track_me(nick: str):
    import sys
    sys.path.insert(1, 'sherlock/sherlock')
    import sherlock
    sys.argv.append(nick)
    sherlock.main()
    print ("Tracking social media finished")
    