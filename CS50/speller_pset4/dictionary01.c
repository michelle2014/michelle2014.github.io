// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {

        // allocate memory for a new node
        node *n = malloc(sizeof(node));
		
		memset(n, 0, sizeof(node));
		
        if (!n)
        {
            unload();
            return false;
        }

        // add word into list
        strcpy(n->word, word);

        if (hashtable[hash(word)] == NULL)
        {
            hashtable[hash(word)] = n;
        }
        else
        {
            n->next = hashtable[hash(word)];
            hashtable[hash(word)] = n;
        }
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // count from 0
    int wordCount = 0;


    // iterate through 26 buckets, if not loaded, return 0
    for (int i = 0; i < N; i++)
    {
        if (!hashtable[i])
        {
            return 0;
        }

        else
        {
            for (node *ptr = hashtable[i]; ptr != NULL; ptr = ptr->next)
            {
                if (strcmp(ptr->word, "") != 0)
                {
                    wordCount++;
                }
            }
        }
    }
    return wordCount;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    for (node *ptr = hashtable[hash(word)]; ptr != NULL; ptr = ptr->next)
    {
        if (strcasecmp(ptr->word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *ptr = n;

        while (ptr != NULL)
        {
            node *temp = ptr;
            ptr = ptr->next;
            free(temp);
        }

    return true;
}
