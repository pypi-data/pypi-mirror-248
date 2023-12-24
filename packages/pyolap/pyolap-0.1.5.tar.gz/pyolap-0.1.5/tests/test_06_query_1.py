from pyolap import euclidolap
from pyolap.euclidolap import OLAPQueryBuilder

# 如果使用容器内Python环境，IP地址填写 127.0.0.1 ！！！
# 如果使用本地Python，IP地址要修改为你的运行docker容器的服务器IP ！！！
olap_ctx = euclidolap.OlapContext("192.168.66.8", 8760)

query_builder = OLAPQueryBuilder()\
    .from_cube("电商销售模型")\
    .set_rows("[Measures].members()")\
    .set_columns("[日期].[2023].children()")

result = olap_ctx.query(query_builder)

print(result)

olap_ctx.close()
