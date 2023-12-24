from typing import List, Tuple, Union

AstNode = Union[str, Tuple[str, List['AstNode']]]

def parse(src: str) -> AstNode:
    """
    parse the source code of WhileDB language and return AstNode
    ```
    AstNode = Tuple[str, List[AstNode]]
    ```
    """

def exec(src: str) -> None:
    """
    execuate the WhileDB code
    """