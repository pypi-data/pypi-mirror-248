from setuptools import setup, find_packages

setup(
    name="connect_spotify",
    version="1.0.3",
    description="Connect to Spotify API with Streamlit",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'streamlit',
        'requests'
    ],
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    license="MIT",
    keywords="streamlit",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
    ],
    project_urls={
        "Source": "https://github.com/Satoshi-Sh/connect-spotify"
    }
)
