import pkg_resources
import sys

def check_requirements():
    required_packages = {
        'psutil': '5.9.0',
        'pywin32': '305',
        'tkinter': None,  # Built into Python
        'ttkthemes': '3.2.2',
        'logging': None,  # Built into Python
        'datetime': None,  # Built into Python
        'threading': None,  # Built into Python
        'json': None,  # Built into Python
        'socket': None,  # Built into Python
        'subprocess': None,  # Built into Python
        'os': None,  # Built into Python
        'sys': None,  # Built into Python
        'ctypes': None,  # Built into Python
        're': None,  # Built into Python
        'traceback': None  # Built into Python
    }

    missing_packages = []
    outdated_packages = []

    for package, min_version in required_packages.items():
        try:
            if min_version:
                installed_version = pkg_resources.get_distribution(package).version
                if pkg_resources.parse_version(installed_version) < pkg_resources.parse_version(min_version):
                    outdated_packages.append((package, installed_version, min_version))
        except pkg_resources.DistributionNotFound:
            if package not in sys.modules:
                missing_packages.append(package)

    if missing_packages or outdated_packages:
        print("\nDependency Check Results:")
        print("------------------------")
        
        if missing_packages:
            print("\nMissing Packages:")
            for package in missing_packages:
                print(f"- {package}")
                
        if outdated_packages:
            print("\nOutdated Packages:")
            for package, installed_version, required_version in outdated_packages:
                print(f"- {package}: installed={installed_version}, required>={required_version}")
                
        return False
    
    print("\nAll dependencies satisfied!")
    return True

if __name__ == "__main__":
    check_requirements()