"""
Audio Source Matcher V1 - Script for OBS-Studio v28+
Created by Scott Fronapfel (scott@scofrona.dev)

Automatically update a child window source to match a parent window source.
Originally created to match an Audio Application Capture to a Game Capture,
thereby reducing the number of sources which need updated on changing games.

Potential future additions:
- Detect active window for the parent without relying exclusively on the "window" property
  (This would allow the child to update if the parent was using "Capture Foreground with Hotkey")
- Use combo boxes to choose sources instead of strings
"""

import obspython as obs


def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "source_name", "Parent Window/Game Capture", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "audio_name", "Child Audio Capture", obs.OBS_TEXT_DEFAULT)
    return props


def script_update(settings):
    global parent_source, audio_source
    parent_source = obs.obs_data_get_string(settings, "source_name")
    audio_source = obs.obs_data_get_string(settings, "audio_name")


def get_source(name):
    return obs.obs_get_source_by_name(name)


def release(source, settings):
    obs.obs_data_release(settings)
    obs.obs_source_release(source)


def callback(calldata):
    input_source = get_source(parent_source)
    output_source = get_source(audio_source)
    source = obs.calldata_source(calldata,"source")
    in_p = obs.obs_source_get_settings(input_source)
    current_window = obs.obs_data_get_string(in_p, "window")
    print(f"{audio_source} changed to {current_window}")
    settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, "window", current_window)
    obs.obs_source_update(output_source, settings)

    release(input_source, in_p)
    release(output_source, settings)

def script_load(settings):
    parent_source = get_source(obs.obs_data_get_string(settings, "source_name"))
    sh = obs.obs_source_get_signal_handler(parent_source)
    obs.signal_handler_connect(sh, "update", callback)


def script_description():
    return "Match a given Win/Game Capture source with a given App Audio Capture"






## On Source Change for GameCapture

## Get Window of GameCapture

## Set GameAudio to match GameCapture
