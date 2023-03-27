import psutil

def GetCPUinfo():
    print("CPU COUNT: ",psutil.cpu_count()) # CPU逻辑数量
    print("logical CPU COUNT: ",psutil.cpu_count(logical=False))# CPU物理核心
    print("-"*10,"CPU","-"*10)
    print(psutil.cpu_percent(interval=1, percpu=False),"%")
    print("-"*25,'\n')

    print("-"*10,"RAM","-"*10)
    print(psutil.virtual_memory().percent,"%")
    print("-"*25,'\n')

if __name__ == '__main__':
    GetCPUinfo()