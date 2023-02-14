# 阅后自焚（Self-immolation after reading）

+ Messages表存储消息
+ RequestRecords表存储ip访问次数（防止暴力破解，每日有访问最大次数限制）
+ 数据存储在sqlite中


    消息阅后自焚，那天看了伪装者后心血来潮写的，记录灵感喷发。界面很简陋（只想用一个文件去实现），主要是为了记录其中的实现思想和方式。

# 使用该代码
+ python3.10
+ pip install -r .\requirements.txt
+ flask run --host=0.0.0.0 --port 9999
