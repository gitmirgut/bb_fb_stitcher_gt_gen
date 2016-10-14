from setuptools import setup

install_reqs = ['numpy', 'matplotlib', 'bb_fb_stitcher']
dep_links = []

setup(
    name='bb_fb_stitcher_gt_gen',
    version='0.0.0.dev1',
    description='Is used to generate Ground Truth data.',
    long_description='',
    entry_points={
        'console_scripts': [
            'bb_gt_generator = gt_generator.scripts.bb_gt_generator:main'
        ]
    },
    url='https://github.com/gitmirgut/bb_fb_stitcher_gt_gen',
    author='gitmirgut',
    author_email="gitmirgut@users.noreply.github.com",
    packages=['gt_generator', 'gt_generator.scripts'],
    install_requires=install_reqs,
    dependency_links=dep_links,
    license='GNU GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5'
    ]
)