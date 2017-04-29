import os
import platform
import psutil
import wmi
import subprocess

BYTE_TO_KILOBYTE = 1024
BYTE_TO_MEGABYTE = 1024 * 1024
BYTE_TO_GIGABYTE = 1024 * 1024 * 1024
BYTE_TO_MEGABITS = 0.8 * 100000

class SysInfo():
    def __init__(self):
        self.erros = 1
        self.os = platform.system()
        self.osName = platform.platform()
        self.osVersion = platform.version()
        self.osArchitecture = platform.machine()

        self.cpus = psutil.cpu_count()
        self.disks = psutil.disk_partitions()
        self.nets = psutil.net_if_addrs()
        # 0 - non NVIDIA GPU | 1 - NVIDIA GPU
        self.gpuType = 0
        self.gpu = {}

        self.up = 0
        self.down = 0

        self.drive = ["C:", "D:", "E:", "F:", "G:", "H:"]
        self.disk = [0] * 6
        self.disk_temp = [0] * 6

        self.CPU()
        self.GPU()
        self.RAM()
        self.SWAP()
        self.DISK()
        self.NET()
        self.USER()

    def info(self):
        print("%-30s%-20s" %("Operating System:", self.os))
        print("%-30s%-20s" %("System Name:", self.osName))
        print("%-30s%-20s" %("System Version:", self.osVersion))
        print("%-30s%-20s" %("System Architecture:", self.osArchitecture))
        print("%-30s%-20s" %("CPU's:", self.cpus))
        print("%-30s%-20s%-20s" %("CPU Usage:", "", self.CPU_usage()))
        print("%-30s%-20s%-20s" %("GPU Usage:", "", self.GPU_usage_gpu()))
        print("%-30s%-20s" %("RAM total:", self.RAM_total()))
        print("%-30s%-20s" %("RAM free:", self.RAM_free()))
        print("%-30s%-20s%-29s" %("RAM Usage:", self.RAM_usage_total(), self.RAM_usage_percent()))
        print("%-30s%-20s" %("SWAP total:", self.SWAP_total()))
        print("%-30s%-20s" %("SWAP free:", self.SWAP_free()))
        print("%-30s%-20s%-29s" %("SWAP Usage:", self.SWAP_usage_total(), self.SWAP_usage_percent()))
        print("%-30s%-20s" %("DISK total:", self.DISK_total()))
        print("%-30s%-20s" %("DISK free:", self.DISK_free()))
        print("%-30s%-20s%-29s" %("DISK Usage:", self.DISK_usage_total(), self.DISK_usage_percent()))
        print("%-30s%-20s" %("NET Name:", self.NET_name()))
        print("%-30s%-20s" %("NET Address:", self.NET_address()))
        print("%-30s%-20s" %("NET Up-speed:", self.NET_upspeed()))
        print("%-30s%-20s" %("NET Down-speed:", self.NET_downspeed()))
        print("%-30s%-20s" %("USER user:", self.USER_user()))
        print("%-30s%-20s" %("USER uptime:", self.USER_uptime()))

    def update(self):
        self.CPU()
        self.GPU()
        self.RAM()
        self.SWAP()
        self.DISK()
        self.NET()
        self.USER()

    def CPU(self):
        self.cpu_temp = [0, 0, 0, 0]
        self.cpu = psutil.cpu_percent(interval=1.0, percpu=True)

        try:
            w = wmi.WMI(namespace="root\OpenHardwareMonitor")
            temperature_infos = w.Sensor()
            for sensor in temperature_infos:
                if sensor.SensorType == u'Temperature':
                    if sensor.Name[:-3] == "CPU Core":
                        self.cpu_temp[sensor.Index] = sensor.Value
        except wmi.x_wmi:
            print (u'WMI Exception. Is Open Hardware Monitor running?')

    def GPU(self):
        if self.gpuType <= 1:
            cmd = "nvidia-smi.exe -i 0 -q -a"
            f = open("out.txt", "w")
            subprocess.call(cmd.split(" "), creationflags=0x08000000, shell=False, stdout=f)
            f.close()
            f = open("out.txt", "r")
            lines = f.readlines()
            f.close()
            if len(lines) > 2:
                self.gpuType = 1
        if self.gpuType == 1:
            for i, line in enumerate(open("out.txt", "r")):
                if i == 8 or i == 52 or i == 61 or i == 62 or i == 63 or i == 70 or i == 71 or i == 113:
                    info = [x.strip(' ') for x in line.split(":")]
                    self.gpu[info[0]] = info[1]
        else:
            self.gpuType = 2

    def RAM(self):
        self.ram = psutil.virtual_memory()

    def SWAP(self):
        self.swap = psutil.swap_memory()

    def DISK(self):
        for i,d in enumerate(self.disks):
            if self.disks[i][2]:
                self.disk_temp[i] = 0
                self.disk[i] = psutil.disk_usage(self.drive[i])

                try:
                    w = wmi.WMI(namespace="root\OpenHardwareMonitor")
                    temperature_infos = w.Sensor()
                    for sensor in temperature_infos:
                        if sensor.SensorType == u'Temperature' and sensor.Name == u'Temperature':
                            self.disk_temp[i] = sensor.Value
                except wmi.x_wmi:
                    if self.erros >= 1:
                        print (u'OpenHardwareMonitor is not running...')

    def NET(self):
        self.netspeed = psutil.net_io_counters(pernic=True)
        self.net = psutil.net_if_addrs()

    def USER(self):
        self.user = psutil.users()

    def CPU_usage(self, cpu=0):
        if cpu >= 0 and cpu < self.cpus:
            return int(self.cpu[cpu])

    def CPU_temp(self, cpu):
        return int(self.cpu_temp[cpu])

    def GPU_name(self):
        if self.gpuType == 1:
            return self.gpu["Product Name"]
        else:
            return ""

    def GPU_temp(self):
        if self.gpuType == 1:
            temp = self.gpu["GPU Current Temp"].split(" ")
            return int(temp[0])
        else:
            return 0

    def GPU_usage_gpu(self):
        if self.gpuType == 1:
            gpu = self.gpu["Gpu"].split(" ")
            return int(gpu[0])
        else:
            return 0

    def GPU_usage_mem(self):
        if self.gpuType == 1:
            mem = self.gpu["Memory"].split(" ")
            return int(mem[0])
        else:
            return 0

    def GPU_usage_fan(self):
        if self.gpuType == 1:
            fan = self.gpu["Fan Speed"].split(" ")
            return int(fan[0])
        else:
            return 0

    def GPU_MEM_total(self):
        if self.gpuType == 1:
            total = self.gpu["Total"].split(" ")
            return int(total[0])
        else:
            return 10

    def GPU_MEM_free(self):
        if self.gpuType == 1:
            free = self.gpu["Free"].split(" ")
            return int(free[0])
        else:
            return 0

    def GPU_MEM_used(self):
        if self.gpuType == 1:
            used = self.gpu["Used"].split(" ")
            return int(used[0])
        else:
            return 0

    def RAM_total(self):
        if self.ram[0] != None:
            return int(self.ram[0] / BYTE_TO_MEGABYTE)

    def RAM_free(self):
        if self.ram[1] != None:
            return int(self.ram[1] / BYTE_TO_MEGABYTE)

    def RAM_usage_percent(self):
        if self.ram[2] != None:
            return self.ram[2]

    def RAM_usage_total(self):
        if self.ram[3] != None:
            return int(self.ram[3] / BYTE_TO_MEGABYTE)

    def SWAP_total(self):
        if self.swap[0] != None:
            return int(self.swap[0] / BYTE_TO_MEGABYTE)

    def SWAP_free(self):
        if self.swap[2] != None:
            return int(self.swap[2] / BYTE_TO_MEGABYTE)

    def SWAP_usage_total(self):
        if self.swap[1] != None:
            return int(self.swap[1] / BYTE_TO_MEGABYTE)

    def SWAP_usage_percent(self):
        if self.swap[3] != None:
            return self.swap[3]

    def DISK_total(self, drive=0):
        if self.disk[drive] != None:
            if self.disk[drive][0] != None:
                if self.disk[drive][0] > 100000000:
                    return int(self.disk[drive][0] / BYTE_TO_GIGABYTE)
                else:
                    return int(self.disk[drive][0] / BYTE_TO_MEGABYTE)

    def DISK_free(self, drive=0):
        if self.disk[drive] != None:
            if self.disk[drive][2] != None:
                if self.disk[drive][2] > 100000000:
                    return int(self.disk[drive][2] / BYTE_TO_GIGABYTE)
                else:
                    return int(self.disk[drive][2] / BYTE_TO_MEGABYTE)

    def DISK_usage_total(self, drive=0):
        if self.disk[drive] != None:
            if self.disk[drive][1] != None:
                if self.disk[drive][1] > 100000000:
                    return int(self.disk[drive][1] / BYTE_TO_GIGABYTE)
                else:
                    return int(self.disk[drive][1] / BYTE_TO_MEGABYTE)

    def DISK_usage_percent(self, drive=0):
        if self.disk[drive] != None:
            if self.disk[drive][3] != None:
                return self.disk[drive][3]

    def DISK_temp(self, drive=0):
        if self.disk_temp[drive] != None:
            return int(self.disk_temp[drive])

    def NET_name(self, net="Ethernet"):
        for i in self.net:
            if i == net:
                return str(i)

    def NET_address(self, net="Ethernet"):
        net = self.net[net][1]
        return str(net[1])

    def NET_upspeed(self, net="Ethernet"):
        if len(self.netspeed) != None:
            if self.netspeed[net] != None:
                curr = self.netspeed[net].bytes_sent
                upspeed = curr - self.up
                self.up = curr
                return int(upspeed / BYTE_TO_KILOBYTE)

    def NET_downspeed(self, net="Ethernet"):
        if len(self.netspeed) != None:
            if self.netspeed[net] != None:
                curr = self.netspeed[net].bytes_recv
                downspeed = curr - self.down
                self.down = curr
                return int(downspeed / BYTE_TO_KILOBYTE)

    def USER_user(self, user=""):
        for i in self.user:
            return i[0]

    def USER_uptime(self):
        return psutil.Process(os.getpid()).create_time()