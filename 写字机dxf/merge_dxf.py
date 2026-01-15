import ezdxf
from ezdxf.addons import Importer

def merge_with_offset(source_doc, target_doc, offset_x=0, offset_y=0):
    """
    将 source_doc 的模型空间内容导入 target_doc，并整体偏移 (offset_x, offset_y)
    """
    # 创建一个临时文档，用于预处理偏移
    temp_doc = ezdxf.new(dxfversion=target_doc.dxfversion)
    
    # 复制源文档的模型空间到临时文档
    source_msp = source_doc.modelspace()
    temp_msp = temp_doc.modelspace()
    
    # 克隆所有实体并添加到临时文档（同时应用偏移）
    for entity in source_msp:
        try:
            new_entity = entity.copy()  # 复制实体
            # 应用偏移
            move_entity(new_entity, offset_x, offset_y)
            temp_msp.add_entity(new_entity)
        except Exception as e:
            print(f"跳过无法复制或移动的实体 {entity.dxftype()}: {e}")
            continue

    # 现在用 Importer 将临时文档导入目标文档（此时已偏移）
    importer = Importer(temp_doc, target_doc)
    importer.import_modelspace()
    importer.finalize()

def move_entity(entity, dx, dy):
    """应用 XY 平移"""
    if entity.dxftype() == 'LWPOLYLINE':
        # LWPOLYLINE 的点存储在 vertices 属性中（不是 dxf 属性）
        points = []
        for x, y, start_width, end_width, bulge in entity.get_points():
            points.append((x + dx, y + dy, start_width, end_width, bulge))
        entity.set_points(points)



# --- 主程序 ---
base_dxf = ezdxf.new()
spacing = 400
current_x = 0
current_y = 0

# +x向右 +y向上
with open('input.txt', 'r', encoding='utf-8') as input:
    a = input.read()
for i in a:
    if i == '\n':
        print('huanhang')
        current_x=0
        current_y-=spacing
    elif i == ' ':
        current_x+=spacing/2
    else:
        try:
            file_dxf = ezdxf.readfile('Chinese_User/'+ i +'.dxf')
            current_x += spacing
            merge_with_offset(file_dxf, base_dxf, offset_x=current_x, offset_y=current_y)
        except Exception as e:
            print(f"合并文字 {i} 失败: {e}")

base_dxf.saveas('output.dxf')
print("合并并分散排列完成！")
