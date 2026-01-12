#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
评论分析智能体使用示例
"""

from comment_analyzer import CommentAnalyzer


def example1():
    """示例1：基础使用"""
    print("=" * 60)
    print("示例1：基础使用")
    print("=" * 60)
    
    analyzer = CommentAnalyzer()
    
    comments = [
        "昨天更新后应用一直闪退，根本用不了！",
        "界面设计太难看了，按钮也找不到",
        "会员价格太贵了，能不能便宜点",
        "很多歌曲都变灰了，版权太少了",
        "希望能添加夜间模式，晚上用着太亮了",
        "不错的产品，就是广告有点多",
        "太棒了！非常喜欢这个应用！",
    ]
    
    analyzer.add_comments(comments)
    report = analyzer.generate_report()
    print(report)
    print()


def example2():
    """示例2：包含无效数据"""
    print("=" * 60)
    print("示例2：包含无效数据")
    print("=" * 60)
    
    analyzer = CommentAnalyzer()
    
    comments = [
        "应用一直崩溃，没法用",
        "123456",
        "广告太多，烦死了",
        "",
        "非常好用！",
    ]
    
    analyzer.add_comments(comments)
    report = analyzer.generate_report()
    print(report)
    print()


def example3():
    """示例3：P0高危问题"""
    print("=" * 60)
    print("示例3：P0高危问题")
    print("=" * 60)
    
    analyzer = CommentAnalyzer()
    
    comments = [
        "充值后钱扣了但VIP没到账！",
        "应用闪退，完全无法使用",
        "崩溃了，根本打不开",
    ]
    
    analyzer.add_comments(comments)
    report = analyzer.generate_report()
    print(report)
    print()


def example4():
    """示例4：单条评论分析"""
    print("=" * 60)
    print("示例4：单条评论分析")
    print("=" * 60)
    
    analyzer = CommentAnalyzer()
    
    comments = [
        "希望能优化一下界面，现在的按钮有点小，操作不太方便"
    ]
    
    analyzer.add_comments(comments)
    report = analyzer.generate_report()
    print(report)
    print()


if __name__ == "__main__":
    example1()
    example2()
    example3()
    example4()
