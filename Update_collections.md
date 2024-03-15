Once you make the changes to the collection's modules make sure you change the version on the `galaxy.yml` file.
**~/collections/ansible_collections/skenderidis/f5_awaf/galaxy.yml**

To update the collection change directory to the F5_awaf collection
```
cd ~/collections/ansible_collections/skenderidis/f5_awaf/
```

Run the command `ansible-galaxy collection build` on the directory of the collection
```
  ansible-galaxy collection build
```

Logon to ansible-galaxy and get a token and then publish the new 

ansible-galaxy collection publish skenderidis-f5_awaf-X.Y.Z.tar.gz --token <token>

