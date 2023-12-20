#-*- coding: utf-8 -*-
"""
Created on Jul 18, 2018  @author: CloudSkyRiver. File function: download today's Bing China wallpaper, and set as windows desktop background.
"""
import urllib.request, requests, os.path, ctypes, win10toast, json
from pypac import PACSession
from pypac.parser import PACFile
from PIL import Image, ImageFont, ImageDraw

notifymsg = 'today\'s Bing wallpaper'
def save_img(img_url,dirname): #save downloaded file to directory: dirname
    try:
        if not os.path.exists(dirname):
            print ('directory ',dirname,'not exist, creating now.') #os.mkdir(dirname)
            os.makedirs(dirname)
        basename = os.path.basename(img_url)  #get the image name,  including suffix
        basename = basename[10:]
        basename = basename[:basename.index('&')]
        filepath = os.path.join(dirname, basename)  #join directory name and image name together
        urllib.request.urlretrieve(img_url,filepath)  #download image,  and save to directory: dirname
        add_img_description(notifymsg,filepath)
        desktopNotification = win10toast.ToastNotifier()
        desktopNotification.show_toast(img_url, notifymsg, duration=10)
    except IOError as e: # if above function can't work,  it may caused by company network env
        print('network evn is not direct connection, will use company proxy settings.' + '\n')
        with open(r"C:\Users\zzhu25\OneDrive - azureford\important-docs\00.PythonScripts\pacfile") as f:
            pac = PACFile(f.read())
        session = PACSession(pac)
        r = session.get(img_url)
        with open(filepath,'wb') as fi:
            fi.write(r.content)
        add_img_description(notifymsg,filepath)
        desktopNotification = win10toast.ToastNotifier()
        desktopNotification.show_toast(img_url, notifymsg, duration=10)
    except Exception as e:
        print ('Error : ',e)
    print("Save", filepath, "successfully!")
    return filepath

## another wallpaper source: https://momentumdash.com/app/backgrounds.json
##def get_img_url(raw_img_url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=1&n=1"):  # get the real img url by using the raw_img_url address
def get_img_url(raw_img_url = "http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"):  # get the real img url by using the raw_img_url address
    global notifymsg
    try:
        r = requests.get(raw_img_url)
    except:
        with open(r"C:\Users\zzhu25\OneDrive - azureford\important-docs\00.PythonScripts\pacfile") as f:
            pac = PACFile(f.read())
        session = PACSession(pac)
        r = session.get(raw_img_url)
        rtext = json.loads(r.text)
        img_url = 'https://cn.bing.com' + rtext['images'][0]['url']
        notifymsg = rtext['images'][0]['copyright']
    else:
        rtext = json.loads(r.text)
        img_url = 'https://cn.bing.com' + rtext['images'][0]['url']  # get the correct url for image
        notifymsg = rtext['images'][0]['copyright']
    print('img_url:', img_url)
    return img_url

def get_iciba_daily_sentence(iciba_daily_sentence_url = 'http://open.iciba.com/dsapi'):
    try:
        r = requests.get(iciba_daily_sentence_url)
    except:
        with open(r"C:\Users\zzhu25\OneDrive - azureford\important-docs\00.PythonScripts\pacfile") as f:
            pac = PACFile(f.read())
        session = PACSession(pac)
        r = session.get(iciba_daily_sentence_url)
        rtext = json.loads(r.text.encode('ascii').decode('unicode_escape'))
    else:
        rtext = json.loads(r.text.encode('ascii').decode('unicode_escape'))
    print('from iciba daily sentence:\n',rtext['content'],'\n',rtext['note'],'\n')
    return rtext['content'], rtext['note']
def add_img_description(notifymsg,filepath):
    # font = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc",20)
    font = ImageFont.truetype("Ubuntu-R.ttf",20)
    imagetemp = Image.open(filepath)
    draw = ImageDraw.Draw(imagetemp)
    x, y = 10, 980

    #draw text border:
    draw.text((x-1,y), notifymsg, fill=(112,39,77), font=font)
    draw.text((x+1,y), notifymsg, fill=(112,39,77), font=font)
    draw.text((x,y-1), notifymsg, fill=(112,39,77), font=font)
    draw.text((x,y+1), notifymsg, fill=(112,39,77), font=font)

    # draw text
    draw.text((x-1,y-1), notifymsg, (250,250,250), font=font)

    imagetemp.save(filepath)
def set_img_as_wallpaper(filepath):  # set this image as desktop wallpaper by using filepath
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    SPIF_UPDATEINIFILE = 1
    SPI_SETDESKWALLPAPER = 20
    user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, filepath, SPIF_UPDATEINIFILE)
def main():
    dirname = r"C:\Users\zzhu25\OneDrive - azureford\important-docs\00.PythonScripts\BingWallPaper\saved_wallpaper" #image saved to
    img_url = get_img_url()
    filepath = save_img(img_url, dirname)   #this is image saved filepath
    set_img_as_wallpaper(filepath)
main()
