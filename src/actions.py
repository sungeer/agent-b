from src.agent import AgentDecision


def get_weather(city: str) -> str:
    mock_data = {
        '北京': '晴，15°C，东风3级',
        '上海': '多云，18°C，南风2级',
        '广州': '小雨，22°C，偏东风',
        '深圳': '阴，24°C，东南风2级',
        '成都': '多云，16°C，微风',
    }
    return mock_data.get(city, f'{city}：晴，20°C（模拟数据）')


def execute_action(decision: AgentDecision) -> str:
    if decision.action == 'answer':
        return decision.content or '（AI 没有提供内容）'
    elif decision.action == 'get_weather':
        city = decision.city or '未知城市'
        weather = get_weather(city)
        return f'{city}的天气：{weather}'
    else:
        return f'（未知动作 {decision.action!r}）{decision}'
