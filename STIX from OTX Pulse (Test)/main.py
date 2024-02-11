from OTXv2 import OTXv2
import os, json

class OTX_Test:
    def __init__(self, otx_api_key):
        self.parent_dir_to_save_stix = os.path.join(os.path.dirname(os.path.realpath(__file__)), "STIXs")
        self.otx = OTXv2(otx_api_key)
        
    def search_pulses(self, search, result_count=5):
        self.pulses = self.otx.search_pulses(search, max_results=result_count)["results"]
    
    def save_pulse_details_as_json(self):
        for i, json_data in enumerate(self.pulses):
            pulse_details = self.otx.get_pulse_details(json_data["id"])
            save_file = open(os.path.join(self.parent_dir_to_save_stix, f"{i}_stix.json"), "w")  
            json.dump(pulse_details, save_file, indent = 6)  
            save_file.close()

# TEST
if __name__ == "__main__":
    otx = OTX_Test("947dd2c3c7389ab6a5f8302c0389318cba166934ffe82654e3dd1fe968a02595")
    search = input("Search: ")
    otx.search_pulses(search)
    otx.save_pulse_details_as_json()

