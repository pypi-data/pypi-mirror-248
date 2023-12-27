AppVer="0.1.24"

# sed -i "s/^DkAppVer.*/DkAppVer = '$AppVer'/" ./setup.py

sed -i "s/^DkAppVer.*/DkAppVer = '$AppVer'/" ./src/dknovautils/dk_imports.py
sed -i "s/^DkAppVer.*/DkAppVer = '$AppVer'/" ./src/dknovautils/dkat.py

sed -i "s/^version =.*/version = '$AppVer'/" ./pyproject.toml

rm ./dist/*

python3 -m build

# python3 setup.py sdist build
export PATH=$PATH:~/.local/bin

# test repo
# python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload dist/*


#        输入用户名 密码 即可完成上传。


:<<EOF

在wsl 中执行
    cd ../dknovautils
    ./upload.sh

    会自动修改 相关文件中的版本号。运行脚本完成上传。 在wsl2中运行。

访问该网址进行注册：https://pypi.org/account/register/
pip账号 dknova dikisite@outlook.com pwd:zh


What is a Circular Import?

pip install -U dknovautils

from dknovautils.dkat import AT


在wsl2中安装beepy有错误

说找不到文件 alsa/asoundlib.h
安装一个开发库 sudo apt install libasound2-dev


升级到新的package结构

https://packaging.python.org/en/latest/tutorials/packaging-projects/

sudo apt-get install python3-venv

python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine


    pip服务器可能不再支持search功能
    python3 -m pip search dknovautils


    用如下命令安装特定版本的库 事实证明tuna的更新是明显滞后的 可能滞后一天以上的时间
    python3 -m pip install dknovautils==0.1.9 -i https://pypi.tuna.tsinghua.edu.cn/simple



EOF

