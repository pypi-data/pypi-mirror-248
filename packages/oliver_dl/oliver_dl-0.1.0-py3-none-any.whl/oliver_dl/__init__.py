import requests
import aiohttp
import asyncio
import time
import re
import progressbar
import subprocess
import sys

class Downloader:
    def __init__(self, url, quality=None):
        
        quality_playlist = requests.get(url)

        # print(quality_playlist.content.decode('utf-8'))

        regex = re.compile(r'#EXT-X-STREAM-INF:.*?RESOLUTION=([0-9x]+).*?\n([^#\n]+)', re.MULTILINE)
        matches = regex.findall(quality_playlist.content.decode('utf-8'))

        video_qualities = [match[0] for match in matches]
        video_links = [match[1] for match in matches]
        
        
        quality_choice = 0
        if quality is None:
            for i, quality in enumerate(video_qualities):
                print(f"[{i}] {quality}")
            quality_choice = int(input("Select quality: "))
        else:
            quality_choice = [i for i, q in enumerate(video_qualities) if quality in q][0]

        print (f"Selected {video_qualities[quality_choice]}")
        # video_link = self.folder + video_links[quality_choice]
        self.folder = url[:url.rfind('/') + 1]
        self.url = video_links[quality_choice] if video_links[quality_choice].startswith("http") else self.folder + video_links[quality_choice]
        self.folder = self.url[:self.url.rfind('/') + 1]

        lines = requests.get(self.url ).content.decode('utf-8').split('\n')

        
        self.ts_files = [self.folder + line.strip() for line in lines if not line.startswith('#')]
        print(f"Found {len(self.ts_files)} files")
        # print(self.ts_files[0])
        self.total = len(self.ts_files)
        self.bar = progressbar.ProgressBar(max_value=self.total,redirect_stdout=True,redirect_stderr=True)
        self.i = 1

    async def fetch(self, file, session):
        try:
            async with session.get(file) as response:   
                response =  await response.read()
                self.bar.update(self.i)
                self.i += 1
                return response
        except Exception as e:
            print(f"Failed to get data from {file}: {e}")
            return None

    def save(self, outpath=''):
        filename = asyncio.run(self.download())

        if not outpath.endswith('/') and outpath != '':
            outpath = outpath + '/'
        
        subprocess.run(['ffmpeg', "-hide_banner", "-loglevel", "error", '-i', f"{filename}.ts", '-c', 'copy',  f"{outpath}{filename}.mp4"])
    

    async  def download(self):
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(file, session) for file in self.ts_files]
            results = await asyncio.gather(*tasks)

        self.bar.finish()
        filename = input("Enter filename: ")
        with open(f"{filename}.ts", 'wb') as f_out:
            for content in results:
                if content is not None:
                    f_out.write(content)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Total time: {elapsed_time} seconds")
        return filename
        

        

    
       

        

#random comment
        
        


