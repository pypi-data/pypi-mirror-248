from setuptools import setup, find_namespace_packages

setup(
    name="polychromy",
    version="1.0.2",
    packages=find_namespace_packages(include=['polychromy', 'polychromy.*'], exclude=['images']),
    # Use find_packages and exclude the folder
    include_package_data=True,
    install_requires=["textlinebreaker >= 0.1.0 "],  # Add any dependencies here
    
    # other setup configurations...

    # Explicitly include 'polychromy.data' package
    package_data={
        "polychromy": ["data/colors.json"],
        "polychromy.data": [],  # Add specific data files if necessary
    },
)
