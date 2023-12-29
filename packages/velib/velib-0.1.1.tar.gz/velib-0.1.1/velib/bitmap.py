

class Bitmap(object):
    def __init__(self, _max: int, array: list = None):
        self.size = self.calc_elem_index(_max, True)
        self.array = array if array else [0] * self.size

    @staticmethod
    def calc_elem_index(num: int, up: bool = False) -> int:
        if up:
            return int((num + 31 - 1) // 31)
        return num // 31

    @staticmethod
    def calc_bit_index(num: int) -> int:
        return num % 31

    def set(self, num: int):
        elem_index = self.calc_elem_index(num)
        byte_index = self.calc_bit_index(num)
        elem = self.array[elem_index]
        self.array[elem_index] = elem | (1 << byte_index)

    def clean(self, index: int):
        elem_index = self.calc_elem_index(index)
        byte_index = self.calc_bit_index(index)
        elem = self.array[elem_index]
        self.array[elem_index] = elem & (~(1 << byte_index))

    def test(self, index: int) -> bool:
        elem_index = self.calc_elem_index(index)
        byte_index = self.calc_bit_index(index)
        if self.array[elem_index] & (1 << byte_index):
            return True
        return False

    @staticmethod
    def list_to_bitmap(_max: int, list_size: int, _list: list) -> 'Bitmap':
        bit_map = Bitmap(_max)
       
        for i in range(_max):
            bit_map.set(i)
       
        for i in range(list_size):
            bit_map.clean(i)
    
        for index, value in enumerate(_list):
            bit_map.set(value - 1)

        return bit_map

    @staticmethod
    def to_list(list_size: int, _ids: int) -> list:
        bit_map = Bitmap(0, [_ids])

        bit_list = []
        for i in range(list_size):
            if bit_map.test(i):
                bit_list.append(i + 1)
        return bit_list

