from distutils.spawn import find_executable


def is_installed(executable):
    """Check that executable is available to PATH."""
    return bool(find_executable(executable))
