from huggingface_hub import hf_hub_download

VERIFIED_PROVIDER = [
    "erfanzar",
    "LucidBrains"
]

AVAILABLE_MODELS = [
    "LinguaMatic-1B-GGUF",
    "LinguaMatic-2.7B-GGUF",
    "LinguaMatic-Tiny-GGUF",
    "Pixely1B-GGUF"
]

AVAILABLE_FORMATS = [
    "Q2_K",
    "Q3_K_S",
    "Q3_K_M",
    "Q3_K_L",
    "Q4_K_S",
    "Q4_K_M",
    "Q5_K_S",
    "Q5_K_M",
    "Q6_K"
]

PROMPTING_STYLES = [
    "Llama2",
    "OpenChat"
]

CHAT_MODE = [
    "Instruction",
    "Chat"
]


def prepare_model_to_load(
        model_name: str,
        quantize_format: str,
        provider: str = "erfanzar",
        check_availability: bool = True
):
    """
    The prepare_model_to_load function is used to prepare the model name and format for loading.

    :param model_name: str: Specify the model name
    :param quantize_format: str: Specify the format of the model
    :param provider: str: Specify the provider of the model
    :param check_availability: bool: Check if the model is available in libreassist
    :return: The model name and the file path of the quantized model
    """
    if check_availability:
        assert model_name in AVAILABLE_MODELS, (
            f"Couldn't Find the model {model_name} available Models are {AVAILABLE_MODELS}"
        )
        assert quantize_format in AVAILABLE_FORMATS, (
            f"Couldn't Find the format {quantize_format} Available formats for `{model_name}` Model are"
            f" {AVAILABLE_FORMATS}"
        )

    if provider not in VERIFIED_PROVIDER:
        print(
            "\033[1;32mWarning\033[1;0m : the provider you have chosen is not a valid provider in LibreAssist "
            "Be Careful with Model Behavior"
        )

    file_path = f"{model_name}.{quantize_format}.gguf"
    repo_id = f"{provider}/{model_name}"
    return repo_id, file_path


def download_model_gguf(

        model_name: str,
        quantize_type: str,
        provider: str,
        hf_token: str = None
):
    """
    The function `download_model_gguf` downloads a model from a specified provider using the given model
    name and quantize type.

    :param model_name: The name of the model you want to download
    :type model_name: str
    :param quantize_type: The `quantize_type` parameter is a string that specifies the type of
    quantization to be applied to the model. Quantization is a technique used to reduce the memory
    footprint and computational requirements of a model by representing the model's weights and
    activations with lower precision numbers. Common quantization types include "
    :type quantize_type: str
    :param provider: The `provider` parameter refers to the source or provider of the model. It could be
    a specific organization, platform, or repository that hosts the model
    :type provider: str
    :param hf_token: the huggingface access token
    :type hf_token: str
    :return: the reference to the downloaded model.
    """

    repo_id, file_path = prepare_model_to_load(
        model_name,
        quantize_type,
        provider
    )
    tkn = {}
    if hf_token is not None or hf_token != "":
        tkn = dict(token=hf_token)
    ref = hf_hub_download(
        repo_id=repo_id,
        filename=file_path,
        **tkn
    )
    return ref
