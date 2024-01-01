import datetime
import pathlib
import re
from textwrap import dedent
from textwrap import indent

import packaging.version
import requests
import tabulate
import wcwidth
from tqdm import tqdm

FILE_HEAD = r"""
.. _plugin-list:

Pytest Plugin List
==================

Below is an automated compilation of ``pytest``` plugins available on `PyPI <https://pypi.org>`_.
It includes PyPI projects whose names begin with "pytest-" and a handful of manually selected projects.
Packages classified as inactive are excluded.

For detailed insights into how this list is generated,
please refer to `the update script <https://github.com/pytest-dev/pytest/blob/main/scripts/update-plugin-list.py>`_.

.. warning::

   Please be aware that this list is not a curated collection of projects
   and does not undergo a systematic review process.
   It serves purely as an informational resource to aid in the discovery of ``pytest`` plugins.

   Do not presume any endorsement from the ``pytest`` project or its developers,
   and always conduct your own quality assessment before incorporating any of these plugins into your own projects.


.. The following conditional uses a different format for this list when
   creating a PDF, because otherwise the table gets far too wide for the
   page.

"""
DEVELOPMENT_STATUS_CLASSIFIERS = (
    "Development Status :: 1 - Planning",
    "Development Status :: 2 - Pre-Alpha",
    "Development Status :: 3 - Alpha",
    "Development Status :: 4 - Beta",
    "Development Status :: 5 - Production/Stable",
    "Development Status :: 6 - Mature",
    "Development Status :: 7 - Inactive",
)
ADDITIONAL_PROJECTS = {  # set of additional projects to consider as plugins
    "logassert",
}


def escape_rst(text: str) -> str:
    """Rudimentary attempt to escape special RST characters to appear as
    plain text."""
    text = (
        text.replace("*", "\\*")
        .replace("<", "\\<")
        .replace(">", "\\>")
        .replace("`", "\\`")
    )
    text = re.sub(r"_\b", "", text)
    return text


def iter_plugins():
    regex = r">([\d\w-]*)</a>"
    response = requests.get("https://pypi.org/simple")

    match_names = (match.groups()[0] for match in re.finditer(regex, response.text))
    plugin_names = [
        name
        for name in match_names
        if name.startswith("pytest-") or name in ADDITIONAL_PROJECTS
    ]

    for name in tqdm(plugin_names, smoothing=0):
        response = requests.get(f"https://pypi.org/pypi/{name}/json")
        if response.status_code == 404:
            # Some packages, like pytest-azurepipelines42, are included in https://pypi.org/simple
            # but return 404 on the JSON API. Skip.
            continue
        response.raise_for_status()
        info = response.json()["info"]
        if "Development Status :: 7 - Inactive" in info["classifiers"]:
            continue
        for classifier in DEVELOPMENT_STATUS_CLASSIFIERS:
            if classifier in info["classifiers"]:
                status = classifier[22:]
                break
        else:
            status = "N/A"
        requires = "N/A"
        if info["requires_dist"]:
            for requirement in info["requires_dist"]:
                if re.match(r"pytest(?![-.\w])", requirement):
                    requires = requirement
                    break

        def version_sort_key(version_string):
            """
            Return the sort key for the given version string
            returned by the API.
            """
            try:
                return packaging.version.parse(version_string)
            except packaging.version.InvalidVersion:
                # Use a hard-coded pre-release version.
                return packaging.version.Version("0.0.0alpha")

        releases = response.json()["releases"]
        for release in sorted(releases, key=version_sort_key, reverse=True):
            if releases[release]:
                release_date = datetime.date.fromisoformat(
                    releases[release][-1]["upload_time_iso_8601"].split("T")[0]
                )
                last_release = release_date.strftime("%b %d, %Y")
                break
        name = f':pypi:`{info["name"]}`'
        summary = ""
        if info["summary"]:
            summary = escape_rst(info["summary"].replace("\n", ""))
        yield {
            "name": name,
            "summary": summary.strip(),
            "last release": last_release,
            "status": status,
            "requires": requires,
        }


def plugin_definitions(plugins):
    """Return RST for the plugin list that fits better on a vertical page."""

    for plugin in plugins:
        yield dedent(
            f"""
            {plugin['name']}
               *last release*: {plugin["last release"]},
               *status*: {plugin["status"]},
               *requires*: {plugin["requires"]}

               {plugin["summary"]}
            """
        )


def main():
    plugins = list(iter_plugins())

    reference_dir = pathlib.Path("doc", "en", "reference")

    plugin_list = reference_dir / "plugin_list.rst"
    with plugin_list.open("w", encoding="UTF-8") as f:
        f.write(FILE_HEAD)
        f.write(f"This list contains {len(plugins)} plugins.\n\n")
        f.write(".. only:: not latex\n\n")

        wcwidth  # reference library that must exist for tabulate to work
        plugin_table = tabulate.tabulate(plugins, headers="keys", tablefmt="rst")
        f.write(indent(plugin_table, "   "))
        f.write("\n\n")

        f.write(".. only:: latex\n\n")
        f.write(indent("".join(plugin_definitions(plugins)), "  "))


if __name__ == "__main__":
    main()
