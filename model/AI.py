import random
import model.config_model as config_model

class AI:
    def __init__(self, bass_list):
        self.bass_list = bass_list

    def rec_model(self, start_nero: list) -> list:
        for base in self.bass_list:
            final_nero = [0 for _ in range(len(base))]

            for nero_num, conn_list in enumerate(base):
                for conn_list_num in range(len(conn_list)):
                    final_nero[nero_num] += conn_list[conn_list_num] * start_nero[conn_list_num]
            start_nero = final_nero

        return final_nero

    # def study(self):
    #     pass

    def get_bass(self):
        return self.bass_list

class ModelDino(AI):
    def __init__(self, record=0):
        self.bass_list = [
            [  # 2 base
                [random.randint(1, 1_000) * config_model.min_step for _ in range(config_model.start_data_size)],  # -> 1n
                [random.randint(1, 1_000) * config_model.min_step for _ in range(config_model.start_data_size)]  # -> 2n
            ],
            [  # 3 base
                [random.randint(1, 1_000) * config_model.min_step for _ in range(2)],  # -> 1n
                [random.randint(1, 1_000) * config_model.min_step for _ in range(2)]  # -> 2n
            ]
        ]
        super().__init__(self.bass_list)
        self.record = record
        self.diffusions = 100 # %
        self.bass_list_record = self.bass_list

    def study(self, score: int):
        if score < self.record:
            self.bass_list = self.bass_list_record
        else:
            self.record = score
            self.bass_list_record = self.bass_list

        for i_base in range(len(self.bass_list)):
            for i_nero in range(len(self.bass_list[i_base])):
                for i_weights in range(len(self.bass_list[i_base][i_nero])):
                    self.bass_list[i_base][i_nero][i_weights] += random.randint(1, 100) * config_model.min_step * (self.diffusions / 100) * ((i_base + 1) / len(self.bass_list)) * [1, -1][random.randint(0, 1)]
        self.diffusions = min(0.1, self.diffusions * 0.90)


if __name__ == '__main__':
    ai = ModelDino()
    ai.rec_model([1, 1, 1])

    ai.study(12)
    ai.rec_model([1, 1, 1])
