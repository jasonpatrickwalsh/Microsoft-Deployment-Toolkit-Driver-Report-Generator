from cx_Freeze import setup, Executable
	
setup(
    name = "MDT Driver Report Utility",
    version = "2.0",
    description = "MDT Driver Report Utility",
	author="Jason Walsh",
    executables = [Executable("DriverReporter.py")])