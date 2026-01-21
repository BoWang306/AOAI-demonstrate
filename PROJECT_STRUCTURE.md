# 项目结构

## 目录组织

```
webapp/
├── lib/                        # 核心逻辑库
│   ├── __init__.py
│   ├── api_client.py          # Azure OpenAI API 客户端
│   ├── config_manager.py      # 配置管理
│   └── models.py              # 模型定义和常量
│
├── utils/                      # UI 工具库
│   ├── __init__.py
│   ├── styles.py              # CSS 样式
│   └── ui_components.py       # 可复用 UI 组件
│
├── pages/                      # Streamlit 多页面
│   └── 1_🔧_模型配置管理.py   # 配置管理页面
│
├── .devcontainer/             # Dev Container 配置
│   ├── Dockerfile
│   ├── devcontainer.json
│   └── README.md
│
├── app.py                     # 主应用入口
├── model_configs.json         # 模型配置文件
├── test_cases_example.json    # 测试用例示例
├── config_helper.py           # 配置助手（遗留）
├── demo.py                    # 演示脚本（遗留）
├── README.md                  # 项目说明
└── requirements.txt           # 依赖列表
```

## 核心模块说明

### lib/ - 核心逻辑库

#### api_client.py
- `AzureOpenAIClient`: API 客户端类
  - `chat_completion()`: 调用聊天完成 API
  - `test_connection()`: 测试连接
  - `_parse_error()`: 解析和友好化错误信息

#### config_manager.py
- `ConfigManager`: 配置管理类
  - `load_configs()`: 加载配置文件
  - `save_configs()`: 保存配置文件
  - `validate_endpoint()`: 验证 endpoint 格式
  - `validate_api_key()`: 验证 API key
  - `add_config()`: 添加配置
  - `update_config()`: 更新配置
  - `delete_config()`: 删除配置
  - `copy_config()`: 复制配置

#### models.py
- `AVAILABLE_MODELS`: 可用模型列表
- `REASONING_SUPPORTED_MODELS`: 支持推理的模型
- `REASONING_EFFORTS`: 推理级别选项
- `REASONING_HELP`: 推理帮助信息

### utils/ - UI 工具库

#### styles.py
- `CUSTOM_CSS`: 统一的自定义 CSS 样式

#### ui_components.py
- `display_error()`: 显示友好错误信息
- `display_metrics()`: 显示性能指标
- `display_config_details()`: 显示配置详情

## 页面架构

### app.py - 主页面
- 首页和主要功能入口
- 4 个功能标签页：
  1. 💬 聊天测试
  2. 📝 单次调用
  3. 📊 批量测试
  4. 📖 模型信息

### pages/1_🔧_模型配置管理.py
- 独立的配置管理页面
- 功能：添加、编辑、删除、复制、测试配置
- 导入导出配置

## 设计原则

### 1. 关注点分离
- **逻辑层** (lib/): 纯业务逻辑，不依赖 UI
- **展示层** (pages/): UI 展示，调用逻辑层
- **工具层** (utils/): 可复用的 UI 组件

### 2. 模块化
- 每个模块职责单一明确
- 模块间低耦合
- 易于测试和维护

### 3. 可扩展性
- 新增模型：只需修改 `lib/models.py`
- 新增页面：在 `pages/` 目录添加新文件
- 新增 UI 组件：在 `utils/ui_components.py` 添加

### 4. Streamlit 最佳实践
- 遵循 Streamlit 多页面应用规范
- 使用 session_state 管理状态
- 页面独立，可单独运行

## 使用说明

### 开发新功能

1. **添加新的业务逻辑**
   ```python
   # 在 lib/ 创建新模块
   # lib/new_feature.py
   class NewFeature:
       def do_something(self):
           pass
   ```

2. **添加新页面**
   ```python
   # 在 pages/ 创建新文件
   # pages/2_🎯_新功能.py
   import streamlit as st
   from lib.new_feature import NewFeature
   
   st.title("新功能")
   # ... 页面代码
   ```

3. **添加 UI 组件**
   ```python
   # 在 utils/ui_components.py 添加
   def display_new_component(data):
       st.markdown(...)
   ```

### 测试

```bash
# 运行主应用
streamlit run app.py

# 单独测试某个页面
streamlit run pages/1_🔧_模型配置管理.py
```

### 代码规范

- 使用类型提示
- 函数添加文档字符串
- 变量命名清晰明确
- 遵循 PEP 8 规范

## 依赖管理

主要依赖：
- `streamlit`: Web 应用框架
- `openai`: Azure OpenAI Python SDK

安装依赖：
```bash
pip install -r requirements.txt
```
