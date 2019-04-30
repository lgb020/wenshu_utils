## 裁判文书相关解析/解密工具
开源自己之前爬文书写的相关工具  
截止到2019.04.30, 文书网现存的反爬参数基本都能在这找到  
除了RunEval和wzws_cid的解析依赖nodejs, 其他参数均用Python实现

### 环境
1. python3.6+(如果低于3.6会报错, 例: f-string特性. 如有需要请自行修改兼容其他版本python)
2. 安装requirements.txt
3. nodejs(外部依赖)

### 使用方法
参考demo.py 或 tests/里的测试用例 

### 测试
手动运行tests/里的测试用例

或

通过pytest测试
```bash
pip install pytest
pytest
```

或

通过docker构建测试
```bash
docker build -t wenshu_utils .  # 构建镜像
docker run --rm wenshu_utils    # 运行
```
