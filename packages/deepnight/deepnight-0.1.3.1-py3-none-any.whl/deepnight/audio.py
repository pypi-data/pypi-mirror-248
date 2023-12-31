import httpx
from ._globals import BASE_URL
import os as _os
from tqdm import tqdm

def load_file(path):
    try:  
        with open(path, "rb") as e:  
            files = {"audio_file": (path, e, "application/octet-stream")}  
        return files  
    except Exception as e:  
        print(e)


class Audio:
    def __init__(self, apikey: str, api_version: str, timeout: int) -> None:
        self.apikey = apikey
        self.api_version = api_version
        self.timeout = timeout

    def list_models(self):  # `self` here is not to be used but is passed to maintian consistency
        # print(BASE_URL)
        audio_models = {  
            "transcription": {  
                "vani-base": {  
                    "multi-lingual": True,  
                    "auto-detect": True,  
                    "translate": True  
                },  
                "vani-large": {  
                    "multi-lingual": True,  
                    "auto-detect": True,  
                    "translate": True  
                }  
            }  
        }  
    
        print(audio_models) 


    def transcribe(
        self,
        engine: str,
        path: str,
        timestamps: bool,
        translate: bool
    ) -> str:
        d_ = {
            "engine": engine,
            "timestamps": timestamps,
            "translate": translate
        }
        h_ = {
            "deepnight-authorization": self.apikey,
            "deepnight-api_v": self.api_version
        }

        client = httpx.Client(timeout=self.timeout)

        file_size = _os.path.getsize(path)

        try:
            # Open the file in binary mode and send it directly in the POST request
            with open(path, "rb") as file:
                files = {"audio_file": (path, file, "audio/*")}
                response = client.post(
                    f"{BASE_URL}/{engine}",
                    headers=h_,
                    data=d_,
                    files=files,
                    # Disable progress bar update by setting unit to None
                    # (we'll manually update it based on the number of bytes read)
                    # hooks={'response': lambda r, *args, **kwargs: pbar.update(len(chunk)) if chunk else None}
                )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Request to DEEPNIGHT failed with status code {response.status_code}")
                print("DEEPNIGHT Response content:", response.text)

        except httpx.RequestError as e:
            print("We couldn't connect to the API.")

        finally:
            client.close()


    def create_instance(self):
        # ins_model = input("Please select your model:\n\nPress 'A' for Vani Base\nPress 'B' for Vani Large")
        # _os.system("cls")
        # ins_name = input("Please give a name to your instance: ")
        # _os.system("cls")

        # instance = {
        #     "type": "Transcription",
        #     "model": "vani-base" if ins_model == "A" else "vani-large",
        #     "name": ins_name,
        # }

        print("NOT AVAILABLE YET. COMING SOON!")