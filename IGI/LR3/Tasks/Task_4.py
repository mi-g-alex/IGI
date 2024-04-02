from Decorator import task_decorator


@task_decorator
def task_4():
    """
        **Lab Work 3 | Task 4**

        * Developer: Gorgun Alexander

        * Date: 29.03.2024

        I. Determine number of words whose length is 3 characters
        II. Find words whose number of vowels is equal to number of consonants and their ordinal numbers
        III. Print words in descending order of their lengths
    """

    s = ("So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and "
         "stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the"
         " daisies, when suddenly a White Rabbit with pink eyes ran close by her.")

    s = s.replace(',', '').replace('.', '').replace('-', '').lower()
    list_of_word = s.split(' ')
    list_of_vowel = {'a', 'o', 'i', 'e', 'y', 'u'}

    print("Words with len 3:", len([i for i in list_of_word if len(i) == 3]))
    print()
    list_of_vc = {i + 1: item for i, item in enumerate(list_of_word) if
                  len([j for j in item if j in list_of_vowel]) == len([j for j in item if j not in list_of_vowel])}

    print("Vowel == Consonant: ")
    print(list_of_vc)
    print()

    list_of_word.sort(key=lambda x: len(x), reverse=True)
    print("Sorted in descending order of lengths:")
    print(list_of_word)
