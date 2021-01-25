import os
from dash_core_components import Checklist
def get_folder_checks(basePath= "frames_folder"):

    folder_ls = os.listdir(basePath)
    folder_options = []
    for folder in folder_ls:
        #num = len(os.listdir(folder))
        item = {'label': folder, 'value': folder},
        folder_options.append(item)
    if '.DS_Store' in folder_ls:
        folder_ls.remove('.DS_Store')
    folder_checks =Checklist(id = "folder-checks",
        options=[{'label': folder, 'value': str(basePath + '/' + folder)}
                    for folder in folder_ls],
        #options=folder_options,
        labelStyle = dict(display='block')
    )
    return folder_checks