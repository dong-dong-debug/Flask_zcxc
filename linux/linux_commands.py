import paramiko
import time
import threading


class Python_Linux:
    def __init__(self):
        self.thread = None
        self.running = False
        self.ip = "192.168.137.100"
        self.port = "22"
        self.user = "root"
        self.password = "dyx000710"

    # 建立连接
    def connect(self):
        try:
            # 创建SSHClient 实例对象
            self.ssh = paramiko.SSHClient()
            # 调用方法，表示没有存储远程机器的公钥，允许访问
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接远程机器，地址，端口，用户名密码
            self.ssh.connect(self.ip, self.port, self.user, self.password, timeout=10)
        except Exception as e:
            print("连接错误{}".format(e))

    # 关闭连接
    def close(self):
        self.ssh.close()

    # 上传文件
    def upload_file(self, local_file, remoute_file):
        self.connect()
        try:
            sftp = self.ssh.open_sftp()
            # 从本地上次文件到linux
            sftp.put(local_file, remoute_file)
        except Exception as e:
            print("连接错误{}".format(e))
        finally:
            sftp.close()
            self.close()

    # 解压文件
    def unzip_file(self):
        self.connect()
        with self.ssh.invoke_shell() as execute:
            execute.send("cp /home/zc/PPU/test.zip /home/zc/PPU/bak/" + "\n")
            time.sleep(2)
            execute.send("unzip /home/zc/PPU/bak/test.zip -d /home/zc/PPU/bak/" + "\n")
            time.sleep(2)
        self.close()

    # 修改文件
    def update_file(self):
        self.connect()
        with self.ssh.invoke_shell() as execute:
            execute.send('sed -i "s/NO/YES/g" /home/zc/PPU/bak/PPU_config.txt\n')
            time.sleep(2)
            execute.send('sed -i "s/2/100/g" /home/zc/PPU/bak/PPU_config.txt\n')
            time.sleep(2)
        self.close()

    # 监控python进程
    def process_find_python(self):
        self.connect()
        stdin, stdout, stderr = self.ssh.exec_command("ps -ef | grep TestProcess.py")
        result = stdout.readlines()
        self.close()
        return result

    # 启动python程序
    def open_python_process(self):
        self.connect()
        self.ssh.exec_command("python /home/zc/PPU/bak/TestProcess.py")
        self.close()

    # 杀死进程
    def kill_python_process(self, port):
        self.connect()
        with self.ssh.invoke_shell() as execute:
            execute.send(f"kill -9 {port}" + "\n")
            time.sleep(3)
        self.close()

    # 监控进程状态
    def process_find_python_status(self):
        # status 0:未启动  1：正在启动
        result = self.process_find_python()
        if result[0].__contains__('grep'):
            status = 0
        else:
            status = 1
        return status

    # 获取端口号
    def get_process_port(self):
        result = self.process_find_python()
        port = result[0].split()[1]  # 获取端口号码
        return port

    # 获取进程开启时间
    def get_process_start_time(self):
        result = self.process_find_python()
        port = result[0].split()[4]  # 获取时间
        return port

    # 查询文件夹文件个数
    def find_file_nummber(self, filepath):
        self.connect()
        stdin, stdout, stderr = self.ssh.exec_command(f'ls {filepath} -l |grep "^-"|wc -l')
        result = stdout.readlines()
        self.close()
        return result[0]

    # 移动文件到指定位置
    def form_source_to_dest_2(self, sourcepath, destpath):
        result = self.find_filename(sourcepath)
        print(result[2].strip())
        print(len(result))
        print(result)
        self.connect()
        for i in range(len(result)):
            sourcefile = sourcepath + "/" + result[i].strip()
            print(sourcefile)
            destfile = destpath + "/" + result[i].strip()
            print(destfile)
            command = "mv " + sourcefile + " " + destfile
            print(command)
            self.ssh.exec_command(command)
        self.close()
        return result

    # 查看指定文件夹下所有文件名称
    def find_filename(self, filepath):
        self.connect()
        stdin, stdout, stderr = self.ssh.exec_command(f"ls {filepath}")
        result = stdout.readlines()
        self.close()
        return result

    # 根据文件数量移动位置
    def form_source_to_dest_by_num(self, sourcepath, destpath):
        num = self.find_file_nummber(sourcepath)
        if int(num) >= 10:
            self.form_source_to_dest(sourcepath, destpath)
        if self.running:
            self.thread = threading.Timer(5, self.form_source_to_dest_by_num,
                                          kwargs={"sourcepath": sourcepath, "destpath": destpath})
            self.thread.start()

    # 开启搬运
    def active_carry(self, sourcepath, destpath):
        self.running = True
        thread = threading.Timer(5, self.form_source_to_dest_by_num,
                                 kwargs={"sourcepath": sourcepath, "destpath": destpath})
        thread.start()

    # 关闭搬运任务
    def close_carry(self):
        self.running = False

    # 将状态和开启时间插入到txt文件
    def insert_status_and_time_to_txt(self):
        port = self.get_process_port()
        time = self.get_process_start_time()
        with open("log/message.txt", "a+") as file:
            message = port + " " + time + "\n"
            file.write(message)

    # 读取上一次开启时的端口号和时间
    def get_file_last_port_time(self):
        with open("log/message.txt", "r") as file:
            lines = file.readlines()
            last_line = lines[-1]
        port = last_line.split()[0]
        time = last_line.split()[1]
        return port, time


if __name__ == '__main__':
    result = Python_Linux().get_file_last_line()
    print(result)
    print(result.split()[0])
