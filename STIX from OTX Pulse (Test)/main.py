from OTXv2 import OTXv2
import os, json

class OTX_Test:
    def __init__(self, otx_api_key):
        self.parent_dir_to_save_stix = os.path.join(os.path.dirname(os.path.realpath(__file__)), "STIXs")
        self.otx = OTXv2(otx_api_key)
        
    def search_pulses(self, search, result_count=5):
        SEARCH_PULSES = "{}/search/pulses".format("/api/v1")   
        search_pulses_url = self.otx.create_url(SEARCH_PULSES, q=search, page=1, limit=25, sort="-modified")
        self.pulses = self.otx._get_paginated_resource(search_pulses_url, max_results=result_count)["results"]
    
    def save_pulse_details_as_json(self):
        for i, json_data in enumerate(self.pulses):
            pulse_id = json_data["id"]
            pulse_details = self.otx.get_pulse_details(pulse_id)
            save_file = open(os.path.join(self.parent_dir_to_save_stix, f"{i}_{pulse_id}.json"), "w")  
            json.dump(pulse_details, save_file, indent = 6)  
            save_file.close()

# TEST
if __name__ == "__main__":
    otx = OTX_Test("OTX_API_KEY")
    search = input("Search: ")
    otx.search_pulses(search)
    otx.save_pulse_details_as_json()

