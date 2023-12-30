#!/usr/bin/env python3

"""Main module for the README-AI CLI application."""

__package__ = "readmeai"

import asyncio
import os
import traceback

from readmeai.cli.options import prompt_for_custom_image
from readmeai.config.settings import (
    AppConfig,
    AppConfigModel,
    ConfigHelper,
    GitConfig,
    ImageOptions,
    load_config,
    load_config_helper,
)
from readmeai.core import logger, model, preprocess
from readmeai.markdown import headers, tree
from readmeai.services import git_operations as vcs

logger = logger.Logger(__name__)


def main(
    align: str,
    api_key: str,
    badges: str,
    emojis: bool,
    image: str,
    model: str,
    offline: bool,
    output: str,
    repository: str,
    temperature: float,
) -> None:
    """Main method of the readme-ai CLI application."""
    logger.info("Executing readme-ai CLI application.")
    os.environ["OPENAI_API_KEY"] = (
        api_key if api_key is not None else os.getenv("OPENAI_API_KEY", None)
    )
    conf = load_config()
    conf_model = AppConfigModel(app=conf)
    conf_helper = load_config_helper(conf_model)
    conf.git = GitConfig(repository=repository)
    conf.paths.output = output
    conf.cli.emojis = emojis
    conf.cli.offline = offline
    conf.llm.model = model
    conf.llm.temperature = temperature
    conf.md.align = align
    conf.md.badges_style = badges
    if image == ImageOptions.CUSTOM.name:
        conf.md.image = prompt_for_custom_image(None, None, image)
    else:
        conf.md.image = image
    asyncio.run(readme_agent(conf, conf_helper))


async def readme_agent(conf: AppConfig, conf_helper: ConfigHelper) -> None:
    """Orchestrates the README file generation process."""
    logger.info(f"Processing repo: {conf.git.source}: {conf.git.repository}")
    logger.info(f"Using llm model: {conf.llm.model}")
    logger.info(f"Output file path: {conf.paths.output}")

    llm = model.OpenAIHandler(conf)
    name = conf.git.name
    repo = conf.git.repository

    try:
        temp_dir = vcs.clone_repo_to_temp_dir(repo)
        repo_tree = tree.TreeGenerator(
            conf_helper=conf_helper,
            root_directory=temp_dir,
            repo_url=repo,
            project_name=name,
        ).generate_and_format_tree()
        conf.md.tree = conf.md.tree.format(repo_tree)

        logger.info(f"Directory tree structure: {conf.md.tree}")

        parser = preprocess.RepositoryParser(conf, conf_helper)
        dependencies, files = parser.get_dependencies(temp_dir)

        logger.info(f"Dependencies: {dependencies}")

        # Generate README.md file contents via OpenAI API.
        if conf.cli.offline is False:
            code_summary = await llm.code_to_text(
                files,
                conf_helper.ignore_files,
                conf.prompts.summaries,
                repo_tree,
            )
            prompts = [
                conf.prompts.slogan.format(conf.git.name),
                conf.prompts.overview.format(
                    repo, repo_tree, dependencies, code_summary
                ),
                conf.prompts.features.format(
                    repo, repo_tree, dependencies, code_summary
                ),
            ]
            slogan, overview, features = await llm.chat_to_text(prompts)
        else:
            code_summary = [
                (str(file_path), conf.md.default)
                for file_path, _ in files.items()
            ]
            slogan, overview, features = (
                conf.md.default,
                conf.md.default,
                conf.md.default,
            )

        conf.prompts.slogan = slogan
        conf.md.header = conf.md.header.format(
            conf.md.align, conf.md.image, name.upper(), slogan
        )
        conf.md.intro = conf.md.intro.format(overview, features)
        headers.build_readme_md(conf, conf_helper, dependencies, code_summary)

    except Exception as exc_info:
        logger.error(
            f"Exception: {exc_info}\nStacktrace: {traceback.format_exc()}"
        )
    finally:
        await llm.close()

    logger.info("Finished readme-ai execution.")
