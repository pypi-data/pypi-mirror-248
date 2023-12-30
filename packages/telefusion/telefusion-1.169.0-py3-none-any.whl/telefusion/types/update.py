import telefusion


class Update:
    @staticmethod
    def stop_propagation():
        raise telefusion.StopPropagation

    @staticmethod
    def continue_propagation():
        raise telefusion.ContinuePropagation
