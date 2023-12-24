from pyolap import euclidolap

date_members_info = [
    ["2023", "Q1", "M1"],
    ["2023", "Q1", "M2"],
    ["2023", "Q1", "M3"],
    ["2023", "Q2", "M4"],
    ["2023", "Q2", "M5"],
    ["2023", "Q2", "M6"],
    ["2023", "Q3", "M7"],
    ["2023", "Q3", "M8"],
    ["2023", "Q3", "M9"],
    ["2023", "Q4", "M10"],
    ["2023", "Q4", "M11"],
    ["2023", "Q4", "M12"]
]

region_members_info = ["北京", "天津", "上海", "重庆", "广州", "深圳", "杭州", "苏州"]

goods_members_info = [
    ["游戏机", "PS"],
    ["游戏机", "XBOX"],
    ["游戏机", "Switch"],
    ["体育用品", "山地自行车"],
    ["体育用品", "皮划艇"],
    ["体育用品", "足球"]
]

pay_members_info = ["信用卡", "微信", "支付宝"]

# 如果使用容器内Python环境，IP地址填写 127.0.0.1 ！！！
# 如果使用本地Python，IP地址要修改为你的运行docker容器的服务器IP ！！！
olap_ctx = euclidolap.OlapContext("192.168.66.8", 8760)

date_dimension = olap_ctx.get_dimension_by_name("日期")
date_dimension.create_members(date_members_info)

region_dimension = olap_ctx.get_dimension_by_name("地区")
region_dimension.create_members(region_members_info)

goods_dimension = olap_ctx.get_dimension_by_name("商品")
goods_dimension.create_members(goods_members_info)

pay_dimension = olap_ctx.get_dimension_by_name("支付方式")
pay_dimension.create_members(pay_members_info)

olap_ctx.close()
