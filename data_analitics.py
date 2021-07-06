
class KnwingTheError:
    value_current=1
    value_last = 1
    value_highest = 1

    error_from_highest = 0
    error_from_last = 0


    def __init__(self):
        pass
        
    def adding_value(self,value_taked):
        self.value_current = int(value_taked)
        if self.value_current >= self.value_highest:
            self.value_highest = self.value_current
            self.error_from_highest = 0
        else:
            self.error_from_highest = 100 - (self.value_current*100/self.value_highest)
        if self.value_current >= self.value_last:
            self.error_from_last = 0
        else:
            self.error_from_last = 100 - (self.value_current*100/self.value_last)
        data=(f'Sensor values:\n highest->{self.value_highest} ; last->{self.value_last} ; current->{self.value_current} \n error from highest->{self.error_from_highest} \n error from last->{self.error_from_last}')
        # print(f'Sensor values:')
        # print(f'highest->{self.value_highest} ; last->{self.value_last} ; current->{self.value_current} ')
        # print(f'error from highest->{self.error_from_highest}')
        # print(f'error from last->{self.error_from_last}')
        self.value_last = self.value_current
        return data