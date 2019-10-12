import random
from IPython.display import clear_output

class HangMan():
    def __init__(self):
        modes = ('easy', 'normal', 'hard')
        self.categories = {
            'music' : {
                'easy' :  ['Beat', 'Guitar', 'Drums', 'Chord', 'Note'],
                'normal': ['Chorus', 'Verse', 'Soprano', 'Tenor', 'Violin'],
                'hard' : ['Allegro', 'Adagio', 'Bass', 'Alto', 'Accompaniment']
            }
        }
        m = ''
        while not m in modes:
            m = input('easy, normal, or hard?: ').strip().lower()
        self.mode = m

        c = ''
        while not c in self.categories.keys():
            c = input('music or music?:').strip().lower()
        self.category = c

        self.alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
        self.ciphers = {
            'normal' : ['_' for i in range(26)],
            'easy' : self.randomPermute(list(self.alphabet[::])),
            'hard': self.randomPermute(list(self.alphabet[::]))
        }

        self.initialLives = {
            'normal': 7,
            'easy': 7,
            'hard': 3,
        }
        self.lives = self.initialLives[self.mode]
        self.cipher = self.ciphers[self.mode]
        self.dictionary = self.initialiseDictionary(self.cipher)
        self.remaining = set(self.alphabet)
        self.guessed = set({})

        self.word = self.chooseWord().strip().lower()
        self.end_game = False
        self.runGame()


    def chooseWord(self):
        num_choices = len(self.categories[self.category][self.mode])
        r = random.randint(0,num_choices-1)
        return self.categories[self.category][self.mode][r]

    def randomPermute(self,aList):
        # for each item in the list
        # generates a random integer between 0 and the len of the list
        # and switches the value at the current index with the value at the random index
        for i in range(len(aList)):
            j = random.randint(0,25)
            aList[i], aList[j] = aList[j], aList[i]
        return aList

    def initialiseDictionary(self, cipher):
        '''
            initialiseDictionary takes a list of 26 characters, cipher,
            and returns a dictionary that maps the letters of the english alphabet
            to their game representation based on the passed in cipher
        '''
        # {letter : index of representation of the letter in the alphabet list}
        seed_dict = {
            'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3, 'e' : 4, 'f' : 5, 'g' : 6,
            'h' : 7, 'i' : 8, 'j' : 9, 'k' : 10,'l' : 11, 'm' : 12,  'n' : 13,
            'o' : 14, 'p' : 15, 'q' : 16, 'r' : 17, 's' : 18, 't' : 19, 'u' : 20,
            'v' : 21, 'w' : 22, 'x' : 23, 'y' : 24, 'z' : 25
        }
        for k,v in seed_dict.items():
            seed_dict[k] = { 'masked': cipher[v], 'revealed': self.alphabet[v] }
        return seed_dict


    def maskWord(self):
        '''
        self.remaining is the set of letters not yet guessed.
        self.guessed is the set of letters guessed so far.
        maskWord iterates through the passed in word --
            -- If the character is in remained, concatenate the masked form
            -- else if the character is in guessed, concatenate the revealed form (user has guessed)
        '''
        masked_word = ''
        for char in self.word:
            if char in self.remaining:
                # TODO, logic for setting self.won as True or False
                # or could just do i 'masked_word == word' afterwards
                masked_word += self.dictionary[char]['masked']
            elif char in self.guessed:
                masked_word += self.dictionary[char]['revealed'].upper()
        return masked_word

    def displayWord(self):
        masked_word = self.maskWord()
        for char in masked_word:
            print(char, ' ', end = '')
        print('\n')
        return

    def runGame(self):
        self.end_game = False
        clear_output()
        while not self.end_game:
            self.lost_life = False
            print(f'You have {self.lives} lives remaining.')
            print(f'You have guessed: {self.guessed} ')
            self.displayWord()
            c  = input('Guess a letter or type quit to exit: ').strip().lower()
            clear_output()
            # check and clean up input
            if c in self.alphabet:
                if c in self.remaining:
                    self.remaining.remove(c)
                    self.guessed.add(c)
                    if c in self.word:
                        print(f'{c} is in the word')
                    elif c not in self.word:
                        self.lives -= 1
                        print(f'{c} is not in the word')
                else:
                    print(f'You already guessed {c}')
            elif c == 'quit':
                self.end_game = True
            else:
                print('Invalid input.')
            if self.word.upper() == self.maskWord():
                print(f'You win!  The word is {self.word}.')
                self.end_game = True
            if self.lives <= 0:
                print(f'No more lives. The word is {self.word}.')
                self.end_game = True
            self.displayWord()

        if input('Play again? y/n:').strip().lower() in 'yes':
            HangMan()
            return
        else:
            return False


HangMan()
