[![license](https://img.shields.io/badge/license-MIT-brightgreen)](https://spdx.org/licenses/MIT.html)
[![pipelines](https://gitlab.com/jlecomte/python/gitlab-ci-scripts/badges/master/pipeline.svg)](https://gitlab.com/jlecomte/python/gitlab-ci-scripts/pipelines)
[![coverage](https://gitlab.com/jlecomte/python/gitlab-ci-scripts/badges/master/coverage.svg)](https://jlecomte.gitlab.io/python/gitlab-ci-scripts/coverage/index.html)

# gitlab-ci-scripts

(deprecated, unmaintained)

Quick and dirty GitLab CI helper scripts.

A quick and dirty helper script to convert a xml coverage report into a valid cobertura file that will be accepted by GitLab CI.

This enables the merge request pages to have coverage shown on the code review tab.

## Installation from PyPI

You can install the latest version from PyPI package repository.

~~~bash
python3 -mpip install -U gitlab-ci-scripts
~~~

## GitLab CI Usage

Sample gitlab-ci.yml snippet for coverage:

~~~yaml
coverage:
  script:
    - python3 -m pytest --cov-report=xml:coverage.tmp.xml -- tests
    - pycov-convert-relative-filenames < coverage.tmp.xml > coverage.xml
  artifacts:
    when: always
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
~~~

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Locations

  * GitLab: [https://gitlab.com/jlecomte/python/gitlab-ci-scripts](https://gitlab.com/jlecomte/python/gitlab-ci-scripts)
  * PyPi: [https://pypi.org/project/gitlab-ci-scripts](https://pypi.org/project/gitlab-ci-scripts)
