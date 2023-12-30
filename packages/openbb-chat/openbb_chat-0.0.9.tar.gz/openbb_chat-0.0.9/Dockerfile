FROM nvidia/cuda:11.7.1-devel-ubuntu22.04

# Update system
RUN apt update && apt install -y python3-pip && apt install -y python3-venv

# Configure Poetry
ENV POETRY_VERSION=1.5.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /openbb-chat/

# Add dependencies
ADD poetry.lock /openbb-chat/poetry.lock
ADD pyproject.toml /openbb-chat/pyproject.toml
RUN poetry install --no-root
ADD openbb_chat /openbb-chat/openbb_chat
ADD README.md /openbb-chat/README.md
RUN poetry install --only-root

# Add project root
ADD .project-root /openbb-chat/.project-root

# Add scripts, data and configs
ADD scripts /openbb-chat/scripts/
ADD data /openbb-chat/data/
ADD configs /openbb-chat/configs/

# Add mkdocs documentation
ADD docs /openbb-chat/docs
ADD mkdocs.yml /openbb-chat/mkdocs.yml

# Tests
ADD tests /openbb-chat/tests/

ENTRYPOINT ["/bin/bash"]

# IMPORTANT: To reduce start up time, download HF models and mount Docker with /root/.cache/huggingface/hub/ mapped to the local downloads
