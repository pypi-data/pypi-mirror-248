import setuptools

with open("README.md", mode = "r", encoding = "utf-8") as fh:
	long_description = fh.read()
	
# with open("requirements.txt", mode = "r", encoding = "utf-8") as rf:
# 	requirements = list(map(lambda x : x.strip(), filter("".__ne__, rf.readlines())))
	
setuptools.setup(
	
	name                          = "KeyDnn",
	version                       = "0.1.0",
	author                        = "Keywind",
	author_email                  = "watersprayer127@gmail.com",
	description                   = "Deep Learning Framework Implemented by Kevin Sheu.",
	long_description              = long_description,
	long_description_content_type = "text/markdown",
	url                           = "https://github.com/keywind127/keydnn",
	project_urls                  = {
		"Bug Tracker" : "https://github.com/keywind127/keydnn/issues",
	},
	classifiers                   = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	package_dir                   = { "" : "src" },
	packages                      = setuptools.find_packages(where = "src"),
	python_requires               = ">=3.6",
	
	install_requires              = [
		"markdown",
		"numpy"
    ]
	
)