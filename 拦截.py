import subprocess  # 拦截cmd输出使用的库
import re  # 使用正则匹配消息
import threading  # 多线程加快运行速度
import time
import requests  # 进行消息回答的获取以及回复
import pandas as pd  # 准备实现本地词库
from api import news_api  # 实现新闻
from api import music_api  # 实现点歌
from api import api_group_1  # 实现每日一言等
from bs4 import BeautifulSoup
import random
# ---------------------------------------------------------------------------------------------------
time_run_1 = time.time()
# ---------------------------------------------------------------------------------------------------
# 发送消息
# 存放获取的各种消息，以后有必要可能需要将各个消息存放的内容分开
dict_receive = {'message_type': '', 'sender_msg': '', 'sender_name': '', 'sender_id': '', 'sender_msg_id': '',
                'sender_belongs_to_the_group': '',
                'sender_belongs_to_the_group_id': ''}
# ---------------------------------------------------------------------------------------------------
# 获取群的ID与名称，为了实现多群喊话做准备
group_id_list = []
group_name_list = []
# ---------------------------------------------------------------------------------------------------
or_msg_1 = subprocess.Popen(["go-cqhttp_windows_amd64.exe"], stdout=subprocess.PIPE)  # 拦截cmd输出
or_msg_2 = ""  # 存放获取到的消息
# ---------------------------------------------------------------------------------------------------36
jdm = False  # 使用这个判断多线程获取回答的继续执行
ans_msg = {"answer": ""}  # 存放获取到的回答，确实找不到什么好的资源共享的方式了
ccm = True  #判断是否有消息，以便加快运行速度
count_msg_receive = 0
# ---------------------------------------------------------------------------------------------------
data_word = pd.read_excel("words/word.xlsx")
word_question = data_word.loc[:, 'question']  # 读取question内容
word_answer = data_word.loc[:, 'answer']  # 读取answer内容
total = data_word.shape[0]  # data.shape可以获取行，列的数
# ---------------------------------------------------------------------------------------------------
class Listener_processing():  # 接收消息并处理
    def receive(self):  # 初步处理消息，注意，使用正则后，获取到的前面的消息会加上其他的字符，这会导致出错
        global or_msg_2, dict_receive,ccm
        line = or_msg_1.stdout.readline()  # 通过循环来一步一步的输出消息
        try:
            decoded_line = line.decode("UTF-8")  # 解码，正常的话，会输出十六进制的字符
            # ee = msg.append(str(decoded_line))
            # print(decoded_line)
            # ee  = re.findall(r"(.*)",decoded_line)
            # print(ee)
            leve_1_msg = re.search(r"\[(.*)\] \[(.*)\]:(.*)", decoded_line)  # 获取正常的cmd输出
            or_msg_2 = leve_1_msg.group(3)  # 剔除前面无用的字符
            print(or_msg_2)
            ccm = True
        except:
            pass

    def processe_private(self):  # 分离私聊消息

        global or_msg_2, dict_receive,ccm,count_msg_receive
        try:
            # print(msg)
            #记得冒号后面，时间戳的括号前面，一定要加空格进行匹配，否则会把空格匹配进去，导致我们后面无法进行各种消息的判断
            mpg = re.findall(r"收到好友 (.*)\((.*)\) 的消息: (.*) \((.*)\)", or_msg_2)
            flag = "private"

            if mpg == []:
                pass
            else:
                ccm = False
                count_msg_receive = count_msg_receive + 1
                print(mpg)
                sum_1 = threading.Thread(target=Listener_processing().add_to_dictionary(flag, mpg))
                sum_1.start()
                print(dict_receive)

        except:
            pass

    def processe_group(self):  # 分离群聊消息
        global or_msg_2, dict_receive,ccm,count_msg_receive
        try:
            # print(msg)
            mpg = re.findall(r"收到群 (.*)\((.*)\) 内 (.*)\((.*)\) 的消息: (.*) \((.*)\)", or_msg_2)
            flag = "group"

            if mpg == []:
                pass
            else:
                ccm = False
                count_msg_receive = count_msg_receive + 1
                print(mpg)
                sum_1 = threading.Thread(target=Listener_processing().add_to_dictionary(flag, mpg))
                sum_1.start()
                print(dict_receive)

        except:
            pass

    def add_to_dictionary(self, flag, original_msg):
        global dict_receive
        if flag == "private":
            dict_receive['message_type'] = flag
            dict_receive["sender_msg"] = str(original_msg[0][2])
            dict_receive["sender_name"] = str(original_msg[0][0])
            dict_receive["sender_id"] = str(original_msg[0][1])
            dict_receive["sender_msg_id"] = str(original_msg[0][3])
            pass
        elif flag == "group":
            dict_receive['message_type'] = flag
            dict_receive["sender_msg"] = str(original_msg[0][4])
            dict_receive["sender_name"] = str(original_msg[0][2])
            dict_receive["sender_id"] = str(original_msg[0][3])
            dict_receive["sender_msg_id"] = str(original_msg[0][5])
            dict_receive["sender_belongs_to_the_group"] = str(original_msg[0][0])
            dict_receive["sender_belongs_to_the_group_id"] = str(original_msg[0][1])
            pass
        else:
            pass

        pass

    def main_Listener_processing(self):
        sun_1 = threading.Thread(target=Listener_processing().receive())
        sun_1.start()
        sun_1.join()
        sun_2 = threading.Thread(target=Listener_processing().processe_private())
        sun_3 = threading.Thread(target=Listener_processing().processe_group())
        sun_2.start()
        sun_3.start()


class Send_operation():  # 可视化获取的消息类别等
    def Send_msg_answer(self):  # 进行回复
        # 输出逻辑回答的消息
        url = 'http://127.0.0.1:5700'
        if dict_receive['message_type'] == 'private':
            urls = url + "/send_private_msg?user_id=" + dict_receive['sender_id'] + '&' + 'message=' + ans_msg['answer']
            answer_post_use = requests.post(url=urls).json()  # 发送消息
            # print('>>>:' * 3 + "已回答:" + "\n " + msg)
            Send_operation().clear_()
            pass
        elif dict_receive['message_type'] == 'group':

            urls = url + '/send_group_msg?group_id=' + dict_receive[
                'sender_belongs_to_the_group_id'] + '&' + "message=" + ans_msg["answer"]
            # print(urls)
            answer_post_use = requests.post(url=urls)  # 发送消息
            # print('>>>:' * 3 + "\n" + "已回答:" + msg)
            Send_operation().clear_()
            pass
        else:

            pass

        return None

    def clear_(self):
        dict_receive['message_type'] = ""
        dict_receive['sender_msg'] = ""
        dict_receive["sender_id"] = ""
        dict_receive["sender_name"] = ""
        dict_receive["sender_belongs_to_the_group"] = ""
        dict_receive["sender_belongs_to_the_group_id"] = ""
        dict_receive["sender_msg_id"] = ""
        ans_msg["answer"] = ""


class answer_logic():  # 回复逻辑
    # 逻辑回答，以后可能会再改，将判断分开，用多线程
    def get_API_answer_1(self):  # 本地词库一级回答
        # 回答消息的第一优先级
        # 放到前面提前处理
        global jdm, dict_receive
        num = 0
        for num in range(total):
            num = +num
              # 前加的意思是先进行一次运行下一次再 +1
            answer_Pre_post = str(word_question[num])

            '''
            因为回答的消息在同行，所以后面也是num。
            因为xlsx里面的数字是int类型，我们获取的消息里面的数字是str
            所以要用str转化一下，这个漏洞我找了好久
            哭~~~~~。
            '''
            if dict_receive['sender_msg'] == answer_Pre_post:
                jdm = True
                msg = word_answer[num]
                ans_msg['answer'] = msg

                return msg  # 弹出本地词库消息，便于下面发送
            else:
                jdm = False
                pass
    def get_API_answer_2(self):
        global jdm, news_api, ans_msg,dict_receive,count_msg_receive
        if jdm == True:
            pass
        else:
            if dict_receive['sender_msg'] == "菜单" or dict_receive['sender_msg'] == "/":  # 回答消息的第二优先级
                jdm = True
                msg = "1.聊天\n2.多群喊话\n3.新闻\n4.点歌(网抑云)\n5.每日一句"  # \n可以实现多行输出
                ans_msg['answer'] = msg

                # return msg


            elif dict_receive['sender_msg'] == "新闻" or dict_receive['sender_msg'] == "/3":

                jdm = True
                msg = news_api.news_content()
                ans_msg['answer'] = msg

                # return msg
            elif "点歌" in dict_receive['sender_msg']:

                jdm = True
                musics_id = music_api.music_id(music_api.handle_content(dict_receive['sender_msg']))
                msg = "[CQ:music,type=163,id={}]".format(musics_id)
                ans_msg['answer'] = msg

                # return msg

            elif dict_receive['sender_msg'] == "每日一句" or dict_receive['sender_msg'] == "/5":
                jdm = True
                num = random.choice([1, 2, 3])
                print(num)
                if num == 1:
                    msg = api_group_1.wangyiyun()
                elif num == 2:
                    msg = api_group_1.philosophy_of_life()
                else:
                    msg = api_group_1.i_counted_the_days_on_earth()
                ans_msg['answer'] = msg
            elif dict_receive['sender_msg'] == "控制面板" or dict_receive['sender_msg'] == "copa":
                if '1732373074' == dict_receive['sender_id']:
                    jdm = True
                    time_run_2 = time.time()
                    time_run = (time_run_2 - time_run_1)/60
                    msg = '接收消息总数:' + str(count_msg_receive) +"\n"+ '运行总时长:'+ str(time_run)+"分钟\n"
                    ans_msg['answer'] = msg
                    # return msg
                else:
                    jdm = True
                    msg = '您的等级不够'
                    ans_msg['answer'] = msg


            else:  # 回答消息的第三优先级
                jdm = False
                # return None

    def get_API_answer_3(self):
        global jdm
        if jdm == False:
            urls = "https://v.api.aa1.cn/api/api-xiaoai/talk.php?msg={}".format(dict_receive['sender_msg'])
            answer_get = requests.get(url=urls).text
            soup = BeautifulSoup(answer_get,"lxml")
            line = soup.select("body p")
            msg = line[0].string
            ans_msg['answer'] = msg
            # return msg
        else:
            pass

    def get_answer(self):  # 多线程进行寻找回答，加快速度
        global jdm,dict_receive
        # print(1)


        sunm_1 = threading.Thread(target=answer_logic().get_API_answer_1())
        sunm_2 = threading.Thread(target=answer_logic().get_API_answer_2())

        sunm_1.start()
        # sunm_1.join()
        sunm_2.start()
        # sunm_2.join()

        sunm_3 = threading.Thread(target=answer_logic().get_API_answer_3())
        sunm_3.start()
        # sunm_3.join()
        msg = str(ans_msg['answer'])
        return msg

# ---------------------------------------------------------------------------------------------------
class receive_messages(Send_operation):  # 多群喊话中转站，因为启动喊话程序需要等待主人发送消息所以便需要循环等待消息发送
    def receive_(self):

        while True:
            # 提示准备接收消息
            Send_operation().Send_msg_answer()

            Listener_processing().main_Listener_processing()
            # 输出获取到的需要喊话的内容
            word = dict_receive['sender_msg']  # 获取要发送的消息
            # print(word)
            if word == '接收消息中......' or word == '':
                pass
            else:
                Send_operation().Send_msg_answer()
                return word


# ---------------------------------------------------------------------------------------------------

def ee():
    global ccm
    if ccm == True:
        pass
    else:
        answer_logic().get_answer()

        Send_operation().Send_msg_answer()


if __name__ == '__main__':
    while True:
        sun_1 = threading.Thread(target=Listener_processing().main_Listener_processing())
        sun_2 = threading.Thread(target=ee())
        sun_1.start()
        sun_2.start()
        sun_2.join()
