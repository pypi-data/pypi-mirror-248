from setuptools import setup, find_packages

setup(
    name="connect-spotify",
    version="1.0.0",
    description="Connect to Spotify API with Streamlit",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'streamlit',
        'requests'
    ],
    license="MIT",
    keywords="streamlit",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
    ],
    project_urls={
        "Source": "https://github.com/Satoshi-Sh/streamlit-api"
    }
)
