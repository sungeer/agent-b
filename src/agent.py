import logging
from typing import Literal

from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage

from src.llm import llm

log = logging.getLogger(__name__)


class AgentDecision(BaseModel):
    action: Literal['answer', 'get_weather']
    content: str = Field(default='', description='直接回答的内容')
    city: str = Field(default='', description='查天气时的城市名')


def run_agent(user_input: str) -> AgentDecision:
    prompt = '你是一个智能助手。当用户问你问题时，判断是直接回答，还是需要查天气。'

    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=user_input),
    ]

    structured_llm = llm.with_structured_output(
        AgentDecision,
        method='function_calling'
    )

    decision = structured_llm.invoke(messages)

    log.info(f'[AI 决策]: {decision}')

    return decision
