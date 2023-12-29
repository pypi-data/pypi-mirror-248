#  cli
from oliver_dl import Downloader
if __name__ == "__main__":
    m3u8_link = None
    # for arg in sys.argv:
    #     if arg.startswith("-l="):
    #         m3u8_link = arg.split("=")[1]
    #         break

    if m3u8_link is None:
        m3u8_link = input("Enter m3u8 link: ")

    f = Downloader(m3u8_link)
    f.save()
            