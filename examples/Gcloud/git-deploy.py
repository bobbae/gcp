#!/usr/bin/env python3

#
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import subprocess
import sys
import time

show_debug = os.environ.get("DEBUG", None)
verbose = True if show_debug and "v" in show_debug.lower() else None

retry = False
if len(sys.argv) > 1 and sys.argv[1] == "retry":
    retry = True


def _cli(exe, params, return_failure):
    if verbose:
        print("\033[96m" + exe + " " + params + "\033[0m")
    resp = subprocess.run(
        [exe] + params.replace("\n", "").split(" "), capture_output=True
    )
    status = resp.stdout.decode("utf-8").strip()
    failure = resp.stderr.decode("utf-8").strip()
    if return_failure:
        return status, failure
    else:
        return status


def git(params, return_failure=False):
    return _cli("git", params, return_failure=return_failure)


def gcloud(params, return_failure=False):
    return _cli("gcloud", params, return_failure=return_failure)


def output(msg):
    print("\033[95m" + msg + "\033[0m")


def debug(msg):
    if show_debug:
        print("\033[93m" + msg + "\033[0m")


def error_return(msg):
    print("\033[91m" + msg + "\033[0m")
    sys.exit(1)


status, failure = git("status -sb", return_failure=True)

if failure:
    error_return(failure)

# ## main...origin/main
m = re.search("(?P<local>\w*)\.\.\.(?P<origin>\w*)/(?P<branch>\w*)", status).groupdict()
local, origin, branch = m["local"], m["origin"], m["branch"]

debug(f"detected origin: {origin}\ndetected branch: {branch}")

remote = git("remote -v").split("\n")

# origin\tgit@github.com:name/repo (fetch)
# origin\tgit@github.com:name/repo (push)
git_remote = [x for x in remote if "push" in x and origin in x][0]
m = re.search(":(?P<owner>.*)/(?P<name>.*) ", git_remote).groupdict()
owner, name = m["owner"], m["name"]

debug(f"detected remote: {owner}/{name}")

if retry:
    debug("mode: retry, skipping push")
else:
    debug("checking push status")

    pending = git(f"log {origin}/{branch}..{local}")
    if not pending:
        error_return(
            "git says: Everything up-to-date (you don't have any pending commits to push!)"
        )

    output(f"pushing {branch} branch to {origin} (github.com/{owner}/{name})...")

    os.system(f"git push {origin} {branch}")

trigger_id = gcloud(
    "beta builds triggers list"
    f" --filter github.owner={owner}"
    f" --filter github.name={name}"
    f" --filter github.push.branch=^{branch}$"
    f" --format value(id)"
)

if not trigger_id:
    alltriggers = gcloud(
        "beta builds triggers list"
        " --format table(id,github.owner,github.name,github.push.branch)"
    )
    debug(alltriggers)
    error_return("No trigger found for this repo (are you in the right project?)")

debug(f"located trigger: {trigger_id}")

if retry:
    debug("mode retry: triggering build manually")
    output(
        f"manually triggering build on {branch} branch to {origin} (github.com/{owner}/{name})... "
    )
    gcloud(f"beta builds triggers run {trigger_id} --branch {branch}")

for counter in range(3):
    debug(f"Trying to find build. Attempt {counter}")
    build_id = gcloud(
        "builds list"
        f" --filter buildTriggerId={trigger_id}"
        f" --filter status=WORKING"
        f" --format value(id)"
    )
    if not build_id:
        time.sleep(3)
        continue
    else:
        break
else:
    error_return("No current builds (did it fail to start up in time?)")

debug(f"located running build: {build_id}")

stream_cmd = f"gcloud beta builds log --stream {build_id}"

output(f"streaming build {build_id}... (exit with ctrl-C)")

os.system(stream_cmd)
