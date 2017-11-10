import os
import queue
import requests
import progressbar

class Task:
    def __init__(self,MusicBean):
        self.mina = MusicBean.rank
        self.name = MusicBean.name
        self.url_music = MusicBean.mp3_url #歌曲
        self.url_lrc = MusicBean.lyric_url #歌词
        self.flag =  str(MusicBean.index)

class DownloadManager:

    def __init__(self,dirc):
        self.dirc = dirc
        if not os.path.exists(self.dirc):
            os.mkdir(self.dirc)
        self.queue = queue.Queue(maxsize = 0)
        self.queue_fail = queue.Queue(maxsize = 0)
    def start(self):
        p = progressbar.ProgressBar()
        N = self.queue.qsize()
        for i in p(range(N)):
            task = self.queue.get()
            self.download(task)
        # while self.queue.empty() is not True:
        #     task = self.queue.get()
        #     self.download(task)

    def download(self, task):
        # print('download: ', task.mina+' - '+task.flag+' '+task.name, ',      remainder:', self.queue.qsize())

        dir = self.dirc+'/'+task.mina
        try:
            if not os.path.exists(dir):
                os.mkdir(dir)
            file = dir +'/'+task.flag+'.mp3'

            with open(file, 'wb') as f:
                resp = requests.get(task.url_music)
                if resp.status_code == 200:
                    f.write(resp.content)
                resp.close()

            file = dir + '/' + task.flag + '.lrc'
            with open(file, 'wb') as f:
                resp = requests.get(task.url_lrc)
                if resp.status_code == 200:
                    f.write(str(resp.json()['lrc']['lyric']).encode('utf-8'))
                resp.close()
        except Exception as e:
            print(e)


