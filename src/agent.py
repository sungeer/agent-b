import logging

from langchain_core.messages import SystemMessage, HumanMessage

from src.llm import llm
from src import toolset

log = logging.getLogger(__name__)

tools = [
    toolset.get_weather,
    toolset.web_search,
    toolset.get_current_time,
    toolset.calculate,
]
tools_map = {t.name: t for t in tools}


def run_agent(user_input: str) -> str:
    prompt = '你是一个智能助手，可以使用工具来帮助用户回答问题。'
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=user_input),
    ]

    llm_with_tools = llm.bind_tools(tools)

    for i in range(3):
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            log.info(f'无需工具调用，第[{i}]轮结束')
            return response.content or ''

        log.info(f'工具调用第[{i + 1}]轮')
        for tc in response.tool_calls:
            tool_func = tools_map.get(tc['name'])
            if tool_func is None:
                log.warning(f'未知工具: {tc["name"]}')
                continue
            log.info(f'执行工具: {tc["name"]}，参数: {tc["args"]}')
            result = tool_func.invoke(tc)
            log.info(f'工具结果: {str(result)[:100]}')
            messages.append(result)

    log.warning('工具调用达到上限3轮，强制总结')
    summary_prompt = SystemMessage(content='请根据已有的工具返回信息，简洁地回答用户的问题。')
    messages.append(summary_prompt)
    response = llm.invoke(messages)
    return response.content or ''
