"""
DRA Studio 路径文件管理器
用于读取和解析台达 DRA Studio 的路径文件 (.drc, .rl)
"""

import os
import logging
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DRAPathManager:
    """DRA Studio 路径文件管理器"""
    
    def __init__(self, dra_projects_path: str = None, dra_extension: str = '.rl'):
        """
        初始化 DRA 路径管理器
        
        Args:
            dra_projects_path (str): DRA Studio 项目目录路径
            dra_extension (str): 路径文件扩展名 (.drc 或 .rl)
        """
        self.dra_projects_path = dra_projects_path or r'C:\DRA\Projects'
        self.dra_extension = dra_extension
        self.paths = {}  # {路径名: 路径编号}
        self.path_files = {}  # {路径名: 文件路径}
        
    def load_paths_from_directory(self) -> Dict[str, int]:
        """
        从指定目录扫描并加载路径文件
        
        Returns:
            Dict[str, int]: {路径名: 编号}
        """
        self.paths.clear()
        self.path_files.clear()
        
        if not os.path.exists(self.dra_projects_path):
            logger.warning(f"DRA 项目目录不存在: {self.dra_projects_path}")
            return {}
        
        try:
            files = os.listdir(self.dra_projects_path)
            path_files = [f for f in files if f.endswith(self.dra_extension)]
            
            for idx, filename in enumerate(sorted(path_files), 1):
                path_name = os.path.splitext(filename)[0]
                file_path = os.path.join(self.dra_projects_path, filename)
                
                self.paths[path_name] = idx
                self.path_files[path_name] = file_path
                logger.info(f"加载路径: {path_name} (编号: {idx})")
            
            logger.info(f"成功加载 {len(self.paths)} 个路径文件")
            return self.paths
            
        except Exception as e:
            logger.error(f"加载路径文件时出错: {e}")
            return {}
    
    def parse_drc_file(self, drc_file_path: str) -> List[str]:
        """
        解析 .drc 项目文件并提取路径列表
        DRC 文件通常是 XML 格式
        
        Args:
            drc_file_path (str): .drc 文件路径
            
        Returns:
            List[str]: 路径名称列表
        """
        paths = []
        
        try:
            if not os.path.exists(drc_file_path):
                logger.warning(f"DRC 文件不存在: {drc_file_path}")
                return paths
            
            # 尝试解析 XML
            tree = ET.parse(drc_file_path)
            root = tree.getroot()
            
            # 查找 Path 或 Path 相关的节点
            # 实际结构需根据 DRA Studio 版本调整
            for path_elem in root.findall('.//Path'):  # 递归查找
                path_name = path_elem.get('name') or path_elem.text
                if path_name:
                    paths.append(path_name)
            
            logger.info(f"从 {os.path.basename(drc_file_path)} 提取 {len(paths)} 个路径")
            return paths
            
        except ET.ParseError as e:
            logger.error(f"XML 解析错误 ({drc_file_path}): {e}")
            # 如果不是 XML，尝试文本模式
            return self._parse_drc_text(drc_file_path)
        except Exception as e:
            logger.error(f"解析 DRC 文件时出错: {e}")
            return paths
    
    def _parse_drc_text(self, drc_file_path: str) -> List[str]:
        """
        以文本模式解析 DRC 文件
        
        Args:
            drc_file_path (str): 文件路径
            
        Returns:
            List[str]: 路径列表
        """
        paths = []
        
        try:
            with open(drc_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # 查找可能的路径定义模式
                # 常见模式：Path="name" 或 <path name="name">
                import re
                
                # 尝试多种模式
                patterns = [
                    r'Path\s*=\s*["\']([^"\']+)["\']',
                    r'<path\s+name\s*=\s*["\']([^"\']+)["\']',
                    r'name\s*=\s*["\']([^"\']+)["\']',
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        paths.extend(matches)
                        break
            
            if paths:
                logger.info(f"从文本模式提取 {len(paths)} 个路径")
            
            return list(set(paths))  # 去重
            
        except Exception as e:
            logger.error(f"文本解析失败: {e}")
            return paths
    
    def get_available_paths(self) -> List[Tuple[str, int]]:
        """
        获取所有可用的路径
        
        Returns:
            List[Tuple[str, int]]: [(路径名, 编号), ...]
        """
        if not self.paths:
            self.load_paths_from_directory()
        
        return [(name, num) for name, num in sorted(self.paths.items(), key=lambda x: x[1])]
    
    def get_path_number(self, path_name: str) -> int:
        """
        获取路径的编号
        
        Args:
            path_name (str): 路径名称
            
        Returns:
            int: 路径编号 (0 表示未找到)
        """
        return self.paths.get(path_name, 0)
    
    def validate_path(self, path_name: str) -> bool:
        """
        验证路径是否存在
        
        Args:
            path_name (str): 路径名称
            
        Returns:
            bool: 路径是否有效
        """
        return path_name in self.paths
    
    def get_path_file(self, path_name: str) -> str:
        """
        获取路径文件的完整路径
        
        Args:
            path_name (str): 路径名称
            
        Returns:
            str: 文件路径
        """
        return self.path_files.get(path_name, "")


# 使用范例
if __name__ == "__main__":
    manager = DRAPathManager(dra_projects_path=r'C:\DRA\Projects')
    
    # 加载所有路径
    paths = manager.load_paths_from_directory()
    print(f"加载的路径: {paths}")
    
    # 获取所有可用路径
    available = manager.get_available_paths()
    print(f"可用路径: {available}")
    
    # 查询特定路径编号
    if available:
        path_name, path_num = available[0]
        print(f"路径 '{path_name}' 的编号是: {path_num}")
    
    # 解析 DRC 文件
    drc_path = r'C:\DRA\Projects\project.drc'
    paths_from_drc = manager.parse_drc_file(drc_path)
    print(f"DRC 中的路径: {paths_from_drc}")
