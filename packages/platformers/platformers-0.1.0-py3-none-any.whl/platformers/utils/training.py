import logging


class PerSampleEventFilter:
    def __init__(self, per_sample, begin_counting=0):
        self.last_sample = 0
        self.per_sample = per_sample
        self.over_begin = False
        self.begin = begin_counting

    def check_int(self, interger):
        engine_samples = interger
        next_sample_point = self.last_sample + self.per_sample
        if engine_samples >= next_sample_point and engine_samples >= self.begin:
            if not self.over_begin:
                self.over_begin = True
                self.last_sample = self.begin
                return False
            else:
                self.last_sample += self.per_sample
            return True
        return False

    def __call__(self, engine):
        if engine.is_gradient_accumulation_boundary():
            engine_samples = engine.global_samples
            next_sample_point = self.last_sample + self.per_sample
            if engine_samples >= next_sample_point and engine_samples >= self.begin:
                self.last_sample += self.per_sample
                return True
        return False

    @property
    def n_samples(self):
        return self.last_sample

class PerTokenSampler:
    def __init__(self, per_token, seq_len=8192, begin_counting=0):
        self.last_token = 0
        self.per_token = per_token
        self.over_begin = False
        self.begin = begin_counting
        self.seq_len = seq_len

    def check_int(self, interger):
        num_tokens = interger
        next_point = self.last_token + self.per_token
        if num_tokens >= next_point and num_tokens >= self.begin:
            if not self.over_begin:
                self.over_begin = True
                self.last_token = self.begin
                return False
            else:
                self.last_token += self.per_token
            return True
        return False

    def __call__(self, engine):
        if engine.is_gradient_accumulation_boundary():
            return self.check_int(engine.global_samples * self.seq_len)

    @property
    def m_tokens(self):
        # show as per M
        return self.last_token / 1024 ** 2

    @property
    def k_tokens(self):
        return self.last_token / 1024

    @property
    def b_tokens(self):
        return self.last_token / 1024 ** 3

    @property
    def tokens(self):
        return self.last_token
