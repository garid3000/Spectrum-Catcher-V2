import os, time

dev = '/dev/video2'
class Py_v4l2():
    def __init__(self, dev, optimize_every=3, upperBorder = 230, lowerBorder = 100):
        self.possible_expos = [1, 2, 5, 10, 20, 39, 78, 156, 312, 625, 1250, 2500]
        self.devname = dev
        self.s_gain = 'gain'
        self.s_expo = 'exposure_absolute'
        self.gain = self.read_prop(self.s_gain)
        self.expo = self.read_prop(self.s_expo)
        self.expo_i = self.get_expo_i()
        # border
        self.optimize_count        = 0
        self.optimize_every        = optimize_every
        self.optimize_upper_border = upperBorder
        self.optimize_lower_border = lowerBorder

    def read_prop(self, prop):
        #os.system('v4l2-ctl -d {} --list-ctrls'.format(self.devname))
        return int(os.popen('v4l2-ctl -d {} -C {}'.format(self.devname, prop)).read().split()[-1])

    def set_prop(self, prop, value):
        #os.system('v4l2-ctl -d {} --list-ctrls'.format(self.devname))
        if prop == self.s_gain:
            if not (1 <= value <= 33):
                return "out of range"
        if prop == self.s_expo:
            if not (value in self.possible_expos):
                return "out of range"

        return os.popen('v4l2-ctl -d {} -c {} {}'.format(self.devname, prop, value)).read()



    def set_gain(self, value):
        if not (1 <= value <= 33):
            return "out of range"
        return os.popen('v4l2-ctl -d {} -c gain={}'.format(self.devname, value)).read()

    def set_expo(self, value):
        if not (value in self.possible_expos):
            return "out of range"
        return os.popen('v4l2-ctl -d {} -c exposure_absolute={}'.format(self.devname, value)).read()

    def set_expo_i(self, value_i):
        if not (0 <= value_i <= 11):
            return "out of range"
        value = self.possible_expos[value_i]
        return os.popen('v4l2-ctl -d {} -c exposure_absolute={}'.format(self.devname, value)).read()


    def get_gain(self):
        self.gain = int(os.popen('v4l2-ctl -d {} -C gain'.format(self.devname)).read().split()[-1])
        return self.gain

    def get_expo(self):
        self.expo = int(os.popen('v4l2-ctl -d {} -C exposure_absolute'.format(self.devname)).read().split()[-1])
        return self.expo

    def get_expo_i(self):
        tmp = int(os.popen('v4l2-ctl -d {} -C exposure_absolute'.format(self.devname)).read().split()[-1])
        self.expo_i = self.possible_expos.index(tmp)
        return self.expo_i


    def optimize_expo(self, current_max):
        # def optimizing_expo(current_max):
        if self.optimize_count >= self.optimize_every:
            self.optimize_count  = 0
            if current_max < self.optimize_lower_border:
                if self.expo_i >= 11:
                    return 'max'
                else:
                    self.set_expo_i(self.expo_i + 1)
                    self.get_expo_i()
                    #time.sleep(.3)
                    return 'increasing'

            elif current_max > self.optimize_upper_border:
                if self.expo_i <= 0:
                    return 'min'
                else:
                    self.set_expo_i(self.expo_i - 1)
                    self.get_expo_i()
                    #time.sleep(.3)
                    return 'decreasing'

            else:
                return 'steady'
        else:
            self.optimize_count += 1
            return 'inprocess'



if __name__ == "__main__":
    v4l2 = Py_v4l2(dev)
