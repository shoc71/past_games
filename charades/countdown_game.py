import random

intro = "You're playing countdown; letters will be drawn at random and you have to get the biggest word possible"
vowels = "aeiou"
consonant = "qwrtypsdfghjklzxcvbnm"
max_cap = 9
enter_list = []
count = 0

def user_input():
    global enter_here
    enter_here = input("what section letter would you like? \
    \n(1.vowel/2.consonant): ")

def entering_list(count):
    if enter_here == "1" or enter_here == "vowel" or enter_here == "1.vowel":
        count += 1
        r_vowel = random.choice(vowels.upper())
        enter_list.append(r_vowel)
        print(f"your letter is \"{r_vowel}\" \nyou have {max_cap-count} letters to go")
    elif enter_here == "2" or enter_here == "consonant" or enter_here == "2.consonant":
        count += 1
        r_consonant = random.choice(consonant.upper())
        enter_list.append(r_consonant)
        print(f"your letter is {r_consonant} you have {max_cap-count} letters to go")
        print(f"you have {max_cap-count} letters to go")

    
while True:
    if len(enter_list) > 3:
        break
    else:
        user_input()
        entering_list(count)

print(enter_list)
