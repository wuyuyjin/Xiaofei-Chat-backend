import os
from qiniu import Auth, put_file, etag

def upload_to_qiniu(local_file_path):
    # 设置七牛云的 Access Key 和 Secret Key
    access_key = 'CX_D80jzVT8EJTA25VO2c1zjS62iRxFFvGr66lqq'
    secret_key = 'ZGbvi12n4-AIy7xvn60uNk0kDE-qYbtzTKSEAXTm'

    # 设置要上传的七牛云空间名称
    bucket_name = 'wyjchat'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 获取文件名作为上传的 key
    file_name = os.path.basename(local_file_path)
    key = file_name

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 上传文件
    ret, info = put_file(token, key, local_file_path)

    # 打印上传结果信息
    print(info)

    # 校验上传结果
    assert ret['key'] == key
    assert ret['hash'] == etag(local_file_path)
