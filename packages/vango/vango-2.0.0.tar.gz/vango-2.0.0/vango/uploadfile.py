# _*_ coding:utf-8 _*_

"""python
Created on 2023/12/27
@author: Jan
@theme:超大文件读取与存储
"""

import os
from smb.SMBConnection import SMBConnection
from smb.smb_structs import OperationFailure
import json
import requests

BASE_URL = 'http://mvango.37wan.com'

'''
建立smb服务连接
:param user_name:
:param passwd:
:param ip:
:param port: 445或者139
:return:
'''
def connect(user_name, passwd, ip, port):
    samba = None
    status = False
    try:
        samba = SMBConnection(user_name, passwd, '', '', use_ntlm_v2=True)
        samba.connect(ip, port)
        status = samba.auth_result

    except:
        samba.close()
    return samba, status


'''
返回samba server上的文件更新时间（时间戳），如果出现OperationFailure说明无此文件，返回0
:param samba:
:param service_name:
:param file_path:
:return:
'''
def get_last_updatetime(samba, full_file_path, service_name, sub_path):
    try:
        f_name = os.path.basename(full_file_path)
        smb_file_path = os.path.join(sub_path, f_name)
        return 1, smb_file_path, os.path.getsize(full_file_path), f_name
        sharedfile_obj = samba.getAttributes(service_name, smb_file_path)
        return sharedfile_obj.last_write_time, smb_file_path, os.path.getsize(full_file_path), f_name
    except OperationFailure:
        return 0, "", 0, ""


def createMultistageDir(samba, service_name, smb_path):
    dirs = smb_path.split('/')
    for i in range(1, len(dirs) + 1):
        try:
            samba.createDirectory(service_name, '/'.join(dirs[:i]))
        except:
            pass  # 如果目录已存在，忽略错误


def upload_file_to_service(samba, path, service_name, result, sub_path):
    if os.path.isfile(path) and not os.path.basename(path).startswith("."):
        handle_file_upload(samba, path, service_name, sub_path)
        timestamp, smb_file_path, file_size, show_name = get_last_updatetime(samba, path, service_name, sub_path)
        if timestamp != 0:
            sub_file_path = smb_file_path
            if sub_file_path.startswith('/'):
                sub_file_path = sub_file_path.lstrip('/')
            result_item = {
                "name": service_name + "/" + sub_file_path,
                "size": file_size,
                "success": "true",
                "show_name": show_name
            }
            result.append(result_item)

    elif os.path.isdir(path):
        if not sub_path.endswith('/'):
            sub_path += '/'
        sub_path += os.path.basename(path) + "/"
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path) and not filename.startswith("."):
                handle_file_upload(samba, file_path, service_name, sub_path)
                timestamp, smb_file_path, file_size, show_name = get_last_updatetime(samba, file_path, service_name,
                                                                                     sub_path)
                if timestamp != 0:
                    sub_file_path = smb_file_path
                    if sub_file_path.startswith('/'):
                        sub_file_path = sub_file_path.lstrip('/')
                    result_item = {
                        "name": service_name + "/" + sub_file_path,
                        "size": file_size,
                        "success": "true",
                        "show_name": show_name
                    }
                    result.append(result_item)
            elif os.path.isdir(file_path):
                upload_file_to_service(samba, file_path, service_name, result, sub_path)
    else:
        print("The path is not a valid file or directory")


'''
上传文件
:param service_name: 服务名（smb中的文件夹名）
:param full_file_path: 文件的全路径
:return: None
'''
def handle_file_upload(samba, full_file_path, service_name, sub_path):
    try:
        if not os.path.isfile(full_file_path):
            print('File {full_file_path} does not exist.')
            return
        # 不存在则创建
        createMultistageDir(samba, service_name, sub_path)

        file_size = os.path.getsize(full_file_path)
        f_name = os.path.basename(full_file_path)
        smb_file_path = os.path.join(sub_path, f_name)


        if file_size <= 1024 * 1024 * 1024:  # 小于或等于1GB
            with open(full_file_path, 'rb') as f:
                samba.storeFile(service_name, smb_file_path, f)
        else:
            with open(full_file_path, 'rb') as fp:
                offset = 0
                while True:
                    chunk_data = fp.read(10 * 1024 * 1024)
                    if not chunk_data:
                        break
                    samba.storeFileFromOffset(service_name, smb_file_path, fp, offset)
                    offset += len(chunk_data)
    except Exception as e:
        print('Error with upload: {e}')



def _get_user_info():
    if os.path.exists(r"c:\tmp\user.txt"):
        userFile = r"c:\tmp\user.txt"
    elif os.path.exists(r"C:\tmp\user.txt"):
        userFile = r"C:\tmp\user.txt"
    else:
        userFile = r'./user.txt'
    user = []
    if os.path.exists(userFile):
        with open(userFile, 'r') as f:
            userInfo = f.read()
            f.close()
            user = userInfo.split(' ')
    return user


# 上传资产文件
# path 本地文件路径 必填
# code 资产编号 必填
# asset_name 资产中文名 必填
# asset_project 资产项目 必填
# options 额外参数 非必填
def upload_asset_files(path, code, asset_name, asset_project, options):
    response = {"code": 0, "message": "", "data":[]}
    token, err = get_user_token()
    if len(token) == 0 or not token:
        response["message"] = err
        return response
    # 先获取资产的详情
    asset_info = get_asset_detail(token, asset_name, code, asset_project, options)
    if asset_info["code"] != 1:
        response["message"] = '获取资产(' + asset_name + ')详情失败,原因:' + asset_info["message"]
        return response
    # 获取到详情之后，开始上传 # samba, full_file_path, service_name, sub_path
    samba, status = connect(asset_info["data"]["smb_info"]["user_name"],
                            asset_info["data"]["smb_info"]["user_pwd"],
                            asset_info["data"]["smb_info"]["smb_host"],
                            asset_info["data"]["smb_info"]["smb_port"])
    if not status:
        response["message"] = 'smb服务器连接失败！'
        return response
    service_name = asset_info["data"]["share_name"]
    sub_path = asset_info["data"]["upload_path"]
    asset_id = asset_info["data"]["asset_id"]
    result = []
    upload_file_to_service(samba, path, service_name, result, sub_path)
    if len(result) > 0:
        # 执行回调处理
        asset_callback = upload_asset_file_callback(token, asset_id, asset_name, result)
        if asset_callback["code"] != 1:
            response["message"] = '资产(' + asset_name + ')回调失败,原因:' + asset_callback["message"]
            return response
    response["code"] = 1
    response["message"] = "success"
    response["data"] = result
    return response


# 资产文件上传回调
# asset_id    资产ID      必填
# name        资产中文名   必填
# result      文件数组     必填
def upload_asset_file_callback(token, asset_id, asset_name, result):
    params = {"asset_id": asset_id, "name": asset_name, "file_type": 1, "files": result}
    headers = {"Authorization": "Bearer " + token}
    url = BASE_URL + '/api/asset/openapi_upload_callback'

    response = requests.post(url=url, json=params, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    return response.json()


# 获取资产的详细信息
# name          任务中文名      必填
# code          资产编号        必填
# asset_project 资产项目        选填
# options       额外参数        非必填
def get_asset_detail(token, name, code, asset_project, options):
    params = {"code": code, "name": name, "asset_project": asset_project, "options": json.dumps(options)}
    headers = {"Authorization": "Bearer " + token}
    url = BASE_URL + '/api/asset/openapi_info'

    response = requests.post(url=url, data=params, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    return response.json()





# 获取任务的详细信息
# name          任务中文名      必填
# code          资产编号        必填
# project_name  项目名称        选填
# asset_project 资产项目        选填
# options       额外参数        非必填
def get_task_detail(name, code, project_name, asset_project, options):
    response = {"code": 0, "message": "", "data": []}
    token, err = get_user_token()
    if len(token) == 0 or not token:
        response["message"] = err
        return response

    params = {"code": code, "name": name, "project_name": project_name, "asset_project": asset_project,
              "options": options}
    headers = {"Authorization": "Bearer " + token}
    url = BASE_URL + '/api/task/openapi_detail'

    response = requests.get(url=url, params=params, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    return response.json()


# 上传文件
# task_id    任务ID      必填
# file_path  本地文件路径 必填
# options    额外参数     非必填
def upload_task_file(task_id, file_path, options):
    response = {"code": 0, "message": "", "data": []}
    token, err = get_user_token()
    if len(token) == 0 or not token:
        response["message"] = err
        return response

    # 获取任务的上传路径
    task_path_info = get_task_path_info(task_id)
    if task_path_info["code"] != 1:
        response["message"] = '获取任务(' + task_id + ')路径信息失败,原因:' + task_path_info["message"]
        return response

    samba, status = connect(task_path_info["data"]["smb_info"]["user_name"],
                            task_path_info["data"]["smb_info"]["user_pwd"],
                            task_path_info["data"]["smb_info"]["smb_host"],
                            task_path_info["data"]["smb_info"]["smb_port"])
    if not status:
        response["message"] = 'smb服务器连接失败！'
        return response

    service_name = task_path_info["data"]["root_path"]
    sub_path = task_path_info["data"]["upload_path"]
    version = task_path_info["data"]["version"]
    asset_id = task_path_info["data"]["asset_id"]
    pipeline_id = task_path_info["data"]["pipeline_id"]

    result = []
    upload_file_to_service(samba, file_path, service_name, result, sub_path)
    if len(result) > 0:
        # 执行回调处理
        task_callback = upload_task_file_callback(token, task_id, options["file_type"], result, version, asset_id, pipeline_id)
        if task_callback["code"] != 1:
            response["message"] = '任务(' + task_id + ')回调失败,原因:' + task_callback["message"]
            return response

    response["code"] = 1
    response["data"] = result
    return response


# 任务文件上传回调
# task_id      任务ID      必填
# file_type    资产中文名   必填
# result       文件数组     必填
# version      版本号       必填
# asset_id     资产ID       必填
# pipeline_id  任务流程ID    必填
def upload_task_file_callback(token, task_id, file_type, result, version, asset_id, pipeline_id):
    params = {"task_id": task_id, "version": version, "file_type": file_type, "task_files": result, "asset_id": asset_id,
              "pipeline_id": pipeline_id}
    headers = {"Authorization": "Bearer " + token}
    url = BASE_URL + '/api/task/file_upload_callback'

    response = requests.post(url=url, json=params, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    return response.json()


# 获取任务的详细信息
# name          任务中文名      必填
# code          资产编号        必填
# project_name  项目名称        选填
# asset_project 资产项目        选填
# options       额外参数        非必填
def get_task_path_info(task_id):
    token, err = get_user_token()
    if len(token) == 0 or not token:
        print(err)
        return ""

    params = {"task_id": task_id}
    headers = {"Authorization": "Bearer " + token}
    url = BASE_URL + '/api/task/openapi_file_upload_info'

    response = requests.post(url=url, json=params, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    return response.json()

# 1、获取token
def get_user_token():
    user = _get_user_text()
    name = ''
    account = ''
    if user[0]:
        name = user[0]
    if len(user) > 1 and user[1]:
        account = user[1]
    if len(name) == 0 or len(account) == 0:
        return "", "个人信息获取失败"

    params = {"user_name": name, "login_account": account}
    url = BASE_URL + '/api/auth/token'

    response = requests.post(url=url, data=params)
    if response.status_code == 200:
        response_data = json.loads(response.text)
        if response_data["code"] == 1:
            return response_data['data']['token'], ""
    return "", ""


def _get_user_text():
    if os.path.exists(r"c:\tmp\user.txt"):
        userFile = r"c:\tmp\user.txt"
    elif os.path.exists(r"C:\tmp\user.txt"):
        userFile = r"C:\tmp\user.txt"
    else:
        userFile = r'./user.txt'
    user = []
    if os.path.exists(userFile):
        with open(userFile, 'r') as f:
            userInfo = f.read()
            f.close()
            user = userInfo.split(' ')
    return user