# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['freedvtnc2']

package_data = \
{'': ['*']}

install_requires = \
['cffi>=1.16.0,<2.0.0',
 'configargparse>=1.7,<2.0',
 'kissfix>=7.0.11,<8.0.0',
 'prompt-toolkit>=3.0.43,<4.0.0',
 'pyaudio>=0.2.14,<0.3.0',
 'pydub>=0.25.1,<0.26.0',
 'setuptools>=69.0.3,<70.0.0',
 'tabulate>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['freedvtnc2 = freedvtnc2:__main__.main']}

setup_kwargs = {
    'name': 'freedvtnc2',
    'version': '0.0.1',
    'description': '',
    'long_description': "A KISS TNC using the freedv data modems.\n\n## Features\n - KISS interface (virtual serial, or TCP)\n - Chat\n - DATAC1, DATAC3 and DATAC4 modes\n\n## Unsupported\n - Windows\n\n## Requirements\n - hamlib\n - portaudio / pyaudio\n - c build tools\n\n## Install\n\n```sh\n# install required system packages\nsudo apt-get update\nsudo apt install git build-essential cmake pipx portaudio19-dev python3 python3-dev libhamlib-utils\n\n# install codec2 (the debian packaged versions do not contain DATAC4 modem)\ngit clone https://github.com/drowe67/codec2.git\ncd codec2\nmkdir build_linux\ncd build_linux\ncmake ..\nmake\nsudo make install\n\n# install freedvtnc2\npipx install /freedvtnc2-0.1.0.tar.gz\n\n# make sure the PATH is set correctly\npipx ensurepath\nsource ~/.profile\n```\n\n## Running\n```\n# Run rigctld in background. See rigctld --help on how to configure your rig\nrigctld -m 1 -r /dev/null &\n\n# Test to make sure rigctl works\nrigctl -m 2 T 1 # enable PTT\nrigctl -m 2 T 0 # disable PTT\n\n# Get argument help\nfreedvtnc2 --help\n\n#list audio devices\nfreedvtnc2 --list-audio-devices\n\nfreedvtnc2 --output-device 0 --input-device 0 --log-level DEBUG # it's useful to have debug turned on when first testing\n```\n\nThe connect your favorite kiss tools up to the TNC over TCP port 8001 or PTS interface if enabled\n\n## Testing\n\nThe CLI has a handy `test_ptt` to make test that PTT and sound output is working.\n\n## Command line arguments\n```\nusage: freedvtnc2 [-h] [-c C] [--no-cli] [--list-audio-devices] [--log-level {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}] [--input-device INPUT_DEVICE] [--output-device OUTPUT_DEVICE]\n                  [--output-volume OUTPUT_VOLUME] [--mode {DATAC1,DATAC3,DATAC4}] [--follow] [--max-packets-combined MAX_PACKETS_COMBINED] [--pts] [--kiss-tcp-port KISS_TCP_PORT]\n                  [--kiss-tcp-address KISS_TCP_ADDRESS] [--rigctld-port RIGCTLD_PORT] [--rigctld-host RIGCTLD_HOST] [--ptt-on-delay-ms PTT_ON_DELAY_MS] [--ptt-off-delay-ms PTT_OFF_DELAY_MS]\n                  [--callsign CALLSIGN]\n\noptions:\n  -h, --help            show this help message and exit\n  -c C, -config C       config file path\n  --no-cli              [env var: FREEDVTNC2_CLI]\n  --list-audio-devices\n  --log-level {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}\n                        [env var: FREEDVTNC2_LOG_LEVEL]\n  --input-device INPUT_DEVICE\n                        [env var: FREEDVTNC2_INPUT_DEVICE]\n  --output-device OUTPUT_DEVICE\n                        [env var: FREEDVTNC2_OUTPUT_DEVICE]\n  --output-volume OUTPUT_VOLUME\n                        in db. postive = louder, negative = quiter [env var: FREEDVTNC2_OUTPUT_DB]\n  --mode {DATAC1,DATAC3,DATAC4}\n                        The TX mode for the modem. The modem will receive all modes at once\n  --follow              When enabled change TX mode to the mode being received. This is useful for stations operating automatically. [env var: FREEDVTNC2_FOLLOW]\n  --max-packets-combined MAX_PACKETS_COMBINED\n                        How many kiss packets to combine into a single transmission [env var: FREEDVTNC2_MAX_PACKETS]\n  --pts                 Disables TCP and instead creates a PTS 'fake serial' interface [env var: FREEDVTNC2_PTS]\n  --kiss-tcp-port KISS_TCP_PORT\n                        [env var: FREEDVTNC2_KISS_TCP_PORT]\n  --kiss-tcp-address KISS_TCP_ADDRESS\n                        [env var: FREEDVTNC2_KISS_TCP_ADDRESS]\n  --rigctld-port RIGCTLD_PORT\n                        TCP port for rigctld - set to 0 to disable rigctld support [env var: FREEDVTNC2_RIGTCTLD_PORT]\n  --rigctld-host RIGCTLD_HOST\n                        Host for rigctld [env var: FREEDVTNC2_RIGTCTLD_HOST]\n  --ptt-on-delay-ms PTT_ON_DELAY_MS\n                        Delay after triggering PTT before sending data [env var: FREEDVTNC2_PTT_ON_DELAY_MS]\n  --ptt-off-delay-ms PTT_OFF_DELAY_MS\n                        Delay after sending data before releasing PTT [env var: FREEDVTNC2_PTT_OFF_DELAY_MS]\n  --callsign CALLSIGN   Currently only used for chat [env var: FREEDVTNC2_CALLSIGN]\n\nArgs that start with '--' can also be set in a config file (~/.freedvtnc2.conf or specified via -c). Config file syntax allows: key=value, flag=true, stuff=[a,b,c] (for details, see syntax at\nhttps://goo.gl/R74nmi). In general, command-line values override environment variables which override config file values which override defaults.\n```\n\n## CLI commands\n```\nFreeDVTNC2 Help^\n---------------\ncallsign\n   Sets callsign - example: callsign N0CALL\nclear\n   Clears TX queues\ndebug\n   Open the debug shell\nexception\n   Raises and exemption to test the shell\nexit\n   Exits FreeDVTNC2\nfollow\n   Allows the tx modem to change to the mode last received - follow on\nhelp\n   This help\nlist_audio_devices\n   Lists audio device parameters\nlog_level\n   Set the log level\nmax_packets_combined\n   Set the max number of packets to combine together for a single transmission\nmode\n   Change TX Mode: mode [DATAC1, DATAC3, DATAC4]\nmsg\n   Send a message\nsave_config\n   Save a config file to ~/.freedvtnc2.conf. Warning this will override your current config\nsend_string\n   Sends string over the modem\ntest_ptt\n   Turns on PTT for 2 seconds\nvolume\n   Set the volume gain in db for output level - you probably want to use soundcard configuration or radio configuration rather than this.\n\n```\n\nCredits\n--\nDavid Rowe and the FreeDV team for developing the modem and libraries ",
    'author': 'xssfox',
    'author_email': 'xss@sprocketfox.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}
from build_lib import *
build(setup_kwargs)

setup(**setup_kwargs)
