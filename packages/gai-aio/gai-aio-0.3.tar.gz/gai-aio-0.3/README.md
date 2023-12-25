# Gai/Gen: Universal LLM Wrapper

This is a Universal Multi-Modal Wrapper Library for LLM.

This library is designed to facilitate the use of comparable open source models on the local machine and facilitate the seamless switch between OpenAI API and open source models, adhering closely to the OpenAI API specs.

It is designed to be:

-   Dead-simple to use. One object, Gaigen (short for GAI generator), is all you need to generate text, speech, image and video.

-   Drop-in replacement for OpenAI API across models of all modality.

-   Focus on small models (7 billion parameters and below) that can be run on commodity hardware. That is why it is a singleton wrapper. Only one model is loaded and cached into memory at any one time.

**Note**: When using the singleton, make sure the generator is loaded using the GetInstance() method instead of the Gaigen() constructor.

The wrappers are organised under the `gen` folder according to 4 categories:

-   ttt: Text-to-Text
-   tts: Text-to-Speech
-   stt: Speech-to-Text
-   itt: Image-to-Text

---

## Setting Up

This package can be installed from PyPI:

```bash
pip install gai-aio
```

or clone from github:

```bash
git clone https://www.github.com/kakkoii1337/gai-aio
```

## Configuration

-   Create the default application directory `~/gai` and the default models directory `~/gai/models`.

-   Copy the `gai.json` config file from the repository into `~/gai`. This configuration file is used by the library to locate and interact with the models.

## API Key

-   All API keys should be stored in a `.env` file in the root directory of the project. For example,

    ```.env
    OPENAI_API_KEY=<--replace-with-your-api-key-->
    ANTHROPIC_API_KEY=<--replace-with-your-api-key-->
    ```

## Requirements

-   The instructions are tested mainly on:
    -   Windows 11 with WSL
    -   Ubuntu 20.04.2 LTS
    -   NVIDIA RTX 2060 GPU with 8GB VRAM
    -   CUDA Toolkit is required for the GPU accelerated models. Run `nvidia-smi` to check if CUDA is installed.
        If you need help, refer to this https://gist.github.com/kakkoii1337/8a8d4d0bc71fa9c099a683d1601f219e

## Credits

TTT

-   TheBloke for all the quantized models in the demo
-   turboderp for ExLlama
-   Meta Team for the LLaMa2 Model
-   HuggingFace team for the Transformers library and open source models
-   Mistral AI Team for Mistral 7B Model
-   ggerganov for LLaMaCpp

ITT

-   Liu HaoTian for the LLaVa Model and Library

TTS

-   Coqui-AI for the xTTS Model

STT

-   OpenAI for Open Sourcing Whisper v3

## Examples

Refer to 'gai.ipynb'
