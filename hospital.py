from __future__ import annotations

class Person(object):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.role = None

    def hello(self):
        print("Hello!")

class Patcient(Person):
    def __init__(self: Patcient, name: str, age: int):
        super(Patcient, self).__init__(name, age)
        self.role = "Patcient"

    def hello(self):
        super(Patcient, self).hello()
        print("I'm patcient!")

class Doctor(Person):
    def __init__(self: Doctor, name: str, age: int):
        super(Doctor, self).__init__(name, age)
        self.role = "Doctor"

    def hello(self):
        super(Doctor, self).hello()
        print("I'm doctor!")

class Hospital:
    def __init__(self: Hospital):
        self.__patcients: list[Patcient] = []
        self.__doctors: list[Doctor] = []
        return None

    def append(self, person: Person):
        if isinstance(person, Person):
            if isinstance(person, Patcient):
                self.__patcients.append(person)
            elif isinstance(person, Doctor):
                self.__doctors.append(person)
            else:
                print("not patcient or doctor")
        else:
            print("not person")

    def output(self, person_type):
        match person_type:
            case d if issubclass(person_type, Doctor):
                self.__print_persons(self.__doctors)
            case p if issubclass(person_type, Patcient):
                self.__print_persons(self.__patcients)
        
    def organize_meet(self: Hospital, doctor: Doctor, patcient: Patcient, time: str) -> Meet:
        if doctor in self.__doctors and patcient in self.__patcients:
            meet = Meet(self, doctor, patcient, time)
            with open("meets.txt", 'a') as f:
                f.write(f'Doctor: {meet.doctor.name}, Patcient: {meet.patcient.name}, time: {meet.time}\n')
            return meet
        else:
            print("nah")

    def __print_persons(self: Hospital, persons: list[Person]):
        for index, person in enumerate(persons):
            print(f'Index: {index + 1}, Name: {person.name}, Age: {person.age}, Role: {person.role}')

    def meets_output(self):
        with open("meets.txt", 'r') as f:
            print("".join(f.readlines()))

class Meet:
    def __init__(self, hospital: Hospital, doctor: Doctor, patcient: Patcient, time: str):
        if isinstance(hospital, Hospital) and isinstance(doctor, Doctor) and isinstance(patcient, Patcient):
            self.hospital = hospital
            self.doctor = doctor
            self.patcient = patcient
            self.time = time


hospital = Hospital()

kirill = Patcient("Kirill Crack", 25)
bogdan = Patcient("Bogdan Nasvaj", 18)

seva = Doctor("Vselovod", 52)
erik = Doctor("Erik", 52)


hospital.append(kirill)
hospital.append(bogdan)
hospital.append(seva)
hospital.append(erik)

print("---------------------------------------------")
hospital.output(Patcient)
print("---------------------------------------------")
hospital.output(Doctor)
print("---------------------------------------------")

seva.hello()
kirill.hello()
hospital.organize_meet(seva, kirill, "11:50")
hospital.meets_output()
