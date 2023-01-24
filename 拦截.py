import os,subprocess
import re
import threading
# ---------------------------------------------------------------------------------------------------
# 发送消息
# 存放获取的各种消息，以后有必要可能需要将各个消息存放的内容分开
dict_receive = {'message_type': '', 'sender_msg': '', 'sender_name': '', 'sender_id': '', 'sender_msg_id': '',
                'sender_group_id': '', 'sender_self_id': ''}
# ---------------------------------------------------------------------------------------------------
or_msg = subprocess.Popen(["go-cqhttp_windows_amd64.exe"],stdout=subprocess.PIPE)  #拦截cmd输出
msg = ""  #存放获取到的消息

class Listener_processing(): #接收消息并处理
    def receive(self):
        global msg
        line = or_msg.stdout.readline()
        try:
            decoded_line = line.decode("UTF-8")
            # ee = msg.append(str(decoded_line))
            # print(decoded_line)
            # ee  = re.findall(r"(.*)",decoded_line)
            # print(ee)
            leve_1_msg = re.search(r"\[(.*)\] \[(.*)\]:(.*)", decoded_line)
            msg = leve_1_msg.group(3)
            print(msg)
        except:
            pass

    def processe_private(self):
        global msg
        try:
            #print(msg)
            ee = re.findall(r"收到好友 (.*)\((.*)\) 的消息:(.*)\((.*)\)", msg)
            if ee == []:
                pass
            else:
                print(ee)
        except:
            pass

    def processe_group(self):
        try:
            # print(msg)
            ee = re.findall(r"收到群 (.*)\((.*)\) 内 (.*)\((.*)\) 的消息:(.*)\((.*)\)", msg)
            if ee == []:
                pass
            else:
                print(ee)
        except:
            pass

    def main_Listener_processing(self):
        sun_1 = threading.Thread(target=Listener_processing().receive())
        sun_1.start()
        sun_1.join()
        sun_2 = threading.Thread(target=Listener_processing().processe_private())
        sun_3 = threading.Thread(target=Listener_processing().processe_group())
        sun_2.start()
        sun_3.start()


while True:
    Listener_processing().main_Listener_processing()
























