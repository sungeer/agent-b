from datetime import datetime

import pytz
import requests
from pydantic import BaseModel, Field
from langchain_core.tools import tool


class WeatherInput(BaseModel):
    city: str = Field(description='城市名称')


@tool(args_schema=WeatherInput)
def get_weather(city: str) -> str:
    """查询指定城市的天气信息。"""
    weather_data = {
        '北京': '晴，15°C，东风3级',
        '上海': '多云，18°C，南风2级',
        '广州': '小雨，22°C，偏东风',
        '深圳': '阴，24°C，东南风2级',
        '成都': '多云，16°C，微风',
    }
    return weather_data.get(city, f'{city}：晴，20°C（模拟数据）')


class SearchInput(BaseModel):
    query: str = Field(description='搜索关键词')


@tool(args_schema=SearchInput)
def web_search(query: str, max_results: int = 3) -> str:
    """搜索互联网上的信息，适合查找新闻、事实、最新资讯。"""
    url = 'https://api.duckduckgo.com/'
    params = {
        'q': query,
        'format': 'json',
        'no_html': '1',
        'skip_disambig': '1',
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = []
        if data.get('AbstractText'):
            results.append(f'摘要：{data["AbstractText"]}')
        for topic in data.get('RelatedTopics', [])[:max_results]:
            if isinstance(topic, dict) and topic.get('Text'):
                results.append(f'- {topic["Text"]}')
        if results:
            return '\n'.join(results)
        return f'没有找到关于「{query}」的搜索结果'
    except requests.Timeout:
        return '搜索超时，请稍后重试'
    except requests.RequestException as e:
        return f'搜索网络错误：{e}'


class CurrentTimeInput(BaseModel):
    timezone: str = Field(description='时区名称，字符串，默认 Asia/Shanghai')


@tool(args_schema=CurrentTimeInput)
def get_current_time(timezone: str = 'Asia/Shanghai') -> str:
    """获取当前时间。"""
    try:
        tz = pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        tz = pytz.timezone('Asia/Shanghai')
        timezone = 'Asia/Shanghai（时区名无效，已回退）'

    now = datetime.now(tz)
    return now.strftime(f'%Y年%m月%d日 %H:%M:%S（{timezone}）')


class CalculateInput(BaseModel):
    expression: str = Field(description='数学表达式字符串，例如：(3+5)*2')


@tool(args_schema=CalculateInput)
def calculate(expression: str) -> str:
    """计算数学表达式，支持加减乘除和括号。"""
    allowed_chars = set('0123456789+-*/()., ')
    if not all(c in allowed_chars for c in expression):
        return f'表达式包含不允许的字符，拒绝计算：{expression!r}'

    try:
        result = eval(expression)  # noqa: S307
        return f'{expression} = {result}'
    except ZeroDivisionError:
        return '错误：除数不能为零'
    except SyntaxError:
        return f'表达式语法错误：{expression!r}'
    except Exception as e:
        return f'计算出错：{e}'
