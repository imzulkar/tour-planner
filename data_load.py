import json
from tour_planner.models import District,Division
def load_data():
    with open('districts.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data
    return []

def save_data():
    data = load_data()
    district = data.get('districts')
    for item in district:
        id = int(item['division_id'])
        print(id)
        print(type(id))
        division = Division.objects.get(id=id)
        district = District(name=item['name'], bn_name=item['bn_name'], lat=item['lat'], lon=item['long'], division=division)
        district.save()
    
save_data()