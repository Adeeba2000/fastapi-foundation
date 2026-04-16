from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Annotated, Optional

class Patient(BaseModel):

    name: str
    age: int
    email: EmailStr
    married: Optional[bool] = False
    allergies: Optional[List[str]] = Field(max_length = 5)
    contact: Dict[str, str]


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)

patient_info = {
    'name':'john', 'age':30, 'email':'john123@gmail.com', 'married':True, 'allergies':['pollen','dust'], 'contact':{'phn': '1224', 'tel': '2345'}
}

patient1 = Patient(**patient_info)

update_patient_data(patient1)

#Field Validator
class Employee_Patient(BaseModel):

    name: str
    age: int
    email: EmailStr
    married: Optional[bool] = False
    allergies: Optional[List[str]] = Field(max_items = 5)
    contact: Dict[str, str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):

        valid_domains = ['hdfc.com', 'icici.com']

        domain = value.split('@')[-1]

        if domain not in valid_domains:
            raise ValueError('Invalid domain.')
        
        return value
    
patient_info2 = {
    'name':'john', 'age':30, 'email':'john123@hdfc.com', 'married':True, 'allergies':['pollen','dust'], 'contact':{'phn': '1224', 'tel': '2345'}
}

patient2 = Employee_Patient(**patient_info2)

update_patient_data(patient2)

#Model Validator
class Senior_Citizen_Patient(BaseModel):

    name: str
    age: int
    email: EmailStr
    married: Optional[bool] = False
    allergies: Optional[List[str]] = Field(max_length = 5)
    contact: Dict[str, str]

    @model_validator(mode= 'after')
    def validate_emergency_contact(self):

        if self.age > 60 and 'emergency' not in self.contact:
            raise ValueError('Senior citizen must have emergency contact.')
        
        return self


#Computed Field - calculated thorough other fields
class Patient_P(BaseModel):

    name: str
    age: int
    email: EmailStr
    height: int
    weight: int
    married: Optional[bool] = False

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/(self.height**2),2)
    

#Serialization: Exporting model into dict/json

#Converting this model into dict
temp = patient1.model_dump()  
# temp = patient1.model_dump(include = ['name'])   #to control which fileds to include in dict
print(patient1, type(patient1))
print(temp, type(temp))

#Converting this model into json
temp2 = patient1.model_dump_json()  
print(patient1, type(patient1))
print(temp2, type(temp2))