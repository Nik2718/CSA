#*****************************************************************************
import pickle
import os

class Entry:
    def __init__(self, name, surname, patronymic, number, note):
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.number = number
        self.note = note

    def __eq__(self, other):
        if not isinstance(other, Entry):
            return NotImplemented
        return (self.name == other.name and
                self.surname == other.surname and
                self.patronymic == other.patronymic and
                self.number == other.number and
                self.note == other.note)

    def __str__(self):
        result = ""
        for s in (self.name, self.surname, self.patronymic,
                  self.number):
            if s != None:
                result+=str(s)
            result += "; "
        if self.note != None:
            result += str(self.note)
        return result

class Book:
    def __init__(self):
        if os.path.isfile("catalogue.pickle"):
            with open("catalogue.pickle", "rb") as f:
                self.catalogue = pickle.load(f)
        else:
            self.catalogue = []

    def add(self, ent):
        if isinstance(ent, Entry):
            if ent not in self.catalogue:
                self.catalogue.append(ent)

    def delete(self, ent):
        if isinstance(ent, Entry):
            if ent in self.catalogue:
                self.catalogue.remove(ent)

    def select(self, name=None, 
                     surname=None,
                     patronymic=None,
                     number=None):
        result_list = []
        for ent in self.catalogue:
            is_selected = (name in (None, ent.name) and
                           surname in (None, ent.surname) and
                           patronymic in (None, ent.patronymic) and
                           number in (None, ent.number))
            if is_selected:
                result_list.append(ent)
        return result_list

    def save(self):
        with open("catalogue.pickle", "wb") as f:
            pickle.dump(self.catalogue, f)








