# -----------------------------SETTING ENVIRONMENT-----------------------------
import os
import uvicorn
import requests
import elevenlabs
from fastapi import FastAPI
from publitio import PublitioAPI
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


def MainFunction(names):
    ELEVENLABS_API = os.getenv("ELEVENLABS_API")
    PUBLITIO_API = os.getenv("PUBLITIO_API")
    PUBLITIO_SECRET = os.getenv("PUBLITIO_SECRET")
    GOOEY_API = os.getenv("GOOEY_API")

    elevenlabs.set_api_key(ELEVENLABS_API)
    publitio_api = PublitioAPI(PUBLITIO_API, PUBLITIO_SECRET)

    # -----------------------------ELEVENLABS-----------------------------

    if not os.path.exists("Audios/"):
        os.mkdir("Audios")

    Names = names

    for name in Names:
        text = f"Hi {name}, my name is Max, welcome to ADAPTA."
        # voice = "tcm9oOOhlpLxWHalMXbM" #max
        voice = "Adam"  # me
        audio = elevenlabs.generate(text=text, voice=voice)
        audio_filename = f"Audios/{name}.mp3"
        elevenlabs.save(audio, audio_filename)
        print(f"Saved {name}.mp3")

    # -----------------------------PUBLITIO UPLAODER-----------------------------

    folder_path = "Audios/"

    def Audio_Uploader(folder_path):
        uploaded_urls = {}

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "rb") as f:
                r = publitio_api.create_file(
                    file=f,
                    title=filename,
                    description=filename,
                )
                print(f"Uploaded {filename} to Publitio.")
                url_download = r.get("url_preview")
                if url_download:
                    uploaded_urls[filename] = url_download
                else:
                    print(f"Failed to get URL for {filename}")

        return uploaded_urls

    uploaded_urls = Audio_Uploader(folder_path)

    # -----------------------------CLEARING THE DIRECTORY-----------------------------
    directory = "Audios/"
    files = os.listdir(directory)

    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")

    # -----------------------------GOOEY AI LIPSYNC------------------------------
    url_list = list(uploaded_urls.values())
    print(url_list)
    names_list = list(uploaded_urls.keys())
    print(names_list)

    generated_urls = []

    results = []

    for name, url in zip(names_list, url_list):
        payload = {
            "input_face": "https://raw.githubusercontent.com/SOBANEJAZ/api-testing/main/video.mp4",
            "input_audio": url,
        }

        response = requests.post(
            "https://api.gooey.ai/v2/Lipsync/",
            headers={"Authorization": "Bearer " + GOOEY_API},
            json=payload,
        )
        assert response.ok, response.content

        result_info = {
            "name": name,
            "output_video": response.json()["output"]["output_video"],
        }
        results.append(result_info)


# for item in result:
#     print(f"Lipsync result for {item['name']}: {item['output_video']}")

app = FastAPI()

# -----------------------------SETTING ENVIRONMENT-----------------------------
import os
import uvicorn
import requests
import elevenlabs
from fastapi import FastAPI
from publitio import PublitioAPI


def MainFunction(names):
    ELEVENLABS_API = os.getenv("ELEVENLABS_API")  # chan
    PUBLITIO_API = os.getenv("PUBLITIO_API")
    PUBLITIO_SECRET = os.getenv("PUBLITIO_SECRET")
    GOOEY_API = os.getenv("GOOEY_API")

    elevenlabs.set_api_key(ELEVENLABS_API)
    publitio_api = PublitioAPI(PUBLITIO_API, PUBLITIO_SECRET)

    # -----------------------------ELEVENLABS-----------------------------

    if not os.path.exists("Audios/"):
        os.mkdir("Audios")

    Names = names

    for name in Names:
        text = f"Hi {name}, my name is Max, welcome to ADAPTA."
        # voice = "tcm9oOOhlpLxWHalMXbM" #max
        voice = "Adam"  # me
        audio = elevenlabs.generate(text=text, voice=voice)
        audio_filename = f"Audios/{name}.mp3"
        elevenlabs.save(audio, audio_filename)
        print(f"Saved {name}.mp3")

    # -----------------------------PUBLITIO UPLAODER-----------------------------

    folder_path = "Audios/"

    def Audio_Uploader(folder_path):
        uploaded_urls = {}

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "rb") as f:
                r = publitio_api.create_file(
                    file=f,
                    title=filename,
                    description=filename,
                )
                print(f"Uploaded {filename} to Publitio.")
                url_download = r.get("url_preview")
                if url_download:
                    uploaded_urls[filename] = url_download
                else:
                    print(f"Failed to get URL for {filename}")

        return uploaded_urls

    uploaded_urls = Audio_Uploader(folder_path)

    # -----------------------------CLEARING THE DIRECTORY-----------------------------
    directory = "Audios/"
    files = os.listdir(directory)

    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")

    # -----------------------------GOOEY AI LIPSYNC------------------------------
    url_list = list(uploaded_urls.values())
    print(url_list)
    names_list = list(uploaded_urls.keys())
    print(names_list)

    generated_urls = []

    results = []

    for name, url in zip(names_list, url_list):
        payload = {
            "input_face": "https://raw.githubusercontent.com/SOBANEJAZ/api-testing/main/video.mp4",
            "input_audio": url,
        }

        response = requests.post(
            "https://api.gooey.ai/v2/Lipsync/",
            headers={"Authorization": "Bearer " + GOOEY_API},
            json=payload,
        )
        assert response.ok, response.content

        result_info = {
            "name": name,
            "output_video": response.json()["output"]["output_video"],
        }
        results.append(result_info)
    return results


# Define your FastAPI endpoint
@app.post("/generate_videos")
async def generate_videos(names: list[str]):
    results = MainFunction(names)
    return {"results": results}


@app.get("/")
def root():
    a = "Hello I made an API"
    return a
