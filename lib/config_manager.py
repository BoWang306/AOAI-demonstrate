"""
配置管理模块
负责加载、保存、验证模型配置
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
import re


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "model_configs.json"):
        self.config_file = Path(config_file)
    
    def load_configs(self) -> List[Dict]:
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {str(e)}")
                return []
        return []
    
    def save_configs(self, configs: List[Dict]) -> bool:
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(configs, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {str(e)}")
            return False
    
    def validate_endpoint(self, endpoint: str) -> bool:
        """验证 endpoint 格式"""
        pattern = r'^https?://[a-zA-Z0-9][-a-zA-Z0-9.]*[a-zA-Z0-9]\.(openai\.azure\.com|azure\.com)'
        return bool(re.match(pattern, endpoint))
    
    def validate_api_key(self, api_key: str) -> bool:
        """验证 API key 格式"""
        return bool(api_key and len(api_key) >= 32)
    
    def get_config_by_id(self, configs: List[Dict], config_id: int) -> Optional[Dict]:
        """根据 ID 获取配置"""
        return next((c for c in configs if c['id'] == config_id), None)
    
    def get_unique_config_id(self, configs: List[Dict]) -> int:
        """生成唯一的配置 ID"""
        if not configs:
            return 1
        return max([c.get('id', 0) for c in configs]) + 1
    
    def add_config(self, configs: List[Dict], new_config: Dict) -> List[Dict]:
        """添加新配置"""
        new_config['id'] = self.get_unique_config_id(configs)
        configs.append(new_config)
        return configs
    
    def update_config(self, configs: List[Dict], config_id: int, updated_config: Dict) -> List[Dict]:
        """更新配置"""
        for i, conf in enumerate(configs):
            if conf['id'] == config_id:
                updated_config['id'] = config_id
                configs[i] = updated_config
                break
        return configs
    
    def delete_config(self, configs: List[Dict], config_id: int) -> List[Dict]:
        """删除配置"""
        return [c for c in configs if c['id'] != config_id]
    
    def copy_config(self, configs: List[Dict], config_id: int) -> List[Dict]:
        """复制配置"""
        config = self.get_config_by_id(configs, config_id)
        if config:
            new_config = config.copy()
            new_config['id'] = self.get_unique_config_id(configs)
            new_config['model_name'] = f"{config['model_name']}-copy"
            configs.append(new_config)
        return configs
