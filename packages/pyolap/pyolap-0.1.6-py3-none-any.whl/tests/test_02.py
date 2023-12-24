from pyolap import euclidolap

# 如果使用容器内Python环境，IP地址填写 127.0.0.1 ！！！
# 如果使用本地Python，IP地址要修改为你的运行docker容器的服务器IP ！！！
olap_ctx = euclidolap.OlapContext("192.168.66.8", 8760)

# create_dimensions方法将返回一个list，其内部元素为Dimension类的实例
dimensions = olap_ctx.create_dimensions("日期", "地区", "商品", "支付方式")

for dimension in dimensions:
    print(f"{type(dimension)} - [{dimension.name}]维度已被创建")

olap_ctx.close()
