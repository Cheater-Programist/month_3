# https://www.tiktok.com/@codex_kg/video/7327987700139691271
# https://www.tiktok.com/@codex_kg/video/7327987700139691271?is_from_webapp=1&sender_device=pc&web_id=7289042945105217029

import requests, os

# input_url = input("URL: ")
# print(input_url)

# currentId = .split('/')[5].split('?')[0]


def installing(a):
    current_id = a.split('/')[5].split('?')[0]
    # print(current_id)

    video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={current_id}').json()
    # print(video_api)

    video_url = video_api.get('aweme_list')[0].get('video').get('play_addr').get('url_list')[0]   #the path of video
    # print(video_url)

    if video_url:
        print("Start to installing...")
        try:
            os.mkdir('video')  #Creates a folder
        except:
            print("Folder video created")
        
        try:
            with open(f"video/{current_id}.mp4", 'wb') as video_file:
                video_file.write(requests.get(video_url).content)  #.content as a downloader, or reader code
            print("The video installed successfuly")
        except:
            print("Somethong went wrong")