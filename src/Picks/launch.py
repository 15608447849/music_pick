import os,requests

from bs4 import BeautifulSoup

from src.Download.DownloadManage import DownloadManager, Task
from src.Entry.JsonBean import ToplistBean, MusicBean
from src.Entry.JsonUtils import list2jsonAndToFile, string2JsonBean



if __name__ == '__main__':
    root_path = os.path.abspath('./resources').replace("\\", "/")
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    url = "http://music.163.com/discover/toplist"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find('div', class_='n-minelst n-minelst-2')
    li_list = div.find_all("li")
    list = []
    for li in li_list:
        a = li.find("a")
        obj = ToplistBean()
        index = a['href'].find('?')
        obj.href = 'http://music.163.com/api/playlist/detail?' + a['href'][index + 1:]
        obj.alt = a.img['alt']
        list.append(obj.__dict__)
    list2jsonAndToFile(list, root_path + '/rank.json')
    # 根据排行榜 获取榜单歌曲 string2JsonBean()
    mlist = []
    down = DownloadManager(root_path+'/music')
    for item in list:
        url = item['href']
        response = requests.get(url)
        print(response.json()['result']['name'])
        arr = response.json()['result']['tracks']
        index = 0
        for it in arr:
            muc = MusicBean()
            muc.rank = item['alt'] #排行榜
            muc.name = it['name'] #歌曲名
            muc.index = index+1 #排行榜位置
            muc.mp3_url = 'http://music.163.com/song/media/outer/url?id=%s.mp3'%(it['id']) #音乐连接
            muc.lyric_url = 'http://music.163.com/api/song/lyric?os=osx&id=%s&lv=-1&kv=-1&tv=-1'%(it['id']) #音乐歌词
            muc.songs_url = 'http://music.163.com/api/song/detail/?id=%s&ids=[%s]'%(it['id'],it['id']) #音乐歌词
            print('     ',muc.index, muc.name)
            down.queue.put(Task(muc))
            mlist.append(muc.__dict__)
            index=index+1

        # print(string2JsonBean())
    list2jsonAndToFile(mlist, root_path + '/music.json')
    down.start()