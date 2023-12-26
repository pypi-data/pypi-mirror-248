from setuptools import setup

setup(
  name='madstory_core',
  version='0.0.9',
  packages=['madstory_core'],
  author = "Shariq Torres",
  description = "Core library for the MadStory storytelling platform",
  author_email="shariq.torres@gmail.com",
  test_require=['pytest'],
  setup_requires=['pytest-runner']
)