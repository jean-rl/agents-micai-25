# AI Agents using Small Language Models - MICAI 2025

![tutorial-banner](./slides/tutorial_banner.png)

Welcome to the repository of the tutorial. We're happy to have you here!

Here we've packed a small collection of resources to help you get started with building AI agents using small language models. The repository is structured as follows:

- `utils/`: Contains the `llama-server` binary (compiled for T4 instances) required to run `colab_agents.ipynb` on Google Colab, and the MCP utility script used by `mcp.ipynb`.
- `papers/`: A collection of relevant papers and articles that provide deeper insights into the topics covered in the tutorial.
- `slides/`: The slide deck used during the tutorial presentation.

# 🚀 Getting Started

To get started, clone this repository to your local machine:

```bash
git clone https://github.com/jean-rl/agents-micai-25.git
cd agents-micai-25
```

Make sure you have the necessary dependencies installed. You can find the requirements in the `notebooks/` directory.

# 🐍 Installation

If you plan to run the notebooks locally, ensure you have Python and Jupyter installed. You can set up a virtual environment and install the required packages using uv (preferred).

#### uv 

**Only for local setup**. To install follow the official instructions for your OS [here](https://docs.astral.sh/uv/getting-started/installation/).

#### Inference Engine

- `Colab`: If you wish to run the `colab_agents.ipynb` notebook on Google Colab, no additional setup is required. The notebook is pre-configured to use the `llama-server` binary included in the `utils/` folder.
- `Local Setup`: First download and install LM Studio from [this link](https://lmstudio.ai/). Then download a compatible model for local inference using the user interface. We recommend `qwen/qwen3-4b-thinking-2507` or `llama3.1-8b`. To see full logs while running any language model, open a terminal and run `lms log stream`, for more details visit the [log-stream](https://lmstudio.ai/docs/cli/log-stream) documentation.

# ⚙️ Tutorial Structure & Requirements

The tutorial is divided into **three** main sections, you can use this as a guide to navigate through the materials, but we recommend following the order presented in the slides.

#### 🧪 1. Language Models Overview

**You can run this module either locally or in Google Colab**. The associated notebooks are `tokenizer.ipynb`, `forward_bert.ipynb`, and `attention_mechanism.ipynb`. Here we cover the basics of language models, including tokenization, model architecture, and attention mechanisms used in transformer-based models.

#### 🧩 2. MCPs

**You can run this module only locally with LMStudio**. The associated notebook is `mcp.ipynb`, and the utility scripts are in the `utils/mcp/` folder. Here we explore the Model Context Protocol (MCPs) and how it's used to enchance the capabilities of language models for tools usage.

#### 🧠 3. Agents Module

**You can run this module either locally or in Google Colab**. The associated notebooks are `colab_agents.ipynb` and `lmstudio_agents.ipynb`. Here we dive into building AI agents using small language models, demonstrating how an agent framework can be implemented for experimental purposes.

# Contact

If you have any questions or need further assistance, feel free to reach out to any of the tutorial organizers:

- Hugo J. Escalante [hugo.jair@gmail.com]
- Luis Arellano [arellano.luis.3c@gmail.com]
- Jeanfed Ramirez [jeanfed.ramirez@gmail.com]

We hope you find this tutorial helpful and enjoy exploring the world of AI agents with small language models!