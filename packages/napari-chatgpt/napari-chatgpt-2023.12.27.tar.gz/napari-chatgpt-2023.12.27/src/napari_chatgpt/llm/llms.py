from arbol import aprint
from langchain.callbacks.manager import AsyncCallbackManager
from langchain.chat_models import ChatOpenAI, ChatAnthropic


def instantiate_LLMs(llm_model_name: str,
                     temperature: float,
                     tool_temperature: float,
                     chat_callback_handler,
                     tool_callback_handler,
                     memory_callback_handler,
                     verbose: bool = False
                     ):
    aprint(f"Instantiating LLMs with model: '{llm_model_name}', t={temperature}, t_tool={tool_temperature}. ")
    if 'gpt-' in llm_model_name:
        # Instantiates Main LLM:
        main_llm = ChatOpenAI(
            model_name=llm_model_name,
            verbose=verbose,
            streaming=True,
            temperature=temperature,
            callback_manager=AsyncCallbackManager(
                [chat_callback_handler])
        )

        # Instantiates Tool LLM:
        tool_llm = ChatOpenAI(
            model_name=llm_model_name,
            verbose=verbose,
            streaming=True,
            temperature=tool_temperature,

            callback_manager=AsyncCallbackManager([tool_callback_handler])
        )

        # Instantiates Memory LLM:
        memory_llm = ChatOpenAI(
            model_name=llm_model_name,
            verbose=False,
            temperature=temperature,
            callback_manager=AsyncCallbackManager([memory_callback_handler])
        )

        max_token_limit = 8000 if 'gpt-4' in llm_model_name else 2000


    elif 'claude' in llm_model_name:

        # Instantiates Main LLM:
        main_llm = ChatAnthropic(
            model=llm_model_name,
            verbose=verbose,
            streaming=True,
            temperature=temperature,
            max_tokens_to_sample=4096,
            callback_manager=AsyncCallbackManager(
                [chat_callback_handler])
        )

        # Instantiates Tool LLM:
        tool_llm = ChatAnthropic(
            model=llm_model_name,
            verbose=verbose,
            streaming=True,
            temperature=tool_temperature,
            max_tokens_to_sample=4096,
            callback_manager=AsyncCallbackManager([tool_callback_handler])
        )

        # Instantiates Memory LLM:
        memory_llm = ChatAnthropic(
            model=llm_model_name,
            verbose=False,
            temperature=temperature,
            max_tokens_to_sample=4096,
            callback_manager=AsyncCallbackManager([memory_callback_handler])
        )

        max_token_limit = 8000

    return main_llm, memory_llm, tool_llm, max_token_limit
