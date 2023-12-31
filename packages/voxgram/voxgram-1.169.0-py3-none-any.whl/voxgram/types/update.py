import voxgram


class Update:
    @staticmethod
    def stop_propagation():
        raise voxgram.StopPropagation

    @staticmethod
    def continue_propagation():
        raise voxgram.ContinuePropagation
