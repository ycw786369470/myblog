import time as t
from CDM.code import cdm_run
from clean_disk import format_disk
from H2.code import h2_run
from ATTO.code import atto_run
from AS_SSD.code import as_ssd_run
from PCMark.code import pcmark_run
from HDTune.code import hd_run
from IOmeter.code import iometer_run


tool_path = ''      # 配置工具文件目录
start = t.time()

# # 运行HDTune测试
# hd_run.main()
# print('HDTune测试完成！')
# t.sleep(5)
# format_disk.main()

# # 运行CDM所有版本
# cdm_run.cdm()
# print('CDM测试完成！')
# t.sleep(1)
# format_disk.main()
# t.sleep(1)

# # 运行h2testw1.4
# h2_run.main()
# print('H2测试完成！')
# t.sleep(1)
# format_disk.main()
# t.sleep(1)

# # 运行ATTO测试
# atto_run.main()
# print('ATTO测试完成')
# t.sleep(1)
# format_disk.main()
# t.sleep(1)



# # 运行PCMark测试
# pcmark_run.main()
# print('PCMark测试完成！')
# t.sleep(1)
# format_disk.main()
# t.sleep(1)

# # 运行IOMeter测试
# iometer_run.iometer_0()
# t.sleep(1)
# iometer_run.iometer_10G()
# print('IOMeter测试完成！')
# t.sleep(1)
# format_disk.main()
# t.sleep(1)

elapsed = (t.time() - start)
print("Time used:", elapsed)
