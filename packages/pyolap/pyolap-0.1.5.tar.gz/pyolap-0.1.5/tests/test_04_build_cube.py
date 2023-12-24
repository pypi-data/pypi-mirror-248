from pyolap import euclidolap

# 如果使用容器内Python环境，IP地址填写 127.0.0.1 ！！！
# 如果使用本地Python，IP地址要修改为你的运行docker容器的服务器IP ！！！
olap_ctx = euclidolap.OlapContext("192.168.66.8", 8760)

date_dimension = olap_ctx.get_dimension_by_name("日期")
region_dimension = olap_ctx.get_dimension_by_name("地区")
goods_dimension = olap_ctx.get_dimension_by_name("商品")
pay_dimension = olap_ctx.get_dimension_by_name("支付方式")

cube = olap_ctx.build_cube("电商销售模型",
                           [date_dimension, region_dimension, goods_dimension, pay_dimension],
                           ["销售额", "销售数量"])

olap_ctx.close()
