

# show_device 每页的数量
SHOW_PAGE_SIZE = 15
# device_search 每页的大小
SEARCH_PAGE_SIZE = 18
# 设备展示的列名
DEVICE_SHOW_COLUMN_NAMES = [
    '设备编号',
    '设备品牌',
    '设备型号',
    '上市年份',
    '分辨率',
    '固件版本',
    '卡片形态',
    '卡槽',
    '状态'
]
# 需求表列名
DEMAND_LIST = [
    '序号',
    '编号',
    '品牌',
    '型号',
    '卡槽',
    '版本',
    '搭配',
    '分辨率',
]
# 样品信息列名
SAMPLE_INFO_LIST = [
    '需求发起人',
    '',
    '搭&emsp;&emsp;&emsp;配',
    # '版&emsp;&emsp;&emsp;本',
    '料&emsp;&emsp;&emsp;号',
    '&ensp;样品数量&ensp;',
    '&ensp;测试周期&ensp;',
    '上传',
    '兼容性测试版本',
    '备&emsp;&emsp;&emsp;注',

]

# 搭配对应
MASTER_CONTROL = 0
FLASH = 1
DIE = 2
COLLO_TYPES_CHOICES = (
    (MASTER_CONTROL, '主控'),
    (FLASH, 'flash'),
    (DIE, 'die'),
)

