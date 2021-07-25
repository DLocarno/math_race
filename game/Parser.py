import pygame
import os

class Parser():

    def __init__(self):
        self.index = 0
        
    def load_transcript(self, transcript):
        self.transcript_file = transcript
        try:
            with open(self.transcript_file) as file:
                self.transcript = file.readlines()
        except:
            print("No transcript named", self.transcript_file, "found.")
            return None
        
        # Removes additional lines after delimeter at end of text transcript
        delete_remaining = False
        for line in range(0, len(self.transcript), 1):
            if self.transcript[line] == "*END\n":
                delete_remaining = True
            if delete_remaining == True:
                del self.transcript[line:]
                break
                
    def get_text(self):
        self.current_text = []
        for i in range(self.index, len(self.transcript), 1):
            if self.transcript[i] != "\n":
                self.current_text.append(self.transcript[i])
                self.index += 1
            else:
                self.index += 1
                break
        
        # remove all newline chars
        self.current_text = [el.strip() for el in self.current_text]
        
        return self.current_text

        