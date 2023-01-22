class Icon:
    def __init__(self, nerdfont: bool = True) -> None:
        self.nerdfont = nerdfont

    @property
    def RESTARTED(self) -> int:
        return 0xf2dd if self.nerdfont else 0x2609
    
    @property
    def STARTED(self) -> int:
        return 0xf2dd if self.nerdfont else 0x26a1

    @property
    def FINISHED(self):
        return 0xebe9 if self.nerdfont else 0x2600
    
    @property
    def EXIT(self):
        return 0xead0 if self.nerdfont else 0x26bd