from .connections.QlikRepository import QlikSenseRepository


class QlikSenseTask:
    def __init__(self, task_json: dict, qrs: QlikSenseRepository):
        self.__qrs: QlikSenseRepository = qrs

        self.id = task_json['id']
        self.name = task_json['name']
        self.is_enabled = task_json['enabled']
        self.next_execution = task_json['operational']['nextExecution']
        self.last_execution_result = {
            key: task_json['operational']['lastExecutionResult'][key]
            for key in ['status', 'startTime', 'stopTime', 'duration', 'scriptLogLocation']
        }

    def __get_full(self):
        full = self.__qrs.get_task(self.id)
        return full.json()

    def start(self):
        return self.__qrs.start_task(self.id)

    def stop(self):
        return self.__qrs.stop_task(self.id)

    def enable(self):
        self_full = self.__get_full()
        self_full['enabled'] = True
        enabled = self.__qrs.update_task(self_full)
        return enabled

    def disable(self):
        self_full = self.__get_full()
        self_full['enabled'] = False
        disabled = self.__qrs.update_task(self_full)
        return disabled




