class Card:
    def __init__(self, value, suit):
        self.face = value
        self.suit = suit
    
    @property
    def value(self):
        if self.face == 'A':
            return [1, 14]
        faces = {'J':11, 'Q':12, 'K':13}
        if self.face in faces.keys():
            return [faces[self.face]]
        else:
            return [int(self.face)]
    
    def __str__(self):
        return f'({self.face}, {self.suit})'
    
    def __gt__(self, other):
        return max(self.value) > max(other.value)
    
    def __lt__(self, other):
        return max(self.value) < max(other.value)

class Hand:
    def __init__(self, card1, card2, card3):
        self.card1 = card1
        self.card2 = card2
        self.card3 = card3
    
    def __is_straight(self, values):
        from itertools import product
        for a, b, c in product(*values):
            lst = sorted([a, b, c])
            if lst[0] + 1 == lst[1] and lst[1] + 1 == lst[2]:
                return True
        return False
    
    def __is_flush(self, values):
        if len(set(values)) == 1:
            return True
        return False
    
    def __is_trip(self, values):
        from itertools import product
        for a, b, c in product(*values):
            if a==b and b ==c and a==c:
                return True
        return False
    
    def __is_pair(self, values):
        from itertools import product
        for a, b, c in product(*values):
            if len(set([a, b, c])) == 2:
                return True
        return False
    
    def __str__(self):
        return f'{str(self.card1)},{str(self.card2)},{str(self.card3)}'
    
    def get_rank(self):
        hands = ['high card', 'pair', 'flush', 'straight', 'three of a kind', 'straight flush']
        return hands.index(self.value)
    
    def __eq__(self, other):
        my_rank = self.get_rank()
        oth_rank = other.get_rank()
        if my_rank == oth_rank:
            my_values = self.order_cards()
            oth_values = other.order_cards()
            for m, o in zip(my_values, oth_values):
                if m != o:
                    return False
            return True
        else:
            return False
        
    def count(self):
        count = {}
        for card in self.order_cards():
            count[card] = count.get(card, 0) + 1
        return count
    
    def __gt__(self, other):
        my_rank = self.get_rank()
        oth_rank = other.get_rank()
        if my_rank == oth_rank:
            if len(set(self.order_cards())) == 2:
                my_count = sorted(list(self.count().items()), key = lambda x: -x[1])
                oth_count = sorted(list(other.count().items()), key = lambda x: -x[1])
                if my_count[0][0] > oth_count[0][0]:
                    return True
                elif my_count[0][0] == oth_count[0][0]:
                    if my_count[1][0] > oth_count[1][0]:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                my_values = self.order_cards()
                oth_values = other.order_cards()
                for m, o in zip(my_values, oth_values):
                    if m > o:
                        return True
                return False
        elif my_rank > oth_rank:
            return True
        else:
            return False
    
    def __lt__(self, other):
        return not self.__eq__(other) and not self.__gt__(other)
        
    @property
    def highest_card(self):
        faces = [self.card1.value, self.card2.value, self.card3.value]
        return max([max(v) for v in faces])
    
    def order_cards(self):
        faces = [self.card1.value, self.card2.value, self.card3.value]
        return list(reversed(sorted([max(v) for v in faces])))
    
    @property
    def value(self):
        suits = [self.card1.suit, self.card2.suit, self.card3.suit]
        faces = [self.card1.value, self.card2.value, self.card3.value]
        is_straight = self.__is_straight(faces)
        is_flush = self.__is_flush(suits)
        if is_straight and is_flush:
            return 'straight flush'
        if is_straight and not is_flush:
            return 'straight'
        if not is_straight and is_flush:
            return 'flush'
        if self.__is_trip(faces):
            return 'three of a kind'
        if self.__is_pair(faces):
            return 'pair' 
        return 'high card'
