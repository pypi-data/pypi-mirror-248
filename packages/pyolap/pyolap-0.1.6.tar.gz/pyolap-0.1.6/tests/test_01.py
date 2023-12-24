from pyolap import euclidolap

olap_ctx = euclidolap.OlapContext("192.168.66.8", 8760)

olap_ctx.close()




def print_aligned_matrix(matrix):
    if not matrix or not matrix[0]:
        print("Empty matrix.")
        return
    # 获取每列的最大字符宽度
    column_widths = [max(len(str(matrix[row][col])) for row in range(len(matrix))) for col in range(len(matrix[0]))]
    # 打印二维数组
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            # 使用字符串格式化来对齐输出
            print("{:>{width}}".format(matrix[row][col], width=column_widths[col]), end="  ")
        print()

# 示例用法
example_matrix = [
    [1, '非ASCII字符', 3],
    ['A', 'B', 'C'],
    ['X', 'Y', 'Z']
]

print_aligned_matrix(example_matrix)

print("########################################################")

def get_element_width(element):
    # 计算字符串长度，考虑 Unicode 字符宽度
    return sum(2 if ord(char) > 255 else 1 for char in str(element))

def print_list_element_width(my_list):
    for element in my_list:
        width = get_element_width(element)
        print(f"Element: {element}, Width: {width}")

# 示例 list
my_list = ['Hello', '你好', '😊']

# 打印每个元素的字符宽度
print_list_element_width(my_list)
