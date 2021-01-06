import PySimpleGUI as sg


def create_osint_gui() -> (list, sg.PySimpleGUI.Window):
    sg.theme('DarkAmber')
    layout = [[sg.Text('Enter coordinates'), sg.InputText(size=(68, 10))],[sg.Button('Track coordonate')],[sg.FileBrowse("Choose picture"), sg.InputText(size=(68, 10))],[sg.Button('Extract EXIF')],
              ]
    return sg.Window('OSINT', layout, size=(630, 150))


def gui_osint_funct():
    window = create_osint_gui()
    while True:
        event, values = window.read()
        if event == None:
            break
        if event == "Track coordonate" and values[0]:
            try:
                from geopy.geocoders import Nominatim
                geolocator = Nominatim(user_agent="http")
                location = geolocator.reverse(values[0])
                print(values[0], " --> ", location.address)
            except Exception as e:
            	print (e)
        if event == "Extract EXIF" and values[1]:
            import exifread
            with open(values[1], 'rb') as fd:
                tags = exifread.process_file(fd)
                if tags:
                    for tag in tags.keys():
                        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                            print (tag, tags[tag])
                else:
                    print ("No EXIF data found!")
    window.close()