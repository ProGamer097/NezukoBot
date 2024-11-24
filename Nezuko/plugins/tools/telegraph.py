import requests
import base64
from pyrogram import filters
from Nezuko import app


IMGBB_API_KEY = "5a43c16114ccb592a47a790a058fcf65"

def upload_to_imgbb(file_path):
    url = "https://api.imgbb.com/1/upload"
    
    with open(file_path, 'rb') as file:
        image_data = base64.b64encode(file.read()).decode('utf-8')
        
        response = requests.post(
            url,
            data={
                'key': IMGBB_API_KEY,
                'image': image_data,  
            }
        )
    
    data = response.json()
    if response.status_code == 200 and data['success']:
        return data['data']['url']
    else:
        raise Exception(f"ImgBB upload failed: {data.get('error', 'Unknown error')}")


IMGBB_API_KEY = "5a43c16114ccb592a47a790a058fcf65"


@app.on_message(filters.command('tgm'))
def ul(_, message):
    reply = message.reply_to_message
    if reply.media:
        i = message.reply("**Downloading....**")
        path = reply.download()
        try:
            img_url = upload_to_imgbb(path)
            i.edit(f'Your ImgBB [link]({img_url})', disable_web_page_preview=True)
        except Exception as e:
            i.edit(f"An error occurred: {str(e)}")
