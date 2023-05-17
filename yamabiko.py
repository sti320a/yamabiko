import abc

class IVoiceDetector(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def start(self) -> None:
        raise NotImplementedError()


class Yamabiko:

    def __init__(
        self,
        voice_detector: IVoiceDetector
    ):
        self.voice_detector = voice_detector

    def run(self):
        self.voice_detector.start()



# 利用例
if __name__=='__main__':

    from voice_detector import VoiceDetector

    voice_detector = VoiceDetector()
    yamabiko = Yamabiko(voice_detector)
    yamabiko.run()

