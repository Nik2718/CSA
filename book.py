#*****************************************************************************
import pickle
import os

class Entry:
    def __init__(self, surname, name, patronymic, number, note):
        self.surname = str(surname)
        self.name = str(name)
        self.patronymic = str(patronymic)
        self.number = str(number)
        self.note = str(note)

    def __eq__(self, other):
        if not isinstance(other, Entry):
            return NotImplemented
        return (self.surname == other.surname and
                self.name == other.name and
                self.patronymic == other.patronymic and
                self.number == other.number and
                self.note == other.note)

    def __str__(self):
        result = ""
        for s in (self.surname, self.name, self.patronymic,
                  self.number):
            result+=str(s)
            result += "; "
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

    def delete(self, surname, name, patronymic, number):
        catalogue_size = len(self.catalogue)
        i = 0
        while i < catalogue_size:
            ent = self.catalogue[i]
            is_selected = (surname in ("", ent.surname) and
                           name in ("", ent.name) and
                           patronymic in ("", ent.patronymic) and
                           number in ("", ent.number))
            if is_selected:
                self.catalogue.pop(i)
                catalogue_size = catalogue_size - 1
            else:
                i = i + 1

    def search(self, surname="", 
                     name="",
                     patronymic="",
                     number=""):
        result_list = []
        for ent in self.catalogue:
            is_selected = (surname in ("", ent.surname) and
                           name in ("", ent.name) and
                           patronymic in ("", ent.patronymic) and
                           number in ("", ent.number))
            if is_selected:
                result_list.append(ent)
        return result_list

    def search_note(self, text):
        text = str(text)
        result_list = []
        for ent in self.catalogue:
            if ent.note.find(text) >= 0:
                result_list.append(ent)
        return result_list

    def save(self):
        with open("catalogue.pickle", "wb") as f:
            pickle.dump(self.catalogue, f)








