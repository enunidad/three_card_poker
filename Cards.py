class Rank:
    def __init__(self, rank):
        self.value = rank
    @property
    def index(self):
        rank_map = {'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
        return int(rank_map.get(self.value, self.value))
    def __repr__(self):
        return f'Rank(rank = "{self.value}")'
    def __str__(self):
        return self.value
    def __eq__(self, other):
        return self.value == other.value
    def __gt__(self, other):
        return self.index > other.index
    def __ge__(self, other):
        return self > other or self == other
    def __lt__(self, other):
        return not self >= other
    def __le__(self, other):
        return self < other or self == other

class Suit:
    def __init__(self, shape):
        self.value = shape
    def __repr__(self):
        return f'Suit(shape = "{self.value}")'
    def __str__(self):
        return self.value
    def __eq__(self, other):
        return self.value == other.value
    def __gt__(self, other):
        return False
    def __ge__(self, other):
        return self == other or self > other
    def __lt__(self, other):
        return False
    def __le__(self, other):
        return self. == other or self < other
    
class Card:
    def __init__(self, value, suit):
        self.face = Rank(value)
        self.suit = Suit(suit)
    def __repr__(self):
        return f'Card(value = "{self.face.value}", suit = "{self.suit.value}")'
    def __str__(self):
        return f'{str(self.face)}{str(self.suit)}'
    def __eq__(self, other):
        return self.face == other.face
    def __gt__(self, other):
        return self.face > other.face
    def __ge__(self, other):
        return self > other or self == other
    def __lt__(self, other):
        return not self >= other
    def __le__(self, other):
        return self < other or self == other

class Hand:
    def __init__(self, card1, card2, card3):
        self.cards = list(reversed(sorted([card1, card2, card3], key = lambda x: x.face)))

    @property
    def is_royal_flush(self):
        my_cards = set([card.face.value for card in self.cards])
        if len(my_cards) < 3:
            return False, None
        if 'A' not in my_cards:
            return False, None
        sf, err1 = self.is_straight_flush
        if sf and len(my_cards ^ set('QKA')) == 0:
            return True, err1
        else:
            return False, None
    @property
    def is_straight_flush(self):
        straight, err1 = self.is_straight
        flush, err2 = self.is_flush
        if straight and flush:
            return True, err1
        else:
            return False, None
    @property
    def is_straight(self):
        valids = 'A23,234,345,456,567,678,789,89T,9TJ,TJQ,JQK,QKA'.split(',')
        my_cards = set([card.face.value for card in self.cards])
        if len(my_cards) < 3:
            return False, None
        for valid in valids:
            ref_cards = set(valid)
            if len(ref_cards ^ my_cards) == 0:
                return True, self.cards
        return False, None
    @property
    def is_flush(self):
        suits = set([card.suit.value for card in self.cards])
        if len(suits) == 1:
            return True, self.cards
        else:
            return False, None
    @property
    def is_trips(self):
        f = set([card.face.value for card in self.cards])
        if len(f) == 1:
            return True, self.cards
        else:
            return False, None

    @property
    def is_pair(self):
        f = set([card.face.value for card in self.cards])
        if len(f) == 2:
            if self.cards[0] == self.cards[1]:
                to_return = self.cards
            else:
                to_return = self.cards[1:] + self.cards[:1]
            return True, to_return
        else:
            return False, None

    @property
    def value(self):
        order = list(reversed(['pair', 'flush', 'straight', 'trips', 'straight_flush', 'royal_flush']))
        for rank in order:
            result, msg = eval(f'self.is_{rank}')
            if result == True:
                return rank, msg
        return 'high card', self.cards
    @property
    def index(self):
        order = list(reversed(['pair', 'flush', 'straight', 'trips', 'straight_flush', 'royal_flush']))
        for i, rank in enumerate(order):
            result, msg = eval(f'self.is_{rank}')
            if result == True:
                return i, msg
        return 6, self.cards

    def __eq__(self, other):
        mine, m = self.index
        your, y = other.index
        if mine == your:
            for s, o in zip(m, y):
                if s != o:
                    return False
            return True
        else:
            return False
                
    def __gt__(self, other):
        mine, m = self.index
        your, y = other.index
        if mine <= your:
            if mine < your:
                return True
            else:
                for s, o in zip(m, y):
                    if s > o:
                        return True
                return False
        else:
            return False
    def __ge__(self, other):
        return self > other or self == other
    def __lt__(self, other):
        return not self >= other
    def __le__(self, other):
        return self < other or self == other
        
    def __repr__(self):
        return 'Hand(' + ', '.join([f'card{i+1} = {card}'for i, card in enumerate(self.cards)]) + ')'
    def __str__(self):
        return f'{", ".join([str(card) for card in self.cards])}'
