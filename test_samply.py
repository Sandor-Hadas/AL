import pytest
import os
import filecmp

# Make sure clean run
os.system("rm -rf TestData/test_out.*")
os.system("rm -rf TestData/ctest_out.*")

# Generate test data
os.system("python al.py --in TestData/input.xml --out TestData/test_out.html")
os.system("python al.py --in TestData/input.csv --out TestData/test_out.xml")
os.system("python al.py --in TestData/input.json --out TestData/test_out.csv")
os.system("python al.py --in TestData/input.json --out TestData/test_out.json")
os.system("python al.py --in TestData/input.json --print txt >TestData/ctest_out.txt")
os.system("python al.py --in TestData/input.json --print html >TestData/ctest_out.html")

# Test output
assert( filecmp.cmp("TestData/Master_out.html", "TestData/test_out.html") )
assert( filecmp.cmp("TestData/Master_out.xml", "TestData/test_out.xml") )
assert( filecmp.cmp("TestData/Master_out.csv", "TestData/test_out.csv") )
assert( filecmp.cmp("TestData/Master_out.json", "TestData/test_out.json")  )
assert( filecmp.cmp("TestData/cMaster_out.txt", "TestData/ctest_out.txt") )
assert( filecmp.cmp("TestData/cMaster_out.html", "TestData/ctest_out.html") )

# Generate Master data
#os.system("python al.py --in TestData/input.xml --out TestData/Master_out.html")
#os.system("python al.py --in TestData/input.csv --out TestData/Master_out.xml")
#os.system("python al.py --in TestData/input.json --out TestData/Master_out.csv")
#os.system("python al.py --in TestData/input.json --out TestData/Master_out.json")
#os.system("python al.py --in TestData/input.json --print txt >TestData/cMaster_out.txt")
#os.system("python al.py --in TestData/input.json --print html >TestData/cMaster_out.html")

# Clean after run
os.system("rm -rf TestData/test_out.*")
os.system("rm -rf TestData/ctest_out.*")

