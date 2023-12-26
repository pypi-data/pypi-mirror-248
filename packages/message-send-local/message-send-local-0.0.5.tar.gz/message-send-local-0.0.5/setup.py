"""imports"""
import setuptools

PACKAGE_NAME = "message-send-local"
# Since all PACAKGE_NAMEs are with an underscore, we don't need this. Why do we need it?
package_dir = "message_send_platform_invitation"

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.5',
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles message_send_platform_invitation Python",
    long_description="PyPI Package for Circles message_send_platform_invitation Python",
    long_description_content_type='text/markdown',
    url="https://github.com/circles-zone/message-send-platform-invitation-local-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    # TODO: Update which packages to include with this package
    install_requires=[
        'pytest>=7.4.0',
        'user-context-remote>=0.0.17',
        'python-sdk-local>=0.0.27',
        'messages-local',
        'database-mysql-local'
    ],
)
