from setuptools import setup

VERSION = '1.0.0'
DESC = 'The Python Framework for One-Time Pad Cipher'

setup(
    name='otpyf',
    version=VERSION,
    description=DESC,
    author='35mpded',
    author_email="35mpded@gmail.com",
    packages=['otpyf'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Security :: Cryptography',
	'Topic :: Communications',
	'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux'
    ],
)

