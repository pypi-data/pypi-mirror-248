## 安装

```bash
pip install long-utils
```

### 图中找图
```python
from long_utils.image.search import ImgFindImg

img = ImgFindImg(img_source='static/big.png', img_search='static/small.png')
img.find_coord(is_debug=True)

# 或者只拿取小图在原图中的坐标rectangle, 小图在原图中的大小result，confidence表示准确率
res = img.find_coord()
# [{'result': (539.0, 21.5), 'rectangle': ((524, 10), (524, 33), (554, 10), (554, 33)), 'confidence': 1.0}]
print(res)
```

### 简单日志输出
```bash
```python
from long_utils import logger

logger.error(message="xxxx")
logger.success(message="xxxx")
logger.warning(message="xxxx")
logger.info(message="xxxx")
logger.debug(message="xxxx")

logger.success_bg('xxxx')
logger.error_bg('xxxx')
logger.warning_bg('xxxx')
logger.debug_bg('xxxx')
logger.info_bg('xxxx')
logger.color('xxxx', fg='blue', bg='black')
```






