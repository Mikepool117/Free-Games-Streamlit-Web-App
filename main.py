import requests, segno, streamlit, io
from urllib.request import urlopen


#Page title config
streamlit.set_page_config(
    page_title="Free Games🎮 - A streamlit webapp made using gamerpower API. ",
    page_icon="Resources\My Computer.ico",
    layout="centered",
    menu_items={
        'Get Help': 'https://github.com/Mikepool117',
        'Report a bug': "https://github.com/Mikepool117",
        'About': "Webapp Developed by *Mikepool 117*.Powered By GamerPower API and hosted using streamlit cloud",
    }
)


#Check API Status and stops further execution 
try :
    if requests.get("https://www.gamerpower.com/api/giveaways").status_code != 200 :
        streamlit.error("It appears that the API is having trouble. 💀💀")
        streamlit.stop()
except :
    #Works when running locally and you are offline
    streamlit.error('''
                    You are offline 🌐.
                    ''')
    streamlit.stop()
    
#Streamlit cache declaration for api requests to make the app faster
@streamlit.cache(ttl=28800)
def steam_fetch() :
    #Fetches the steam entries from api and returns a dict with the required entries
    api_url = "https://www.gamerpower.com/api/giveaways"
    data_parameters = {'platform' : 'steam', 'sort-by' : 'popularity', 'type' : 'game'}
    data = requests.get(api_url,params=data_parameters).json()
    steam_dict = {}
    for game in data :
        steam_dict[game['title']] = [game['image'], game['description'], game['open_giveaway']]
    return steam_dict

@streamlit.cache(ttl=28800)
def epic_fetch() :
    #Fetches the epic game store entries from api and returns a dict with the required entries
    api_url = "https://www.gamerpower.com/api/giveaways"
    data_parameters = {'platform' : 'epic-games-store', 'sort-by' : 'popularity', 'type' : 'game'}
    data = requests.get(api_url,params=data_parameters).json()
    epic_dict = {}
    for game in data :
        epic_dict[game['title']] = [game['image'], game['description'], game['open_giveaway']]
    return epic_dict

@streamlit.cache(ttl=28800)
def gog_fetch() :
    #Fetches the steam entries from api and returns a dict with the required entries
    api_url = "https://www.gamerpower.com/api/giveaways"
    data_parameters = {'platform' : 'pc', 'sort-by' : 'popularity', 'type' : 'game'}
    data = requests.get(api_url,params=data_parameters).json()
    game_dict = {}
    for game in data :
        if game['platforms'] == "PC, Epic Games Store" or game['platforms'] == "PC, Steam" :
            continue
        game_dict[game['title']] = [game['image'], game['description'], game['gamerpower_url'],game['platforms']]
    return game_dict

#Image,URL to QR
@streamlit.experimental_memo(ttl=28800)
def qr(url,bg) :
    #use the url for qr and the image as the background for qr
    qrcode = segno.make(url, error = 'h')
    #write into bytes stream to avoid saving image on disk
    out = io.BytesIO()
    #also use the image url as a file object using urllib.Request.urlopen()
    qrcode.to_artistic(background = urlopen(bg), target = out, scale = 5, kind = 'jpeg')
    return out

#Function Blocks using session state to make checkbox widget act like a radio widget
def steam_call() :
    streamlit.session_state.EpicCheckBox = False
    streamlit.session_state.GOGCheckBox = False
    
def epic_call() :
    streamlit.session_state.GOGCheckBox = False
    streamlit.session_state.SteamCheckBox = False
    
def gog_call() :
    streamlit.session_state.SteamCheckBox = False
    streamlit.session_state.EpicCheckBox = False

def open_tab(url) :
    webbrowser.open_new_tab(url)


#Title for the page
streamlit.title('View Free Games Available')
streamlit.header('Choose a platform')


#The Platform Selection Checkbox
check1, check2, check3 = streamlit.columns(3)
with check1 :
    steam_check = streamlit.checkbox('Steam', key='SteamCheckBox', help='Show Games for Steam', on_change=steam_call)
with check2 :
    epicgames_check = streamlit.checkbox('Epic Games', key="EpicCheckBox", help='Show games for Epic Games Store', on_change=epic_call)
with check3 :
    gog_check = streamlit.checkbox('Other Stores', key='GOGCheckBox', help='Show Games for GOG, Itch.io and other such stores', on_change=gog_call)
streamlit.markdown('''---''')

#Progress Bar Setup
progress = streamlit.empty()

#Show entries using Checkbox boolean values
#Show steam games if the steam checkbox is checked
if steam_check :
    steam_dict = steam_fetch()
    with progress.container() :
        inc = 100//len(steam_dict)
        progress_bar = streamlit.progress(0)
        ctr = 1
    for game in steam_dict :
        progress_bar.progress(inc*ctr)
        ctr += 1
        with streamlit.container() :
            image, title, description = streamlit.columns(3)
            with image :
                streamlit.image(steam_dict[game][0])
            with title :
                streamlit.markdown(f'''##### {game}''')
            with description :
                streamlit.caption(steam_dict[game][1])
            with streamlit.expander('See QR CODE') :
                streamlit.image(qr(steam_dict[game][2], steam_dict[game][0]))
    progress.empty()

if epicgames_check :
    epic_dict = epic_fetch()
    with progress.container() :
        inc = 100//len(epic_dict)
        progress_bar = streamlit.progress(0)
        ctr = 1
    for game in epic_dict :
        progress_bar.progress(inc*ctr)
        ctr += 1
        with streamlit.container() :
            image, title, description = streamlit.columns(3)
            with image :
                streamlit.image(epic_dict[game][0])
            with title :
                streamlit.markdown(f'''##### {game}''')
            with description :
                streamlit.caption(epic_dict[game][1])
            with streamlit.expander('See QR CODE') :
                streamlit.image(qr(epic_dict[game][2], epic_dict[game][0]))
    progress.empty()

if gog_check :
    game_dict = gog_fetch()
    with progress.container() :
        inc = 100//len(game_dict)
        progress_bar = streamlit.progress(0)
        ctr = 1
    for game in game_dict :
        progress_bar.progress(inc*ctr)
        ctr += 1
        with streamlit.container() :
            image, title, description,= streamlit.columns(3)
            with image :
                streamlit.image(game_dict[game][0])
            with title :
                streamlit.markdown(f'''##### {game}''')
            with description :
                streamlit.caption(game_dict[game][1])
            with streamlit.expander('See QR CODE') :
                streamlit.image(qr(game_dict[game][2], game_dict[game][0]))
    progress.empty()
                
