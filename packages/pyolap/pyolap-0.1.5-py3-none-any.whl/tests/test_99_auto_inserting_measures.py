import requests

from pyolap import euclidolap

# 如果使用容器内Python环境，IP地址填写 127.0.0.1 ！！！
# 如果使用本地Python，IP地址要修改为你的运行docker容器的服务器IP ！！！
olap_ctx = euclidolap.OlapContext("192.168.66.8", 8760)

cube = olap_ctx.get_cube_by_name("电商销售模型")
cube.voluntarily_generates_measures()

url = "https://sysbase.oss-cn-beijing.aliyuncs.com/电商销售模型度量数据.txt"
response = requests.get(url)
response.encoding = "UTF8"

if response.status_code == 200:
    print(response.text)
else:
    print("error")

olap_ctx.close()
