# 扫码点餐系统后台
---
## 使用方法
- 启动服务器
    ```
    cd code
    virtualenv -p /usr/bin/python3 --no-site-packages venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    gunicorn -w 4 -b 0.0.0.0:5000 manage:app
    ```
- 打开浏览器，输入地址
    ```
    <ip>:5000/
    ```
    - 其中\<ip\>是web后台所在机器的IP地址
- 浏览器显示
    ```
    OK
    ```

