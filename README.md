# merkle_tree_python_example

The repository contains code for generating a Merkle tree for a fake chunked sequence of DNA bases.

Imagine that the original owner of the fake data is a scientist that scatters the chunks of her data file in a p2p network for download by any interested network participant.

The network participant who downloads the data does so chunk by chunk.

This scheme of scattering the file chunks distributes the load across the network, and it allows the client to acquire the download from multiple sources, or seeds, which decreases the load on the individual seeds, and not to mention, it is a nice feature since it ought to be the downloading party's responsibility to care for open ports, rather than to demand that one central seed occupy the majority of her bandwidth by providing a free service to a curious downloader.

Of course, the client donwloader will wish to know an answer to the question: **is the current chunk in queue for download *really* a chunk from the original dataset?**

We can imagine that to address this question, the original owner of the dataset -- Scientist Sally - was a smooth operator, and she created a Merkle tree of the data and listed the Merkle root as the key to the data, and provided a gRPC service on her protected, secured, and registered EC2 instance, which responds to client requests for authenicity of a chunk with an audit trail for the hash of the chunk from the Merkle tree.

In so doing, clients interested in answering the above question can send the hash of a downloaded chunk to Sally's service, and her service can respond with an audit trail for the client to prove to their self that the chunk belongs to the original dataset.

Note, however, that in the event that the client does not trust Scientist Sally's gRPC service for provision of the audit trail, there is very little that can be done to help. Thus, trust is still required by using Merkle trees. However, as noted, Merkle trees do make downloading more safe and efficient by spreading out the trust and the burden for the seeders.

## Contents
* notebook/Merkle_Trees.ipynb
* notebook/merkle_tree_example.py

## Run
```
git clone https://github.com/dnck/merkle_tree_python_example.git && cd merkle_tree_python_example
python ./py/merkle_tree_example.py
```
