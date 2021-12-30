import requests

server_endpoint = "http://localhost:8000"

# concept
concept = requests.get(server_endpoint + "/concept/")
print(concept.json()['results'][0])
concept = requests.get(server_endpoint + "/concept/?f=concept_id:35530122")
print(concept.json()['results'][0])
concept = requests.get(server_endpoint + "/concept/?f=concept_name:SUBCUTANEOUS INJECTION")
print(concept.json()['results'][0])
concept = requests.get(server_endpoint + "/concept/?f=concept_code:8f665d4b-2d9c-8b5a-e053-2995a90a4caa")
print(concept.json()['results'][0])
concept = requests.get(
    server_endpoint + "/concept/?f=concept_id:35530122,concept_code:8f665d4b-2d9c-8b5a-e053-2995a90a4caa")
print(concept.json()['results'][0])

# condition occurrecne
condition_occ = requests.get(server_endpoint + "/condition-occurrence/")
print(condition_occ.json()['results'][0])
condition_occ = requests.get(server_endpoint + "/condition-occurrence/?f=condition_source_value:162864005")
print(condition_occ.json()['results'][0])
condition_occ = requests.get(server_endpoint + "/condition-occurrence/?f=condition_type_concept__concept_name:EHR")
print(condition_occ.json()['results'][0])
condition_occ = requests.get(
    server_endpoint + "/condition-occurrence/?f="
                      "condition_type_concept__concept_name:EHR,condition_source_concept__concept_name:Body")
print(condition_occ.json()['results'][0])

# death
death = requests.get(server_endpoint + "/death/")
print(death.json()['results'][0])
death = requests.get(server_endpoint + "/death/?f=cause_source_value:22298006")
print(death.json()['results'][0])
death = requests.get(server_endpoint + "/death/?f=cause_concept__concept_name:No")
print(death.json()['results'][0])

# drug-exposure
drug = requests.get(server_endpoint + "/drug-exposure/")
print(drug.json()['results'][0])
drug = requests.get(server_endpoint + "/drug-exposure/?f=route_concept__concept_name:No")
print(drug.json()['results'][0])
drug = requests.get(server_endpoint + "/drug-exposure/?f=drug_source_value:308182,route_concept__concept_name:No")
print(drug.json()['results'][0])

# person
person = requests.get(server_endpoint + "/person/")
print(person.json()['results'][0])
person = requests.get(server_endpoint + "/person/?f=race_concept__concept_name:White")
print(person.json()['results'][0])
person = requests.get(
    server_endpoint + "/person/?f=race_concept__concept_name:White,gender_concept__concept_name:FEMALE")
print(person.json()['results'][0])

# person 통계
person_count = requests.get(server_endpoint + "/person/count/")
print(person_count.json())

# visit occurrecne
visit_occ = requests.get(server_endpoint + "/visit-occurrence/")
print(visit_occ.json()['results'][0])
visit_occ = requests.get(server_endpoint + "/visit-occurrence/?f=visit_concept__concept_name:Outpatient")
print(visit_occ.json()['results'][0])
visit_occ = requests.get(
    server_endpoint + "/visit-occurrence/?f=visit_source_value:ac25f574-971c-4685-8034-359a00b09857")
print(visit_occ.json()['results'][0])

# visit 통계
visit = requests.get(server_endpoint + "/visit/count/")
print(visit.json())
