# WARDEN Performance Dashboard
By: Dane Camacho, Luc Berger-Vergiat, Christian Glusa

## What is WARDEN for?
Warden is software for parsing XML data and displaying it as "dive-in"-able graphs hosted on a Dash(Flask) app

## Installation Guide
1. Clone the repository `git clone git@github.com/sandialabs/warden`
2. Install the package `pip install .`

### Starting a WARDEN instance
1. Configure by creating a configuration file `config.yaml`. See `config.yaml.sample` for an example.
2. Run `warden_init_or_update` to initialize the folder using the configuration in `config.yaml`
3. Run `warden_run_dashboard` to launch the webserver.

It is recommended to run `warden_init_or_update` at regular intervals
using crontab or a systemd timer to pull new data from the
repositories.

## Required Data Format

XML data files need to be formatted like so:
```
<?xml version="1.0"?>
<performance-report date="2024-03-28T11:10:49" name="nightly_run_2024_03_28" time-units="seconds">
  <metadata key="Trilinos Version" value="ccf0c14624"/>
<timing name="Base Timer" value="0.246703">
  <timing name="SubTimer1" value="0.0306649"/>
  <timing name="SubTimer2" value="0.0306649">
    <timing name="SubSubTimer1 value="0.0206649>
    <timing name="SubSubTimer2 value="0.01>
  </timing>
</timing>
</performance-report>
```

Each timing element must contain one "name" and one "value" attribute


## URLs

Datasets can be directly accessed using the URLs 

http://HOST:PORT/?dataset=DATASET

and 

http://HOST:PORT/?dataset=DATASET&second_dataset=DATASET
