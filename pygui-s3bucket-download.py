import PySimpleGUI as sg
import boto3
import os
import time

#This code need to be run from a machine that hase all the required policies in place to access an s3 bucket.

BUCKET_NAME = '<Insert bucket name here>'
source_file = "<Insert location where the files will be downloaded>"
destination_file = "<Insert location where the files need to be moved (final location)>"
s3 = boto3.resource('s3')
my_bucket = s3.Bucket('<Insert bucket name here>')

#create empty lists to be filled

s3_objects_empty = []
s3_objects = []
downoald_file_name  = None

#Get object keys and add to s3_objects list
for my_bucket_object in my_bucket.objects.all():
    s3_objects.append(my_bucket_object.key)

#design the GUI

sg.change_look_and_feel('LightGrey1')	# Adding a touch of color
# All the stuff inside your window.

layout = [  [sg.Image(r'<Insert logo location here, if not delete this line>', size=(190,60))],
            [sg.Text('<Insert bucket name here> Bucket List', font='Courier 12 bold')],
            [sg.Input(do_not_clear=True, size=(20,1),enable_events=True, key='_INPUT_'), sg.Button('Search', key='_SEARCH_')],
            [sg.Listbox(s3_objects_empty, size=(50,20), enable_events=True, key='_LIST_', font='Courier')],
            [sg.Button('Download Selected File', key='_BUTTON_KEY_'), sg.Button('Exit')],
            [sg.Image(r'Insert logo location here, if not delete this line', size=(90,20)), sg.Text('Developed by Deepak Nadiminti', font='Courier')]]


#Logic behind the frontend

window = sg.Window('<Insert application title here>').Layout(layout)
# Event Loop
while True:
    event, values = window.Read()
    if event is None or event == 'Exit':                # always check for closed window
        break
    if event == '_SEARCH_':                         # if a keystroke entered in search field
        search = values['_INPUT_']
        new_values = [x for x in s3_objects if search in x]  # do the filtering
        window.Element('_LIST_').Update(new_values)     # display in the listbox
    #else:
        #   window.Element('_LIST_').Update(s3_objects)          # display original unfiltered list
    if event == '_LIST_' and len(values['_LIST_']):     # if a list item is chosen
        downoald_file_name = values['_LIST_']
        #print (downoald_file_name)
        sg.Popup('Selected ', values['_LIST_'])
    if event == '_BUTTON_KEY_' and not downoald_file_name is None:
        print (str(downoald_file_name[0]))
        #window['_DOWNLOAD_'].update('File being downloaded')
        s3 = boto3.resource('s3')
        s3.Bucket(BUCKET_NAME).download_file(downoald_file_name[0],downoald_file_name[0])
        source_file = source_file+'/'+str(downoald_file_name[0])
        destination_file = destination_file+'/'+str(downoald_file_name[0])
        while not os.path.exists(source_file):
            time.sleep(1)
        if os.path.isfile(source_file):
            os.replace(source_file, destination_file)
            print('Download Finished!')
        sg.Popup('Downloaded ', downoald_file_name[0])
        downoald_file_name  = None
        source_file = "<Insert location where the files will be downloaded>"
        destination_file = "<Insert location where the files need to be moved (final location)>"

window.Close()

