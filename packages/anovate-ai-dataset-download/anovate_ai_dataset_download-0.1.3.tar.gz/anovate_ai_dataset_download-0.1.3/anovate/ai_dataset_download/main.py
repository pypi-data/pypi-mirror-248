import hashlib
import typer
from PyInquirer import prompt
from rich import print as rprint
import boto3
import requests
from pycognito import AWSSRP
import os
from tqdm.contrib.concurrent import process_map


SERVICE_NAME = "cognito-idp"
REGION_NAME = "eu-west-1"
APP_CLIENT_ID = "5sal7ribtg5c6evpo5d2ba6n4u"
USER_POOL = "eu-west-1_WxajqWOza"
BASE_URL = "https://nu42pnfemh.eu-west-1.awsapprunner.com/api"
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "datasets")


app = typer.Typer()
cognito = boto3.client(SERVICE_NAME, region_name=REGION_NAME)


def authenticate_and_get_token(username: str, password: str) -> None:
    aws_srp = AWSSRP(
        username=username,
        password=password,
        pool_id=USER_POOL,
        client_id=APP_CLIENT_ID,
        client=cognito,
    )
    auth_params = aws_srp.get_auth_params()
    resp = cognito.initiate_auth(
        AuthFlow="USER_SRP_AUTH",
        AuthParameters=auth_params,
        ClientId=APP_CLIENT_ID,
    )

    challenge_response = aws_srp.process_challenge(
        resp["ChallengeParameters"], auth_params
    )
    resp = cognito.respond_to_auth_challenge(
        ClientId=APP_CLIENT_ID,
        ChallengeName="PASSWORD_VERIFIER",
        ChallengeResponses=challenge_response,
    )
    return resp["AuthenticationResult"]["IdToken"]


def get_datasets(access_token: str):
    response = requests.get(
        url=f"{BASE_URL}/datasets",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"download": True},
    )
    datasets = {dataset["name"]: dataset["id"] for dataset in response.json()["items"]}
    return datasets


def get_images(access_token: str, dataset_id: int, completed_only: bool):
    params = {"download": True}
    if completed_only:
        params["status"] = "COMPLETED"
    response = requests.get(
        url=f"{BASE_URL}/datasets/{dataset_id}/images",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params,
    )
    return response.json()["items"]


def get_image_url(access_token: str, image_id: int):
    response = requests.get(
        url=f"{BASE_URL}/images/{image_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"download": True, "quality": "ORIGINAL"},
    )
    return response.json()["image_url"]


def get_image_hash(filename):
    try:
        with open(filename, "rb") as f:
            bytes = f.read()
            readable_hash = hashlib.sha256(bytes).hexdigest()
            return readable_hash
    except FileNotFoundError:
        return None


def handle_image(image_info: dict):
    image_name = image_info["image"]["path"]
    image_path = os.path.join(image_info["images_folder"], image_name)
    image_hash = get_image_hash(image_path)
    if image_hash != image_info["image"]["hash"]:
        img_url = get_image_url(image_info["access_token"], image_info["image"]["id"])
        r = requests.get(img_url, allow_redirects=True)
        open(image_path, "wb").write(r.content)


@app.command("download-dataset")
def download_dataset(
    username: str = typer.Option(prompt=True),
    password: str = typer.Option(prompt=True, hide_input=True),
    dataset: str = typer.Option(
        default=None,
        prompt=False,
        help="Dataset name if not supplied will be prompted to select dataset",
    ),
    completed_only: bool = typer.Option(
        default=False,
        prompt=False,
        help="Download only completed images",
    ),
    download_latest_export: bool = typer.Option(default=False, prompt=False),
):
    access_token = authenticate_and_get_token(
        username,
        password,
    )
    datasets = get_datasets(access_token)
    if not dataset:
        choices = [{"name": name} for name in datasets.keys()]
        module_list_question = [
            {
                "type": "list",
                "name": "dataset",
                "message": "Select dataset to download: ",
                "choices": choices,
            }
        ]

        dataset = prompt(module_list_question)["dataset"]
    try:
        dataset_id = datasets[dataset]
    except KeyError:
        rprint(f"[red bold]Dataset {dataset} not found")
        return
    rprint(f"[green bold]Downloading dataset : {dataset}")
    images = get_images(access_token, dataset_id, completed_only)
    dataset_path = os.path.join(DOWNLOAD_FOLDER, dataset)
    is_exist = os.path.exists(dataset_path)
    if not is_exist:
        os.makedirs(dataset_path)

    images_folder = os.path.join(dataset_path, "images")
    is_exist = os.path.exists(images_folder)
    if not is_exist:
        os.makedirs(images_folder)

    images = list(
        map(
            lambda image: {
                "access_token": access_token,
                "image": image,
                "images_folder": images_folder,
            },
            images,
        )
    )
    process_map(
        handle_image,
        images,
        max_workers=4,
    )

    if download_latest_export:
        response = requests.get(
            url=f"{BASE_URL}/datasets/{dataset_id}/dataset-export",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"latest": True},
        )
        
        result = response.json()
        if result:
            download_url = result[0]['download_url']
            r = requests.get(download_url, allow_redirects=True)
            open(os.path.join(dataset_path, "export.zip"), "wb").write(r.content)


if __name__ == "__main__":
    app()
