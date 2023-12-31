from setuptools import setup, find_packages
import platform

package_folder = "lib" if platform.architecture()[0] == "32bit" else "lib64"

setup(
    name='UniversalSpeech',
    version='1.0.2',
    packages=find_packages(),
    package_data={'': [f'{package_folder}/*']},
    author='Mahmoud Atef',
    author_email='mahmoud.atef.987123@gmail.com',
    description='UniversalSpeech simplifies speech access in applications through a unified interface, supporting diverse methods such as screen readers, direct synthesis, and native/OS speech engines.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords=['speech', 'accessibility', 'screen reader' 'jaws', 'nvda'],
    url='https://github.com/MahmoudAtef999/PythonUniversalSpeech/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
    ],
)