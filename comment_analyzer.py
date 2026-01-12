#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
评论分析智能体
用于分析用户评论，进行归类、打分、定级，并生成统计报告
"""

import re
from typing import List, Dict, Tuple, Optional
from collections import defaultdict


class CommentAnalyzer:
    """评论分析器"""
    
    # 分类标准关键字
    CATEGORY_KEYWORDS = {
        "1-功能稳定性": [
            "闪退", "崩溃", "卡顿", "无法播放", "播放失败", "下载失败", 
            "网络连接错误", "连接失败", "打不开", "用不了", "无法使用"
        ],
        "2-交互与体验UI/UX": [
            "界面", "设计", "按钮", "找不到", "操作", "繁琐", "复杂",
            "字体", "大小", "夜间模式", "深色模式", "UI", "UX", "难看", "丑"
        ],
        "3-商业化": [
            "会员", "价格", "贵", "便宜", "广告", "弹窗", "数字专辑", 
            "购买", "扣费", "自动扣费", "付费", "VIP", "订阅"
        ],
        "4-内容版权": [
            "版权", "歌曲", "变灰", "下架", "音质", "音效", "曲库", 
            "不全", "少", "没有", "缺失"
        ],
        "5-其他": [
            # 纯情绪宣泄、无意义乱码、好评、非产品相关内容
        ]
    }
    
    # 情感打分标准关键字
    SENTIMENT_KEYWORDS = {
        1: ["草", "操", "妈的", "垃圾", "卸载", "删除", "再也不", "失望透顶", "绝望", "愤怒"],
        2: ["不好", "差", "问题", "bug", "不行", "不满意", "建议改进"],
        3: ["希望", "建议", "可以", "如果", "最好", "建议"],
        4: ["不错", "还行", "喜欢", "好用", "满意", "推荐"],
        5: ["太棒了", "完美", "爱了", "惊喜", "超赞", "非常满意", "五星"]
    }
    
    # 紧迫度标准关键字
    URGENCY_KEYWORDS = {
        "P0": ["崩溃", "闪退", "无法使用", "用不了", "打不开", "扣费", "没到账", "钱", "资损"],
        "P1": ["卡顿", "慢", "问题", "bug", "体验差", "不好用"],
        "P2": ["建议", "希望", "可以", "改进", "优化", "更好"]
    }
    
    def __init__(self):
        self.comments = []
        self.analysis_results = []
    
    def add_comments(self, comments: List[str]):
        """添加评论列表"""
        self.comments = comments
    
    def classify(self, comment: str) -> str:
        """对评论进行分类"""
        # 检查无效数据
        if self._is_invalid(comment):
            return "无效数据"
        
        comment_lower = comment.lower()
        category_scores = {}
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if category == "5-其他":
                continue  # 其他类别最后处理
            score = sum(1 for keyword in keywords if keyword in comment_lower)
            if score > 0:
                category_scores[category] = score
        
        # 如果没有匹配到具体分类，归为"5-其他"
        if not category_scores:
            return "5-其他"
        
        # 返回得分最高的分类，如果得分相同，按优先级返回（序号小的优先）
        if len(category_scores) == 1:
            return list(category_scores.keys())[0]
        
        max_score = max(category_scores.values())
        top_categories = [cat for cat, score in category_scores.items() if score == max_score]
        
        # 如果多个分类得分相同，选择序号最小的
        if len(top_categories) > 1:
            return min(top_categories, key=lambda x: int(x.split('-')[0]))
        
        return top_categories[0]
    
    def score_sentiment(self, comment: str) -> str:
        """对评论进行情感打分"""
        if self._is_invalid(comment):
            return "N/A"
        
        comment_lower = comment.lower()
        sentiment_matches = []
        
        # 检查每个情感等级的关键词
        for score, keywords in sorted(self.SENTIMENT_KEYWORDS.items()):
            for keyword in keywords:
                if keyword in comment_lower:
                    sentiment_matches.append(score)
                    break  # 找到匹配就跳出，避免重复
        
        if not sentiment_matches:
            # 默认中立
            return "3分（中立）"
        
        # 优先选择最低分（更强烈的负面情绪）或最高分（更强烈的正面情绪）
        # 如果有1分或2分，优先选择最低分；否则选择最高分
        if any(s <= 2 for s in sentiment_matches):
            final_score = min(sentiment_matches)
        else:
            final_score = max(sentiment_matches)
        
        sentiment_map = {
            1: "1分（愤怒）",
            2: "2分（不满）",
            3: "3分（中立）",
            4: "4分（满意）",
            5: "5分（惊喜）"
        }
        
        return sentiment_map[final_score]
    
    def determine_urgency(self, comment: str, category: str) -> str:
        """判断评论的紧迫度"""
        if category == "无效数据":
            return "N/A"
        
        comment_lower = comment.lower()
        
        # 检查P0关键词
        for keyword in self.URGENCY_KEYWORDS["P0"]:
            if keyword in comment_lower:
                return "P0（高危）"
        
        # 检查P1关键词
        for keyword in self.URGENCY_KEYWORDS["P1"]:
            if keyword in comment_lower:
                return "P1（重要）"
        
        # 检查P2关键词
        for keyword in self.URGENCY_KEYWORDS["P2"]:
            if keyword in comment_lower:
                return "P2（一般）"
        
        # 默认P2
        return "P2（一般）"
    
    def _count_chinese_chars(self, text: str) -> int:
        """计算中文字符数量"""
        return len(re.findall(r'[\u4e00-\u9fff]', text))
    
    def extract_core_issue(self, comment: str, category: str) -> str:
        """提取核心槽点（3-5字）"""
        if category == "无效数据":
            return "无效数据"
        
        # 根据分类提取关键词
        category_keywords = self.CATEGORY_KEYWORDS.get(category, [])
        comment_lower = comment.lower()
        
        # 优先查找短关键词（2-3字），更容易匹配到3-5字的短语
        sorted_keywords = sorted(category_keywords, key=lambda x: len(x))
        
        for keyword in sorted_keywords:
            if keyword in comment_lower:
                idx = comment_lower.find(keyword)
                # 尝试提取包含关键词的短语（3-5字）
                # 向前扩展最多2个字符，向后扩展最多2个字符
                for start_offset in range(2, -1, -1):
                    for end_offset in range(0, 3):
                        start = max(0, idx - start_offset)
                        end = min(len(comment), idx + len(keyword) + end_offset)
                        phrase = comment[start:end].strip()
                        
                        # 只计算中文字符数量
                        chinese_count = self._count_chinese_chars(phrase)
                        if 3 <= chinese_count <= 5:
                            # 提取纯中文部分
                            chinese_chars = re.findall(r'[\u4e00-\u9fff]', phrase)
                            if len(chinese_chars) >= 3:
                                return ''.join(chinese_chars[:5])
                
                # 如果关键词本身在3-5字范围内，直接返回
                chinese_keyword = ''.join(re.findall(r'[\u4e00-\u9fff]', keyword))
                if 3 <= len(chinese_keyword) <= 5:
                    return chinese_keyword
                elif len(chinese_keyword) == 2:
                    # 2字关键词，尝试前后各加一个字
                    if idx > 0 and idx + len(keyword) < len(comment):
                        extended = comment[max(0, idx-1):min(len(comment), idx+len(keyword)+1)]
                        chinese_extended = ''.join(re.findall(r'[\u4e00-\u9fff]', extended))
                        if 3 <= len(chinese_extended) <= 5:
                            return chinese_extended
                elif len(chinese_keyword) > 5:
                    # 长关键词，取前5字
                    return chinese_keyword[:5]
        
        # 如果没找到，根据分类返回简短描述（3-4字）
        defaults = {
            "1-功能稳定性": "功能问题",
            "2-交互与体验UI/UX": "体验问题",
            "3-商业化": "商业问题",
            "4-内容版权": "版权问题",
            "5-其他": "其他问题"
        }
        return defaults.get(category, "其他问题")
    
    def _is_invalid(self, comment: str) -> bool:
        """判断是否为无效数据（无意义、广告、纯社交请求）"""
        comment = comment.strip()
        
        # 空评论或过短
        if len(comment) < 2:
            return True
        
        # 纯乱码（大部分非中文字符）
        non_chinese = len(re.sub(r'[\u4e00-\u9fff]', '', comment))
        if non_chinese / len(comment) > 0.7 and len(comment) > 10:
            return True
        
        # 纯数字或符号
        if re.match(r'^[\d\s\W]+$', comment):
            return True
        
        return False
    
    def analyze(self) -> List[Dict]:
        """分析所有评论"""
        self.analysis_results = []
        
        for idx, comment in enumerate(self.comments, 1):
            category = self.classify(comment)
            sentiment = self.score_sentiment(comment)
            urgency = self.determine_urgency(comment, category)
            core_issue = self.extract_core_issue(comment, category)
            summary = comment[:10] if len(comment) >= 10 else comment
            
            result = {
                "id": idx,
                "category": category,
                "sentiment": sentiment,
                "urgency": urgency,
                "core_issue": core_issue,
                "summary": summary,
                "original": comment
            }
            
            self.analysis_results.append(result)
        
        return self.analysis_results
    
    def aggregate_statistics(self) -> Dict:
        """聚合统计"""
        stats = defaultdict(lambda: {
            "count": 0,
            "sentiments": [],
            "urgencies": [],
            "core_issues": [],
            "comments": []
        })
        
        for result in self.analysis_results:
            category = result["category"]
            if category == "无效数据":
                continue
            
            stats[category]["count"] += 1
            stats[category]["comments"].append(result)
            
            # 提取情感分数
            sentiment_match = re.search(r'(\d)分', result["sentiment"])
            if sentiment_match:
                stats[category]["sentiments"].append(int(sentiment_match.group(1)))
            
            # 提取紧迫度
            urgency_match = re.search(r'(P\d)', result["urgency"])
            if urgency_match:
                stats[category]["urgencies"].append(urgency_match.group(1))
        
        # 计算统计结果
        aggregated = {}
        for category, data in stats.items():
            count = data["count"]
            avg_sentiment = sum(data["sentiments"]) / len(data["sentiments"]) if data["sentiments"] else 0
            avg_sentiment = round(avg_sentiment, 1)
            
            # 找出最高紧迫度
            urgency_levels = {"P0": 0, "P1": 1, "P2": 2}
            if data["urgencies"]:
                highest_urgency = min(data["urgencies"], key=lambda x: urgency_levels.get(x, 99))
                urgency_label = {
                    "P0": "P0（高危）",
                    "P1": "P1（重要）",
                    "P2": "P2（一般）"
                }.get(highest_urgency, "P2（一般）")
            else:
                highest_urgency = "P2"
                urgency_label = "P2（一般）"
            
            # 找出典型槽点（最高紧迫度下的核心槽点）
            typical_issue = "无"
            if data["comments"]:
                # 找出最高紧迫度的评论
                highest_urgency_comments = [
                    c for c in data["comments"] 
                    if re.search(r'P0', c["urgency"]) and highest_urgency == "P0"
                ]
                if not highest_urgency_comments:
                    highest_urgency_comments = [
                        c for c in data["comments"]
                        if re.search(r'P1', c["urgency"]) and highest_urgency == "P1"
                    ]
                if not highest_urgency_comments:
                    highest_urgency_comments = data["comments"]
                
                if highest_urgency_comments:
                    typical_issue = highest_urgency_comments[0]["core_issue"]
            
            aggregated[category] = {
                "count": count,
                "avg_sentiment": avg_sentiment,
                "highest_urgency": urgency_label,
                "typical_issue": typical_issue
            }
        
        return aggregated
    
    def generate_summary_table(self) -> str:
        """生成核心数据汇总表"""
        stats = self.aggregate_statistics()
        
        if not stats:
            return "| 问题分类 | 出现次数 | 情感均分 | 最高紧迫度 | 典型槽点(3-5字) |\n|---------|---------|---------|-----------|---------------|\n| 无数据 | 0 | 0.0 | - | - |"
        
        lines = ["| 问题分类 | 出现次数 | 情感均分 | 最高紧迫度 | 典型槽点(3-5字) |"]
        lines.append("|---------|---------|---------|-----------|---------------|")
        
        # 按分类序号排序
        sorted_categories = sorted(stats.items(), key=lambda x: int(x[0].split('-')[0]) if x[0].split('-')[0].isdigit() else 999)
        
        for category, data in sorted_categories:
            lines.append(
                f"| {category} | {data['count']} | {data['avg_sentiment']} | {data['highest_urgency']} | {data['typical_issue']} |"
            )
        
        return "\n".join(lines)
    
    def generate_detail_table(self) -> str:
        """生成全量评论分析明细表"""
        if not self.analysis_results:
            return "| ID | 一级分类 | 情感分数 | 紧迫度 | 核心槽点 | 原文摘要（前10字） |\n|----|---------|---------|-------|---------|-----------------|\n| - | - | - | - | - | - |"
        
        lines = ["| ID | 一级分类 | 情感分数 | 紧迫度 | 核心槽点 | 原文摘要（前10字） |"]
        lines.append("|----|---------|---------|-------|---------|-----------------|")
        
        for result in self.analysis_results:
            lines.append(
                f"| {result['id']} | {result['category']} | {result['sentiment']} | {result['urgency']} | {result['core_issue']} | {result['summary']} |"
            )
        
        return "\n".join(lines)
    
    def generate_report(self) -> str:
        """生成完整报告"""
        self.analyze()
        
        summary_table = self.generate_summary_table()
        detail_table = self.generate_detail_table()
        
        report = f"{summary_table}\n\n---\n\n{detail_table}"
        
        return report


def main():
    """主函数 - 示例使用"""
    analyzer = CommentAnalyzer()
    
    # 示例评论
    sample_comments = [
        "昨天更新后应用一直闪退，根本用不了！",
        "界面设计太难看了，按钮也找不到",
        "会员价格太贵了，能不能便宜点",
        "很多歌曲都变灰了，版权太少了",
        "希望能添加夜间模式，晚上用着太亮了",
        "不错的产品，就是广告有点多",
        "太棒了！非常喜欢这个应用！",
    ]
    
    analyzer.add_comments(sample_comments)
    report = analyzer.generate_report()
    
    print(report)


if __name__ == "__main__":
    main()
