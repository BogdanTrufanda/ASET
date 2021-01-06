import jwt


def decode_jwt(par: str):
    try:
        decoded = jwt.decode(par, options={"verify_signature": False})
        print ("-" * 30)
        print (par + "\n")
        for x,y in decoded.items():
            print (x," -> ",y)
        print ("-" * 30)
    except:
        print ("JWT not well formated!")