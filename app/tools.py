from langchain.tools import tool

@tool
def multipy(a:int, b:int) -> int:
    """Use to multipy two numbers"""
    return a * b

@tool
def divide(a:int, b:int) -> int:
    """Use to divide two numbers, a will be divided by b"""
    return a / b