import cryptocode

encoded = str(cryptocode.encrypt("mystring","mypassword"))
print(str(encoded))
## And then to decode it:
decoded = cryptocode.decrypt(encoded, "mypassword")