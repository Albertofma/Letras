import random #To make the random string given to the player
import pandas as pd # type: ignore #This will be used for making a dataframe and with it calculate how common letters are
import unicodedata #For the string manipulation to change accented to unaccented
from collections import Counter, defaultdict
from itertools import combinations #For obtaining all permutations for a 10 letter set
import threading  # For creating the timer
import time  # For the sleep function

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
"""print(letter_counts_df)"""

#We generate a string of 10 letters (in this case we use the dataframe and take the column that has the weights to make it so that its less likely 
#to get a string of 10 weird consonants)
random_string = ''.join(random.choices(letter_counts_df['letter'], weights=letter_counts_df['normalized'], k=10))

#We print the random weighted string
print("Estas son tus 10 letras con las que hacer una palabra, tienes 1 minuto: ", random_string)

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

# Timer function
def timer():
    time.sleep(60)  # Wait for 60 seconds
    print("\nTiempo terminado! La palabra mas larga era: ", longest_word)
    exit()

# Start the timer thread
timer_thread = threading.Thread(target=timer)
timer_thread.start()


# Ask the user for input
user_input = input("Introduzca la palabra mas larga que haya encontrado : ")

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
    print(message, user_input)
else:
    print(message)


print("La palabra mas larga posible era:", longest_word)

