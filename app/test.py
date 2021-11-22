import psutil,datetime,requests
from moviepy.editor import VideoFileClip
from barrage.models import video_compilation as compilationTable
import os
# print(psutil.cpu_count())
# print(psutil.cpu_count(logical=False))
# print(psutil.swap_memory().total/1024/1024/1024)
# print(psutil.virtual_memory().used/1024/1024/1024)
# print(psutil.virtual_memory().total/1024/1024/1024)
# print(psutil.disk_usage('/'))
#
# result = {
#     "CPU": "物理:"+str(psutil.cpu_count(logical=False))+"/逻辑:"+str(psutil.cpu_count())+"/利用率:"+str(psutil.cpu_percent(interval=1))+"%",
#     "MEM": "内存总量:"+str(round(psutil.virtual_memory().total/1024/1024/1024,1))+"G"+"/已用:"+str(round(psutil.virtual_memory().used/1024/1024/1024,1))+"G",
#     "DISK":"硬盘总量:"+str(round(psutil.disk_usage('/').total/1024/1024/1024,1))+"G"+"/已用:"+str(round(psutil.disk_usage('/').used/1024/1024/1024,1))+"G",
# }
# print(result)
# print(psutil.boot_time())
# print(datetime.datetime.now().timestamp())
# print(int(((datetime.datetime.now().timestamp()-psutil.boot_time())/60)%60))
compilationTable.create(v_id=54,vc_ad='compilation/flowers/flowers春',vc_title='flowers春',vc_duaring=104)