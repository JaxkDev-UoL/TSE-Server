from server import start, getDirectory

print("TSE Server starting...")

start();

# forever loop ^








exit(0)

import tempfile

print(tempfile.gettempdir())

f = tempfile.TemporaryFile()
print(f.name)
f.write(b'something on temporaryfile')
f.flush() # flush to disk
f.seek(0) # return to beginning of file
print(f.read()) # reads data back from the file
# f.close() # temporary file is automatically deleted here

input()