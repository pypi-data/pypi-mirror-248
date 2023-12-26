# Copyright (c) 2022-2024, Keivan Tafakkori. All rights reserved.
# See the file LICENSE file for licensing details.

from setuptools import setup, find_packages

# Common packages for all versions of FelooPy

common = [
    'gputil==1.4.0',
    'infix==1.2',
    'matplotlib==3.8.2',
    'nbformat==5.9.2',
    'numba==0.58.1',
    'numpy==1.26.2',
    'openpyxl==3.1.2',
    'pandas==2.1.3',
    'plotly==5.18.0',
    'polars==0.19.19',
    'psutil==5.9.6',
    'py-cpuinfo==9.0.0',
    'scikit-learn==1.3.2',
    'tabulate==0.9.0',
    'win-unicode-console==0.5',
    'xlsxwriter==3.1.9',
    'tqdm==4.66.1',
]

# Interfaces for optimization solvers or algorithms

pico = [
    ''
]

nano = pico + [
    'pymprog==1.1.2',
]

micro = nano + [
    'gekko==1.0.6',
    'mealpy==3.0.1',
]

mini = micro + [
    'cvxpy==1.4.1',
    'ortools==9.8.3296',
]

full = mini + [
    'pydecision==4.3.9',
    'pymoo==0.6.1.1',
]

stock = full + [
    'linopy==0.3.2',
    'mip==1.15.0',
    'niapy==2.1.0',
    'picos==2.4.17',
    'pulp==2.7.0',
    'pygad==3.2.0',
    'pyomo==6.7.0',
    'rsome==1.2.5',
]

# Solvers for optimization problems or algorithms

plus_gurobi = [
    'gurobipy==11.0.0',
]

plus_cplex = [
    'cplex==22.1.1.1',
    'docplex==2.25.236',
]

plus_xpress = [
    'xpress==9.2.5',
]

plus_copt = [
    'coptpy==7.0.4',
]

hyper = stock + plus_gurobi + plus_cplex + plus_xpress + plus_copt

# Might have some os-dependent issues

only_cylp = [
    'cylp==0.92.2',
]

only_linux = [
    'pymultiobjective==1.5.4',
]

mega = hyper + only_cylp + only_linux

extra_dict = {
    'pico': pico,
    'nano': nano,
    'micro': micro, 
    'mini': mini, 
    'full': full, 
    'stock': stock,
    'hyper': hyper,
    'plus_gurobi': plus_gurobi,
    'plus_cplex': plus_cplex,
    'plus_xpress': plus_xpress,
    'plus_copt': plus_copt,
    'only_cylp': only_cylp,
    'only_linux': only_linux,
    'mega': mega}

keywords_list = [
    'computer science',
    'data science',
    'decision making',
    'decision science',
    'industrial engineering',
    'machine learning',
    'management science',
    'mathematical modeling',
    'operations management',
    'operations research',
    'optimization',
    'simulation',
    'supply chain',
    ]

if __name__ == '__main__':

    setup(
        
        name = 'feloopy',
        
        version = '0.2.8',
        
        description = 'FelooPy: An integrated optimization environment (IOE) for automated operations research (AutoOR) in Python.',
        
        packages = find_packages(include=['feloopy', 'feloopy.*']),
        
        long_description = open('./docs/README.md', encoding="utf8").read(),
        
        long_description_content_type = 'text/markdown',
        
        keywords = keywords_list,
        
        author='Keivan Tafakkori',
        
        author_email='k.tafakkori@gmail.com',
        
        maintainer='Keivan Tafakkori',
        
        maintainer_email='k.tafakkori@gmail.com',
        
        url='https://github.com/ktafakkori/feloopy',
        
        download_url='https://github.com/ktafakkori/feloopy/releases',
        
        license='MIT',
        
        entry_points={
        
        "console_scripts": ["feloopy = feloopy.cli:main",
                            "flp = feloopy.cli:main",
                            "fly = feloopy.cli:main",
                            ]},
        
        python_requires='>=3.10',
        
        extras_require=extra_dict,

        install_requires=common,
        
    )
