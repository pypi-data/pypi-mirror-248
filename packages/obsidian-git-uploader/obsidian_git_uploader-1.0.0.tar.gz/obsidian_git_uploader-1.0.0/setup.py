from setuptools import setup, find_packages

setup(
    name             = 'obsidian_git_uploader',
    version          = '1.0.0',
    description      = 'Obsidian Image Commiter Utility',
    author           = 'Revi1337',
    author_email     = 'david122123@gmail.com',
    url              = '',
    download_url     = '',
    install_requires = [
        'requests',
        'beautifulsoup4',
        'clipboard',
        'Markdown',
        'aiohttp'
    ],
	include_package_data=True,
	packages         = find_packages(),
    entry_points     = {
        'console_scripts': [
            'image-commit = obsidian_git_uploader.image_upload:main'
        ]
    },
    keywords         = [
        'GIT COMMITER',
        'git commiter',
        'IMAGE COMMITER',
        'image commiter'
    ],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows"
    ]
)