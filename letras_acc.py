import random #To make the random string given to the player
import pandas as pd # type: ignore #This will be used for making a dataframe and with it calculate how common letters are
import unicodedata #For the string manipulation to change accented to unaccented
from collections import Counter, defaultdict
from itertools import combinations #For obtaining all permutations for a 10 letter set
import threading  # For creating the timer
import time  # For the sleep function
import os #For terminating the program

# Define the file path
file_path = 'palabras.txt'

#Dictionary with accented letters and their unaccented counterparts to be replaced by
accented_to_unaccented = {
    'é': 'e', 'í': 'i', 'ú': 'u', 'á': 'a', 'ó': 'o', 'ü': 'u', 'è': 'e'
}

# Initialize an empty list to store the filtered words
filtered_words = defaultdict(list)#Dict that never raises a key error

#Function to replace accents in how common the letters are
def replace_accented_letters(word):
    return ''.join(accented_to_unaccented.get(char, char) for char in word) #This will parse all the words in the file and replace the first char in the dict (the accented one) with the solution

# Open and read the file
with open(file_path, 'r', encoding='utf-8') as file:
    # Read each line (word) in the file
    for line in file:
        if len(line) > 10: #Only continue id the word has less than 10 letters
            continue
        # Strip any leading/trailing whitespace, force lowercase and check the word length
        word = line.strip().lower()
        word = replace_accented_letters(word) #Call function to replace accents

        filtered_words[''.join(sorted(word))].append(word) 

#This will join every single word below 10 letters
all_letters = ''.join(filtered_words)

#Count the number of letters in the enormous string
letter_counts = Counter(all_letters)

#With this we count the total amount of letters
total_letters = sum(letter_counts.values())

#Dictionary where we the Normalize the letter counts by dividing them by the total amount of letters, this is dict comprehension the syntax is :{key_expression: value_expression for item in iterable}
normalized_counts = {letter: count / total_letters for letter, count in letter_counts.items()}

#Convert the list to a dataframe, where the first parameter is the data, the second means that the keys of the data (this case the letters) are in the rows and then we specify that the column name is normalized
#Then with reset the letters become a regular column
letter_counts_df = pd.DataFrame.from_dict(normalized_counts, orient='index', columns=['normalized']).reset_index()

#then with rename we rename the column
letter_counts_df = letter_counts_df.rename(columns={'index': 'letter'})

#Clean dataframe from the unwanted symbols (-_´)
letter_counts_df = letter_counts_df.sort_values(by='normalized', ascending=False)
indeces_to_remove = [27, 26, 29, 30]
letter_counts_df = letter_counts_df.drop(indeces_to_remove)
letter_counts_df = letter_counts_df.reset_index(drop=True)

#Create a dataframe for vowels and another one for consonants
vowel_indeces = [0, 1, 3, 4, 10]
vowels_df = letter_counts_df.loc[vowel_indeces] #Maintain only the vowels in the dataframe
vowels_df = vowels_df.reset_index(drop=True) #Reset index
consonants_df = letter_counts_df.drop(vowel_indeces) #Drop the vowels
consonants_df = consonants_df.reset_index(drop=True)

"""#We generate a list of 10 letters (in this case we use the dataframe and take the column that has the weights to make it so that its less likely 
#to get a string of 10 weird consonants)
random_string = ''.join(random.choices(letter_counts_df['letter'], weights=letter_counts_df['normalized'], k=10))"""

#Asking the player for a 10 letter string
random_string=""
while (len(random_string) < 10): #loop until the string is 10 letters long
    desired_letter = input("¿Quiere una vocal o una consonante?(v/c)") #We ask for vowels or consonants to the player
    if desired_letter == 'v':
        random_string += random.choices(vowels_df['letter'], weights=vowels_df['normalized'], k=1)[0]#The [0] at the end is because rando.choices generates a list
        #But for concatenation we would need str values, so we choose the first element of the list that happens to be a str
        print(random_string)
    elif desired_letter == 'c':
        random_string += random.choices(consonants_df['letter'], weights=consonants_df['normalized'], k=1)[0] 
        print(random_string)
    else:
        print("\nSi quiere una vocal teclee v, si quiere una consonante teclee c.")

#We print the random weighted string
print("\nEstas son tus 10 letras con las que hacer una palabra, tienes 1 minuto: ", random_string)

#Now we need to find the longest word that can be made with those letters

def find_longest_word(letters, word_list): 
    
     # Iterate over lengths from len(letters) down to 1
    for length in range(len(letters), 0, -1):
        for sample in combinations(letters, length): # Since we have all the words sorted by alphabetical order we can use combinations instead of permutations,
            #We do this since it is way more efficient 
            sorted_letters = ''.join(sorted(sample))#We sort the combination made to look it up in the passed dict (it should be sorted as well for this to work)
            matches = word_list.get(sorted_letters, None)#We see if the sorted string matches the sorted word
            if matches:
                return matches #It they match we have found our longest word

    return None
#Use the longest word function
longest_word = find_longest_word(random_string, filtered_words)

# Event to signal input received
input_event = threading.Event()

# Timer function
def timer():
    if not input_event.wait(60):  # Wait for 60 seconds or until the event is set
        print("\nTiempo terminado! Juego terminado.")
        os._exit(1) #Force the program to exit in the case that the player hasnt submitted anything

# Start the timer thread
timer_thread = threading.Thread(target=timer) #Create a thread object, timer is target function that will run in the new thread
timer_thread.start() #Start it with the start method

# Ask the user for input
try:
    user_input = input("Introduzca la palabra más larga que haya encontrado : ")
    input_event.set()  # Set the event when input is received
except KeyboardInterrupt: #To catch the case where the user does ctrl+c
    print("\nJuego abortado.")
    exit()

user_input = replace_accented_letters(user_input)#Make lowercase then change accents to compare with list that we have

def validate_user_input(user_input, word_list):
    if not (1 <= len(user_input) <= 10):
        return False, "La palabra debe tener entre 1 y 10 letras."
    
    if not all(char in random_string for char in user_input):
        return False, "La palabra contiene caracters invalidos."
    sorted_input = ''.join(sorted(user_input))
    if sorted_input not in word_list:
        return False, "La palabra no pertenece al español."
    
    return True, "Respuesta valida."

is_valid, message = validate_user_input(user_input, filtered_words)

if is_valid:
    print(message)
else:
    print(message)


print("La palabra mas larga posible era:", longest_word)

