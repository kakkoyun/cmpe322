import os

r, w = os.pipe()
reader = open(r)
writer = open(w, 'w')

if os.fork() == 0:
    print("Child have read: ", reader.read(5))
else:
    writer.write("Hello!")
for x, xname in [(reader, "reader"), (writer, "writer")]:
    print(xname + "is readable? ", x.readable())
    print(xname + "is writable?", x.writable())
    print(xname + "is seekable?", x.seekable())
