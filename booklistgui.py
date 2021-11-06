import PySimpleGUI as sg
import glob
import os

sg.theme('LightGray6')
sg.set_options(font="나눔스퀘어_ac 13")
menu_set=[['&Theme']]
SubList=['시','소설','극']
w_layout = 1

layout1 = [[sg.Menu(menu_set,tearoff=False, key='-Menu-')],
           [sg.Text("Reading book is ", font="나눔스퀘어_ac 17")],
           [sg.Text('Title'), sg.Text("            "),sg.InputText(key='-Title-', size=(30))],
           [sg.Text('Category'),sg.Text("  "),sg.Combo(SubList,key='-Category-', size=(5,7))],
           [sg.Text('Contents'),sg.Text("  "),
            sg.Multiline(key='-Content-', size=(30,10),font="나눔스퀘어_ac 12")],
           [sg.Text("                                                                                           "),
            sg.Button("Hey!")],
           [sg.Checkbox("What for?",key="-Whatfor-")],
           [sg.ProgressBar(5, orientation='h', key='-pgbar-'), sg.Text(key="-pging-"), sg.Text("/5")],
           [sg.Button("List")],
           [sg.Button("Exit")]]

layout2 = [[sg.Menu(menu_set,tearoff=False, key='-Menu-')],
           [sg.Text("It's Your BookList!", font="나눔스퀘어_ac 17", justification='c')],
           [sg.InputText(key='-Search-',size=(20)), sg.Button("Search")],
           [sg.Text("    "), sg.Listbox(values=[], change_submits=True, key="-booklist-", size=(20,20), font="나눔스퀘어_ac 12")],
           [sg.Button("Open"),sg.Button("Remove File")],
           [sg.Button("Return"), sg.Button("Exit")]]

layout = [[sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-')]]


#create window
window = sg.Window('BOOK-LIST',layout, size=(700,600), finalize=True, default_element_size=(15,1),grab_anywhere=True)

#button_def
def Hey(values):
    t_name = values['-Title-']
    ttxt_name = '{0}.txt'.format(t_name)
    txt_list = glob.glob("*.txt")
    if ttxt_name not in txt_list:
        f = open('./txt_file/{0}.txt'.format(t_name), 'a', -1, "utf-8")
        f.write(values['-Content-'])
        f.write('\n\n')
        f.close()
        keys_to_clear = ['-Title-', '-Content-', '-Category-']
        for key in keys_to_clear:
            window[key]('')
    else:
        pass  # Already Exist

def Booklist_update():
    k = glob.glob("./txt_file/*.txt")
    k1 = []
    for i in k:
        i = i.split("\\")[1].replace('.txt','')
        k1.append(i)
    window['-booklist-'].Update(values=k1)


#event loop
while True:
    event, values = window.read() #read event
    print(event,values)

    if event in (None, 'Exit', 'Exit1'): #user closed with X or 'Exit' button
        break

    elif event == 'Hey!': #txt file create
        if values['-Title-']=='':
            sg.popup("제목을 입력해주세요!", font="나눔스퀘어_ac 12")
        elif values['-Content-']=="":
            sg.popup("내용을 입력해주세요!", font="나눔스퀘어_ac 12")
        else:
            Hey(values)
            sg.popup("파일 생성 성공!", font="나눔스퀘어_ac 12")

    elif event == "List": #txt file list show
        window['-COL1-'].Update(visible=False)
        window['-COL2-'].Update(visible=True)
        w_layout = 2

        Booklist_update()

    elif event == "Return":
        window['-COL1-'].Update(visible=True)
        window['-COL2-'].Update(visible=False)
        w_layout = 1

    elif event == 'Remove File':
        os.remove("./txt_file/{0}".format(values['-booklist-'][0]+'.txt'))
        sg.popup("파일을 삭제했습니다!", font="나눔스퀘어_ac 12")
        window['-booklist-']('')
        Booklist_update()

    elif event == 'Open':
        a=values['-booklist-'][0]+'.txt'
        print(type(a))
        f = open("./txt_file/{0}".format(a),'r',-1,"utf-8")
        opf = f.read()
        sg.popup("{0}".format(opf), font="나눔스퀘어_ac 12", title=a.replace('.txt',''))
        f.close()

    elif event == 'Search':
        a = values['-Search-']
        k = glob.glob("./txt_file/{0}*.txt".format(a))
        k1 = []
        for i in k:
            i = i.split("\\")[1].replace('.txt', '')
            k1.append(i)
        window['-booklist-'].Update(values=k1)

    elif event=="KINDER":
        a = values['-kinder-']


    else: pass

    if w_layout==1 and values['-Whatfor-']:
        i += 1
        if i>5: i=5
        window['-pgbar-'].UpdateBar(i)
        window['-pging-'].Update(i)


window.close()