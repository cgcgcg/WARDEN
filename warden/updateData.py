#!/usr/bin/env python3
import subprocess
from pathlib import Path
from . common import loadConfig, parseFiles
from datetime import date
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-40s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

def transform_datafiles_to_pickle(config, gitReposLocation, dataLocation):
    # transform from xml/json files to pickle
    logging.info("Processing data")
    for repo in config["repositories"]:
        name = repo["name"]
        repoFolder = gitReposLocation/name
        logging.info(f"Processing repository \"{name}\"")
        assert repoFolder.exists()
        repo_config = repo["benchmark_files"] if "benchmark_files" in repo else []

        for dataset in repo["datasets"]:
            dataset_name = dataset["name"]
            pickleFile = dataLocation/f'{dataset_name}.hkl'
            dataset_path = repoFolder/dataset["path"]
            logging.info(f"Processing data set \"{dataset_name}\"")
            assert dataset_path.exists()
            assert dataset_path.is_dir()
            deletePrefix = None
            if "deletePrefix" in dataset:
                deletePrefix = dataset["deletePrefix"]
            parseFiles(dataset["benchmark_files"] if "benchmark_files" in dataset else repo_config, pickleFile, dataset_path, deletePrefix=deletePrefix)

def main():
    # load config
    logging.info("Reading configuration")
    config = loadConfig("config.yaml")

    baseDir = config["baseDir"]

    gitReposLocation = baseDir/config["gitRepositoriesLocation"]
    gitReposLocation.mkdir(exist_ok=True, parents=True)

    dataLocation = baseDir/config["dataLocation"]
    dataLocation.mkdir(exist_ok=True, parents=True)

    # get data repos
    logging.info("Updating git repos")
    assert "repositories" in config
    for repo in config["repositories"]:
        name = repo["name"]
        repoFolder = gitReposLocation/name
        if not repoFolder.exists():
            if "url" in repo and repo["url"] != "":
                # clone repo
                logging.info(f"Cloning repository \"{name}\"")
                url = repo["url"]
                subprocess.run(["git", "clone", url, name],
                               cwd=gitReposLocation, universal_newlines=True)
            else:
                logging.warn(f"Field \"url\" for repository \"{name}\" is not set. Either set \"url\" or clone repo by hand: git clone <url> {gitReposLocation}/{name}")
        else:
            # pull repo
            logging.info(f"Updating repository \"{name}\"")
            subprocess.run(["git", "pull"],
                           cwd=repoFolder, universal_newlines=True)

    transform_datafiles_to_pickle(config, gitReposLocation, dataLocation)

    # initialize annotations if required
    annotationsFile = baseDir/config["annotations"]["filename"]
    if not annotationsFile.exists():
        logging.info("Initiliazing annotations")
        annotations_df = pd.DataFrame(columns=["dataset_name", "date_only", "note"])
        annotations_df.to_csv(annotationsFile, index=False)
    assert annotationsFile.exists()

if __name__ == "__main__":
    main()
