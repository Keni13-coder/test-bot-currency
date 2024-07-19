import re
from aiogram.filters import BaseFilter, CommandObject
from aiogram.types import Message


class CheckForСurrency(BaseFilter):

    async def __call__(self, message: Message, command: CommandObject) -> bool:
        if args := command.args:
            args = args.strip().split()
            len_args = len(args) == 3
            if len_args:
                return bool(re.match(r'^-?\d+(\.\d+)?$', args[-1]))
            
            return False