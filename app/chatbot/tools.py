from langchain_core.tools import BaseTool

class CountCharactersTool(BaseTool):
    name = "count_characters_tool"
    description = "計算字串中字元數量的工具"

    def _run(self, text: str, char: str) -> int:
        result = text.count(char)
        print(f"CountCharactersTool:", text, char, result)
        return result
