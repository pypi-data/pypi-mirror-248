class Quantifier:

    def __init__(self, obj):
        self.ctr = {}
        self.obj = obj


    def create_basic_counter(self):
        for i in self.obj:
            if i in self.ctr:
                self.ctr[i]+=1
            else:
                self.ctr[i] = 1
        # return self.ctr


    def sort_basic_key(self):
        return dict(sorted(self.ctr.items()))

    def sort_basic_val(self, flag = False):
        return dict(sorted(self.ctr.items(), key = lambda x:x[1], reverse = flag))

    def key_max(self):
        return max(zip(self.ctr.values(), self.ctr.keys()))[1]

    def reduce(self, key):
        if key in self.ctr:
            if self.ctr[key] == 1:
                del self.ctr[key]
            else:
                self.ctr[key] -=1

    def increase(self, key):
        if key in self.ctr:
            self.ctr[key]+=1
        else:
            self.ctr[key] = 1

    def print_ctr(self):
        print(self.ctr)

