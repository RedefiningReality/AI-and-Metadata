import sys, os

def remove_files(rootdir):
	for root, dirs, files in os.walk(rootdir):
		for file in files:
			fullname = os.path.join(root, file)
			if os.path.getsize(fullname) == 0:
				print("Removing empty file " + str(fullname))
				os.remove(fullname)
	print("All empty files removed successfully")

if len(sys.argv) != 2:
	print("Usage: python remove_empty.py [root directory]")
	exit(0)
else:
	remove_files(sys.argv[1])