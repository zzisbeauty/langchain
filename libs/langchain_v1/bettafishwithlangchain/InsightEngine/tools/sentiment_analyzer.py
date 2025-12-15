""" 多语言情感分析工具  基于WeiboMultilingualSentiment模型为InsightEngine提供情感分析功能
"""

import re
import os
import sys
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass

try:
    import torch
    TORCH_AVAILABLE = True
    torch.classes.__path__ = []
except ImportError:
    torch = None  # type: ignore
    TORCH_AVAILABLE = False


try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification

    TRANSFORMERS_AVAILABLE = True
except ImportError:
    AutoTokenizer = None  # type: ignore
    AutoModelForSequenceClassification = None  # type: ignore
    TRANSFORMERS_AVAILABLE = False


# INFO：若想跳过情感分析，可手动切换此开关为False
SENTIMENT_ANALYSIS_ENABLED = True


def _describe_missing_dependencies() -> str:
    missing = []
    if not TORCH_AVAILABLE:
        missing.append("PyTorch")
    if not TRANSFORMERS_AVAILABLE:
        missing.append("Transformers")
    return " / ".join(missing)



# 添加项目根目录到路径，以便导入WeiboMultilingualSentiment
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
weibo_sentiment_path = os.path.join(
    project_root, "SentimentAnalysisModel", "WeiboMultilingualSentiment"
)
sys.path.append(weibo_sentiment_path)



@dataclass
class SentimentResult:
    """情感分析结果数据类"""

    text: str
    sentiment_label: str
    confidence: float
    probability_distribution: Dict[str, float]
    success: bool = True
    error_message: Optional[str] = None
    analysis_performed: bool = True


@dataclass
class BatchSentimentResult:
    """批量情感分析结果数据类"""

    results: List[SentimentResult]
    total_processed: int
    success_count: int
    failed_count: int
    average_confidence: float
    analysis_performed: bool = True



class WeuboMultilingualSentimentAnalyzer:
    """ 多语言情感分析器 封装WeiboMultilingualSentiment模型，为AI Agent提供情感分析功能
    """

    def __init__(self):
        """初始化情感分析器"""
        self.model = None
        self.tokenizer = None
        self.device = None
        self.is_initialized = False
        self.is_disabled = False
        self.disable_reason: Optional[str] = None
    
        # 情感标签映射（5级分类）
        self.sentiment_map = {
            0: "非常负面",
            1: "负面",
            2: "中性",
            3: "正面",
            4: "非常正面",
        }

        if not SENTIMENT_ANALYSIS_ENABLED:
            self.disable("情感分析功能已在配置中关闭。")
        elif not (TORCH_AVAILABLE and TRANSFORMERS_AVAILABLE):
            missing = _describe_missing_dependencies() or "未知依赖"
            self.disable(f"缺少依赖: {missing}，情感分析已禁用。")

        if self.is_disabled:
            reason = self.disable_reason or "Sentiment analysis disabled."
            print(f"WeiboMultilingualSentimentAnalyzer initialized but disabled: {reason}")
        else:
            print("WeiboMultilingualSentimentAnalyzer 已创建，调用 initialize() 来加载模型")

    def disable(self, reason: Optional[str] = None, drop_state: bool = False) -> None:
        """Disable sentiment analysis, optionally clearing loaded resources."""
        self.is_disabled = True
        self.disable_reason = reason or "Sentiment analysis disabled."
        if drop_state:
            self.model = None
            self.tokenizer = None
            self.device = None
            self.is_initialized = False

            
    def enable(self) -> bool:
        """Attempt to enable sentiment analysis; returns True if enabled."""
        if not SENTIMENT_ANALYSIS_ENABLED:
            self.disable("情感分析功能已在配置中关闭。")
            return False
        if not (TORCH_AVAILABLE and TRANSFORMERS_AVAILABLE):
            missing = _describe_missing_dependencies() or "未知依赖"
            self.disable(f"缺少依赖: {missing}，情感分析已禁用。")
            return False
        self.is_disabled = False
        self.disable_reason = None
        return True

    def _select_device(self):
        """Select the best available torch device."""
        if not TORCH_AVAILABLE:
            return None
        assert torch is not None
        if torch.cuda.is_available():
            return torch.device("cuda")
        mps_backend = getattr(torch.backends, "mps", None)
        if (
            mps_backend
            and getattr(mps_backend, "is_available", lambda: False)()
            and getattr(mps_backend, "is_built", lambda: False)()
        ):
            return torch.device("mps")
        return torch.device("cpu")



    def initialize(self) -> bool:
        """ 初始化模型和分词器
        Returns:
            是否初始化成功
        """
        if self.is_disabled:
            reason = self.disable_reason or "情感分析功能已禁用"
            print(f"情感分析功能已禁用，跳过模型加载：{reason}")
            return False

        if not (TORCH_AVAILABLE and TRANSFORMERS_AVAILABLE):
            missing = _describe_missing_dependencies() or "未知依赖"
            self.disable(f"缺少依赖: {missing}，情感分析已禁用。", drop_state=True)
            print(f"缺少依赖: {missing}，无法加载情感分析模型。")
            return False

        if self.is_initialized:
            print("模型已经初始化，无需重复加载")
            return True

        try:
            print("正在加载多语言情感分析模型...")
            assert AutoTokenizer is not None
            assert AutoModelForSequenceClassification is not None

            # 使用多语言情感分析模型
            model_name = "tabularisai/multilingual-sentiment-analysis"
            # local_model_path = os.path.join(weibo_sentiment_path, "model")
            local_model_path = "/app/localmodels/tabularisai-multilingual-sentiment-analysis"

            # 检查本地是否已有模型
            if os.path.exists(local_model_path):
                print("从本地加载模型...")
                self.tokenizer = AutoTokenizer.from_pretrained(local_model_path)
                self.model = AutoModelForSequenceClassification.from_pretrained(local_model_path)
            else:
                print("首次使用，正在下载模型到本地...")
                # 下载并保存到本地
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
                # 保存到本地
                os.makedirs(local_model_path, exist_ok=True)
                self.tokenizer.save_pretrained(local_model_path)
                self.model.save_pretrained(local_model_path)
                print(f"模型已保存到: {local_model_path}")

            # 设置设备
            device = self._select_device()
            if device is None:
                raise RuntimeError("未检测到可用的计算设备")
            
            self.device = device
            self.model.to(self.device)
            self.model.eval()
            self.is_initialized = True
            self.enable()
            device_type = getattr(self.device, "type", str(self.device))
            if device_type == "cuda":
                print("检测到可用 GPU，已优先使用 CUDA 进行推理。")
            elif device_type == "mps":
                print("检测到 Apple MPS 设备，已使用 MPS 进行推理。")
            else:
                print("未检测到 GPU，自动使用 CPU 进行推理。")

            print(f"模型加载成功! 使用设备: {self.device}")
            print("支持语言: 中文、英文、西班牙文、阿拉伯文、日文、韩文等22种语言")
            print("情感等级: 非常负面、负面、中性、正面、非常正面")
            return True

        except Exception as e:
            error_message = f"模型加载失败: {e}"
            print(error_message)
            print("请检查网络连接或模型文件")
            self.disable(error_message, drop_state=True)
            return False
        
    def _preprocess_text(self, text: str) -> str:
        """ 文本预处理
        Args:
            text: 输入文本
        Returns:
            处理后的文本
        """
        # 基本文本清理
        if not text or not text.strip():
            return ""
        # 去除多余空格
        text = re.sub(r"\s+", " ", text.strip())
        return text
    
    def analyze_single_text(self, text: str) -> SentimentResult:
        """ 对单个文本进行情感分析
        Args:
            text: 要分析的文本
        Returns:
            SentimentResult对象
        """
        if self.is_disabled:
            return SentimentResult(
                text=text,
                sentiment_label="情感分析未执行",
                confidence=0.0,
                probability_distribution={},
                success=False,
                error_message=self.disable_reason or "情感分析功能已禁用",
                analysis_performed=False,
            )

        if not self.is_initialized:
            return SentimentResult(
                text=text,
                sentiment_label="未初始化",
                confidence=0.0,
                probability_distribution={},
                success=False,
                error_message="模型未初始化，请先调用initialize() 方法",
                analysis_performed=False,
            )
        
        try:
            # 预处理文本
            processed_text = self._preprocess_text(text)
            if not processed_text:
                return SentimentResult(
                    text=text,
                    sentiment_label="输入错误",
                    confidence=0.0,
                    probability_distribution={},
                    success=False,
                    error_message="输入文本为空或无效内容",
                    analysis_performed=False,
                )
            
            assert self.tokenizer is not None
            # 分词编码
            inputs = self.tokenizer(
                processed_text,
                max_length=512,
                padding=True,
                truncation=True,
                return_tensors="pt",
            )

            # 转移到设备
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # 预测
            assert torch is not None
            assert self.model is not None
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probabilities = torch.softmax(logits, dim=1)
                prediction = int(torch.argmax(probabilities, dim=1).item())

            # 构建结果
            confidence = probabilities[0][prediction].item()
            label = self.sentiment_map[prediction]
            # 构建概率分布字典
            prob_dist = {}
            for label_name, prob in zip(self.sentiment_map.values(), probabilities[0]):
                prob_dist[label_name] = prob.item()

            return SentimentResult(
                text=text,
                sentiment_label=label,
                confidence=confidence,
                probability_distribution=prob_dist,
                success=True,
            )
        
        except Exception as e:
            return SentimentResult(
                text=text,
                sentiment_label="分析失败",
                confidence=0.0,
                probability_distribution={},
                success=False,
                error_message=f"预测时发生错误: {str(e)}",
                analysis_performed=False,
            )
        
    def analyze_batch(self, texts: List[str], show_progress: bool = True) -> BatchSentimentResult:
        """ 批量情感分析
        Args:
            texts: 文本列表
            show_progress: 是否显示进度
        Returns:
            BatchSentimentResult对象
        """
        if not texts:
            return BatchSentimentResult(
                results=[],
                total_processed=0,
                success_count=0,
                failed_count=0,
                average_confidence=0.0,
                analysis_performed=not self.is_disabled and self.is_initialized,
            )

        if self.is_disabled or not self.is_initialized:
            passthrough_results = [
                SentimentResult(
                    text=text,
                    sentiment_label="情感分析未执行",
                    confidence=0.0,
                    probability_distribution={},
                    success=False,
                    error_message=self.disable_reason or "情感分析功能不可用",
                    analysis_performed=False,
                )
                for text in texts
            ]
            return BatchSentimentResult(
                results=passthrough_results,
                total_processed=len(texts),
                success_count=0,
                failed_count=len(texts),
                average_confidence=0.0,
                analysis_performed=False,
            )

        results = []
        success_count = 0
        total_confidence = 0.0

        for i, text in enumerate(texts):
            if show_progress and len(texts) > 1:
                print(f"处理进度: {i + 1}/{len(texts)}")

            result = self.analyze_single_text(text)
            results.append(result)

            if result.success:
                success_count += 1
                total_confidence += result.confidence

        average_confidence = (
            total_confidence / success_count if success_count > 0 else 0.0
        )
        failed_count = len(texts) - success_count

        return BatchSentimentResult(
            results=results,
            total_processed=len(texts),
            success_count=success_count,
            failed_count=failed_count,
            average_confidence=average_confidence,
            analysis_performed=True,
        )