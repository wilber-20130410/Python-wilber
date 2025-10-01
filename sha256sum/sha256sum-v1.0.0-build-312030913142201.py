'''
名称:LambdaTechnology恶意软件检查程序
作者:wilber-20130410
版权: © 2025 wilber-20130410
版本:1.0.0[312030913142201](正式版)
日期:2025.9.13
留言:
1.本代码仅供学习交流使用,请勿用于商业用途。
2.本代码参考了网络上部分代码,在此表示感谢。
3.使用前请确保已经安装以下所使用的库。
4.本人推荐使用Visual Studio Code或PyCharm Community作为IDE(集成开发环境)。
5.需要安装python3及以上python环境(本人使用python3.12.3)。
6.本代码无法直接使用，请在最后一行调整检查目录
7.如果您有建议、发现了Bug、问题或者您进行优化后的代码,欢迎向本人邮箱xuwb0410@163.com发送邮件,本人将在21天内进行回复。
8.LambdaTechnology的文件哈希值截至于发布日期北京时间14:00:00前的哈希值。
9.以上留言不分先后。
'''
# -*- coding: utf-8 -*-

import hashlib
import os
 
def cal_file_sha256(filt_path):
    with open(filt_path, "rb") as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(1024 * 1024):
            file_hash.update(chunk)
    return file_hash.hexdigest()
 
def cal_folder_hash(folder):
    sha256sum_list = ['fadd01f34c01054fbf7ff16e98e37f09f22350e9edfb7a700e65cb3c1980d5ff',
    '1cdd24510427248b26832e288a3598df0af81849b1910f996976def943508c9c',
    '24f21981b78db892a2648db35f96ec17741f11199abfe1aed1e37f440f45fadb',
    '4ca8cfef52bd3cd23f035752f94f6775de34921dd31123b927cee231fa44d277',
    'c06a75b13f855a94d46616796e024c52b499f8f92cf00ccb571ddbc6ff574676',
    'ce0796e4a6a8e06d7dddc41fd48b0d61d6a4a26bd5405f72564594faebc94c6e',
    '80fb018d305fa42b089518e743ac8af37329868c8bc39090419b8b5cbaf8c055',
    '245ff9031a96ef2ffade37bd506c2cf3e602747e29b80a41cb2be9f3c9691154',
    '944c7210ec31f2375a5ee27ec880434a81dc9e3514bf09aecbd6703d743b666e',
    '22d5a70d062707e58c110067d71ae2476fc14dff3630079dfec0e771ac577a81',
    'b398150f536e702e10208ddcffca28e06fb2742fb1c3f154d8bc41ffe7506b4d',
    'd7c42afc29bdb03be2bab6cedf9fc9621d3f631dca5170c5a010c43924dce838',
    '5e59a1c9e4ee98ccca669cfe758242d3a5e5bbf66f3470da1cf1444f1f8458d8',
    'ff471b9e8f004d3be4a9fba1cbc9d53cc4fb09277b780200e6c1cc2b5f413c1d',
    '5c9676b2501deb5432a733497c284aa9569405ee3af9c601b66e13889ea3a845',
    '4a7d3bd6cde2f4259d51ca2291be8caea1edda1f600ca9280b8ca6b823fb5d9d',
    '160c1077dbc47a5740e95bf34f722269d5c0f0f3b4e0431b6549c08b4f2df963',
    '24ea26a9439338b574f01f42774e1a4c0521c5835e6acae51067cb93916bffea',
    '372f41d401fa467da4a15435acc286f14225b335c13f30a98bf123429d72e2c4',
    '6fae07ff769adc757672c8849d9e39594fba02215821b47d43c2bf2dd8cafadd',
    '24afc7a2453ae39aed1b32dd8225450f6d1625d07fc63c7cf7f400f715780f08']
    if not os.path.exists(folder):
        print("Folder doesn't exist %s" % folder)
        return
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isdir(path):
            cal_folder_hash(path)
        else:
            print("File: %s" % path)
            sha256 = cal_file_sha256(path)
            print("SHA256: %s\n" % sha256)
        for sha256sum in sha256sum_list:
            if sha256sum == str(sha256):
                print("哈希值与列表中的哈希值匹配: %s ,为LambdaTechnology的程序\n" % sha256sum)

if __name__ == "__main__":
    cal_folder_hash("/path/to/you/file")
